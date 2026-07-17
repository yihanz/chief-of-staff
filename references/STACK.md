# The stack — what this needs, what each piece does, and what substitutes for it

> **Where it runs is a picture:** `assets/where-it-runs.mermaid` — the cloud-vs-local fork, and why
> every local reader you add costs you the schedule. Read it beside the cloud/local section below.

Everything about connectors in one place: what each role is for, what actually fills it, what
happens when you swap something out, and what provably cannot be bundled.

**No prices and no click paths live here.** They are in `references/VOLATILE.md`, dated and cited.
This file carries the *shapes* and the *arguments*. **The numbers move; the arguments don't.**

**Verified live on 2026-07-17.** The surfaces below were **probed by calling their connectors**, not
read out of their documentation — which matters, because the headline finding is a case where the
documentation and the live call disagree. **Ⓔ marks a claim established by a live call in that
probe.** **⚠️ marks a claim that is NOT VERIFIED** — inferred, single-sourced, or read from a doc and
never tested. **Re-probe anything here older than about three months**; a tool set can change in a
day, and one below changed while this file was being written.

---

## How tool references work

Plugin files use `~~role` as a placeholder for whatever tool you connect in that role. This plugin
is tool-agnostic — it describes workflows in terms of roles rather than products. At run time the
engine **probes for what is actually connected** and does the most it can with what it finds.

**A listed tool is not a capability.** The engine never assumes a role is filled because this file
mentions it. It detects, then acts, then reports what it could not reach.

---

## The roles — two CONTRACTS, three SETS

This mirrors the law's §0b exactly. **A CONTRACT is a set of capabilities a tool either has or does
not have — testable, universal, asked of every person on earth. A SET is whatever this person
happens to have.** The old framing on this page — a tier table listing *mail, notes, messages,
lifelog* as first-class roles — described one person's stack and called it an architecture. It is
gone.

### The two contracts — mandatory, capability-tested, identical for everyone

**`~~state`** (alias: `~~task surface`) — **the engine's database.** The engine keeps no cache and no
memory between runs; **the list is the state.** Four questions, and the answers are not all
pass/fail:

1. **What is open?** Every task manager answers this. It is the least of the four, and it is the only
   one most people check before choosing a tool.
2. **What did you already complete?** An open-row search cannot answer an existence question.
   Without this the engine rebuilds a row you closed an hour ago, forever. **Required.**
3. **Who placed this row — the engine, or you?** Answerable **only by a CLIENT field on the activity
   log.** **Not pass/fail — the answer selects the mode.** See the finding below; it is the reason
   this page was rewritten.
4. **What does it cost — a duration on a row?** A block has a length. Without a duration the engine
   cannot state the cost or enforce the 30-minute floor, and a dated row renders as an all-day
   banner instead of a block.

**And `~~state` must be PERSONAL and DURABLE** — a test of the container, not the feature list. A
surface can answer all four and still fail it. That argument is below.

**`~~container`** (alias: `~~calendar`) — **the physical narrative of where your body is.** Four
capabilities: events over a window (read); **write, proven by attempt, never inferred**; multiple
calendars, enumerable; an access role per calendar, confirmed on the events call.

### The three sets — plural, optional, whatever you actually have

Written `[]` because the cardinality is the point: **zero, one, or five. None is required.**

- **`~~inbound[]`** — every stream where another person can put an obligation on you.
- **`~~intent[]`** — wherever you record your own thinking. **Or nothing, and nothing is a
  legitimate answer most of the time.** Most people do not keep a second brain.
- **`~~evidence[]`** — anything that can confirm or deny a fact. Sent mail, a message thread, a
  health record, a receipt, a lifelog.

**A member of a set is an instance, never a role.** A notes app, a health record, a lifelog — each is
one product some people own. **Authority is a property of the source, never of the set it arrived
in:** `~~evidence[]` holds a health record (a system of record) and a mail thread (a tripwire a
stranger can write to) at the same time.

---

## The client field — the finding that decides everything below

**The test:** a live call to Todoist's `find-activity`, one account, one human, returned three rows
with an **identical `initiatorId`** and these `extraData.client` values: Ⓔ

```
Todoist v26.7.9 (iOS)   ← the human, on his phone
Claude                   ← an agent
ChatGPT                  ← a different agent
```

