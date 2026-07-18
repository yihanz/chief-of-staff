# Every dependency — what this can use, what it needs, and how to turn it on

This is the whole menu in one place. `references/STACK.md` argues *why* each role
matters and what disqualifies a surface; this file is the practical list: what each
thing is, whether you need it, what it costs you, and the exact way to switch it on.

**Two are required. Everything else is optional — but optional is not the same as
unmapped.** An optional connector you turn on still changes what the brief can see,
still needs a credential, still carries a cost someone should have named for you
before you enabled it. So every one of them is here, treated the same way, whether
you end up using it or not.

**One principle worth stating, because it looks like a contradiction and isn't.**
The law and the engine never name a product — they speak in roles, so they stay true
about the next person who reads them. *This* file names real products on purpose,
because a person deciding what to connect cannot act on "a lifelog role." Naming Bee
here as one option you can swap out is the opposite of building "Bee" into the law.
The first helps you act; the second would make the law wrong about someone who has
never heard of it. Both serve the same goal: a thing that works for a stranger, not a
transcript of one person's setup.

---

## The whole menu at a glance

| Capability | Role | Need it? | How it connects | We ship it? |
|---|---|---|---|---|
| A task list | `~~state` — the engine's memory | **Required** | Hosted connector (claude.ai) | You bring one |
| A calendar | `~~container` — where your body is | **Required** | Hosted connector (claude.ai) | You bring one |
| Mail | `~~inbound[]` + `~~evidence[]` | Optional | Hosted connector | You bring one |
| Messages (iMessage) | `~~inbound[]` + `~~evidence[]` | Optional | **Bundled** Desktop Extension | **Yes — `companions/imessage-fixed/`** |
| Notes / second brain | `~~intent[]` | Optional | Extension, or local server | You bring one |
| A lifelog | `~~evidence[]` | Optional | Local server (CLI) | You bring one |
| Health records | `~~evidence[]` | Optional | Hosted connector | You bring one |
| Fitness / workouts | `~~evidence[]` | Optional | Local server (npm) | You bring one |
| Mac automation | capability enabler | Optional | Extension (Browse) | You bring one |

"You bring one" is not a dodge — the next section gives the exact steps for each. Only
one capability could honestly be packaged into this plugin, and it was; the reasoning
for the rest is at the bottom.

---

## The two you need

**A task list — `~~state`.** The engine keeps no memory between runs; your list *is*
its memory. Any personal task manager with a completed-items history and durations
works. **Todoist** is the reference surface it was proven against and the safest
default. A work tracker (Linear, Jira, Asana) is the wrong home for this — see the
Phase 0 fork in setup and the work-tracker verdict in STACK; keep the work tracker as
an `~~inbound[]` source instead. Enable in claude.ai → Settings → Connectors.

**A calendar — `~~container`.** Read/write, multiple calendars, per-calendar access.
**Google Calendar** is the common one. iCloud and Outlook work if they present a
writable connector. Enable in claude.ai → Settings → Connectors.

With just these two, connected and nothing else, the brief runs in the cloud, fires
with your computer off, and delivers a real card. Everything below makes it see more.

---

## The optional rungs — what each is, what it costs, how to switch it on

Each entry: what it adds to the card · the honest cost · the exact enable path ·
the credential it needs. Turn on the ones whose gain is worth their cost; skip the
rest; the brief degrades cleanly around whatever you leave off and tells you in one
line what it could not reach.

### Mail — `~~inbound[]` + `~~evidence[]`
- **Adds:** an obligation a person emailed you that never became a task; and closure
  evidence ("paid, per your receipt") from sent mail.
- **Cost:** mail is a tripwire — a stranger can write to it, so it is read for
  obligations but is drafts-only for replies (a property of the surface; the engine
  has no send step). Hosted, so it keeps the brief cloud-eligible.
- **Enable:** claude.ai → Settings → Connectors → **Gmail** (or a Google Workspace /
  Outlook mail connector). **Spark** (Readdle) is a Desktop Extension alternative if
  you live in Spark.
- **Credential:** OAuth, one click.

### Messages (iMessage) — `~~inbound[]` + `~~evidence[]`  ·  **bundled**
- **Adds:** the text that moved a plan — a plumber who pushed a time, a friend who
  changed dinner. Closes the card's `read N/M` blind spot on messages.
- **Cost:** local — the Messages database lives on your Mac, so a brief that uses it
  leaves the pure-cloud path and puts the morning schedule at risk (the exact mechanism
  is the contested one under *How the four enable paths differ*). Reading it means other
  people's words are visible in your session; it is read-only and never leaves your machine.
- **Enable:** this repo ships a fixed reader — double-click
  `companions/imessage-fixed/imessage-fixed.dxt`, grant Full Disk Access, restart. Full
  steps and the stock-connector defects it fixes — starting with reading the messages you
  sent, which the stock reader drops by ~95% — are in `companions/imessage-fixed/README.md`.
- **Credential:** Full Disk Access (macOS gate, you grant it).

### Notes / second brain — `~~intent[]`
- **Adds:** your own thinking as a source — a plan you wrote down that implies a task,
  a decision you can cite.
- **Cost:** most people do not keep a second brain, and nothing is a legitimate answer.
  If the notes live in a local app, the brief that reads them runs locally.
