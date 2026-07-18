# The stack — what this needs, what each piece does, and what substitutes for it

> **Where it runs is a picture:** `assets/where-it-runs.mermaid` — the cloud-vs-local fork, and what
> each local reader you add gains you as well as what it costs the schedule. Read it beside the
> cloud/local section below.

Everything about connectors in one place: what each role is for, what actually fills it, what
happens when you swap something out, and what provably cannot be bundled.

**No prices and no click paths live here.** They are in `references/VOLATILE.md`, dated and cited.
This file carries the *shapes* and the *arguments*. **The numbers move; the arguments don't.**

**Verified live on 2026-07-17.** The surfaces below were **probed by calling their connectors**, not
read out of their documentation — which matters, because the headline finding is a case where the
documentation and the live call disagree. **Ⓔ marks a claim established by a live call in that
probe.** **⚠️ marks a claim that is NOT VERIFIED** — inferred, single-sourced, or read from a doc and
never tested. **Re-probe anything here older than about three months** — a tool set can change in a
day.

---

## How tool references work

Plugin files use `~~role` as a placeholder for whatever tool you connect in that role. This plugin
is tool-agnostic — it describes workflows in terms of roles rather than products. At run time the
engine **probes for what is actually connected** and does the most it can with what it finds.

**A listed tool is not a capability.** The engine never assumes a role is filled because this file
mentions it. It detects, then acts, then reports what it could not reach.

---

## The roles — two CONTRACTS, three SETS

This mirrors §0b's contract. **A CONTRACT is a set of capabilities a tool either has or does not
have — testable, universal, asked of every person on earth. A SET is whatever this person happens to
have.**

*Mail, notes, messages, a lifelog* are set members — each one a product somebody connected, never a
first-class role. **A role named after one person's sources is a stack wearing the syntax of an
architecture, and it is wrong about the second person who reads it.**

### The two contracts — mandatory, capability-tested, identical for everyone

**`~~state`** (alias: `~~task surface`) — **the engine's database.** The engine keeps no cache and no
memory between runs; **the list is the state.** Five questions, and the answers are not all
pass/fail:

1. **What is open?** Every task manager answers this. It is the least of the five, and it is the only
   one most people check before choosing a tool.
2. **What did you already complete?** An open-row search cannot answer an existence question.
   Without this the engine rebuilds a row you closed an hour ago, forever. **Required.**
3. **Who placed this row — the engine, or you?** Answerable **only by a CLIENT field on the activity
   log.** **Not pass/fail — the answer selects the mode.** See the finding below; it is the fact
   everything else on this page turns on.
4. **Does a TIME OF DAY stick — an hour on a row?** **Ask this BEFORE the duration, always.
   Placement needs to know WHEN before it needs to know HOW LONG.** The entire calculus — the
   envelope, captive windows, the anchors, the stagger, the ladder, door two's container — resolves
   to **an hour**, and on a date-only surface there is **no field to write it into.** A length is
   what you write *second*.
   **Prove it with a disposable row — write an hour, read the field BACK, delete it. Never read a
   field's NAME as the answer** (§13): a field called *due date* may take a datetime, and one
   documented as a datetime may drop the time on write. **A write that returns success and silently
   drops the hour is the whole failure mode**, and only the read-back catches it.
   **Not pass/fail, and not a hard stop — no time of day is a DEGRADED mode.** A surface that cannot
   carry an hour makes this engine **narrower, never wrong**: it reads the same physical narrative,
   computes the same envelope, and writes fewer fields. **§6's third flip-condition is what that
   costs.**
