# Volatile facts — prices, plans, and click paths

**As of 2026-07-17.** Every fact below was verified against the vendor's own page on that date, and
each one carries the URL it came from. Nothing here is remembered, inferred, or carried over from a
previous version of this file.

**Re-verify anything older than about three months.** After **2026-10-17**, treat every number and
every click path on this page as a claim, not a fact. Vendors reprice without announcing it and
redesign settings screens without telling anyone. A price you quote from a stale file is the first
lie a new user catches you in, and after that nothing else you say gets the benefit of the doubt.

**Where this file disagrees with any skill, this file wins.** The skills carry the *shape* of a
journey — the destinations, the traps, the arguments. This file carries the current clicks and the
current numbers. If a skill states a price, the skill is wrong by construction: it isn't dated and
it isn't sourced.

**If a fact you need isn't here, say the screen may have moved** rather than reconstructing it from
memory. An honest "check this, it may have changed" costs nothing. A confidently wrong path costs
the whole relationship.

---

## Todoist — plans and pricing

| Plan | Price |
|---|---|
| **Beginner** | Free |
| **Pro** | **$7 / month**, or **$60 / year** |
| **Business** | **$10 / user / month**, or **$8 / user / month billed annually** |

**The two facts that are load-bearing here, and neither is about money:**

- **Task durations are a PAID feature (Pro and above).** *(That is what the sources below establish,
  and it is all they establish.)* *Why this matters here:* **without a duration the engine cannot
  state what a thing costs and cannot enforce the floor**, so task-derived rows render a `—` time
  gutter rather than an hour with nothing behind it. On Beginner the engine still runs and still
  places rows at their hour; **what the upgrade buys is the visible length and the enforceable
  floor.**
  **Say "the floor," never a number — this file does not own that value.** It is 30 minutes by
  default and the profile's grain wherever the person states one (§0c). A number here would be a
  calibration wearing this file's date and citation, and no source below establishes it.
  **What a Beginner-tier timed row with no duration draws on a calendar is NOT a fact this file
  carries.** No source below speaks to it — it depends on the user's own task↔calendar sync, which is
  not observable from a pricing page. **The engine probes it on the first run and reports what it
  found.** Anything else here would be a guess wearing this file's date and citation, which is the
  one thing this file exists to prevent.
- **Activity history: 7 days on Beginner, full history on Pro.**
  *Why this matters here:* that log is the engine's **only** discriminator between a row it placed
  and a row the user placed. Past the 7-day cap it cannot prove ownership, so it stops re-placing
  anything at all — safe, silent, and inert.

**Filters: 3 on Beginner, 150 on Pro.** *Why this matters here:* minor. Noted so nobody argues the
upgrade on filter count — the argument is durations and history, not filters.

**Sources:**
- https://www.todoist.com/help/articles/todoist-plans-pricing-and-billing-faq-Vq2z0HWL6
- https://www.todoist.com/pricing

**⚠ UNRESOLVED CONTRADICTION — file upload limit.** The pricing page says Pro uploads are **100MB**;
the help-centre FAQ says **25MB**. Both are Todoist's own pages and they disagree. **Do not quote
either number as fact.** Nothing in this system depends on upload size, so this is flagged rather
than resolved — but it is a live demonstration of why a fact needs a source and a date.

---

## Todoist — signup

**https://todoist.com/auth/signup** — sign up with email/password, or with Google, Apple, or
Facebook. Then verify the email address.

*Why this matters here:* "connect Todoist" said to someone who has no Todoist account is a dead end
they blame themselves for. Free is a real product and the engine runs on it.

**⚠ FLAG — approximate below this point.** Todoist publishes no step-by-step documentation for the
screens that follow signup. Any sub-step described downstream of the signup form is reconstructed,
not sourced. **Say so if you dictate them**, and expect the onboarding questions to have been
reordered.

---

## Todoist — upgrading to Pro

**Do this on the web. NOT on iOS.** *Why this matters here:* upgrading inside the iOS app bills
through the App Store, and someone who already has a web subscription can end up **double-billed**
via App Store + Mac App Store. This is a real, reported outcome, not a theoretical one.

1. Go to **todoist.com** and log in.
2. Click the **avatar, top left**.
3. Click **Settings**.
4. Click **Subscription**.
5. Click **Upgrade to Pro**.
6. Choose **yearly or monthly**.
7. Click **Continue to checkout**.
8. Enter payment.
9. Click **Subscribe**.

**Source:** https://www.todoist.com/help/articles/set-up-a-todoist-pro-subscription-PLxdCDaH9

---

## Todoist → Claude connector

**Works on any Claude plan, including Free.** No upgrade needed on the Claude side.

1. **Log in to claude.ai FIRST.** The flow breaks otherwise.
2. Click the **plus button at the lower left** of the chat box.
3. Click **Connectors**.
4. Click **Add connector**.
5. Click **Browse connectors**.
6. Search **Todoist**.
7. Click **Connect**.
8. Complete the **OAuth** login and **approve** the access screen.
9. **OPEN A NEW CHAT.**

