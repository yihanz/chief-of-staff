#!/usr/bin/env python3
# imessage-fixed v1.4.0 — read-only iMessage MCP reader (Python stdlib only).
# Fixes the stock connector's defects AND the two this line adds:
#   - short-code / bare-number handles that never matched (forced +1 prefix)
#   - message text lost to attributedBody (typedstream) decoding
#   - SENT messages silently dropped: a message you send has handle_id = 0, so
#     any query that JOINs on handle_id discards ~95% of your own side. Threads
#     are resolved through chat membership, not handle_id, and every read
#     LEFT JOINs the handle so sent rows survive and are marked from_me.
#   - Apple Cash / payment balloons (amount lives in payload_data, text empty)
#     surfaced with a label instead of returning blank.
# Read-only. Schema-aware, bounded, and defensive: never crashes the stdin loop,
# clamps caller limits, orders and de-duplicates thread listings, reads the live
# WAL database read-only (an immutable fallback warns on stderr if it ever has to
# skip the WAL), and closes every connection.
import sys, os, re, json, sqlite3, pwd, datetime

VERSION = "1.4.0"
APPLE_EPOCH = 978307200
LIMIT_MAX = 500
HOURS_MAX = 24 * 400
DAYS_MAX  = 4000

_BAD = ('streamtyped','NSMutableString','NSString','NSAttributedString','NSDictionary',
        'NSObject','NSValue','NSNumber','NSData','NSMutableData','__kIM','bplist','$class',
        '$archiver','NSKeyedArchiver','NSMutableAttributedString','DDScannerResult',
        'NSParagraphStyle','NSColor','NSFont','NSRange','WNSArray')

# ---------- text decoding ----------

def _decode_typed(blob):
    # Recover the message body from an NSArchiver typedstream: find the NSString
    # class marker, read its length prefix, take exactly that many bytes. Every
    # slice is bounds-checked, so a malformed blob returns '' rather than raising.
    if not blob: return ''
    if isinstance(blob,str): blob=blob.encode('utf-8','surrogateescape')
    i = blob.find(b'NSString')
    if i == -1:
        i = blob.find(b'NSMutableString')
        if i == -1: return ''
        i += 15
    else:
        i += 8
    p = blob.find(bytes([43]), i)
    if p == -1 or p - i > 16: return ''
    p += 1
    if p >= len(blob): return ''
    n = blob[p]; p += 1
    if n == 129:
        if p+2 > len(blob): return ''
        n = int.from_bytes(blob[p:p+2], 'little'); p += 2
    elif n == 130:
        if p+4 > len(blob): return ''
        n = int.from_bytes(blob[p:p+4], 'little'); p += 4
    elif n > 127:
        return ''
    if n <= 0 or p + n > len(blob): return ''
    return blob[p:p+n].decode('utf-8', 'replace')

def _decode_fallback(blob):
    # Only if the typedstream parse fails. Keeps EVERY printable run (never just
    # the longest) so multi-paragraph text is not truncated.
    if isinstance(blob,str): blob=blob.encode('utf-8','replace')
    t = blob.decode('utf-8','replace')
    runs=[]; cur=[]
    for ch in t:
        if ord(ch) < 32 or ord(ch) == 127 or ord(ch) == 65533:
            if cur:
                s=''.join(cur)
                if len(s)>=2: runs.append(s)
                cur=[]
        else:
            cur.append(ch)
    if cur:
        s=''.join(cur)
        if len(s)>=2: runs.append(s)
    runs=[r for r in runs if not any(b in r for b in _BAD)]
    return chr(10).join(runs).strip()

def _decode(blob):
    if not blob: return ''
    s=_decode_typed(blob)
    return s if s else _decode_fallback(blob)

def _amount(payload):
    # Best-effort dollar amount from an Apple Cash payload. The payload is an
    # archived plist saturated with '$' keys and stray numbers, so we accept ONLY
    # a currency-tagged value WITH cents ($NN.NN / USD NN.NN). No confident match
    # -> '' (caller falls back to a plain label). Better to under-label than to
    # fabricate a number an assistant will quote as fact.
    if not payload: return ''
    try:
        s = payload.decode('utf-8','replace') if isinstance(payload,(bytes,bytearray)) else str(payload)
    except Exception:
        return ''
    m = re.search(r'(?:USD|US\$|\$)\s?(\d{1,3}(?:,?\d{3})*\.\d{2})(?!\d)', s)
    return ("$" + m.group(1)) if m else ''

