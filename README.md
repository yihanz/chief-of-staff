# Chief of Staff

**Every morning it reads your calendar and task list, works out what you actually owe today, puts
it where you can physically do it, and hands you one card. It costs nothing to start. To begin,
type:**

```
set up my chief of staff
```

You'll see your first card in **under a minute** — setup runs a real pass before it asks you
anything. Then comes the interview: **about two dozen questions**, at your pace, and **ten minutes
of them gets you something that works.** The rest, and connecting anything you haven't connected,
takes as long as it takes. **You can stop after any phase.**

---

## What you actually get

One day, rendered:

> **Thursday** · 16 July, 07:00
>
> `Clear` — nothing collides today; one envelope is tighter than it looks.
>
> | Commitments | First move ready | Envelope opens | Your own work |
> |---|---|---|---|
> | 4 | 4 | 14:10 | **9 days dark** |
>
> ---
>
> `09:00` **Reply to the venue about the deposit** — draft's already in your inbox; they asked
> Tuesday and the hold lapses Friday.
>
> `13:00` **The venture — 90 minutes, protected** — 9 days dark against a "most days" cadence, so
> this went in before anything reactive could take the slot.
>
> `14:10` **Envelope opens — don't fill it** — 35 to get ready, 45 door-to-door, 10 to be early.
>
> `15:45` **Quarterly review with your accountant** — last year's figures are attached to the row;
> the folder's by the door.
>
> `—` **Renew the passport** — undated is correct: nobody's waiting and nothing breaks until you
> book the trip. It stays visible and unplaced.
>
> ---
>
> *Closed 1 — "payment received, 14 July" from the invoice thread. Didn't create 6 — no
> counterparty, no clock. Swept 1 ghost block. `read 6/7` — iMessage didn't answer, so anything
> that moved a time by text is unknown. `write-once` — created 3, revised nothing; a block placed
> last week is 20 minutes, under the floor, and it's yours to resize.*

Two things there are the whole product. **`14:10` is the envelope** — the engine computes the real
cost of a 15:45 appointment (getting ready, life slack, travel, arriving early), refuses to place
anything inside it, and tells you the hour your day actually ends. It never writes the envelope to
your calendar: it's a rule about what may be placed, plus that one line. That's why you stop
arriving flustered at things you had "free time" before. **"9 days dark"** is the number that tells
you whether any of this is working.

### What that card renders on a free task list — read this before the `13:00` sells you anything

*(This is about your **task list's** free tier — a different "free" from the Claude plan further
down. Both are real; they cost you different things.)*

**Time blocks need a task duration, and on nearly every task list a duration is a paid feature** —
Todoist included; `references/VOLATILE.md` carries the current price and the date it was checked.
Here is exactly what that costs you, and we'll keep it to what this package actually owns.

**Without a duration the engine cannot state what a thing costs, and cannot enforce the floor** —
the shortest block it will place, which is a default your profile overrides. So the time gutter
renders `—` rather than an hour it has nothing to stand behind. That is a fact about the engine, and
it's true on any surface, on any tier.

**What your own calendar draws for a timed row with no length, this page does not predict.** The
engine doesn't author a calendar event for a task — your task list's sync draws that row, and how it
draws it is a property of your task app and your setup, neither of which we can see from here.
**So the engine probes it on the first run and tells you what it found**, in the receipts. That's
the answer we can actually stand behind, and it's about your list rather than a guess about lists in
general.

| On the card above | Free | Paid |
|---|---|---|
| `09:00` Reply to the venue — **and every other task-derived row** | placed at `09:00`; the gutter reads **`—`** | a block at `09:00` |
| `13:00` The venture, protected — **the second door's block** | placed; the gutter reads **`—`** | 90 minutes you can see |
| `15:45` Quarterly review | `15:45` | `15:45` — it's a real calendar event, not a task |
| `14:10` Envelope opens | `14:10` | `14:10` — computed, never a block on either tier |

**The card names which one you're on**, in a line of the receipts, together with what the duration
probe actually found on your list. It also reports the floor as unenforceable rather than
pretending to hold it.

