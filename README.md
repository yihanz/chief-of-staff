# Chief of Staff

**Every morning it reads your calendar and task list, works out what you actually owe today, puts
it where you can physically do it, and hands you one card. It costs nothing to start. To begin,
type:**

```
set up my chief of staff
```

You'll see your first card in about **two minutes** — setup runs a real pass before it asks you
anything. Then comes the interview, about twenty questions at your pace: **budget 20–40 minutes**
depending on how much you're connecting. You can stop after any phase and still have something
that works.

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
> counterparty, no clock. Swept 1 ghost block. Sources 6/7 — messages didn't answer, so anything
> that moved a time by text is unknown. Write-once — created 3, revised nothing; one block I placed
> last week is 20 minutes, under the floor, and it's yours to resize.*

Two things there are the whole product. **`14:10` is the envelope** — the engine computes the real
cost of a 15:45 appointment (getting ready, life slack, travel, arriving early), puts it on the
calendar, and refuses to fill it. That's why you stop arriving flustered at things you had "free
time" before. **"9 days dark"** is the number that tells you whether any of this is working.

---

## The honest version, before you go further

This gives an AI write access to your calendar and task list and lets it read your mail while you
sleep. The design's central bet is that **an agent that creates almost nothing is more useful than
one that captures everything** — so the obligation gate defaults to doing nothing, the engine can't
send mail, and every rule about your decisions resolves toward leaving your stuff alone. The real
risks are: a public calendar mirror if you take the free iCloud path, a local shell bridge if you
enable one, and the ordinary fact that hosted connectors mean your data flows through a vendor.
None of those are hidden from you, and two of the three are avoidable.

The long version is `references/RISK.md`. **Read it before you connect anything with write
access.** It's the only document here you actually have to read.

---

## What it will and won't do

**Will:**

- Create a task from the world only when it can name **a counterparty and a clock** from evidence
  read this run — **or** protect a block for a lane *you declared*, when it can prove that lane is
  starving. Those are the only two doors. There is no third.
- Place work by **activation cost**, not duration — an errand rides a trip you're already taking;
  admin goes in the window where you're stuck in a chair anyway.
- Compute the real **envelope** around an appointment and refuse to fill it.
- **Close loops on evidence** and tell you the sentence that justified each one.
- Ship every task with **the first move already made** — the draft written, the number found.
- Report what it **refused to create**, and what it **could not reach**.

**Won't:**

- **Send email.** Drafts only — and on the recommended mail surface, sending isn't possible at all
  because the capability doesn't exist.
- **Re-open anything you closed.** Your close is final and is never audited.
- **Move a block you placed.** It places a row once; after that the row is yours.
- **Rebuild something you parked.** Your decisions live on the list and it reads them.
- **Render a partial run as a complete one.** Silence about a failure is the one unforgivable bug.

**And on almost every task list, it won't edit anything at all — ever.** Telling an agent's rows
apart from yours needs a field that exactly one product on the landscape actually has. Without it,
the engine **creates and never revises**: if something it made ends up the wrong shape, it says so
in one line rather than reaching back into your list. That's the honest default, and it's arguably
the *safer* product — most of the rules above exist to stop an engine touching your stuff, and this
way the verb simply isn't in its hands. Where the field does exist, the engine may also tidy up
**its own** rows. **Neither mode ever reaches a row you placed or touched**, and it names which mode
it's in on every card.

---

## Install

**This is distributed as a file — `chief-of-staff.plugin`. There's no marketplace for it yet.**
Install it however your Claude client installs a local plugin file; if yours doesn't offer a way,
ask whoever sent it to you, because they installed it somehow.

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

### On the free plan? You can have almost all of this.

**The wall is on plugins, not on skills.** Plugins need a paid plan. **Skills don't — they work on
Free, Pro, Max, Team and Enterprise alike** (you need code execution turned on). Connectors work
everywhere too, on every plan and every surface, **including mobile.**