def _balloon_label(bbid, payload):
    # A message carried by an iMessage app extension ("balloon") often has no
    # text — content is in payload_data. Give it a readable label instead of a
    # blank line. Payments are the one that actually carries meaning.
    b = bbid or ''
    if 'PeerPayment' in b or 'PassbookUIService' in b:
        amt = _amount(payload)
        return "[Apple Cash: " + amt + "]" if amt else "[Apple Cash payment]"
    if 'URLBalloonProvider' in b: return ''     # link preview: URL is already in text/attributedBody
    if 'DigitalTouch' in b: return '[Digital Touch]'
    if 'Handwriting' in b:  return '[handwritten message]'
    if 'Fitness' in b or 'Workout' in b: return '[activity share]'
    return '[app message]'

def _text(row):
    t = (_rk(row,'text') or '').strip()
    a = _decode(_rk(row,'attributedBody'))
    body = a if (a and len(a) > len(t)) else (t or a)
    if not body:
        bbid = _rk(row,'balloon_bundle_id')
        if bbid:
            lbl = _balloon_label(bbid, _rk(row,'payload_data'))
            if lbl: return lbl
    return body

def _rk(row,key,default=None):
    try: return row[key]
    except (IndexError,KeyError): return default

def _ts(ns):
    if ns is None: return None
    try:
        secs = ns/1e9+APPLE_EPOCH if ns>10**11 else ns+APPLE_EPOCH
        return datetime.datetime.fromtimestamp(secs).strftime("%Y-%m-%d %H:%M:%S")
    except Exception: return None

def _clamp(v, default, hi):
    # A caller (an LLM) can pass anything. Never allow a negative LIMIT — in
    # SQLite that means UNLIMITED, the DoS the cap exists to prevent. A negative
    # ask becomes 0 (nothing); 0 is honoured as "none"; too-large is capped.
    try: v=int(v)
    except (TypeError, ValueError): return default
    if v < 0: return 0
    return min(v, hi)

# ---------- database ----------

_MCOLS=set(); _HAS_CHAT=False; _DATE_NS=True