**Step 9 is not optional and it is the single most common "it didn't work."** Tools load only at the
start of a conversation. In the chat where the connector was added, it does not exist yet.
*Why this matters here:* this step guarantees setup gets interrupted, which is why setup must resume
by probing rather than re-asking.

**GOTCHA — say "reschedule", never "change the date".** On a recurring task, "change the date"
**strips the recurrence** — a weekly task quietly becomes a one-off and the user finds out a month
later when it never comes back. "Reschedule" preserves it.

**Batch limit: 25 tasks per call.** *Why this matters here:* a sweep touching more than 25 rows has
to be chunked, and a chunked write is a write that can half-land.

**Source:** https://www.todoist.com/help/articles/use-claude-with-the-todoist-connector-ANlg7v13q

---

## Google Calendar and Gmail → Claude

**These are two separate connectors.** Connect each one.

1. Go to **https://claude.ai/customize/connectors**.
2. Click the **"+"** next to **Connectors**.
3. Find each one — **Google Calendar**, then **Gmail**.
4. Click **Connect**.
5. Complete **Google OAuth**.

**To use either in a chat:** click the **"+" at the lower left**, or type **"/"** → **Connectors** →
**toggle it on**.

**The capability split, which is the whole reason this stack is safe:**

- **Google Calendar = full read + write.** Create, update, delete events.
- **Gmail = read + drafts. There is NO send tool.**

**Tell them about the consent screen BEFORE they see it.** Anthropic's documentation explicitly
warns that Google's consent screen mentions send permission, and states: **"The send function is not
enabled."**
*Why this matters here:* "drafts only" is enforced by the **absence of the capability**, not by a
promise in a prompt. It is the single best safety property in this stack and it costs nothing. Say
it *before* the consent screen, because otherwise that screen stops exactly the people who were
right to be careful.

**Source:** https://support.claude.com/en/articles/10166901-use-google-workspace-connectors

---

## Microsoft 365 → Claude

**THE WALL, STATED FIRST: personal @outlook.com / @hotmail.com / @live.com accounts CANNOT connect.
At all. Not on any Claude plan, not for any amount of money.** This is not a paywall. It is not
supported.

*Why this matters here:* someone whose only calendar is a personal Outlook account has no path, and
they would rather know in minute three than week three. Do not soften it and do not invent a
workaround.

**Work/school accounts can connect, with two conditions:**

1. It must be a **Microsoft Entra work/school tenant**.
2. A **Global Admin must grant tenant-wide consent, once.** This is an email to IT, not a button —
   unless the user *is* the admin.

**And the capability once it's done: the calendar is READ-ONLY** unless an admin separately enables
the write tools, which requires an **Entra re-consent** *and* an **org setting** change. **Assume
read-only until proven otherwise.**

*Why this matters here:* read-only isn't a degraded engine — it's a different output mode. The
engine switches to **propose-only**: it renders the exact event it would have made and the user
creates it. The gate, the envelopes, and the brief work identically.

**End-user clicks, once the admin has consented:**

1. Go to **https://claude.ai/customize/connectors**.
2. Find **Microsoft 365**.
3. Click **Connect**.
4. Sign in with the **work account**.

**Source:** https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector

---

## Slack → Claude — and the 2026-08-03 cutover

**✅ RE-VERIFIED 2026-07-17 — every quote in this section was checked against its source and is
current. Nothing changed. 17 days to the cutover.** The date, both plan-gate quotes, the
Owner/Primary-Owner setup restriction, the Enterprise-only role restriction, the connector's
all-paid-plans gate, the install-first prerequisite, and the Owner-enables-first rule for Team and
Enterprise members all appear verbatim on the vendor's pages as quoted below. **The unresolved
consequence below is still unresolved** — re-read after 2026-08-03.

**Two different products share the word "Slack," and telling them apart is the whole entry.**

| | What it is | Plan gate, verbatim |
|---|---|---|
| **The Slack connector** | **What this engine uses.** Claude searches your channels, DMs and shared files. | *"available for all paid plans (Pro, Max, Team, and Enterprise)"* |
| **Claude in Slack → Claude Tag** | The `@Claude` app *inside* Slack. **This engine does not use it.** | *"Claude Tag is available on Team and Enterprise plans in beta."* |

**THE DATE, verbatim from two separate Anthropic help-centre articles:** *"Claude in Slack will be
switched over to the new Claude Tag experience on **August 3, 2026**."*

**THE TIERS, verbatim:** *"Claude Tag is available on Team and Enterprise plans in beta."* Setup is
**Primary Owner or Owner only** — *"The Admin role can't."* Role-based member restriction is
**Enterprise-only**.

**⚠ THE CONSEQUENCE STILL DOES NOT RESOLVE — and that is the finding, not a gap in the search.**
The connector is documented as all-paid-plans. But the same article states a prerequisite:
**"You must install Claude in Slack before enabling and using the Slack connector."** The thing that
prerequisite names is what is retired on 2026-08-03, and its replacement is Team/Enterprise-only and
admin-provisioned. **No Anthropic page states what a Pro or Max individual's Slack connector does on
2026-08-04.** Not "it keeps working." Not "it breaks." **Unstated.** **Do not resolve this by
reasoning about it** — it needs a live probe after the date.

