# iMessage Fixed Reader

A read-only iMessage reader for Claude on macOS. It exists because the stock
iMessage connector has defects that make it miss real messages, and this fixes
them. It is independently useful — you do not need the chief-of-staff brief to
want it — and it is what that brief reads when it asks "did a text move one of
today's plans?"

MIT-licensed and self-contained: one Python file, standard library only, no
network, no writes. It ships with a 40-case test suite (`test_reader.py`, run it
with `python3 test_reader.py`) covering the sent-side fix, handle matching,
decoding, payments, exclusions, schema variants, malformed-input survival, and
the JSON-RPC lifecycle.

---

## What it fixes

**1. It reads the messages you SENT — the stock reader drops almost all of them.**
This is the big one. In the Messages database, a message you send is stored with
`handle_id = 0` (there's no external "sender" — it's you). Any reader that finds
messages by joining on `handle_id`, as the stock one does, therefore discards
your entire side of every conversation. Measured on a real 207,000-message
database: of 92,925 sent messages, the old join returned **5,005** — it was
losing **95%** of everything the owner had ever said. A conversation read that
way is half a transcript, and you cannot tell who said what. This reader resolves
a thread through its **chat membership** instead of the handle, and `LEFT JOIN`s
everywhere, so sent and received both come back, each marked `from_me`. On that
same database it now returns all **92,925**.

**2. Short-code and bare-number handles never matched.** The stock reader
forces a `+1` country prefix onto the handle it queries, so a two-factor code
from `123456`, or a number saved without `+1`, returned nothing — the message
was there and the tool said empty. This matches the handle in every shape it
actually takes: exact, `+1`-prefixed, and de-prefixed.

**3. Message text was lost to encoding.** Modern Messages often stores the
real sentence in an `attributedBody` blob (an NSArchiver typedstream) and
leaves the `text` column empty or holding only a URL. The stock reader returned
the raw hex or the bare URL — the actual words gone. This decodes the
typedstream properly (Unicode-aware, multi-paragraph safe) and prefers
whichever source is more complete.

**4. Apple Cash and other app messages came back blank.** A payment or an
iMessage-app message keeps its content in `payload_data`, not `text`, so it read
as an empty line or vanished. Payments are now surfaced as `[Apple Cash: $50.00]`
(the amount when it can be read cleanly, otherwise `[Apple Cash payment]`), and
other app balloons get a short label instead of a blank.

It also adds what the stock reader lacks: **thread enumeration** (discover which
conversations are active without knowing a number first), **named-chat reads**
(a group chat or contact by name), and **attachment filenames**.

Reactions (tapbacks) and system rows (someone renamed the group, joined, left)
are deliberately filtered out — they are not conversation, and for reading a
thread they are noise.

---

## What it reads, and what it does not

Everything here is stated so you can decide, not to alarm you.

- It reads your local Messages database — the same `~/Library/Messages/chat.db`
  the Messages app uses — **read-only**, opened with SQLite's `mode=ro` and
  `immutable` flags. It cannot modify a message, send one, or delete one. There
  is no write path in the code.
- That database contains **messages other people sent you**. Reading it means
  their words are visible to the model in your session, on your machine. They
  did not opt into that; you are deciding it for them. That is a real thing to
  weigh, and it is the honest reason this is off by default and opt-in.
- Nothing it reads leaves your computer except insofar as you send it to Claude
  in a session you started. The reader has no network code — it speaks only to
  Claude over local stdin/stdout.
- macOS gates the Messages database behind **Full Disk Access**. Nothing can
  read it — not this, not the stock connector — until you grant that access
  yourself, deliberately, in System Settings. That gate is macOS protecting you,
  and it is the one manual step you cannot skip.

---

## Prerequisites

- **macOS** (the Messages database is an Apple format).
- **Python 3** — the reader is standard-library only, so any `python3` works.
  If `python3` is missing, install Apple's command-line tools once:
  `xcode-select --install`.
- **Claude Desktop** — extensions run on the desktop app, not the web app.

---

## Install

**The reader (2 minutes):**

1. Double-click `imessage-fixed.dxt` in this folder. Claude Desktop opens and
   offers to install it. (If you would rather not run a prebuilt bundle, see
   "Build it yourself" below — it is one `zip` command over the same files.)
2. Grant **Full Disk Access** so it can reach the Messages database:
   System Settings → Privacy & Security → Full Disk Access → turn on the entry
   for Claude (or for the Python it runs, if that appears instead).
3. Quit and reopen Claude Desktop.

**Check it works:** ask Claude *"list my recent iMessage threads."* If it comes
back with senders and counts, you are done. If it says it cannot open the
database, Full Disk Access is not granted yet — redo step 2 and restart.

**Build it yourself instead of using the prebuilt bundle:**

```
cd companions/imessage-fixed
zip -r imessage-fixed.dxt manifest.json server
```

A `.dxt` is just a zip of `manifest.json` plus the `server/` folder; double-click
the one you built. Or skip the bundle entirely and point a raw MCP config at
`server/main.py` with `python3`.

---

## If the chief-of-staff brief uses this

Reading messages is a **local** capability: the database lives on your Mac, so a
scheduled brief that depends on it runs on your Mac, which means it fires when
your computer is awake rather than on a fixed cloud schedule. That is the
trade the brief's own docs describe — richer input, less reliable timing. Add
it when the messages you want caught (a plumber who texted a new time, a friend
who moved dinner) are worth a brief that waits for your laptop. If they are not,
the brief runs fine without it.

---

## Tools

| Tool | What it returns |
|---|---|
| `imsg_list_threads` | Recent conversations — sender, message count, latest line. The durable way to discover senders. |
| `imsg_read_thread` | One thread by phone number or short code, newest first, with attachments. |
| `imsg_read_chat` | A named group chat or contact, by substring match. |
| `imsg_recent` | Every message across all senders in the last N hours, read-state-independent. |
| `imsg_search` | Full-text search over decoded message bodies. |

---

## License and independence

MIT (see `LICENSE`). This tool is separately licensed from the chief-of-staff
plugin it ships beside — the plugin's personal-use terms do not apply here, and
you may lift this folder into its own repository and use it anywhere. It fixes a
general problem with the stock connector and stands on its own.
