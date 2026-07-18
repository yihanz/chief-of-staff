#!/usr/bin/env python3
# imessage-fixed v1.1.0 — read-only iMessage MCP reader (Python stdlib only).
# Fixes the stock connector's short-code + attributedBody defects; adds thread
# enumeration, named-chat reads, attachments; schema-aware and defensive.
import sys, os, re, json, sqlite3, pwd, datetime

VERSION = "1.2.0"
APPLE_EPOCH = 978307200

_BAD = ('streamtyped','NSMutableString','NSString','NSAttributedString','NSDictionary',
        'NSObject','NSValue','NSNumber','NSData','NSMutableData','__kIM','bplist','$class',
        '$archiver','NSKeyedArchiver','NSMutableAttributedString','DDScannerResult',
        'NSParagraphStyle','NSColor','NSFont','NSRange','WNSArray')
_TAILCUT = ('HttpURL','__kIM','NSHTTPURL','NSColor','NSFont','NSParagraph')

def _decode_typed(blob):
    # Parse the NSArchiver typedstream properly: locate the NSString class
    # marker, then read its length prefix and take exactly that many bytes.
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
        n = int.from_bytes(blob[p:p+2], 'little'); p += 2
    elif n == 130:
        n = int.from_bytes(blob[p:p+4], 'little'); p += 4
    elif n > 127:
        return ''
    if n <= 0 or p + n > len(blob): return ''
    return blob[p:p+n].decode('utf-8', 'replace')

def _decode_fallback(blob):
    # Only if the typedstream parse fails. Keeps EVERY printable run
    # (never just the longest) so multi-paragraph text is not truncated.
    if isinstance(blob,str): blob=blob.encode('utf-8','replace')
    t = blob.decode('utf-8','replace')
    runs=[]; cur=[]
    for ch in t:
        if ord(ch) < 32 or ord(ch) == 127 or ord(ch) == 65533:
            if cur:
                s = ''.join(cur)
                if len(s) >= 2: runs.append(s)
                cur=[]
        else:
            cur.append(ch)
    if cur:
        s = ''.join(cur)
        if len(s) >= 2: runs.append(s)
    runs = [r for r in runs if not any(b in r for b in _BAD)]
    return chr(10).join(runs).strip()

def _decode(blob):
    if not blob: return ''
    s = _decode_typed(blob)
    if s: return s
    return _decode_fallback(blob)
def _rk(row,key,default=None):
    try: return row[key]
    except (IndexError,KeyError): return default

def _text(row):
    # Prefer whichever source is MORE complete. The old rule discarded a
    # clean URL-only text column in favour of a corrupted decode.
    t = (_rk(row, 'text') or '').strip()
    a = _decode(_rk(row, 'attributedBody'))
    if a and len(a) > len(t): return a
    return t or a
def _ts(ns):
    if ns is None: return None
    try:
        secs = ns/1e9+APPLE_EPOCH if ns>10**11 else ns+APPLE_EPOCH
        return datetime.datetime.fromtimestamp(secs).strftime("%Y-%m-%d %H:%M:%S")
    except Exception: return None

def _thr_ns(seconds_back):
    v=int((datetime.datetime.now().timestamp()-APPLE_EPOCH-seconds_back)*1e9)
    return max(v,-2**63+1)

_MCOLS=set()
def _open():
    errs=[]; home=pwd.getpwuid(os.getuid()).pw_dir
    cands=[os.environ.get("IMSG_DB"),os.path.join(home,"Library/Messages/chat.db"),
           os.path.expanduser("~/Library/Messages/chat.db")]
    seen=[]; [seen.append(x) for x in cands if x and x not in seen]
    for db in seen:
        if not os.path.exists(db): errs.append(f"{db}: not found"); continue
        for uri in (f"file:{db}?mode=ro",f"file:{db}?mode=ro&immutable=1"):
            try:
                con=sqlite3.connect(uri,uri=True,timeout=5); con.row_factory=sqlite3.Row
                try: con.execute("PRAGMA busy_timeout=4000")
                except Exception: pass
                con.execute("SELECT 1 FROM message LIMIT 1")
                global _MCOLS; _MCOLS=set(r[1] for r in con.execute("PRAGMA table_info(message)"))
                return con
            except Exception as e: errs.append(f"{db}({uri.split('?')[1]}): {e}")
    raise RuntimeError("cannot open chat.db :: "+json.dumps(
        {"hint":"grant Full Disk Access to the python below then restart Claude",
         "python":sys.executable,"home":home,"tried":seen,"errors":errs}))

def _sf(alias="m"):
    f=""
    if "item_type" in _MCOLS: f+=f" AND IFNULL({alias}.item_type,0)=0"
    if "associated_message_type" in _MCOLS: f+=f" AND IFNULL({alias}.associated_message_type,0)=0"
    return f

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