**Everything else is unchanged, and it is not a demo:** the gate and the six things it refused, both
doors, closure on evidence, the envelope, the appointment events, the ghost sweep, the coverage
token, and `9 days dark`. **Door two still fires on the free tier** — the `13:00` row is placed, at
its hour, with the dark-day count behind it; the door is not what the free tier takes. **What the
upgrade buys is the placement** — not the door but the *length*: a block you can see, at an hour
your body can actually do it, and a floor the engine can hold instead of merely report. It's the one
spend setup argues for, and you can say no.

**One more free-tier limit on that second door, since we're being exact.** Protecting the `13:00`
block also needs your task list's **activity history** — the engine reads it to check it isn't
re-placing a block you already killed. Free tiers cap that history to a short window (VOLATILE has
the current length). **Where the cadence you declared runs longer than that window, the door goes
quiet rather than guess.** `9 days dark` still renders and still climbs, so it isn't invisible — and
if that number is climbing while no blocks ever appear, **the card says why, in a line of its own.**

**That line is the door-two line, and it names a cause rather than a symptom.** `9 days dark` is a
number, and a number has no *because*. Three causes reach you:

- ***"door two is quiet on `<lane>` — its cadence outruns the log's window."*** The free-tier limit
  above. **This is the door working:** it went quiet instead of guessing. A longer history is what
  moves it.
- ***"door two cannot fire on this surface — no activity log."*** Your list keeps no history at all,
  so the check can never run. **This one is permanent — no plan, no upgrade, no setting revives
  it.** The repair is a different task list, or none.
- ***"door two has no hour to place — this surface carries a date, not a time."*** Your list takes a
  date but drops the hour, so there's nowhere to write a block *at* 13:00.

**The line is absent exactly when the door can fire, and never absent when it can't** — so nothing
there means nothing is wrong. **Don't read the write mode for this.** `write-once` answers a
different question: most people run write-once over a live log and door two fires for them every
week. **A dead log and a dead clock are different repairs, and being handed the wrong one is how you
buy the wrong thing.**

---

## The honest version, before you go further

This gives an AI write access to your calendar and task list and lets it read your mail while you
sleep. The design's central bet is that **an agent that creates almost nothing is more useful than
one that captures everything** — so the obligation gate defaults to doing nothing, mail is
drafts-only (and on the recommended mail surface there's no send verb at all, **which is a property
of the surface you chose, not a promise this package makes**), and every rule about your decisions
resolves toward leaving your stuff alone. The real risks are: a public calendar mirror if you take
the free iCloud path, a mail surface that *can* send if you choose one, and the ordinary fact that
hosted connectors mean your data flows through a vendor — none of them hidden from you, and mostly
avoidable. Mac automation is a further surface, as wide as your own account; it's a capability to
weigh with open eyes, not a trap, and `references/RISK.md` §4 is where to weigh it.

The long version is `references/RISK.md`. **Read it before you connect anything with write
access.** It's the only document here you actually have to read.

---

## What it will and won't do

**Will:**

- Create a task from the world only when it can name **a counterparty and a clock** from evidence
  read this run — **or** protect a block for a lane *you declared*, when it can prove that lane is
  starving. **Those are the two doors that make work.** There is a third that doesn't — it's for
  offers, it's named below, and it writes.
- Place work by **activation cost**, not duration — an errand rides a trip you're already taking;
  admin goes in the window where you're stuck in a chair anyway.
- Compute the real **envelope** around an appointment and refuse to fill it.
- **Close loops on evidence** and tell you the sentence that justified each one.
- Ship every task with **the first move already made** — the number found, the draft written where
  you've connected a mailbox that drafts.
- Report what it **refused to create**, and what it **could not reach**.

**Won't:**

- **Send email.** Drafts only. The engine's own rules ban sending — and on the recommended mail
  surface the ban isn't being relied on, because the send capability doesn't exist there at all.
  **On a mail surface that *can* send, "drafts only" stops being a guarantee and becomes a
  configuration you must not get wrong.**
- **Re-open anything you closed.** Your close is final and is never audited.
- **Move a block you placed.** It places a row once; after that the row is yours.
- **Rebuild something you parked.** Your decisions live on the list and it reads them.
- **Render a partial run as a complete one.** Silence about a failure is the one unforgivable bug.