def _try(uri):
    # Open + probe as a unit: if the probe fails on an openable-but-odd file, the
    # connection is closed here rather than left dangling for the GC.
    global _MCOLS,_HAS_CHAT,_DATE_NS
    con=sqlite3.connect(uri,uri=True,timeout=5)
    try:
        con.row_factory=sqlite3.Row
        try: con.execute("PRAGMA busy_timeout=4000")
        except Exception: pass
        con.execute("SELECT 1 FROM message LIMIT 1")
        _MCOLS=set(r[1] for r in con.execute("PRAGMA table_info(message)"))
        tabs=set(r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'"))
        _HAS_CHAT={'chat','chat_message_join','chat_handle_join'} <= tabs
        mx=con.execute("SELECT MAX(date) FROM message").fetchone()[0] or 0
        _DATE_NS = mx > 10**14   # nanoseconds ~1e18; legacy seconds ~1e9
        return con
    except Exception:
        con.close(); raise

def _open():
    home=pwd.getpwuid(os.getuid()).pw_dir
    cands=[os.environ.get("IMSG_DB"),os.path.join(home,"Library/Messages/chat.db"),
           os.path.expanduser("~/Library/Messages/chat.db")]
    seen=[]; [seen.append(x) for x in cands if x and x not in seen]
    errs=[]
    for db in seen:
        if not os.path.exists(db): errs.append(f"{db}: not found"); continue
        # 1) read-only: with Full Disk Access this reads the live WAL, so the
        #    newest messages are included. This is the path that runs in practice.
        try:
            return _try(f"file:{db}?mode=ro")
        except Exception as e: errs.append(f"{db}(ro): {e}")
        # 2) fallback ONLY if (1) can't open the WAL (rare). immutable ignores the
        #    -wal, so the newest un-checkpointed messages may be missing — say so
        #    on stderr so a stale read is never silent. No copying: a manual copy
        #    of a live db+-wal+-shm can be torn/inconsistent, which is worse.
        try:
            con=_try(f"file:{db}?mode=ro&immutable=1")
            sys.stderr.write("imessage-fixed: warning — opened immutable; newest (WAL) messages may be missing\n")
            return con
        except Exception as e: errs.append(f"{db}(immutable): {e}")
    raise RuntimeError("cannot open chat.db :: "+json.dumps(
        {"hint":"grant Full Disk Access to the python below then restart Claude",
         "python":sys.executable,"home":home,"tried":seen,"errors":errs}))

def _thr(seconds_back):
    base=datetime.datetime.now().timestamp()-APPLE_EPOCH-seconds_back
    v=int(base*1e9) if _DATE_NS else int(base)
    return max(v,-2**63+1)

def _sf(alias="m"):
    # Exclude group-event rows (item_type != 0) and tapbacks/reactions
    # (associated_message_type != 0). Payments are item_type 0 / assoc 0, so they
    # pass. Guarded on column presence for schema variants.
    f=""
    if "item_type" in _MCOLS: f+=f" AND IFNULL({alias}.item_type,0)=0"
    if "associated_message_type" in _MCOLS: f+=f" AND IFNULL({alias}.associated_message_type,0)=0"
    return f

def _like_escape(s):
    return s.replace('\\','\\\\').replace('%','\\%').replace('_','\\_')

# Handle match: exact (short codes), +1-prefixed, +-prefixed, and de-prefixed.
_MATCH=("(h.id = :q OR h.id = '+1'||:q OR h.id = '+'||:q "
        "OR replace(replace(h.id,'+1',''),'+','') = :q)")

def _files(con,mid):
    try:
        rows=con.execute("""SELECT a.filename FROM message_attachment_join maj
          JOIN attachment a ON a.ROWID=maj.attachment_id WHERE maj.message_id=?""",(mid,)).fetchall()
        return [os.path.basename(r[0]) for r in rows if r[0]]
    except Exception: return []

def _row(con,r,want_files=False):
    d={"ts":_ts(_rk(r,"date")),"from_me":bool(_rk(r,"is_from_me")),
       "handle":_rk(r,"_handle") or ("me" if _rk(r,"is_from_me") else None),
       "text":_text(r)}
    if _rk(r,"cache_has_attachments"):
        d["attachments"]=_files(con,_rk(r,"ROWID")) if want_files else True
    if _rk(r,"display_name"): d["chat"]=_rk(r,"display_name")
    return d

def _nonempty(d):
    return bool(d.get("text") or d.get("attachments"))

def _chats_for_handle(con, handle):
    # Chat ROWIDs that include this handle. Prefer one-on-one chats (single
    # participant) so a direct thread isn't flooded by groups they're also in;
    # fall back to every chat with them if there's no 1:1.
    rows=con.execute(f"""SELECT chj.chat_id AS cid,
          (SELECT COUNT(*) FROM chat_handle_join x WHERE x.chat_id=chj.chat_id) AS npart
        FROM chat_handle_join chj JOIN handle h ON h.ROWID=chj.handle_id
        WHERE {_MATCH}""",{"q":str(handle)}).fetchall()
    ids=[r["cid"] for r in rows]
    solo=[r["cid"] for r in rows if r["npart"]==1]
    return solo or ids

# ---------- tools ----------

def read_thread(handle,limit=20):
    # Both sides of a conversation, newest first. Resolved through the chat so
    # SENT messages (handle_id = 0) are included. No silent fallback to the
    # by-handle path when chat tables exist — that path drops the sent side, and
    # hiding a failure behind it would resurrect the exact bug this fixes.
    limit=_clamp(limit,20,LIMIT_MAX); con=_open()
    try:
        cids=_chats_for_handle(con,handle) if _HAS_CHAT else []
        if cids:
            # The normal path: every message in this person's chat(s), both sides.
            ph=",".join("?"*len(cids))
            rows=con.execute(f"""SELECT m.*, h.id AS _handle FROM message m
              JOIN chat_message_join cmj ON cmj.message_id=m.ROWID
              LEFT JOIN handle h ON h.ROWID=m.handle_id
              WHERE cmj.chat_id IN ({ph}){_sf()}
              GROUP BY m.ROWID
              ORDER BY m.date DESC LIMIT ?""",(*cids,limit)).fetchall()
        else:
            # No chat for this handle (or a schema with no chat tables). There is
            # then no conversation, so no sent side to recover — the received-by-
            # handle rows are the complete answer. This runs only when the chat
            # lookup legitimately found nothing; a query ERROR is never swallowed
            # into this path, which would hide a regression of the sent-side fix.
            rows=con.execute(f"""SELECT m.*, h.id AS _handle FROM message m
              JOIN handle h ON h.ROWID=m.handle_id
              WHERE {_MATCH}{_sf()} ORDER BY m.date DESC LIMIT :lim""",
              {"q":str(handle),"lim":limit}).fetchall()
        return [d for d in (_row(con,r,True) for r in rows) if _nonempty(d)]
    finally:
        con.close()

def recent(hours=24,limit=60):
    hours=_clamp(hours,24,HOURS_MAX); limit=_clamp(limit,60,LIMIT_MAX); con=_open()
    try:
        thr=_thr(hours*3600)
        rows=con.execute(f"""SELECT m.*, h.id AS _handle FROM message m
          LEFT JOIN handle h ON h.ROWID=m.handle_id
          WHERE m.date>:thr{_sf()} ORDER BY m.date DESC LIMIT :lim""",{"thr":thr,"lim":limit}).fetchall()
        return [d for d in (_row(con,r) for r in rows) if _nonempty(d)]
    finally:
        con.close()

def search(query,days=30,limit=40):
    # Two passes so a text-column match is never silently dropped by a scan cap.
    # Pass 1 lets SQL filter the text column, so recall there is COMPLETE within
    # the window (bounded only by `limit`). Pass 2 covers messages whose words live
    # only in the attributedBody blob — those require decoding, so it is a bounded,
    # best-effort scan of the most recent such messages.
    q=(query or '').strip()
    if not q: return []
    days=_clamp(days,30,DAYS_MAX); limit=_clamp(limit,40,LIMIT_MAX)
    if limit==0: return []
    con=_open()
    try:
        thr=_thr(days*86400); like=f"%{_like_escape(q)}%"; ql=q.lower()
        seen=set(); out=[]
        for r in con.execute(f"""SELECT m.*, h.id AS _handle FROM message m
              LEFT JOIN handle h ON h.ROWID=m.handle_id
              WHERE m.date>:thr{_sf()} AND m.text LIKE :like ESCAPE '\\'
              ORDER BY m.date DESC LIMIT :lim""",{"thr":thr,"like":like,"lim":limit}):
            rid=_rk(r,"ROWID")
            if rid in seen: continue
            seen.add(rid); out.append(_row(con,r))
            if len(out)>=limit: break
        if len(out)<limit:
            cap=min(limit*50,4000)
            for r in con.execute(f"""SELECT m.*, h.id AS _handle FROM message m
                  LEFT JOIN handle h ON h.ROWID=m.handle_id
                  WHERE m.date>:thr{_sf()} AND IFNULL(m.text,'') NOT LIKE :like ESCAPE '\\'
                    AND m.attributedBody IS NOT NULL
                  ORDER BY m.date DESC LIMIT :cap""",{"thr":thr,"like":like,"cap":cap}):
                rid=_rk(r,"ROWID")
                if rid in seen: continue
                d=_row(con,r)
                if ql in (d["text"] or "").lower():
                    seen.add(rid); out.append(d)
                    if len(out)>=limit: break
        out.sort(key=lambda d: d["ts"] or "", reverse=True)
        return out
    finally:
        con.close()

def list_threads(hours=72,limit=40):
    # Enumerate CONVERSATIONS (chats), not handle_ids. Exactly one latest message
    # per chat (highest ROWID at the max date, so tied timestamps don't fan out),
    # ordered newest chat first.
    hours=_clamp(hours,72,HOURS_MAX); limit=_clamp(limit,40,LIMIT_MAX); con=_open()
    try:
        if not _HAS_CHAT: return []
        thr=_thr(hours*3600)
        rows=con.execute(f"""
          WITH g AS (SELECT cmj.chat_id AS cid, COUNT(*) AS cnt, MAX(m.date) AS mx
                     FROM chat_message_join cmj JOIN message m ON m.ROWID=cmj.message_id
                     WHERE m.date>:thr{_sf()} GROUP BY cmj.chat_id)
          SELECT c.display_name AS _dn, c.chat_identifier AS _ci, g.cnt AS cnt, m2.*, h.id AS _handle
          FROM g JOIN chat c ON c.ROWID=g.cid
          JOIN message m2 ON m2.ROWID=(
              SELECT m3.ROWID FROM chat_message_join cj3 JOIN message m3 ON m3.ROWID=cj3.message_id
              WHERE cj3.chat_id=g.cid AND m3.date=g.mx{_sf('m3')} ORDER BY m3.ROWID DESC LIMIT 1)
          LEFT JOIN handle h ON h.ROWID=m2.handle_id
          ORDER BY g.mx DESC LIMIT :lim""",{"thr":thr,"lim":limit}).fetchall()
        out=[]
        for r in rows:
            d=_row(con,r); d["conversation"]=_rk(r,"_dn") or _rk(r,"_ci"); d["count"]=_rk(r,"cnt")
            out.append(d)
        return out
    finally:
        con.close()

def read_chat(name,limit=30):
    nm=(name or '').strip()
    if not nm: return []
    limit=_clamp(limit,30,LIMIT_MAX); con=_open()
    try:
        like=f"%{_like_escape(nm)}%"
        rows=con.execute(f"""SELECT m.*, h.id AS _handle, c.display_name FROM message m
          JOIN chat_message_join cmj ON cmj.message_id=m.ROWID
          JOIN chat c ON c.ROWID=cmj.chat_id
          LEFT JOIN handle h ON h.ROWID=m.handle_id
          WHERE (c.display_name LIKE :q ESCAPE '\\' OR c.chat_identifier LIKE :q ESCAPE '\\'){_sf()}
          ORDER BY m.date DESC LIMIT :lim""",{"q":like,"lim":limit}).fetchall()
        return [d for d in (_row(con,r,True) for r in rows) if _nonempty(d)]
    finally:
        con.close()

TOOLS=[
 {"name":"imsg_read_thread","description":"Read a conversation by phone number OR short code (e.g. 123456, 5551234567, +15551234567) — BOTH sides, the messages you sent and received, newest-first, with from_me and attachments.",
  "inputSchema":{"type":"object","properties":{"handle":{"type":"string"},"limit":{"type":"integer","default":20}},"required":["handle"]}},
 {"name":"imsg_recent","description":"Every message across all conversations in the last N hours, sent and received, read-state-independent.",
  "inputSchema":{"type":"object","properties":{"hours":{"type":"integer","default":24},"limit":{"type":"integer","default":60}},"required":[]}},
 {"name":"imsg_search","description":"Full-text search decoded message bodies (sent and received) over the last N days.",
  "inputSchema":{"type":"object","properties":{"query":{"type":"string"},"days":{"type":"integer","default":30},"limit":{"type":"integer","default":40}},"required":["query"]}},
 {"name":"imsg_list_threads","description":"Enumerate recent conversations (name, message count, latest message) in the last N hours — the durable way to discover threads.",
  "inputSchema":{"type":"object","properties":{"hours":{"type":"integer","default":72},"limit":{"type":"integer","default":40}},"required":[]}},
 {"name":"imsg_read_chat","description":"Read a named conversation (group chat or contact display name / identifier) by substring match, both sides.",
  "inputSchema":{"type":"object","properties":{"name":{"type":"string"},"limit":{"type":"integer","default":30}},"required":["name"]}},
]

def dispatch(n,a):
    a=a or {}
    if n=="imsg_read_thread": return read_thread(a.get("handle"),a.get("limit",20))
    if n=="imsg_recent": return recent(a.get("hours",24),a.get("limit",60))
    if n=="imsg_search": return search(a.get("query"),a.get("days",30),a.get("limit",40))
    if n=="imsg_list_threads": return list_threads(a.get("hours",72),a.get("limit",40))
    if n=="imsg_read_chat": return read_chat(a.get("name"),a.get("limit",30))
    raise ValueError("unknown tool "+str(n))

def handle_req(req):
    if not isinstance(req,dict): return None       # ignore non-object JSON / batches, never crash
    m=req.get("method"); i=req.get("id")
    if m=="initialize":
        pv=(req.get("params") or {}).get("protocolVersion") or "2025-06-18"
        return {"jsonrpc":"2.0","id":i,"result":{"protocolVersion":pv,"capabilities":{"tools":{}},"serverInfo":{"name":"imessage-fixed","version":VERSION}}}
    if m=="tools/list": return {"jsonrpc":"2.0","id":i,"result":{"tools":TOOLS}}
    if m=="tools/call":
        p=req.get("params") or {}
        try: res=dispatch(p.get("name"),p.get("arguments") or {})
        except Exception as e:
            return {"jsonrpc":"2.0","id":i,"result":{"content":[{"type":"text","text":"error: "+str(e)}],"isError":True}}
        return {"jsonrpc":"2.0","id":i,"result":{"content":[{"type":"text","text":json.dumps(res,ensure_ascii=False)}]}}
    if m and m.startswith("notifications/"): return None
    if i is not None: return {"jsonrpc":"2.0","id":i,"error":{"code":-32601,"message":"method not found"}}
    return None

def main():
    for line in sys.stdin:
        line=line.strip()
        if not line: continue
        try:
            r=handle_req(json.loads(line))
        except Exception:
            continue          # a bad line never takes the server down
        if r is not None:
            sys.stdout.write(json.dumps(r)+"\n"); sys.stdout.flush()

if __name__=="__main__": main()