**⚠ THIS ENTRY GOES STALE BEFORE THE REST OF THE FILE DOES.** The header says re-verify after
**2026-10-17**. **This entry is stale on 2026-08-03** — ten weeks earlier. The file-level horizon
does not vouch for it.

*Why this matters here:* Slack is an optional door-one source — somewhere other people put things on
you. **Nothing in the engine needs it**, so the honest posture is: don't build a setup story on Slack
until someone has probed it after the cutover. The engine only ever *reads* Slack; no write of any
kind depends on this.

**Unchanged and still true:** the connector needs a **paid Slack plan** and a **Slack admin** to
approve the Claude app first. Members of Team/Enterprise Claude orgs *"will not see the option to
enable the Slack connector individually until it's enabled by an Owner."*

**Sources:**
- https://support.claude.com/en/articles/11506255-get-started-with-claude-in-slack
- https://support.claude.com/en/articles/15594475-what-is-claude-tag
- https://claude.com/docs/claude-tag/admins/migrate-from-earlier

**⚠ NOT SOURCED — deliberately left out.** Trade coverage and SEO roundups circulate a *"30-day
opt-in window closing ~2026-07-23"* and specific migration-credit figures. **No Anthropic page states
either**, and Anthropic's own migration doc says only: *"The earlier Claude in Slack app… is being
deprecated; check with your account team for the cutover date."* Omitted rather than carried — a
number from a roundup is exactly the kind of fact this file exists to refuse.

---

## iCloud calendar → Google Calendar (the free path)

**Publishing — needs a computer or tablet. This CANNOT be done from the iPhone.**

1. Go to **icloud.com/calendar** and sign in.
2. **Hover** the calendar in the sidebar.
3. Click the **ⓘ** icon.
4. Turn on **Public Calendar**.
5. Click **Copy Link**.

**Subscribing in Google — computer only. The mobile app cannot add subscriptions.**

6. Go to **calendar.google.com**.
7. Click the **"+"** next to **Other calendars**.
8. Choose **From URL**.
9. **Paste** the link.
10. Click **Add calendar**.
11. **If the link is rejected**, change `webcal://` at the front to `https://` and try again.

**⚠ STEP 11 IS UNVERIFIED PRACTICE — undocumented by both vendors.** Neither Apple nor Google
documents this swap anywhere. It is what works in practice, not a supported instruction. **Flag it
as such when you dictate it.**

### The privacy reality — Apple's own wording

> "To let **anyone** view your calendar—including people not listed in the Shared With list—select
> Public Calendar."

**It is read-only, but it is NOT private.** Full event details — titles, times, locations, notes —
to **anyone holding that link. Forever. No password. No expiry.** And **no free/busy-only option
exists**; Apple offers everything or nothing.

*Why this matters here:* this is the biggest self-inflicted risk in the entire setup and it fails
**silently** — there is no error message, ever. **Never publish a primary calendar.** If someone
takes this path, they should make a purpose-built calendar containing only things they'd be fine
with a stranger reading. Not medical appointments. Not a therapist. Not the meeting whose title is
the deal name.

**Sources:**
- https://support.apple.com/guide/icloud/share-a-calendar-mm6b1a9479/icloud
- https://support.google.com/calendar/answer/37100

---

## iCloud calendar → Outlook (the free path)

**Same publish step as above**, then:

1. Go to **Outlook.com**.
2. Click **Calendar**.
3. Click **Add calendar**.
4. Choose **Subscribe from web**.
5. Paste the **URL**.
6. Click **Import**.

**Microsoft's stated refresh: roughly every 3 hours for personal accounts, roughly every 6 hours for
work accounts — and Microsoft says it "can take more than 24 hours."**

*Why this matters here:* this is the number that reframes the paid option instantly. Hours, not
minutes. "No conflict" on a feed like this means "no conflict as far as a feed that last synced
some hours ago can show."

**⚠ FLAG — that Microsoft page's last-published metadata is 2025-04-24.** The figures are Microsoft's
current published ones, but the page itself is over a year old. Treat the refresh intervals as
approximate.

**Source:** https://support.microsoft.com/en-us/office/import-or-subscribe-to-a-calendar-in-outlook-com-or-outlook-on-the-web-cff1429c-5af6-41ec-a5b4-74f2c278e98c

---

## Paid calendar sync services

| Service | Price | Covers |
|---|---|---|
| **CalendarBridge** | **$5/mo** monthly, or **$4/mo** billed yearly | 2 calendars |
| **CalendarBridge** | **$10/mo** monthly, or **$8/mo** billed yearly | 5 calendars |
| **OneCal** | **$5 / user / month** billed annually | 2 calendars |
| **OneCal** | **$10 / user / month** billed annually | 5 calendars |
| **OneCal** | **$25 / user / month** billed annually | 50 calendars |

**The two things a salesperson wouldn't tell them:**

- **Neither does true real-time iCloud sync. Apple's API doesn't allow it. 5–10 minutes is the
  floor** — a limitation of Apple, not of the product. Anyone promising instant is lying.
- **Both connect using an Apple app-specific password, not OAuth.** That is a **real credential
  handed to a third party**. Revocable, yes. Granular, no. That's the trade.