**Every connector authenticates AS the user.** So the actor on an agent's write is the user —
byte-identical to the actor on your own write. **For a solo person, "who" is always you. An actor
field looks like proof of ownership and is not.** It passes every doc-read and fails the only test
that matters.

**Only a client field separates the agent from the hand. It exists in exactly one product on this
page.**

**And this is not a gap that closes next quarter — it is a shape.** The work trackers are not behind:
**they answer "which colleague changed this?" with a `user_id`, which is the right answer to a
different question**, and they will keep answering that one because that is what their buyers ask.
Todoist ships a client field because ***"which of my devices did this?"* is a real question in a
*personal* tool.** Nothing about that is a roadmap item. **Do not wait for it.**

**What follows from it:** the ownership discriminator is **not a requirement — it is an upgrade.**
The engine's burden of proof already fails safe: *cannot prove it → it is yours → leave it.* The two
modes below are that rule followed to its conclusion and given a name.

---

## The surfaces — probed 2026-07-17

**Ⓔ = established by a live call. ⚠️ = NOT VERIFIED.**

| Surface | Official MCP/connector | Completed query | Activity log → actor / **CLIENT** | Duration | Gate | Type |
|---|---|---|---|---|---|---|
| **Todoist** | ✅ | ✅ Ⓔ | ✅ Ⓔ / **✅ Ⓔ `extraData.client`** | ✅ Ⓔ | log 7d free; duration **Pro** | Personal |
| Asana | ✅ `mcp.asana.com/v2/mcp` | ✅ | ❌ / ❌ — **no stories/activity tool in the V2 set** | ⚠️ start+due, no minutes | `search_tasks` Premium | Team |
| Linear | ✅ `mcp.linear.app/mcp` | ✅ via status | ❌ / ❌ — **no history tool** ⚠️ | ❌ estimate = **story points** | private teams **Business+** | Team |
| ClickUp | ✅ `mcp.clickup.com/mcp` | ⚠️ | ❌ / ❌ no activity tool | ⚠️ | audit **Enterprise** | Team |
| Monday | ✅ `mcp.monday.com/mcp` | ✅ | ✅ `get_board_activity` / **❌ no client** | ⚠️ | private boards **Pro+** | Team |
| Notion | ✅ first-party | ✅ | ❌ / ❌ — audit = **Enterprise owners**; `last_edited_by` = the person Ⓔ | ✅ date ranges ⚠️ | SQL **Business+ w/ Notion AI** | Both |
| Things 3 | ❌ *"We don't offer a direct connection with Claude at this time."* | local only | ❌ | ❌ **no duration** | one-time | Personal |
| Apple Reminders | ❌ | local only | ❌ | ❌ **no duration** (EKReminder) | free | Personal |
| TickTick | ✅ `mcp.ticktick.com` | ✅ | ❌ | ⚠️ no estimate; focus = *elapsed* | Premium | Personal |
| MS To Do | ❌ official | ✅ | ✅ Purview / ⚠️ | ❌ **no duration** | audit **Project Plan 1+**, tenant | Personal |
| Motion | ❌ **see trap** | API only | ❌ UI-only feed | ✅ richest — **unreachable** | no free tier | Personal |
| Akiflow | ✅ `akiflow.com/mcp` | ✅ | ❌ **zero ownership proof** | ✅ | no free tier | Personal |
| Sunsama | ✅ beta, no published tool list ⚠️ | ⚠️ | ❌ | ⚠️ | no free tier | Personal |
| Amie | ✅ `mcp.amie.so` (**shipped Jul 14 — volatile**) | ⚠️ | ❌ | ⚠️ | free tier | Personal |

**Notion's cell is the actor trap wearing a friendlier name.** `last_edited_by` resolves to the
*person* Ⓔ — it is an actor field, and an agent writing through your token is you. The real audit log
is **Enterprise, owners only**.