5. **What does it cost — a duration on a row?** A block has a length. Without a duration the engine
   cannot state the cost or enforce **the floor** — so task-derived rows get the `—` gutter, and the
   floor is reported as unenforceable rather than silently broken. **That is a fact about the ENGINE,
   and it is the only part of this anyone here owns.** What a duration-less *timed* row draws on a
   calendar is a property of that task app and that person's own sync; **probe it and report what the
   probe found** (§13's method) — never predict it. **Not pass/fail:** the surface is present,
   time-blocking is not. **An unwritable hour subsumes this question** — a row you cannot place at a
   time cannot carry a meaningful cost either, because a length with no start is a number about
   nothing. **Ask 4 first and this one may already be answered.**
   *(**The floor is 30 minutes by DEFAULT, and the default names its override: the PROFILE's grain,
   `Your units`, wherever they state one** (§0c). Nobody is asked their grain at onboarding — the law
   says thirty and gets on with it, and the one person for whom thirty is wrong has a named place to
   say so. **Say "the floor," not a number**: this file does not own its value.)*

**And `~~state` must be PERSONAL and DURABLE** — a test of the container, not the feature list. A
surface can answer all five and still fail it. That argument is below.

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

**The test:** `find-activity` was called live against one account with one human behind it. It
returned three rows carrying an **identical `initiatorId`** — and three *different*
`extraData.client` values: Ⓔ

```
<the task app, on a phone>   ← the person, by hand
<an agent>                   ← an agent, writing through the person's token
<a different agent>          ← a different agent, same token
```

**The actor was the same on all three rows. Only the client told them apart.** That is the whole
finding: on this surface the actor field cannot discriminate and the client field can.

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

| Surface | Official MCP/connector | Completed query | Activity log → actor / **CLIENT** | **Time of day** | Duration | Gate | Type |
|---|---|---|---|---|---|---|---|
| **Todoist** | ✅ | ✅ Ⓔ | ✅ Ⓔ / **✅ Ⓔ `extraData.client`** | **✅ Ⓔ — due *datetime*, written and read back** | ✅ Ⓔ | log capped on free; duration paid — VOLATILE | Personal |
| Asana | ✅ `mcp.asana.com/v2/mcp` | ✅ | ❌ / ❌ — **no stories/activity tool in the V2 set** | ⚠️ never probed | ⚠️ start+due, no minutes | `search_tasks` Premium | Team |
| Linear | ✅ `mcp.linear.app/mcp` | ✅ via status | ❌ / ❌ — **no history tool** ⚠️ | ⚠️ **NOT VERIFIED — `dueDate` NEVER PROBED. See note.** | ❌ estimate = **story points** | private teams **Business+** | Team |
| ClickUp | ✅ `mcp.clickup.com/mcp` | ⚠️ | ❌ / ❌ no activity tool | ⚠️ never probed | ⚠️ | audit **Enterprise** | Team |
| Monday | ✅ `mcp.monday.com/mcp` | ✅ | ✅ `get_board_activity` / **❌ no client** | ⚠️ never probed | ⚠️ | private boards **Pro+** | Team |
| Notion | ✅ first-party | ✅ | ❌ / ❌ — audit = **Enterprise owners**; `last_edited_by` = the person Ⓔ | ⚠️ never probed | ✅ date ranges ⚠️ | SQL **Business+ w/ Notion AI** | Both |
| Things 3 | ❌ *"We don't offer a direct connection with Claude at this time."* | local only | ❌ | ⚠️ never probed — no connector to probe with | ❌ **no duration** | one-time | Personal |
| Apple Reminders | ❌ | local only | ❌ | ⚠️ never probed — no connector to probe with | ❌ **no duration** (EKReminder) | free | Personal |
| TickTick | ✅ `mcp.ticktick.com` | ✅ | ❌ | ⚠️ never probed | ⚠️ no estimate; focus = *elapsed* | Premium | Personal |
| MS To Do | ❌ official | ✅ | ✅ Purview / ⚠️ | ⚠️ never probed | ❌ **no duration** | audit **Project Plan 1+**, tenant | Personal |
| Motion | ❌ **see trap** | API only | ❌ UI-only feed | ⚠️ never probed — **unreachable anyway** | ✅ richest — **unreachable** | no free tier | Personal |
| Akiflow | ✅ `akiflow.com/mcp` | ✅ | ❌ **zero ownership proof** | ⚠️ never probed | ✅ | no free tier | Personal |
| Sunsama | ✅ beta, no published tool list ⚠️ | ⚠️ | ❌ | ⚠️ never probed | ⚠️ | no free tier | Personal |
| Amie | ✅ `mcp.amie.so` (**shipped days before this probe — volatile**) | ⚠️ | ❌ | ⚠️ never probed | ⚠️ | free tier | Personal |

**READ THE TIME-OF-DAY COLUMN AS THIRTEEN HOLES AND ONE FACT, because that is what it is.** Exactly
one cell in it is established: Todoist's. **Every other row says "never probed" — and that is the
column's honest state, not a backlog apology.** The column exists because §0b's fourth question
exists; **an empty column that names its emptiness is worth more than a filled one that guesses**,
because the guesses would all be reasonable and some of them would be wrong.

**⚠️ LINEAR'S `dueDate` — NOT VERIFIED, and this file will not guess it either way.** It is
*suspected* to be a **date, not a datetime**, which if true would mean **no life-row on Linear can
carry an hour** and the surface fails §0b's fourth question as well as its fifth. **That suspicion has
never been probed and is not stated as a fact here.** Linear's schema reference is served through
Apollo Studio, which is a JS app and could not be read on 2026-07-17; **the doc-read that would settle
it was attempted and failed.** And a doc-read would not settle it anyway — **§13's whole point is that
a field documented as a datetime may drop the time on write.** **One disposable issue answers this:
write a `dueDate` with an hour in it, read it back, delete it.** Until someone does, Linear's row
carries a hole, and **the work-tracker verdict below does not rest on it** — Linear already fails
questions 3 and 5 on established grounds.

**⚠️ AND THE DEFECT THIS COLUMN EXISTS TO CATCH — the README committed it.** The README generalizes
**Todoist's due-*datetime*** into a claim about **"task lists"** in general. **That is one probe, of
one product, promoted to a universal** — the exact move §0b exists to kill: *a stack wearing the
syntax of an architecture, wrong about the second person who reads it.* **Todoist's datetime is a fact
about Todoist.** The thirteen ⚠️ cells above are what the generalization was actually standing on.
**Whoever owns the README should cut it to Todoist or cut it to nothing.**

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

**Asana's row rests on the live V2 tool list, not on a description of it: there is no stories or
activity tool in it, so actor ❌ / client ❌. Re-probe with `tools/list` before relying on that row.**

**TRAP — `claude.com/connectors/motion` resolves and looks official. It is a different company.**
Motion Creative Analytics (Meta ad analytics), not usemotion.com, whose Motion is the one with the
duration model. Connecting it gets you an ad dashboard.

---

## The work-tracker verdict

**Three independent disqualifiers. Any one of them is fatal on its own — and then a fourth section,
which is not a fourth disqualifier but the CONSEQUENCE the first three imply and never say: door two
cannot run here at all.**

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
- **Question 5 dies.** Linear's `estimate` is **story points, not minutes.** There is no minute field
  to place a block with — so **no life-row on this surface can carry a length the engine can state or
  a floor it can hold.** Every one of them gets the `—` gutter. Placement is the entire product, and
  this surface cannot express it.
- **Question 4 is a hole, not a verdict.** Whether Linear's `dueDate` carries an hour has **never
  been probed** — see the table's note. **It is not needed here.** The steelman is already dead twice
  over; adding a suspicion to a finished argument would weaken it, not strengthen it.

**A surface that fails on the steelman does not fail because of the employer. It fails on the
contract.**

### 4. And the sharpest consequence, which the three disqualifiers above only imply: DOOR TWO IS DEAD

**§2 above is the strongest DISQUALIFIER. This is the strongest SENTENCE — they are not competing,
and this one is downstream of the table rather than of the employer.** It follows from a single cell:
**the work trackers have no reachable activity log.** Asana — no stories or activity tool in the V2
set. Linear — no history tool. ClickUp — no activity tool.

**Follow it through.** §9b's second door — the one that places your own undeadlined work, the whole
reason this system exists rather than being a nicer inbox — **has three conditions, and the third one
is: *"The activity log shows no engine-created container for this lane deleted or dismissed inside
the cadence window. Cannot check the log → do not place."*** And **"cannot name all three →
nothing. Not a nudge. Not a p4. Nothing."**

**No activity log → condition 3 can never be satisfied → the door never opens. Not once. Not ever.**

**Three things make this worse than it first sounds, and each one closes an escape route:**

- **Write-once mode does not rescue it.** The obvious hope is that this is a client-field problem, and
  client-field problems degrade gracefully into write-once. It isn't. §9b's third condition **finds
  engine work by the reserved label, not by a client field** — so it works in *both* modes, and
  **needs the log in both.** The law says so directly: *"it still needs the log: cannot check the log
  → do not place, in either mode. Write-once does not exempt the second door from its third
  condition."* **The graceful-degradation story that saves everything else on this page does not save
  this.**
- **Money does not rescue it.** The missing thing is not a plan tier — **it is a tool in the MCP
  surface.** Linear's history exists in GraphQL and is unreachable through the connector; ClickUp's
  audit log is Enterprise *and* has no activity tool exposed. **You cannot buy your way to a tool that
  isn't in the tool list.** Door two is dead **at any price**, on **every** work tracker here.
- **And it fails silently, which is I5's suppression face.** The door not opening produces **no error
  and no row.** The card renders every morning, correct in every particular, made **entirely of other
  people's demands** — and nothing on it says the half of the product that was supposed to defend your
  own work never ran. **You cannot see an absence.**

**So the verdict is not "a work tracker is a degraded life surface." It is that a work tracker can run
door one forever and door two never, and never say so.** The three disqualifiers above each have a
shape — an exception, a horizon, a contract. **This one has a consequence: the thing you installed
this for is the exact thing that cannot work.**

---

## What a work-tracker user should actually do — two surfaces, one direction

**Nothing above says switch tools. It says what degrades and how it fails.** A worse tool you
actually open beats a better tool you abandon — that is not a slogan, and this section does not get
to overrule it. **The work tracker is excellent at work. Keep it.**

- **Work stays in the work tracker, and the work tracker becomes an `~~inbound[]` source.**
  Assigned-to-me is another person putting an obligation on you — which is exactly what that set is
  for.
- **Life gets a personal `~~state`.** The five questions and both container tests bind that surface
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
  ⚠️ **Two different products wear this name, and the difference is the whole risk.** The
  *connector* is what the engine reads through. *Claude in Slack* is the `@Claude` app — a separate
  thing, which the connector's own documented prerequisite says you must install first. **The app is
  the one being retired**, and its replacement is gated to the top plan tiers. So the question is
  not "is my connector gated?" — it is **whether a connector still works once the app it depends on
  is replaced by something a solo user cannot install. No vendor page says.** Not "fine," not
  "broken." **Unstated.** Date and tiers in VOLATILE. **Probe it after the cutover; do not reason
  it out.**
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
  anything — safe, silent, and inert. Without a duration it cannot state a cost or hold **the floor**
  (30 minutes by default, or the profile's grain where they state one — §0c), so the gutter reads `—`
  and the floor is reported unenforceable — **rows are still placed at their hour; the length is
  what's missing.** Numbers in VOLATILE.

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

## The optional connectors — and what substitutes for them

**The general rule, and it is the whole section: every optional connector is a ROLE, and any tool
that answers the role's question substitutes for it. The engine reads a role, never a product name.**
So swapping one is a **data-migration question, never a capability question** — and no product below
is worth a page of its own, because nothing in the intelligence depends on which one you picked.

| The role | What fills it | What substitutes | The cost that decides it |
|---|---|---|---|
| **`~~intent[]` — your own hand** | a hosted notes workspace · a notes app running a local server on a loopback port | Apple Notes · Obsidian · a folder of Markdown · **email-to-self** | **hosted stays cloud-eligible; every local one pins the brief to the machine** |
| **`~~evidence[]` — corroboration** | a wearable that continuously records the conversations around you | another device of the same kind — **or nothing** | a local corpus that can rot, **and a privacy cost paid by people who did not consent** |

**Notes surfaces: hosted vs local is the deciding factor, not features.** They all hold your own
hand, at identical fidelity — swapping one changes *nothing* about what the engine reads. Migration
is an export: these surfaces export Markdown, so export it, drop it where the new home is, and point
`~~intent[]` there. **A hosted notes surface is also the one place a profile-in-a-note works well**,
because it carries no local dependency.

**And the mechanism under "local pins the brief," now sourced rather than asserted.** Anthropic's
plugins documentation states it directly: *"In Cowork, connectors reach external services through
Anthropic's cloud, not through your local network. **A custom connector must point to a server that's
reachable over the public internet from Anthropic's IP ranges.**"* **A notes app serving on a loopback
port is not reachable from Anthropic's IP ranges** — it reaches Claude only through the desktop app,
as a local connector. So the cost is sharper than "pins the brief to the machine": **in a remote
session the local notes server is not slow or degraded, it is absent.** Quote and URL in VOLATILE.

**Email-to-self is legitimate and common, and it deserves better than a footnote.** If you already
mail yourself notes, **a mail member of `~~inbound[]` already covers `~~intent[]`.** Point the engine
at the self-sent thread and **skip a connector entirely.** No new app, no new permission, no new
subscription, no schedule cost. **For a large number of people this is the correct answer and they
should not be talked out of it.**

**Continuous recorders: a real but narrow gain whose cost is paid by other people, so it is a
deliberate choice rather than a default one.** What one buys is **corroboration** — not a new class of
obligation the engine can find, but the commitment you made out loud that left no written trace. The
engine already finds every obligation that *did* leave one, which is nearly all of them, so this rung
is narrow but genuine: it catches the spoken word nothing else kept. What it costs is paid by other
people: **it records anyone who happens to be in the room, including people who never interacted with
you, in places where they had every reason to assume they weren't being recorded.** `RISK.md` covers
a message reader — a database of everyone who ever texted you. **This is broader and sharper:** a
message reader captures people who *chose* to write to you; a recorder captures people who did not.
**That is a decision about other people, made without them — so make it deliberately, with their
interests in view.** If you want the corroboration and can carry that cost honestly, enable it; if
not, the engine runs fine without it.

**One engine constraint, and it binds every `~~evidence[]` member:** the engine ingests
**first-person** content only, and **never treats an AI-derived summary as a commitment.** A summary
is a claim about what was said, not evidence of an obligation. Only your own words count.

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
with the computer off, and installs in minutes. **This is the fastest path to a working brief and
where everyone starts** — a complete product on day one, not a stepping stone you are meant to leave.
**The local rungs below are there to climb whenever a capability is worth its cost to you** — the
capability ladder under "Where it runs" lays out each one.

### Local servers and extensions — NOT bundlable, and machine-pinning

| Dependency | What it is | Why it cannot be bundled |
|---|---|---|
| **iMessage reader** | A **Desktop Extension (DXT)** reading the local Messages SQLite DB | DXTs install through a **different channel** than plugin `.mcp.json`. A plugin cannot install one. It also needs Full Disk Access, granted by the human. |
| **Apple Notes** | Desktop Extension, AppleScript | Same channel problem; macOS-only; needs automation permission. |
| **A local notes server** (e.g. Reflect) | An **HTTP server the notes app itself runs** on a loopback port | The dependency is *the app running on your machine.* A plugin cannot ship another vendor's desktop app. |
| **A lifelog server** (e.g. Bee) | A binary plus virtualenvs holding **your own downloaded data** | The venv is not a library — it is your corpus. Shipping it would ship your life. |

**The one message reader this package DOES ship — and it is a first-class source, not a fallback.**
`companions/imessage-fixed/` is a read-only, MIT-licensed, Python-standard-library-only iMessage
reader included in the package. It exists because the stock connector has two defects that make it
miss real messages: **(a)** short-code and bare-number handles never matched — the stock reader
forces a `+1` prefix, so a 2FA code from `123456` or a number saved without `+1` came back empty;
**(b)** message text was lost when Messages stored the real sentence in an `attributedBody`
typedstream and left the `text` column empty or holding only a URL. It fixes both, and adds **thread
enumeration, named-chat reads, and attachment filenames.** That is what turns messages into a real
`~~inbound[]` and `~~evidence[]` source — the thing the brief reads to answer *"did a text move one
of today's plans?"* **It still installs through the extension channel** (double-click the bundled
`.dxt`) **or runs as a raw local MCP server** — either way it is local, so the ladder's schedule cost
applies. **Install and tool detail live in `companions/imessage-fixed/README.md`; this file does not
restate them.**

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

| | Cloud / remote | Local / machine-pinned |
|---|---|---|
| Runs on | Anthropic infrastructure | Your machine |
| **Fires with the computer off** | **Yes** | **No** |
| **Access to local files/apps** | **No** | **Yes** |
| MCP servers | connectors on your Claude account | config files + connectors |

**⚠️ THE MECHANISM UNDER THIS TABLE IS NOT SETTLED.** Anthropic's own scheduled-tasks article
contradicts itself on local-folder binding. One sentence reads *"If a scheduled task requires local
files or apps, it will only run locally"*; the same article also says a scheduled task *"can't be
tied to a folder on your computer."* **Both are real, and they cannot both be the whole rule.** Both
quotes, both URLs, and the reasons not to resolve it by picking a side are **in VOLATILE, under
Scheduling.** **Probe it before relying on either reading; quote neither sentence as the rule until
someone does.**

**What survives the contradiction — and it is the whole recommendation, so this section loses nothing
that matters:**

**Under EITHER reading, a local dependency is what puts the brief at risk.** Either it pins the run
to a machine that has to be awake, **or** the scheduled task cannot reach the folder at all — which
is *worse*, and fails *harder*. **There is no reading of the vendor's docs in which adding a local
reader makes the schedule safer.** So:

**Local readers do not merely cost portability. They cost the schedule** — and the ⚠️ above is about
*how*, never *whether*.

**Two things this table must not be read as saying:**

- **"Cloud routine" and "Desktop task" above are Claude Code's products, and this system's brief is a
  Cowork scheduled task — a third thing.** The famous consequences — *one* catch-up run on wake, older
  misses discarded, **"a task scheduled for 9am might run at 11pm if your computer was asleep all
  day"** — are **Claude Code Desktop's documented behaviour.** They are quotable, they are in
  VOLATILE, and **they are not documented for Cowork.** Do not narrate them as this system's.
- **⚠️ What a Cowork scheduled task does when it MISSES a run is not documented anywhere.** No
  catch-up rule, no skip rule. **That is a hole, and it is a hole in the reliability story this
  package sells.** Nobody should be told their brief will catch up.

**⚠️ TWO OTHER FILES STILL QUOTE THE CONTRADICTED SENTENCE AS SETTLED LAW** — `assets/where-it-runs.mermaid`
and the setup skill. **Neither is this file's to edit.** Whoever owns them should read VOLATILE's
Scheduling entry before the next person quotes that sentence to a stranger as the rule.

### The capability ladder — each local surface is a rung you can choose to climb

**A ladder, not a warning label.** Every rung adds something the hosted-only build cannot see, and
every one carries a single honest cost. **Climb as far as the capability is worth to you** — the
costs are printed here so you choose with your eyes open, not so you stay on the ground floor.

| The rung | What you gain | What it costs — stated plainly |
|---|---|---|
| **Messages** | a text that moved a time — the plumber who pushed the appointment, the friend who moved dinner. The package ships a fixed reader for exactly this: `companions/imessage-fixed/`. | The brief runs on a **waking Mac** instead of the cloud. Worth it when the messages you want caught are worth a brief that waits for your laptop. |
| **Local notes** | your own hand, at full fidelity | The notes app has to be running. |
| **Lifelog** | what was actually *said* — the spoken commitment that left no written trace | A local corpus to maintain, a sync that can rot, **and a privacy cost paid by people in the room who did not consent.** A decision about other people; make it deliberately. |

**How to climb: start wherever you like, add a rung the moment its gain is worth its cost, and stop
wherever you want.** A hosted-only build is already a complete product — it runs in the cloud and
fires with the computer off. Each rung above trades a piece of that reach for something the cloud
cannot touch. **Name the gain, accept the cost, enable it. That is informed consent, not a dare —
and nobody has to climb past the rung that serves them.**

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