*Why this matters here:* 5–10 minutes versus Outlook's native **3–6 hours** (and Microsoft's own
"more than 24") is the comparison that actually decides it — **and it needs no public link**. If
iCloud is where someone's life actually is, this is the honest recommendation.

**Sources:**
- https://calendarbridge.com/pricing-individual/
- https://www.onecal.io/pricing

---

## The auto-schedulers — what the market leaders' own defaults concede

**Why these live here and not in the README.** The README argues the shape — that **door two** (work
with no counterparty and no deadline) is the whole point, and that the incumbents' defaults concede
it. **The shape doesn't rot. These citations do.** They are dated vendor facts about a competitor's
default setting, which is precisely the kind of thing that changes in a release nobody announces.
**The README carries the argument; this file carries the quotes and the date. If the README states one
of these as a fact, the README is wrong by construction.**

### Reclaim — the default is that Reclaim's own work never wins

**Verbatim, from Reclaim's own help centre (article updated 2026-06-12):**

> "By default, all non-Reclaim events on your calendar will always be set to Critical (P1) priority,
> so they will never be overbooked by any Reclaim events"

> "Your non-Reclaim events manually set to a lower priority level can only ever be overbooked by
> higher-priority Scheduling Links which will show that time as available — **non-Reclaim events will
> never be overscheduled by Habits, Tasks, or Smart Meetings, regardless of priority levels**"

**Source:** https://help.reclaim.ai/en/articles/6207587-how-reclaim-manages-your-schedule-automatically

**Read the second quote carefully, because it is stronger than the first and it is the one that
matters.** The default (P1) is only half of it. **Even when a user manually downgrades a non-Reclaim
event, Reclaim's own Habits, Tasks and Smart Meetings still cannot overbook it — "regardless of
priority levels."** The single documented exception is a **Scheduling Link**, which offers the time
to *someone else* rather than to your own work. **So on the market leader, work you scheduled for
yourself loses to anything a counterparty put on your calendar, by construction, and the priority
system cannot reverse it.** That is the concession, and it is structural rather than a default.

**BE FAIR ABOUT THIS — the design is defensible and this file does not get to sneer at it.** A tool
that moves a meeting somebody else is expecting you at breaks a promise to a third party who never
agreed to be managed by your scheduler. Reclaim declining to do that is a **correct** call about
consequences, not an oversight, and the same reasoning is why the engine here treats a counterparty's
claim on your time as an envelope rather than a suggestion. **The disagreement is about scope, not
about whether they got it wrong.** Reclaim answers "protect my focus time around my commitments."
Door two asks the different question: what happens to the work nobody is waiting for.

**⚠ TWO CAVEATS, both real:**
- **This is the Reclaim 1.0 documentation, and the page says so:** *"This article refers to Reclaim
  1.0 features and workflows"*, with a separate doc collection for **Reclaim 2.0**. **These quotes may
  not describe 2.0.** Re-verify against 2.0 before putting this in front of anyone who uses it.
- **⚠ NOT VERIFIED: auto-decline.** It is sometimes claimed that Reclaim offers auto-decline as an
  opt-in, which would soften the concession above. **No such feature appears on this page** and
  nothing here establishes it. **Do not include it in the argument without a source.**

### Motion — the hierarchy is verified; the conclusion drawn from it is NOT

**Verbatim, Motion's published scheduling hierarchy** — verified 2026-07-17 at
https://www.usemotion.com/help/time-management/auto-scheduling.md:

> 1. **ASAP** · 2. **Hard deadlines** · 3. **Deadlines (soft/flexible)** · 4. **Priority** ·
> 5. **Duration** · 6. **Start dates** · 7. **Recurrence**

**That list is real and correctly ordered. The inference "recurrence is LAST, therefore work with no
counterparty and no deadline sits at the bottom by construction" IS CONTRADICTED BY THE SAME PAGE, and
must not be written.** Position 7's own description says the opposite of what its position implies:

> "**Recurrence** → Recurring tasks are placed **ahead of** one-off tasks to maintain cadence."

And twice more on the same page: *"Recurring tasks (like daily routines) **may be scheduled first** if
they are the only ones that fit into available time slots, even if a one-off task has a higher
priority"*, and *"Motion auto-schedules recurring tasks **ahead of** one-off tasks with lower priority
to ensure they always fit."*

**The list is an ordering of TIE-BREAK CRITERIA, not a ranking of the work.** Recurrence being the
last criterion consulted does not put recurring work last — the criterion, when it is consulted,
**favours** recurring tasks. **Reading the list position as the work's rank is a misreading, and it is
the flattering one.** Do not ship it. *(Motion's page is also internally loose here: the hierarchy
list and the hint box below it disagree about whether priority or deadlines come first. Treat the
whole hierarchy as a published guideline — the page itself calls it a "guideline" and says
auto-scheduling "doesn't follow a single linear rule" — rather than as a specification.)*

**What Motion's page DOES support, and it is enough:** deadlines and priority dominate the ordering,
**and a task with neither a deadline nor an ASAP flag is ordered only by what is left** — priority,
duration, start date, recurrence. **The argument door two needs is that undeadlined personal work is
ranked by the fields it doesn't have. That is visible in the hierarchy without overclaiming what
position 7 means.**