**And on almost every task list, it won't edit anything at all — ever.** Telling an agent's rows
apart from yours needs a field that exactly one product on the landscape actually has. Without it the
engine runs **write-once**: it **creates and never revises** — if something it made ends up the wrong
shape, it says so in one line rather than reaching back into your list. That's the honest default,
and it's arguably the *safer* product — most of the rules above exist to stop an engine touching your
stuff, and in write-once that whole class of failure isn't unlikely, it's **structurally
impossible**: the verb simply isn't in its hands. Where the field does exist — **maintained** — the
engine may also tidy up **its own** rows, and only ones it can prove it placed and you haven't
touched. **Neither mode ever reaches a row you placed or touched**, and **the card names which mode
you're in, every run.**

**Read that Won't list for what it is: the design's rules, not a warranty.** `LICENSE` says
something harsher — that an AI agent with your credentials can create, modify and delete entries,
and can close a loop you'd already closed. Both are true at once. **The list above is what the rules
require; the licence is what could happen if a rule fails**, and a licence that assumed the rules
held would be worthless to you. See the licence note at the bottom.

---

## Install

**This is distributed as a file — `chief-of-staff.plugin`. There's no marketplace for it yet, and
no public link.** **Plugins also need a paid Claude plan** — Pro, Max, Team or Enterprise. **Skills
don't.** If you're on Free, skip to the next section; you can have nearly all of this.

1. Go to **claude.ai** → **Customize** → **Plugins**.
2. Choose the option to **upload a custom plugin file**, and pick `chief-of-staff.plugin`.
3. **If the picker refuses the file, rename it to `chief-of-staff.zip` and try again.** It's the
   same archive either way, and some pickers only accept `.zip`.

**These screens move, and this one isn't in `references/VOLATILE.md`** — that file carries the dated,
sourced paths for connectors and plans, not this. So if what's on your screen disagrees with the
three steps above, **trust the screen.**

Then, in a **new chat** — plugins only load when a conversation starts — type `set up my chief of
staff`. Setup shows you a card first, then probes what you already have, tells you what's missing
and whether it's worth adding, interviews you, and walks you through creating a scheduled task
(**a plugin cannot ship a schedule**). **A task list and a calendar is the whole floor** —
everything else is whatever you already have. There's one paid upgrade setup will argue for; you
can say no.

**Where the scheduling lives, since this is where people get lost: Cowork is a toggle, not an app.**
Go to **claude.ai**, find the message box, and **select "Cowork" in the bottom left corner.** Same
site, same login, nothing to download, nothing extra to buy. There is no "web version vs. Cowork" —
Cowork *is* on the web.

**"Where do my connectors go?" Nowhere — and that's the good news.** Your task list, your calendar,
your mail are **hosted connectors: you add each one once, in Claude's own connector settings, and
it's live on every surface you use — including mobile, including the unattended 7am run.** Nothing
about them is declared in a file here, and that's deliberate rather than missing: a connector named
in a bundled file would be a *local* one, and a local one **pins your brief to a machine that has to
be awake.** Hosted keeps the run cloud-eligible, which for schedule reliability beats any local connector a
bundled file could declare — a different question from the local *reach* the capability ladder below
invites, which is a deliberate trade, not a downgrade. **The archive does contain `mcp.example.json` — it isn't loaded, it's named that on
purpose, and it covers only that local kind. You don't need to open it.**

### On the free plan? You can have almost all of this.

**The wall is on plugins, not on skills.** Plugins need a paid plan. **Skills don't — they work on
Free, Pro, Max, Team and Enterprise alike.** Connectors work everywhere too, on every plan and every
surface, **including mobile.**

**One switch gates the entire free path, and it's off by default. Turn it on before you upload
anything:** **Settings → Capabilities → turn on *Code execution and file creation*.** With it off,
the upload screen does nothing useful and nothing on it tells you why. It's a setting, not a plan —
free accounts have it. *(Another click path, so it rots the same way the three above do: if your
screen disagrees, trust the screen. The destination is the capability toggle in Settings.)*

**So the free path is real:**

1. **Put a copy of `references/` inside each skill folder — before you zip.** It lives *beside*
   `skills/`, not inside it, so a skill zipped as it ships arrives with no price sheet, no `RISK`,
   no `STACK` and no profile template. It still runs; it just can't tell you what anything costs,
   and setup will have to send you to the vendor's own page instead. **One copy per skill folder.**
2. **Zip each skill folder** in `skills/` and upload them at **Customize > Skills.**
3. **Connect** your task list, Google Calendar, Gmail — normal connectors, no plan gate.
4. **Start the run yourself:** open a chat and say `run my chief-of-staff brief`.