**So the free path is real:**

1. **Zip each skill folder** in `skills/` and upload them at **Customize > Skills.**
2. **Connect** your task list, Google Calendar, Gmail — normal connectors, no plan gate.
3. **Start the run yourself:** open a chat and say `run my chief-of-staff brief`.

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

**The uncomfortable metric is the point.** If that number climbs while your briefs keep looking
clean and productive, the system is working beautifully at the thing it wasn't built for — and it
will tell you so.

---

## Two design decisions worth knowing

**The law is portable. You are not.** They're kept apart: the law holds no facts about any person,
which is what lets it be shared, audited and improved by strangers. **Your profile lives as a row
on your task list, labelled `cos-profile`** — not as a file on a computer, because a file only
works on that one computer and dies on the next one. Setup writes it with you. It **is not packaged
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

**There's no ladder here and no level you're on.** Two things are required, and they're required
because nothing substitutes for them:

| What it needs | Why there's no way around it |
|---|---|
| **Somewhere your tasks live** | It's the **memory**. The engine keeps nothing between runs — **your list is the state.** Your profile lives there too. |
| **A calendar** | It's the **container** — where your body actually is. Placement is the whole intelligence; with no calendar there's nowhere to put anything. |

**Those two are a real product, today.** The gate, the envelopes, placement by activation cost, the
card — all of it runs on a task list and a calendar alone.

**Everything else falls into three piles, and you might have five of something or none of it:**

- **Places other people can put something on you** — mail, a chat app, work assigned to you.
  **Mail is the highest-leverage thing you can add:** without it the engine can only organize what
  you already knew about; with it, it finds what you'd have missed.
- **Places you write your own thinking** — a notes app, voice capture, a journal, **or nothing.**
  Most people don't keep a second brain, and **nothing is a perfectly good answer.** If you already
  email yourself notes, mail covers this and you're done.
- **Things that can prove a fact** — your sent mail, a message thread, a health record, a receipt.
  Each closes **one** specific blind spot. Worth it only if it's a blind spot you actually have.

**None of the three is required and zero of any of them is legitimate.** The engine does the most it
can with what's connected, then tells you in one line what it couldn't reach — that's the
`sources 6/7` on the card.

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
- **`references/STACK.md`** — when you're picking a connector, or want to know what substitutes.
- **`references/VOLATILE.md`** — when a price or a click path doesn't match what you see on screen.
- **`references/PROFILE.template.md`** — only if you'd rather see the questions before you're
  asked. Setup fills it in with you; you don't need to open it.
- **`assets/architecture.svg`** (source: `assets/architecture.mermaid`) — the design on one page.

Inside the plugin: `chief-of-staff-law` is the operating law (universal, no personal facts),
`chief-of-staff-engine` is the pass that runs, `chief-of-staff-setup` is the onboarding.

---

## Support, uninstall, licence

**Support.** There isn't a desk. This is a personal project shared as-is — if it breaks, tell
whoever gave it to you.

**Uninstall.** Remove the plugin and delete the scheduled task. Everything the engine created
carries the label **`chief-of-staff`**, so one filter finds all of it. Your profile is the row
labelled **`cos-profile`** — delete that and nothing about you is left.

**Licence — it is not MIT.** See `LICENSE`, which is short and in plain English: **you may use and
modify this for yourself, free, forever — including for your own work at your job — but you may not
sell it, redistribute it, or roll it out across an organization** (one person, one install; share
the original instead). **It comes with no warranty and no liability** — an AI writes to your
calendar and task list unattended, it can be wrong, and what it does under your credentials is your
responsibility.

**Version 0.1.0.** Expect rough edges.

---

## Credits

Built from a system that ran daily against one real life for long enough to learn what actually
breaks. The rules here are failures with the reason attached: the duplicate row, the 15-minute
sliver nobody could read, the call scheduled into a departure corridor, the brief that vanished an
hour before it was needed. Each one cost something once.