---

## Dictation (unrelated to this system — neither app connects to it)

### Wispr Flow

| | |
|---|---|
| **Free** | 2,000 words / week desktop, 1,000 / week iPhone — **recurring weekly allowance** |
| **Pro** | **$15/mo**, or **$12/mo** billed annually |
| **Trial** | 14-day Pro trial, **no card required** |
| **Students** | 3 months free, then 50% off |
| **Platforms** | Mac, Windows, iPhone, Android |

**Source:** https://wisprflow.ai/pricing

### Monologue by Every

| | |
|---|---|
| **Free** | **A one-time 1,000-word trial — NOT a recurring allowance.** The vendor labels it "Trial." |
| **Paid** | ~$9.99/mo early-bird, ~$14.99/mo regular; ~$99.99/yr early-bird, ~$143.99/yr regular ⚠️ |
| **Bundled** | Included with an Every subscription (~$288/yr or ~$30/mo) alongside their other products ⚠️ |
| **Platforms** | **macOS + iOS/watchOS only. No Windows. No web.** |

**Sources:** https://www.monologue.to/ · https://apps.apple.com/us/app/monologue-smart-dictation/id6755956193 · https://every.to/pricing
⚠️ The vendor's own pricing page shows a figure that does not reconcile to the App Store listing. **Unresolved — check in-app before quoting.**

**Name collision:** `monologue.to` is Every's. **`monologue.run` is a different, unrelated app.** Roundups conflate them.

**Its MCP is read-only and notes-only** (`api.monologue.to/mcp`, scope `notes:read`). **It does not expose dictation to Claude.** It is not "the dictation app your assistant can use."

### How to talk about dictation — and the claim NOT to repeat

**Never say dictation is "3x" or "4x faster than typing." The number is false as applied here, and
the vendors' own source does not support it.** The 2016 preprint titled *"Speech Is 3x Faster than
Typing"* was **retitled by its own authors** on peer review to *"…for Short Messages… on Touchscreen
Phones"*, and §3.4 states they deliberately chose *"a text transcription task rather than a text
composition task… composition introduces confounds such as thinking time."* **They excluded the
dominant variable, then reported a ratio on what was left.** When composition was actually tested
(Foley, Casiez & Vogel, CHI 2020): end-to-end **1.40x**, and speech users needed **2.1x MORE thinking
time.**

**The honest pitch is willingness, not speed.** You will dump three paragraphs of context you would
never have typed — not because typing them is slower, but because typing them *feels* like work.
And an LLM is the rare reader that does not punish rambling, disfluent, unpunctuated input, so you
get the input-speed win without the quality tax that normally eats it. **That is the whole argument.
Say that; never say 4x.**

**Sources:** https://arxiv.org/abs/1608.07323v1 · https://doi.org/10.1145/3161187 · https://dl.acm.org/doi/10.1145/3313831.3376861

*Why this is here at all:* it is **not part of this system**, does not connect to it, and changes
nothing about how the brief works. Mention it once, at the very end, only if dictation would
obviously help the person in front of you. If they like typing, it does nothing for them.

---

## Claude surfaces, plans, and where things install

**The single most common routing confusion: "web vs Cowork" is a false premise.**

> "Chat and Cowork share one home, so you start both from the same place. On any surface, find the
> message box, select **'Cowork' in the bottom left corner**, then describe your task."

**Cowork is a toggle at claude.ai.** Not a separate app, not a separate purchase, nothing to
download. **Source:** https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile

### Cowork availability — GA on desktop, beta on web/mobile

**Verbatim:** *"Claude Cowork is available for paid plans (Pro, Max, Team, Enterprise)"* — on Claude
Desktop for macOS and Windows, Web at claude.ai, and Claude Mobile (iOS/Android).

**Verbatim:** *"Claude Cowork is in beta on web and mobile, and rolling out over the next several
weeks starting with the Max plan, with more plans to follow."*

**The help centre does NOT call Cowork a research preview.** Checked on both the Get-started and the
surfaces articles on 2026-07-17. *(The phrase does still appear on that page, but attached to a
different feature: "Computer use is a research preview for Pro and Max plans." Do not transplant it
onto Cowork.)* **This file never claimed otherwise — no correction was needed.**

**Sessions run remotely by default (in beta).** Verbatim: *"Work continues if you close your laptop,
and you can open the same session from any surface."*

**The desktop app is still required for four things, verbatim:** *"Local file access. Local
connectors. Browser use. Computer use."* — *"These capabilities reach things on your computer, so
they need the app even though your session runs remotely."*

**⚠ LOAD-BEARING LIMITATION — chat memory does not reach Cowork. Verbatim:**

> "**Memory:** What Claude remembers about you in chat doesn't carry into Cowork sessions yet.
> Within Cowork, memory is supported in projects only."

*Why this matters here — this is the most important line in this file for this system's
architecture.* **The profile lives in a `cos-profile` row on a connected surface, not in chat
memory.** That was an architectural choice made before this limitation was documented; the vendor has
now confirmed it was the only correct one. **A profile in chat memory would be invisible to every
scheduled Cowork run** — the exact surface the morning brief fires from. The choice is not defensive
and it is not a workaround. It is the only design the vendor's own limitation permits. **Do not
"simplify" it into memory.**