- **Enable, by app:**
  - **Apple Notes** — Desktop Extension: Settings → Extensions → Browse → Apple Notes.
  - **Notion** — hosted connector: claude.ai → Settings → Connectors → Notion.
  - **Reflect** — runs a local MCP endpoint; connect it with `mcp-remote` pointed at
    Reflect's local address (see `mcp.example.json` for the shape). Needs the Reflect
    app running.
- **Credential:** per app — OAuth (Notion), Full Disk Access (Apple Notes), the local
  endpoint (Reflect).

### A lifelog — `~~evidence[]`
- **Adds:** what was actually *said*, not just what got written down — the highest-
  recall evidence source and the one with the sharpest cost.
- **Cost:** the real one is other people. A wearable that records your day captures the
  voices of people who never consented to being indexed. That is a genuine thing to
  weigh, and the honest reason to think it through. Local, so it puts the morning
  schedule at risk the same contested way every local reader does, and it is a corpus
  you maintain.
- **Enable:** **Bee** is the example — install the official `bee` CLI and run
  `bee mcp serve`; needs a Bee device and account. (A local search index over your own
  Bee transcripts is a power-user build on top of that — see the note at the bottom on
  why it is not bundled.)
- **Credential:** a Bee account; the CLI handles auth.

### Health records — `~~evidence[]`
- **Adds:** evidence for health-lane tasks — a result to check, a medication to
  reconcile against what a task claims.
- **Cost:** the most sensitive data you can route through a session. Enable it only
  when a health lane is real for you.
- **Enable:** a health-records hosted connector in claude.ai → Settings → Connectors.
- **Credential:** OAuth to the records provider.

### Fitness / workouts — `~~evidence[]`
- **Adds:** a niche but real evidence source — did the workout a task planned actually
  happen.
- **Cost:** low; it is your own log.
- **Enable:** **Hevy** is the example — `npx hevy-mcp`, with a Hevy API key in the
  server's environment (see `mcp.example.json`).
- **Credential:** `HEVY_API_KEY` from the Hevy app.

### Mac automation — capability enabler (not a role)
- **Adds:** local reads and automations that hosted connectors cannot reach — driving
  a local app, reading a local file a connector does not expose.
- **Cost:** it is a general capability — it can do what AppleScript can, which is the
  power and the price in one fact. When a purpose-built read-only tool exists for what
  you want (the bundled iMessage reader is exactly that), prefer it; reach for general
  automation when you actually need the breadth.
- **Enable:** the **"Control your Mac"** extension — Settings → Extensions → Browse.
  It is community-authored (Kenneth Lien / k6l3), open-source, MIT; it is listed in the
  directory, not built by Anthropic. Current details in `references/VOLATILE.md`.
- **Credential:** none beyond installing it; macOS still gates what it can touch.

---

## How the four enable paths differ

You will hit exactly four kinds of "turn it on," and knowing which is which saves the
confusion of looking for a connector that is actually an extension:

1. **Hosted connector** — claude.ai → Settings → Connectors. OAuth, one click, works on
   every surface including mobile, keeps the brief cloud-eligible. Mail, calendar,
   task list, Notion, health. *Prefer these.*
2. **Desktop Extension** — the desktop app → Settings → Extensions → Browse (or a
   bundled `.dxt` you double-click). Runs locally. Apple Notes, Control your Mac, the
   bundled iMessage reader.
3. **Local MCP server** — an entry in the desktop app's config (or `npx`-launched), for
   tools that ship as a package or a script. Reflect, Hevy, Bee. `mcp.example.json`
   shows the shape for each; it is an inert example, nothing loads it until you rename
   and edit it.
4. **Bundled** — shipped in this repo, you install it. Only the iMessage reader.

A hosted connector keeps you in the cloud. Every local one (2, 3, 4) is richer for the
role it fills and puts that brief's schedule at risk — the vendor's own docs contradict
themselves on exactly how (it either pins the run to a waking Mac, or the scheduled task
can't reach the local file at all, which is worse), and under either reading a local
reader is what costs you the reliable morning. The whole picture, both readings, is in
`assets/where-it-runs.mermaid` and `references/VOLATILE.md` → Scheduling.

---

## Why only the iMessage reader is bundled

You might reasonably ask why this package ships a fixed iMessage reader but not a Bee
index or a Reflect bridge. The line is not favoritism; it is three honest tests, and
only one capability passes all three:

- **Universal** — everyone on a Mac has Messages. Almost nobody has a Bee.
- **Fixes a real defect** — the stock iMessage connector silently drops short-code
  senders and loses message text to an encoding bug; the fix is worth shipping. The
  other tools work fine through their own official paths.
- **Clean to ship** — one file, standard library, no account, no personal data baked
  in. A Bee index needs the device, an account, a multi-file build pipeline, and — in
  its author's own build — a line that counts *his* utterances by name. That is a
  personal setup, not a product, and packaging it would be exactly the mistake this
  whole system is trying not to make.

So: the iMessage reader is bundled because it is universal, corrective, and clean.
Everything else is mapped, with the real path to turn it on, because that is what it
honestly is — a great tool you connect, not one we can hand you.