**You get everything except the packaged install and the automatic morning run.** Same pass, same
rules, same card — **you just type five words instead of it firing at 7am.** Scheduled tasks are the
one genuinely paid piece (they're Cowork-only and paid-only). If the automation is ever worth the
money to you, nothing else about your setup changes.

---

## Two doors — why it isn't just another capture tool

**Door one — what arrives.** Most of what lands in your life is not a task. A system that turns all
of it into rows doesn't organize your life; it buries it. So the default is **nothing**, and a
thing earns a row only by naming a person waiting and a date something breaks. That's why the card
is short — and why it tells you it refused six things.

**Door two — what's yours.** Door one is correct and, alone, it inverts the whole system. Your
venture, your book, your portfolio — the work you'd call your life's work — has **no one waiting
and nothing breaking on a date.** A tool with only door one *cannot see it*, and will hand you a
beautiful card every morning made entirely of other people's demands. So the second door is keyed
to **your** declaration instead of a stranger's: you name the lane, and if it's starving, the
engine protects a block for it **before** the reactive work and puts the dark-day count on the card
where you can't miss it.

**This isn't a hunch about the category — the market leader's own default concedes it.** In the
best-known tool of this kind, a meeting another person put on your calendar is treated as top
priority by default and can never be overbooked by the work you asked the tool to protect,
*whatever* priority you gave that work — a defensible choice, since auto-declining someone's meeting
is a sharp edge and they offer that as an option rather than a default. But it means their default
protects a **slot**, and the slot yields; **this one refuses, and when it can't place the block it
makes you look at the number instead of quietly giving the hour away.**
`references/VOLATILE.md` carries the vendor, the quote and the date it was checked.

**The uncomfortable metric is the point.** If that number climbs while your briefs keep looking
clean and productive, the system is working beautifully at the thing it wasn't built for — and it
will tell you so.

### And a third door, which isn't about work — but it writes, so you should hear it from us

**Offers.** A sale on something you already own is not a task and you owe nobody a purchase, so
neither gate above can judge it — door one would refuse every one of them, forever. So the law gives
offers their own quiet door, the **sales rail**, and it is built to stay out of your way: **a
date-only row**, which your calendar renders as an **all-day banner** on the day the offer expires —
its own band, lowest priority, never in the lead, never counted as backlog, never a time block.

**Its gate is three parts, and all three have to come from what the offer itself says:** you already
have a relationship with that brand, it states a real number, and it states a real end date. Fail
any one and nothing is created — **which is most of the time.** It's deliberately over-filtered.

It's named here, and not in the small print, for one reason: **it is a write, it lands on your
calendar, and finding out about it by discovery is the wrong way to find out.** `references/RISK.md`
has its blast radius, including what happens to expired banners in write-once mode.

---

## Two design decisions worth knowing

**The law is portable. You are not.** They're kept apart: the law holds none of your personal
facts — every one of those lives in the profile — which is what lets it be shared, audited and
improved by strangers.

**Portable is not the same as universal, and the law makes the narrower claim on purpose.** It is
universal in how it reasons and in what it does — the gates, the burden of proof, the envelope
arithmetic, the refusal to guess where it can probe. **Its numbers are a different animal: they are
defaults, most of them somebody's calibration rather than physics, and every one of them names, in
the sentence that states it, where it yields.** The 30-minute floor is the honest example — a real
opinion about what a block has to be worth, true of the person it was measured on, and not a fact
about you. **Where a number is wrong about you, your profile overrides it and the law doesn't
argue.** Where the *epistemics* are concerned it argues absolutely: no profile gets to say *close on
a hunch* or *skip the probe*. **A tool that names its assumptions is worth more than one claiming to
have none** — and stripping the opinions out wouldn't make it neutral, it would just hand you a form
instead of a plan.

**Your profile lives as a row on your task list, labelled `cos-profile`** — not as a file on a
computer, because a file only works on that one computer and dies on the next one. Setup writes it with you. It **is not packaged
and is never shared** with whoever handed you this. It **does** pass through the model each run,
the same way your mail and calendar already do — *"not packaged"* is not *"never leaves your
machine,"* and you should hold us to the difference. One test per line: would you send this fact
through a cloud service? If no, leave it out; the engine runs fine without any single field.

**The engine has no memory.** No database, no cache, no state file. **Your task list is the
state.** When you tick a box or drag a block, that *is* the instruction, and it's landed
everywhere, instantly, with no sync. Every pass re-reads everything from scratch — which is why a
missed run is survivable and a stale cache can never lie to you.

---

## Two things it needs. Everything else is whatever you already have.

**Two things are the floor. Everything above them is a ladder — and you're invited to climb it at
your own pace, or stop at the floor, which is itself a real product and no one's idea of falling
behind.** Two things are genuinely required, because nothing substitutes for them:

| What it needs | Why there's no way around it |
|---|---|
| **Somewhere your tasks live** | It's the **memory**. The engine keeps nothing between runs — **your list is the state.** Your profile lives there too. |
| **A calendar** | It's the **container** — where your body actually is. Placement is the whole intelligence; with no calendar there's nowhere to put anything. |

**Those two are a real product, today.** The gate, the envelopes, placement by activation cost, the
card — all of it runs on a task list and a calendar alone.

**Everything above the floor is a rung, and each rung buys something specific on the card. Here is
the ladder and what climbing it actually changes** — you might have five of something or none of it,
and there is no wrong number:

- **Mail — the highest-leverage rung, and the one to add first.** Without it the engine can only
  organize what you already knew about; with it, it *finds* what you'd have missed. This is the
  `09:00` reply-to-the-venue row arriving with its draft already in your inbox, and the receipts
  reading *"Closed 1 — payment received, from the invoice thread."* Nothing else buys as much.
- **Message reading — the bundled iMessage reader.** On the sample card, `read 6/7` is the engine
  naming a blind spot out loud: *"iMessage didn't answer, so anything that moved a time by text is
  unknown."* Add the reader this package ships (`companions/imessage-fixed`) and that line closes —
  the plumber who texted a new time and the friend who moved dinner both get caught, and the coverage
  token reads `read 7/7`. It's a first-class capability here, not a bolt-on: it fixes two real defects
  in the stock iMessage connector on the way — short-code and bare-number handles that never matched,
  and message text lost to `attributedBody` encoding — and it is **read-only: no send, no writes, no
  network.** `companions/imessage-fixed/README.md` is its own doc. **Its cost is schedule, not
  safety:** reading messages is local, so a brief that leans on it runs on a waking Mac (see the
  honest cost below).
- **A place you write your own thinking** — a notes app, voice capture, a journal, **or nothing.**
  Buys capture of what you tell yourself. Most people don't keep a second brain, and **nothing is a
  perfectly good answer;** if you already email yourself notes, mail covers this and you're done.
- **Things that can prove a fact** — your sent mail, a message thread, a health record, a receipt.
  Each buys **one** closed loop: proof is what lets the engine *close* a row on evidence instead of
  leaving it open. Worth it only for a blind spot you actually have.
- **Breadth — Mac automation.** When what you need is local and no purpose-built tool covers it, the
  general **"Control your Mac"** bridge reaches it: the widest rung, with the widest cost. The rule of
  thumb is simple — prefer a purpose-built read-only tool (like the reader above) when one exists, and
  climb to the general bridge when you need reach nothing else gives. `references/RISK.md` §4 is the
  whole weighing.

**The honest cost of the local rungs, kept in plain sight:** anything the engine reads *locally* —
messages, local notes, files on your disk — pins that brief to a machine that is awake. A 7am run
whose slot passes while the laptop sleeps arrives when it wakes, which is why a morning brief can
land at night. Hosted connectors don't carry this cost; local reach trades schedule reliability for
signal no cloud connector can see. **That's the trade, and it's yours to make** — climb for the
signal, or stay hosted for the timing; both are legitimate.

**None of the rungs is required, and any subset — including none of them — is legitimate.** The
engine does the most it can with what's connected, then tells you in one line what it couldn't reach
— that's the `read 6/7` on the card. A complete pass over whatever your stack is reads `sources 6/6`;
the day a source goes dark, the number drops and the receipts name it.

**Use whatever you already have.** If your task manager can't do something, the engine tells you
which part degrades rather than demanding you switch. **A worse tool you actually open beats a
better tool you abandon.**

**One thing worth knowing before you point this at your work tracker: don't.** Your life has a
forty-year horizon — passports, mortgages, health. Your work account has the horizon of your job,
and on the day you leave, SSO deprovisions it and **your whole life's state goes with it** in one
revocation you don't control. Keep the work tracker *for work* — the engine happily reads it as a
place other people put things on you — and give your life its own list on your own account. **Two
lists, one direction, never synced.** `references/STACK.md` has the full argument.

---

## The docs, and when to read them

- **`references/RISK.md`** — before you grant write access. **The one required read.**
- **`references/DEPENDENCIES.md`** — the whole menu: every connector this can use, which two you
  need, and the exact way to turn each on. Start here when you're deciding what to enable.
- **`references/STACK.md`** — the argument behind the menu: why each role matters and what
  disqualifies a surface.
- **`references/VOLATILE.md`** — when a price or a click path doesn't match what you see on screen.
- **`references/PROFILE.template.md`** — only if you'd rather see the questions before you're
  asked. Setup fills it in with you; you don't need to open it.
- **`companions/imessage-fixed/README.md`** — the bundled **read-only iMessage reader** this package
  ships: the two stock-connector defects it fixes, its two-click Desktop-Extension install, and its
  blast radius. A first-class capability, not an afterthought.
- **`assets/architecture.svg`** (source: `assets/architecture.mermaid`) — the design on one page.
- **`mcp.example.json`** — **you don't need to open it, and it's here for completeness.** It isn't
  loaded, and it describes only *local* servers, which your connectors aren't. See the connector
  note above.

Inside the plugin: `chief-of-staff-law` is the operating law — **no personal facts, universal in its
mechanisms, and its numbers defaulted rather than pretended-universal** — `chief-of-staff-engine` is
the pass that runs, `chief-of-staff-setup` is the onboarding.

---

## Support, uninstall, licence

**Support.** There isn't a desk. This is a personal project shared as-is — if it breaks, tell
whoever gave it to you.

**Uninstall.** Remove the plugin and delete the scheduled task — **that alone stops it.** The rest
is cleanup, and it's in **three piles, because no single filter reaches all of them:**

1. **The rows on your task list.** Every one the engine created carries the label
   **`chief-of-staff`** — search `label: chief-of-staff` and what comes back is the complete set.
   Anything without that label is yours, and that search cannot reach it.
2. **The calendar events.** When the engine verified a real appointment that wasn't on any calendar
   you already had, it created **an ordinary event on your calendar.** A calendar event has no task
   label, so **no filter finds these** — they look exactly like events you made, because they are
   the same kind of object. Delete them by hand. There won't be many; that's the only reason it
   ever creates one.
3. **The `✓` ghosts.** On the calendar your task list projects your dated tasks onto, the engine
   sweeps leftover events whose titles start with `✓`. With it gone, nothing sweeps them — filter
   for `✓` there and delete, or delete that projection calendar outright if nothing else lives on
   it.

Your profile is the row labelled **`cos-profile`** — it holds every personal fact you gave this
system, so delete that and nothing about you is left.

**Licence — it is not MIT.** See `LICENSE`, which is short and in plain English: **you may use and
modify this for yourself — no fee, no registration — including for your own work at your job. You
may not sell it, redistribute it, or roll it out across an organization: one person, one install.**
Read "free" as *no fee*, not as *irrevocable* — **the grant is revocable, and it ends automatically
if you breach it.** **It comes with no warranty and no liability** — an AI writes to your calendar
and task list unattended, it can be wrong, and what it does under your credentials is your
responsibility.

**There's no public link to send anyone yet.** The licence asks you not to pass copies around; if
someone wants one, **point them at whoever sent this to you** rather than at your copy.

**And where `LICENSE` contradicts the Won't list above, it's contradicting it on purpose.** The
licence says the agent can create, modify and delete entries in your task list and calendar, and can
close a loop you'd closed yourself. The Won't list says it doesn't do those things. **The Won't list
is the design's rules; the licence is what an AI holding your credentials could do if a rule fails.**
Nothing here is entitled to assume its own rules hold — least of all the document that decides who
carries the loss when they don't.

**Version 0.1.0.** Expect rough edges.

---

## Credits

Built from a system that ran daily against one real life for long enough to learn what actually
breaks. The rules here are failures with the reason attached: the duplicate row, the 15-minute
sliver nobody could read, the call scheduled into a departure corridor, the brief that vanished an
hour before it was needed. Each one cost something once.