**Auto mode will not approve creating a scheduled task.** Verbatim: *"Auto mode won't approve certain
sensitive actions like allowing Cowork to access additional folders on your computer, allowing Cowork
to delete files in a given folder it has access to, **creating scheduled tasks**, and others."*
*Why this matters here:* setup ends by creating a scheduled task. **That step needs a human click no
matter what mode they are in.** Say so before it stalls, or setup looks broken at the last step.

**Sources:**
- https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile

### The real gates

| Capability | Plan | Surface |
|---|---|---|
| **Skills** | **Free, Pro, Max, Team, Enterprise** — *"Skills are available for users on Free, Pro, Max, Team, and Enterprise plans. This feature requires code execution to be enabled."* | all |
| **Plugins** | **Paid only** — *"Plugins are available to all paid plans (Pro, Max, Team, Enterprise)."* | web, Desktop Chat tab, Cowork. Mobile ⚠️ contradicted across docs — see note |
| **Connectors** | **all plans, all surfaces incl. mobile** (Free capped at one custom connector) ⚠️ *the capability, not each connector — see note* | all |
| **Scheduled tasks** | **Cowork, all paid plans** — *"Scheduled tasks are available in Cowork for all paid plans (Pro, Max, Team, Enterprise)."* | Cowork |
| **Desktop Extensions (.mcpb)** | no stated gate ⚠️ — appears to work on Free | **Claude Desktop / Claude Code only** |

**All four quoted rows re-verified against the vendor's pages on 2026-07-17. Unchanged.**

**Sources:** https://support.claude.com/en/articles/13837440-use-plugins-in-claude · https://support.claude.com/en/articles/12512180-use-skills-in-claude · https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities · https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork

**⚠️ THE PLUGINS-ON-MOBILE CONTRADICTION, now pinned to both sides rather than left vague.** The
plugins article enumerates the surfaces and mobile is not among them: *"You can install and use
plugins in chat on the web, the Chat tab in Claude Desktop, and Claude Cowork."* The surfaces
article's per-surface table gives **"Skills and plugins" a ✅ under Mobile.** **Both are Anthropic
pages and they do not reconcile.** The likeliest reading — that the plugins article is enumerating
*chat* surfaces while the table is describing *Cowork* on mobile — **is a reading, not a fact, and it
is not what either page says.** **Do not promise plugins on mobile; do not deny them. Probe it.**

**More plugin facts, verbatim and current:**
- **Hooks and sub-agents:** *"Hooks and sub-agents run only in Cowork, so they appear grayed out in
  chat."*
- **Marketplaces:** *"Sync a marketplace from a GitHub repository or git URL."*
- **⚠ THE COWORK CONNECTOR CAVEAT, and it kills localhost:** *"In Cowork, connectors reach external
  services through Anthropic's cloud, not through your local network. **A custom connector must point
  to a server that's reachable over the public internet from Anthropic's IP ranges.**"*
  *Why this matters here:* a notes app running an HTTP server on a **loopback port** is not reachable
  from Anthropic's IP ranges. **A local notes server does not cost the schedule at the margin — in a
  remote Cowork session it is not reachable at all**, and reaches Claude only through the desktop app
  as a local connector. STACK's "every local one pins the brief to the machine" is the right shape;
  this is the mechanism under it.

**⚠️ Read the Connectors row as the *capability*, not a promise about any one connector. Each
connector sets its own gate on top.** Two in this file already do: the **Slack** connector is
*"available for all paid plans (Pro, Max, Team, and Enterprise)"* — **not Free** — and additionally
needs a paid Slack plan and a Slack admin; **Microsoft 365** needs an Entra work tenant and excludes
personal Outlook accounts entirely. *Why this matters here:* "connectors work on every plan" is true
of the feature and false of the specific connector someone is about to try, and that gap is where a
setup conversation dies.

### The free path — the widest-reach fact in this package

**The wall is on plugins, not skills.** A Free user cannot install the plugin — but **can zip each
folder under `skills/` and upload it at `claude.ai/customize/skills`**, connect Gmail / Google
Calendar / their task list as ordinary connectors, and run the pass by asking for it. **They get
everything except the packaged install and the automatic morning run.**

**The Free upload path, from the vendor's own steps — note the intermediate click, which is easy to
miss and is where a dictated path goes wrong:**

1. **Settings > Capabilities** → enable **Code execution and file creation**. *(Free, Pro, Max. On
   Team/Enterprise an Owner enables it in Organization settings > Skills instead.)*
2. Go to **Customize > Skills** (`claude.ai/customize/skills`).
3. Click the **"+"** button, then **"+ Create skill"**.
4. Select **"Upload a skill."**
5. Upload a **ZIP containing your skill folder**.

**Source:** https://support.claude.com/en/articles/12512180-use-skills-in-claude

