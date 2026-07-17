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

- **Task durations are a PAID feature (Pro and above).** Without a duration, a dated task renders as
  an **all-day banner** at the top of the calendar rather than a time block at a specific hour.
  *Why this matters here:* placement is the entire product. On Beginner the engine still runs, but
  its output degrades into the exact calendar clutter the system exists to remove.
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

### The real gates

| Capability | Plan | Surface |
|---|---|---|
| **Skills** | **Free, Pro, Max, Team, Enterprise** (needs code execution enabled) | all |
| **Plugins** | **Paid only** — *"available to all paid plans (Pro, Max, Team, Enterprise)"* | web, Desktop Chat tab, Cowork. Mobile ⚠️ contradicted across docs |
| **Connectors** | **all plans, all surfaces incl. mobile** (Free capped at one custom connector) | all |
| **Scheduled tasks** | **Cowork only, paid only** | Cowork |
| **Desktop Extensions (.mcpb)** | no stated gate ⚠️ — appears to work on Free | **Claude Desktop / Claude Code only** |

**Sources:** https://support.claude.com/en/articles/13837440-use-plugins-in-claude · https://support.claude.com/en/articles/12512180-use-skills-in-claude · https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities

### The free path — the widest-reach fact in this package

**The wall is on plugins, not skills.** A Free user cannot install the plugin — but **can zip each
folder under `skills/` and upload it at `claude.ai/customize/skills`**, connect Gmail / Google
Calendar / their task list as ordinary connectors, and run the pass by asking for it. **They get
everything except the packaged install and the automatic morning run.**

### Desktop Extensions — the channel a plugin cannot reach

**DXT was renamed MCPB (`.mcpb`) in Sep 2025; `.dxt` still works.** Install: **Settings > Extensions
> Browse extensions** (Anthropic-reviewed), or **Advanced settings > Extension Developer** for a
local file. **A plugin cannot bundle or install one** — separate channel, enforced (admin controls
disable `.mcpb` installs while leaving plugins untouched).

**iMessage and Apple Notes are official Anthropic extensions.** iMessage requires **Full Disk
Access**. **Source:** https://support.claude.com/en/articles/10065433-install-claude-desktop

*Why this matters here:* extensions are the one capability a **Free** user can have that a plugin
user cannot, and they are also the one that forfeits the overnight run — see Scheduling below.

---

## Scheduling — where a task runs

| | Cloud routine | Desktop task |
|---|---|---|
| **Fires with the computer OFF** | **Yes** | **No — the run is SKIPPED** |
| **Access to local files / apps** | **No** | **Yes** |

**A skipped desktop run gets ONE catch-up on wake. Older misses are discarded.** That is why a 7am
brief can arrive at 10pm.

**The reconciling rule, verbatim from the Cowork docs:**

> "If a scheduled task requires local files or apps, it will only run locally."

*Why this matters here:* this is the rule that ties the two halves of setup together. **Every local
dependency added silently converts a reliable cloud brief into a machine-pinned one that gets
skipped whenever the laptop sleeps.** Local readers don't merely cost portability — they cost the
schedule. That price is invisible unless someone says it out loud.

**Sources:**
- https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
- https://code.claude.com/docs/en/desktop-scheduled-tasks