**Sources:** Asana tool set —
[developers.asana.com/docs/mcp-tools-reference](https://developers.asana.com/docs/mcp-tools-reference)
(no stories tool; `search_tasks` "Available on Premium accounts only") ·
[developers.asana.com/docs/using-asanas-mcp-server](https://developers.asana.com/docs/using-asanas-mcp-server)
(the v2 URL) · Linear private teams —
[linear.app/docs/private-teams](https://linear.app/docs/private-teams) · Monday private boards —
[support.monday.com/hc/en-us/articles/115005310185-Private-Boards](https://support.monday.com/hc/en-us/articles/115005310185-Private-Boards)
· Things 3 —
[culturedcode.com/things/support/articles/5510170/](https://culturedcode.com/things/support/articles/5510170/).

**⚠ A LIVE DEMONSTRATION OF WHY THIS FILE DATES ITS CLAIMS — Asana's tool set moved under it.** An
earlier reading of this research had Asana's cell quoting a claim that stories were *"intentionally
left out"* of MCP v2. **That quote does not survive checking, and it is instructive in three separate
ways.** It came from a **forum user, not Asana**; its own "confirmed in another thread" citation
**links back to the thread it is posted in** — a circle; and it has since been **overtaken by
events**: Asana's tools reference, updated the day this was written, now lists `add_comment` as a
write tool and has `get_task` returning comments. **The load-bearing half survives on better
evidence** — there is still **no stories or activity tool** in the live V2 tool list, so actor ❌ /
client ❌ holds, and it holds because the current tool set says so rather than because a stranger
said so. Re-probe with `tools/list` before relying on any Asana row here.

**TRAP — `claude.com/connectors/motion` resolves and looks official. It is a different company.**
Motion Creative Analytics (Meta ad analytics), not usemotion.com, whose Motion is the one with the
duration model. Connecting it gets you an ad dashboard.

---

## The work-tracker verdict

**Three independent disqualifiers. Any one of them is fatal on its own.**

### 1. The rows aren't yours

The vendors document this themselves — this is not a security theory, it is their help centre.

- **Monday:** *"If you are an admin and looking to export the account data, this will export all
  private boards of the account as well. This means that Admins do have access to private boards when
  they export the entire account's data."* Private boards are **Pro+** to begin with.
  ([source](https://support.monday.com/hc/en-us/articles/115005310185-Private-Boards))
- **Linear:** *"When exporting issues from the workspace using our Export tool, admins can choose to
  include issues from any private team."* And: *"The API, webhooks, and integrations such as Zapier
  can expose a user's private team and issue titles."* Private teams need **Business+** — and on
  **non-Enterprise paid plans, workspace admins can see all private teams, update their settings, and
  join one by adding themselves as a member.**
  ([source](https://linear.app/docs/private-teams))
- **ClickUp** is best-of-group — private Spaces on all plans. **Best is not yours.**

**This argument has an exception** — a solo founder owns the admin seat — **so it is the weaker of
the two, and it is not the one that decides this.**

### 2. It doesn't survive your job — the strongest, and it has NO exception

**A life surface has a forty-year horizon.** A passport renews every ten years. A mortgage runs
thirty. A chronic condition runs until you die.

**An employer's workspace has the horizon of your tenure.**

On the day you leave, SSO deprovisions the account and your entire life's state goes with it, in one
revocation you do not control and cannot appeal: every completed row the engine reads to avoid
rebuilding, the whole activity log the burden of proof depends on, every parked decision it must
never resurrect. **You do not put the forty-year data in the three-year container.**

This is the suppression failure at its largest: **the surface does not get noisy, it goes dark** —
and an absence is the thing you cannot see.

### 3. Even the steelman fails

Grant the best case: a **solo founder**, their **own** Linear workspace, on **Business**, with a
private "Life" team. Privacy: fine. Durability: fine. Both of the above are answered.

**It still dies on the contract:**

- **Question 3 dies.** Linear's GraphQL API *has* `IssueHistory`, with `actor` **and `botActor`** —
  the richest ownership model of any surface here. **The MCP exposes no history tool at all.** ⚠️ The
  capability exists and is unreachable, which is the same as absent.
- **Question 4 dies.** Linear's `estimate` is **story points, not minutes.** There is no minute field
  to place a block with. **Every dated life-row becomes an all-day banner** — the exact calendar
  clutter this system exists to remove.

**A surface that fails on the steelman does not fail because of the employer. It fails on the
contract.**

---

## What a work-tracker user should actually do — two surfaces, one direction

**Nothing above says switch tools. It says what degrades and how it fails.** A worse tool you
actually open beats a better tool you abandon — that is not a slogan, and this section does not get
to overrule it. **The work tracker is excellent at work. Keep it.**

- **Work stays in the work tracker, and the work tracker becomes an `~~inbound[]` source.**
  Assigned-to-me is another person putting an obligation on you — which is exactly what that set is
  for.
- **Life gets a personal `~~state`.** The four questions and both container tests bind that surface
  only.
- **When work needs a time-block, the engine writes a personal row whose description carries a
  POINTER — the work item's URL — never a copy.** A pointer cannot go stale against the thing it
  points at. A copy can, silently, and then two rows disagree and neither says which is the source.
- **Never sync them. In either direction.** Bidirectional sync is the duplicate-rebuild problem
  running across two systems that share no ownership ledger: **neither log can see the other's client
  field, so each side reads the other's write as a human's and reconciles it, every pass, forever.**
  Two surfaces with one direction of flow is an architecture. Two surfaces with two is a loop with no
  referee.

---

## The two modes — what the client field actually buys

**Probe the client field at capability-check, every run. The answer selects the mode. It is not a
setting, it is a reading** — and it can flip under you between runs without anyone touching this
file: a plan downgrade caps the log, a vendor ships or drops a field, a token loses a scope.

### WRITE-ONCE MODE — no client field. **This is the honest default.**

**The engine creates, and never modifies.** The verb it loses is *revise* — reshape, re-date,
re-place, upsize, stagger, roll.

It keeps everything that makes it worth running: capture and the full read of every source; the
obligation gate and the second door; **placement — once, at creation — under the entire placement
calculus** (the envelope, captive windows, the floor, the stagger, the anchors, the ladder); closure
on direct evidence in the source that owns the fact; the ghost sweep, whose authority comes from the
probe rather than from a client field; the card and the receipts.

**It loses exactly one thing: self-maintenance.** And it does not go quiet about it — **it reports the
shape problem in one line instead of fixing it.** A sub-floor block. Two rows on one start time. A
row that lapsed. One line each, named, in the output. **Never a silent skip.**

**A real cost, stated: expired sales banners accumulate**, because deleting one needs log proof of
placement. The count gets named. It is yours to see, not the engine's to hide.

### MAINTAINED MODE — a client field exists. **This is the upgrade.**

The engine may maintain **its own** rows — proven from the log, per row, every time: upsize its own
sub-floor blocks, stagger its own collisions, roll its own untouched overdue rows, run anti-rot
against its own output.

**Nothing here reaches a row you placed or touched.** Maintained mode buys a larger set of rows the
engine may fix. **It never buys a broader licence over yours.** Your close is final; your placement
is final.

### Write-once is not the consolation prize — it is arguably the SAFER product

Look at what the closure rules actually are: **an elaborate apparatus for stopping the engine
touching your stuff.** Every rule in it exists because maintained mode *can* reach a row you placed
and must be forbidden to.

**In write-once that entire class of defect is structurally impossible.** No upsize to misfire. No
roll to resurrect a decision you were deliberately letting lapse. No sweep with patrol powers. **Not
because the engine is well-behaved — because the verb is not in its hands.**

**Anything describing write-once as degraded is reading a feature list instead of an outcome.**

**The engine names its mode in the receipts, every run.** Not the first run — every run. A mode you
cannot see is a capability claim you cannot check, and it flips silently.

---

## Inbound reality — and the layer that doesn't exist

### The obligation layer is not an API

**Of twelve connectors checked, exactly one — GitHub's `list_notifications` — exposes a
mention/notification inbox.**

There is no `list_mentions` on Linear, Asana, Atlassian, Notion, Intercom, HubSpot, **or Slack**.
**You must already know which record to look at before you can read its comments.** Asana's
`get_task` returns comments — for a task GID you already have.

**So "who asked me for something this week?" is not a first-class MCP operation almost anywhere.**

**Email is the only inbox ever designed as an inbox.** Everything else is search: it pulls, it needs
a query, and **it misses what you didn't think to ask.** That is the shape of the whole `~~inbound[]`
problem, and no amount of connecting more surfaces fixes it.

### The realistic tiers

**Frictionless:** Google Calendar · Gmail · Todoist · Linear · Notion.

**Works, but behind a gate someone else controls:**

- **Slack** — needs paid Slack + admin. Reads channels **and DMs** via search. **No mention list.**
  ⚠️ **Claude in Slack migrates to Claude Tag on 2026-08-03, and Claude Tag is Team/Enterprise-only.
  The consequence for Pro/Max users is UNDOCUMENTED** — not "fine," not "broken." Unknown. Re-check
  before relying on it.
- **MS Teams** — Anthropic-built, inside M365. Needs an Entra tenant + Global Admin consent.
  **Personal Microsoft accounts are excluded.**
- **GitHub · HubSpot · Asana** — work, with an admin or plan gate.
- **Intercom** — **US-hosted only.**
- **Atlassian** — **Confluence yes / Jira comments unreadable.**

**Effectively impossible — and the four reasons are genuinely different, which is the point:**

- **Discord — architectural.** A bot cannot see your DMs. **No combination of intents reaches
  them.** ⚠️ `claude.com/plugins/discord` has ~28k installs and **points the wrong way** — it lets
  Claude post *to* Discord; it does not let Claude read your DMs.
- **WhatsApp — contractual.** Meta's Business Solution Terms name the category directly: AI
  providers, *"including but not limited to large language models, generative artificial intelligence
  platforms, general-purpose artificial intelligence assistants,"* are **"strictly prohibited"** from
  using the WhatsApp Business Solution where that is the primary functionality.
  ([source](https://www.whatsapp.com/legal/business-solution-terms))
- **Signal — cryptographic.** No API exists. End-to-end encryption means there is **no server-side
  plaintext**, so a remote connector **cannot exist**. Not "isn't built." Cannot be.
- **Telegram — licensing.** Its content-licensing policy bars platform data for AI **"deployment,"**
  which reaches inference, not merely training. **Telegram is stricter here than Discord, despite the
  reputations.**

### Adapter differences that change what the engine is allowed to do

- **Google Calendar has full write. Microsoft 365's calendar is read-only through the connector**
  unless an admin separately enables the write tools. An Outlook user does not get a degraded version
  of calendar writes — they get *none*. The engine detects this and switches to **propose-only**: it
  renders the event it would have made and you create it. **Correct behaviour, not a failure**, and
  the brief says which.
- **Personal Outlook addresses cannot connect at all.** Not a paywall — unsupported. See VOLATILE.
- **Gmail exposes no send tool. Draft-only is architectural** — enforced by the absence of the
  capability, not by a promise in a prompt. **The single best safety property in this stack, and it
  costs nothing.**
- **Free tiers cap activity history and withhold durations.** Both are load-bearing, and **both
  failures are silent.** Past the cap the engine cannot prove ownership, so it stops re-placing
  anything — safe, silent, and inert. Numbers in VOLATILE.

### When your mail is somewhere the connectors don't reach

**The situation:** the mail lives on **iCloud Mail**, **Fastmail**, a self-hosted domain, or a
**personal Outlook address, which cannot connect at all, on any plan.**

**The move: forward into a supported mailbox.** A one-way mirror into a surface the engine can read.

**And the honest shape of it, which is worse than the calendar version:**

- **Replies come from the new address.** A calendar mirror is invisible — nobody can tell your Google
  Calendar is subscribed to your iCloud one. **A forwarded mailbox is visible the moment you answer
  anything**, because the reply arrives from an address your counterparty has never seen.
- **Consolidating mail is a bigger life change than mirroring a calendar.** A calendar mirror is a
  setting. A mail move touches your identity and every person who has your address written down.

**And the option that is genuinely fine: skip it.** **Mail is an `~~inbound[]` member, not a
contract.** The engine runs without it. What you lose is real — mail is where obligations *arrive* —
but **there is no version of this where someone should restructure their email identity to satisfy a
diagram.**

---

## What the optional connectors actually ARE

**A bare table cell is not an explanation.** If a stranger cannot decode a name, the name is doing
no work. Each of these is **one product filling a role — the role is what matters.**

### Notion — an `~~intent[]` member

**What it is:** a hosted notes-and-database workspace. Pages, databases, views; lives on their
servers; official connector.

**What it contributes:** the **knowledge home** — protocols, reference material, decision logs. In
the three-homes split it is the *things you KNOW*, as distinct from the things you *owe* (`~~state`)
and the things you *do at a time* (`~~container`).

**What it asks:** read access to a hosted workspace. No local dependency, so it **stays
cloud-eligible** — which is why it's the one place a profile-in-a-note works well.

### Bee — an `~~evidence[]` member

**What it is:** a **wearable that continuously records the conversations happening around you** and
produces transcripts, summaries, and derived facts from them.

**What it contributes:** **corroboration.** What was *actually said* — and a first-person record of
commitments you made out loud, which is the one category of obligation that leaves no written trace
anywhere else.

**The privacy reality, stated plainly:** **it records everyone around you, and most of them did not
consent.** `RISK.md` covers a message reader — a database of everyone who ever texted you. **This is
broader and sharper:** a message reader captures people who chose to write to you. A continuous
recorder captures anyone who happens to be in the room, including people who never interacted with
you at all, in places where they had every reason to assume they weren't being recorded. **That is a
decision about other people, made without them, and it should be made deliberately or not at all.**

**One engine constraint that matters here:** the engine only ever ingests **first-person** content,
and **never treats an AI-derived summary as a commitment.** A summary is a claim about what was said,
not evidence of an obligation. Only your own words count.

### Reflect — an `~~intent[]` member

**What it is:** a personal notes app that runs a **local HTTP server on a loopback port**; the
connector talks to that server, not to a cloud API.

**What it contributes:** **your own hand** — daily notes, the highest-fidelity record of intentions
that exists anywhere in the stack.

**What it asks:** the app must be **running on the machine**. That makes it a local dependency, and a
local dependency **pins the schedule** — see below.

---

## Replacements — and how to actually do them

**The general rule, stated once: every optional connector is a ROLE, and any tool that answers the
role's question substitutes for it. Nothing in the intelligence depends on a product name.** That is
the whole point of the abstraction — and it means every replacement below is a **data-migration
question, never a capability question.**

### Notion → anything that holds text

**What replaces it:** Apple Notes. Obsidian. A plain folder of Markdown. **Or email-to-self.**

**Email-to-self is legitimate and common, and it deserves better than a footnote.** If you already
mail yourself notes, **a mail member of `~~inbound[]` already covers `~~intent[]`.** Point the engine
at the self-sent thread and **skip a connector entirely.** No new app, no new permission, no new
subscription, no schedule cost. **For a large number of people this is the correct answer and they
should not be talked out of it.**

**Migration:** Notion exports **Markdown + CSV**. Export, drop the result into a folder, point
`~~intent[]` at that folder. Databases arrive as CSV and pages as Markdown; the engine reads prose,
so the Markdown is the part that matters.

**The one cost to name:** Apple Notes, Obsidian, and a Markdown folder are all **local** — they pin
the brief to the machine. Notion and email-to-self are hosted and don't. **That is usually the
deciding factor, not the app's features.**

### Reflect → any notes surface

**What replaces it:** any of the above. There is nothing special about the shape of the data.

**Migration:** Reflect exports **Markdown**. Export it, put it wherever the new home is, point
`~~intent[]` there.

**The role is what matters, not the app.** Reflect's contribution was "your own hand." Any surface
holding your own hand contributes exactly the same thing. Swapping it changes the fidelity of
*nothing*.

### Bee → Limitless, or nothing

**Be honest about both halves of this:**

- **There is no drop-in replacement.** Nothing else produces a continuous first-person record of what
  was said out loud. If that specific record is what you want, the only substitute is another device
  of the same kind — **Limitless** fills the same role.
- **Its blind spot is narrow.** Losing it costs **corroboration, not capability.** The engine still
  finds every obligation that left a written trace — which is nearly all of them. What you lose is
  the verbal commitment nobody wrote down.

**Most people should not add it.** The privacy cost is paid by other people, the schedule cost is paid
by you, and the blind spot it closes is small. **"Nothing" is the right answer for the large
majority**, and setup should say so without a hint of disappointment.

---

## What can and cannot be bundled

**The honest answer to *"package it self-contained, with all the dependencies included."***

**Some of it can be bundled. Some of it provably cannot** — and the reason matters more than the
fact, because **the things that can't be bundled are the same things that stop your brief arriving at
7am.**

### Hosted connectors — bundled by declaration, cloud-eligible

Nothing to install. OAuth, one click, works on any machine, **and keeps the engine cloud-eligible.**
Both contracts have hosted options, and `~~intent[]` does too.

**A build using only hosted connectors is the transfer-grade product.** It runs in the cloud, fires
with the computer off, and installs in minutes. **This is what a novice should start with, and most
people should stop here.**

### Local servers and extensions — NOT bundlable, and machine-pinning

| Dependency | What it is | Why it cannot be bundled |
|---|---|---|
| **iMessage reader** | A **Desktop Extension (DXT)** reading the local Messages SQLite DB | DXTs install through a **different channel** than plugin `.mcp.json`. A plugin cannot install one. It also needs Full Disk Access, granted by the human. |
| **Apple Notes** | Desktop Extension, AppleScript | Same channel problem; macOS-only; needs automation permission. |
| **A local notes server** (e.g. Reflect) | An **HTTP server the notes app itself runs** on a loopback port | The dependency is *the app running on your machine.* A plugin cannot ship another vendor's desktop app. |
| **A lifelog server** (e.g. Bee) | A binary plus virtualenvs holding **your own downloaded data** | The venv is not a library — it is your corpus. Shipping it would ship your life. |

### What CAN legitimately be bundled

- **A `.mcp.json` that *declares* how to launch a local server**, using `${CLAUDE_PLUGIN_ROOT}` for
  any script shipped inside the plugin and `${VAR}` for secrets. **Never put a key in the file** —
  anyone on the machine can read it.
- **An installer/probe script** that checks whether the local dependency exists and prints the exact
  install command.
- **Documentation** of the install, which is what this file is.

**The distinction that matters: you can bundle a *pointer and a probe*. You cannot bundle another
app, another vendor's daemon, an OS permission, or someone's personal data corpus.** Any package
claiming otherwise is lying about what a zip file can do.

---

## Where it runs — a separate axis, decided by your dependency list

**This is not a tier and it is not a preference.** It is decided by what you connected.

| | Cloud routine | Desktop task |
|---|---|---|
| Runs on | Anthropic infrastructure | Your machine |
| **Fires with the computer off** | **Yes** | **No — the run is skipped** |
| **Access to local files/apps** | **No** | **Yes** |
| MCP servers | connectors configured per task | config files + connectors |
| Minimum interval | 1 hour | 1 minute |

And the reconciling rule, from the Cowork docs verbatim: **"If a scheduled task requires local files
or apps, it will only run locally."**

**So every local dependency you add silently converts a reliable cloud brief into a machine-pinned
one that gets skipped whenever the laptop is asleep.** Desktop then runs *one* catch-up on wake and
discards older misses — **which is why a 7am brief can arrive at 10pm.**

**Local readers do not merely cost portability. They cost the schedule.**

### The real cost of each local surface

| You gain | You pay |
|---|---|
| Messages: a text that moved a time | **Cloud eligibility.** The brief now depends on the laptop being awake. |
| Lifelog: what was actually said | A local corpus to maintain, a sync that can rot, **and a privacy cost paid by other people** |
| Local notes: your own hand | The notes app must be running |

**Recommendation: start with hosted connectors only. Add a local dependency only when you can name
the blind spot it closes AND you accept a brief that fires on wake instead of on time.**

---

## How to verify what you actually have

Do not trust this file for what is installed — **it does not own that fact.** Check live:

- **Hosted connectors:** your Claude connector settings.
- **Local MCP servers:** `~/Library/Application Support/Claude/claude_desktop_config.json` and
  `~/.claude.json` (`mcpServers` key).
- **Desktop Extensions:** `~/Library/Application Support/Claude/Claude Extensions/`.

`chief-of-staff-setup` probes all of this at run time and reports what it found. **A listed tool is
not a capability — the probe is the fact.**

---

## Adding a role, or a tool, you don't see here

The engine reads capability from `~~` roles, not product names. If you use a task manager or notes
app not listed, **it works as long as its connector answers the contract's questions above.** Point
`setup` at it and it will probe, report what it found, and tell you which parts of the intelligence
you will and won't get — **and which mode you're in.**