**⚠ NOT VERIFIED — the ZIP size limit is NOT PUBLISHED, and this is a real hole in the free path this
package markets.** The vendor lists *"ZIP file exceeds size limits"* first among its documented
upload failures **and never states the limit.** No byte figure appears on that page or on the
create-custom-skills page. **Do not quote a number — not from a roundup, not from an inference about
other upload limits in this file.** The honest line to a Free user is: *if the upload fails, size is
the vendor's first suspect and the threshold is unpublished — try a smaller skill folder.* **The
other documented failure causes are quotable and worth saying first**, because they are likelier and
they are checkable: *"Skill folder name doesn't match the skill name"*, *"Missing required skill.md
file"*, *"Invalid characters in skill name or description."*

### Desktop Extensions — the channel a plugin cannot reach

**DXT was renamed MCPB (`.mcpb`) in Sep 2025; `.dxt` still works.** Install: **Settings > Extensions
> Browse extensions** (Anthropic-reviewed), or **Advanced settings > Extension Developer** for a
local file. **A plugin cannot bundle or install one** — separate channel, enforced (admin controls
disable `.mcpb` installs while leaving plugins untouched).

**iMessage and Apple Notes are official Anthropic extensions.** iMessage requires **Full Disk
Access**. **Source:** https://support.claude.com/en/articles/10065433-install-claude-desktop

*Why this matters here:* extensions are the one capability a **Free** user can have that a plugin
user cannot, and they are also the one that forfeits the overnight run — see Scheduling below.

### "Control your Mac" — a community osascript extension (NOT Anthropic-built)

**Added 2026-07-17.** A third-party Desktop Extension that runs AppleScript on your Mac through
`osascript`. Recorded here because it is the general-purpose AppleScript bridge some people already
have installed, and it can stand in for AppleScript-driven readers (Apple Notes, Reminders, Messages)
in one extension. **Everything below was verified on 2026-07-17 from the extension's own
`manifest.json`, its public repo, and — for the directory listing — a live Claude Desktop install
record.**

- **Display name:** **"Control your Mac"** — the manifest's `"name"`. Its `"description"` is
  *"Execute AppleScript to automate tasks on macOS."*
- **Author:** **Kenneth Lien** (GitHub **k6l3**, homepage kennethlien.com) — an individual developer.
  **Community-authored, NOT built by Anthropic.** The repo lives under a personal account, not the
  `anthropics` org; the manifest only references Anthropic's `dxt` tooling as the *build* mechanism.