def read_thread(handle,limit=20):
    con=_open()
    rows=con.execute(f"""SELECT m.*, h.id AS _handle FROM message m JOIN handle h ON h.ROWID=m.handle_id
      WHERE {_MATCH}{_sf()} ORDER BY m.date DESC LIMIT :lim""",{"q":str(handle),"lim":limit}).fetchall()
    out=[_row(con,r,True) for r in rows]; con.close(); return out

def recent(hours=24,limit=60):
    con=_open(); thr=_thr_ns(hours*3600)
    rows=con.execute(f"""SELECT m.*, h.id AS _handle FROM message m JOIN handle h ON h.ROWID=m.handle_id
      WHERE m.date>:thr{_sf()} ORDER BY m.date DESC LIMIT :lim""",{"thr":thr,"lim":limit}).fetchall()
    out=[d for d in (_row(con,r) for r in rows) if d["text"] or d.get("attachments")]; con.close(); return out

def search(query,days=30,limit=40):
    con=_open(); thr=_thr_ns(days*86400)
    rows=con.execute(f"""SELECT m.*, h.id AS _handle FROM message m JOIN handle h ON h.ROWID=m.handle_id
      WHERE m.date>:thr{_sf()} ORDER BY m.date DESC""",{"thr":thr})
    out=[]
    for r in rows:
        d=_row(con,r)
        if query.lower() in (d["text"] or "").lower():
            out.append(d)
            if len(out)>=limit: break
    con.close(); return out

def list_threads(hours=72,limit=40):
    con=_open(); thr=_thr_ns(hours*3600)
    rows=con.execute(f"""SELECT h.id AS _handle, g.cnt, m2.* FROM
      (SELECT handle_id, COUNT(*) cnt, MAX(date) mx FROM message m
       WHERE m.date>:thr{_sf()} GROUP BY handle_id ORDER BY mx DESC LIMIT :lim) g
      JOIN handle h ON h.ROWID=g.handle_id
      JOIN message m2 ON m2.handle_id=g.handle_id AND m2.date=g.mx""",{"thr":thr,"lim":limit}).fetchall()
    out=[]
    for r in rows:
        d=_row(con,r); d["count"]=_rk(r,"cnt"); out.append(d)
    con.close(); return out

def read_chat(name,limit=30):
    con=_open()
    try:
        rows=con.execute(f"""SELECT m.*, h.id AS _handle, c.display_name FROM message m
      JOIN chat_message_join cmj ON cmj.message_id=m.ROWID
      JOIN chat c ON c.ROWID=cmj.chat_id
      LEFT JOIN handle h ON h.ROWID=m.handle_id
      WHERE (c.display_name LIKE :q OR c.chat_identifier LIKE :q){_sf()}
      ORDER BY m.date DESC LIMIT :lim""",{"q":f"%{name}%","lim":limit}).fetchall()
    except Exception as e:
        con.close()
        raise RuntimeError('read_chat query failed: ' + str(e))
    out=[_row(con,r,True) for r in rows]; con.close(); return out

TOOLS=[
 {"name":"imsg_read_thread","description":"Read a thread by phone number OR short code (e.g. 123456, 5551234567, +15551234567). Decoded text newest-first, with from_me and attachments.",
  "inputSchema":{"type":"object","properties":{"handle":{"type":"string"},"limit":{"type":"integer","default":20}},"required":["handle"]}},
 {"name":"imsg_recent","description":"Every message across all senders in the last N hours, read-state-independent.",
  "inputSchema":{"type":"object","properties":{"hours":{"type":"integer","default":24},"limit":{"type":"integer","default":60}},"required":[]}},
 {"name":"imsg_search","description":"Full-text search decoded message bodies over the last N days.",
  "inputSchema":{"type":"object","properties":{"query":{"type":"string"},"days":{"type":"integer","default":30},"limit":{"type":"integer","default":40}},"required":["query"]}},
 {"name":"imsg_list_threads","description":"Enumerate recent conversations (sender, message count, latest message) in the last N hours — the durable way to discover senders.",
  "inputSchema":{"type":"object","properties":{"hours":{"type":"integer","default":72},"limit":{"type":"integer","default":40}},"required":[]}},
 {"name":"imsg_read_chat","description":"Read a named conversation (group chat or contact display name / identifier) by substring match.",
  "inputSchema":{"type":"object","properties":{"name":{"type":"string"},"limit":{"type":"integer","default":30}},"required":["name"]}},
]

def dispatch(n,a):
    if n=="imsg_read_thread": return read_thread(a["handle"],a.get("limit",20))
    if n=="imsg_recent": return recent(a.get("hours",24),a.get("limit",60))
    if n=="imsg_search": return search(a["query"],a.get("days",30),a.get("limit",40))
    if n=="imsg_list_threads": return list_threads(a.get("hours",72),a.get("limit",40))
    if n=="imsg_read_chat": return read_chat(a["name"],a.get("limit",30))
    raise ValueError("unknown tool "+str(n))

def handle_req(req):
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
        try: req=json.loads(line)
        except Exception: continue
        r=handle_req(req)
        if r is not None: sys.stdout.write(json.dumps(r)+"\n"); sys.stdout.flush()

if __name__=="__main__": main()