- **License:** **MIT** — manifest `"license": "MIT"`, and the repo carries an MIT license.
- **Open-source:** **https://github.com/k6l3/osascript-dxt** — confirmed resolving on 2026-07-17
  (public, 156 stars; the single tool it exposes is `osascript`, described as *"Execute `osascript -e
  <script>`"*).
- **What it does:** executes arbitrary AppleScript through macOS `osascript`, so it can drive
  scriptable apps and change system settings on the machine.
- **Install:** the Desktop-Extension channel — **Claude Desktop → Settings → Extensions → Browse.**
- **✓ VERIFIED — the directory listing.** It appears in the Anthropic-reviewed **Browse extensions**
  directory. Confirmed on 2026-07-17 from a Claude Desktop install record: the installed extension id
  is `ant.dir.gh.k6l3.osascript` (installed 2026-07-16), and the `ant.dir.` namespace is the one
  Claude assigns to extensions installed **from the directory** — distinct from the `local.dxt.`
  namespace it gives sideloaded ones. **Caveat, because this is a directory and directories change:**
  that is a point-in-time fact; if the listing matters months from now, re-confirm in-app at
  Settings → Extensions → Browse, since an extension can be delisted. The open-source repo carries
  the install either way.

*Why this matters here:* an extension that can run arbitrary AppleScript is a broad capability, and it
is **local** — so the capability ladder's schedule cost applies (a brief that leans on it runs on a
waking Mac), and the same caution any "let a model drive my machine" capability deserves applies too.
Being installable from the Browse directory, if confirmed, is a distribution fact — **not** an
authorship or endorsement one.

**Sources:**
- Manifest (name, author, license, `osascript` tool):
  https://raw.githubusercontent.com/k6l3/osascript-dxt/main/manifest.json
- Repository (public, MIT, community-authored): https://github.com/k6l3/osascript-dxt

---

## Scheduling — where a task runs

**These are THREE DIFFERENT PRODUCTS — do not run them into one table.** **Cowork scheduled tasks** (`/schedule` in a Cowork task) are not
**Claude Code Desktop scheduled tasks**, and neither is a **Claude Code cloud routine**. **This
system's brief is a Cowork scheduled task.** The Claude Code rows below are a comparison, not this
system's runtime — the catch-up rule and the "9am might run at 11pm" line are **Claude Code Desktop's
documented behaviour and are not documented anywhere for Cowork.** Keeping them straight is the
difference between a sourced fact and a plausible one.

### ⚠️⚠️ UNRESOLVED CONTRADICTION — Anthropic's own scheduled-tasks article contradicts itself, and this package leans on the half it likes

**Both quotes are from the SAME article, verified 2026-07-17:**
https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork

> **Top of the article, in the "How scheduled tasks work" note:** "Scheduled tasks use the built-in
> schedule options and work with your connectors and the files saved to your Claude account. **They
> can't be tied to a folder on your computer.**"

> **The manual setup flow, further down the SAME article**, lists among the fields of the *Create
> scheduled task* modal: "**Which folder Claude should work in [optional]**" — carrying the note:
> "**If a scheduled task requires local files or apps, it will only run locally.**"

**These cannot both be fully true.** One says a scheduled task **cannot** be tied to a folder on your
computer. The other offers a field for **choosing the folder** and describes what happens when the
task needs local files. **A third sentence in the same article** — *"Scheduled tasks run remotely, so
they run on their cadence even when your computer is asleep or the Claude Desktop app is closed."* —
is stated flatly, with no local-task exception carved out of it.

**This is recorded as a contradiction, not resolved.** The tempting resolution — *"the folder picker
is vestigial"* or *"'can't be tied to a folder' means the remote runner, and the local path is the
exception"* — **is reasoning, not a source.** No Anthropic page states which sentence governs. **A
plausible reconciliation written down as fact is exactly the failure this file exists to prevent**,
and it would be a comfortable one, because the reading that suits this package is available.

**Why this governs how the package may talk about scheduling.** *"If a scheduled task requires local
files or apps, it will only run locally"* **is real and correctly transcribed — the problem is that
the same article contradicts it.** So it must not be quoted anywhere as the reconciling rule: every
place this package describes where a brief runs presents the contradiction and says to probe it,
never this one sentence as settled law.

**The honest posture, and it costs this package almost nothing:** the *architecture* survives either
way. **Under EITHER sentence, a local dependency is what puts the brief at risk** — either it pins
the run to the machine (sentence two), or the scheduled task **cannot reach the folder at all**
(sentence one), which is *worse* and fails *harder*. **"Start with hosted connectors only" is the
correct recommendation under both readings.** The recommendation does not need the contradiction
resolved. **The claim about mechanism does.**

**→ PROBE IT: create a Cowork scheduled task, try to give it a folder, and see what the modal
actually offers.** One run answers it. **Until someone does, quote neither sentence as the rule** —
quote the *behaviour* ("a local dependency puts the scheduled run at risk; the vendor's docs disagree
about exactly how") and cite this entry.

### Cowork scheduled tasks — what IS verified

- **Gate:** *"Scheduled tasks are available in Cowork for all paid plans (Pro, Max, Team,
  Enterprise)."*
- **Cadences:** **hourly, daily, weekly, weekdays, or manually.** That is the full published list —
  **there is no minutes-level option**, and "manually" means no schedule, run on demand.
- **Remote by default:** *"Scheduled tasks run remotely, so they run on their cadence even when your
  computer is asleep or the Claude Desktop app is closed."* Also, from the surfaces article:
  *"Scheduled tasks run with no device online."*
- **Creating one is not auto-approvable** — see the Cowork section above. Auto mode won't do it.
- **⚠ NOT DOCUMENTED ANYWHERE: what a Cowork scheduled task does when it MISSES a run.** No
  catch-up rule, no skip rule, no retry rule is published for Cowork. **Do not import Claude Code
  Desktop's catch-up rule below and dress it as Cowork's.** It is a different product's documentation.

### Claude Code — cloud routines vs Desktop tasks (a comparison, not this system's runtime)

| | **Cloud routine** | **Desktop scheduled task** |
|---|---|---|
| Runs on | Anthropic cloud | Your machine |
| **Requires the machine on** | **No** | **Yes** |
| **Access to local files** | **No — "(fresh clone)"** | **Yes** |
| **Minimum interval** | **1 hour** — *"expressions that run more frequently are rejected"* | **1 minute** |
| Permission prompts | **None — *"runs autonomously"*** | Configurable per task |
| Maturity | **⚠ *"Routines are in research preview."*** | no stated preview label |
| Shape | **Repo-centric** — *"Each repository you add is cloned on every run"* | folder-centric; a folder is **required** to save the task |
| Cap | **⚠ *"routines have a daily cap on how many runs can start per account"*** — the number is **not published**; the vendor points you at your own usage page | none stated |
| Gate | Pro, Max, Team, Enterprise **with Claude Code on the web enabled** | — |

**⚠ THE ROUTINES TRAP, verbatim, and it silently breaks a working local setup:** *"MCP servers you
added locally in the CLI with `claude mcp add` are stored on your machine rather than your claude.ai
account, **so they do not appear in the connectors list**."* **A connector that works in your terminal
does not exist to a cloud routine.** To use one there it must be added at
`claude.ai/customize/connectors` or declared in a committed `.mcp.json`.

**Desktop's sleep behaviour, verbatim — this is the "7am brief at 10pm" fact and it belongs to Claude
Code Desktop, not to Cowork:**

> "Tasks only run while the desktop app is running and your computer is awake. **If your computer
> sleeps through a scheduled time, the run is skipped.**"

> "Desktop checks whether each task missed any runs **in the last seven days**. If it did, Desktop
> starts **exactly one catch-up run for the most recently missed time and discards anything older.**
> A daily task that missed six days runs once on wake."

> "**A task scheduled for 9am might run at 11pm if your computer was asleep all day.**"

**Sources:**
- https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile
- https://code.claude.com/docs/en/desktop-scheduled-tasks
- https://code.claude.com/docs/en/routines
