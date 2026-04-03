---
name: daily-wrap
description: Make sure to use this skill whenever the user asks for a daily wrap, end-of-day review, daily shutdown, or "wrap up the day". Also trigger when the user says "done for today", "closing out", "EOD check", or wants to clear their head before leaving work. This is the daily counterpart to weekly-wrap.
---

# Daily Wrap

A 5-minute end-of-day shutdown ritual. The goal is to close out today cleanly so tomorrow morning starts with clarity, not catch-up. Over a week, daily wraps also surface patterns that feed into the weekly wrap.

Target: 5 minutes of the user's time. Fast, focused, no fluff.

## Before starting

**Step 0: Process any open plate file.** Check `outbox/` for a `plate-*.md` file. If one exists, process it first — the user may have checked off items and added notes throughout the day that haven't been synced back to the source files yet. Follow the same processing logic as `/whats-on-my-plate` Step 0:
- Checked items (`- [x]`): mark complete in source files (tasks.md, followups.md, project files) and move to `archive/completed.md`
- User-added notes (text below items, modified items): incorporate into relevant files (person files, project files, etc.)
- User-added unchecked items (`- [ ]`): create in the appropriate source file
- Delete the plate file after processing
- Briefly tell the user what you processed: "Processed today's plate: marked N items complete, incorporated notes on X."

**Then gather today's context.** Do this in parallel:

- `areas/tasks.md` — tasks due today or overdue
- All `projects/*/` files — project-specific tasks due today or overdue
- `areas/followups.md` — follow-ups due today or overdue
- `areas/interactions.md` — today's interactions (filter by date)
- `areas/recurring.md` — anything due today
- Tomorrow's calendar context (if available from recent interactions)

## Present the wrap

Keep it tight. Present a short summary and walk through it interactively. The user should be reacting and deciding, not reading paragraphs.

### 1. Today's action items

Pull all tasks and follow-ups that were due today (or already overdue coming into today). Present them as a checklist for the user to process. **For each item, include a concrete next step** — see the "Make items actionable" principle in CLAUDE.md.

```
Tasks due today:
- [ ] Task A (due today) — Done? Reschedule? Drop?
      → [Draft message / link / suggested action]
- [ ] Task B (overdue from Mon) — Done? Reschedule? Drop?
      → [Draft message / link / suggested action]

Follow-ups due today:
- [ ] Waiting on X from Person — Received? Nudge? Push date?
      → Draft nudge: "Hey [person], circling back on [thing] — any update?"
```

Examples of actionable next steps:
- **"Reply to Alex about API review"** → draft the reply based on interaction context
- **"Send hiring committee feedback"** → link to the relevant doc or Slack thread
- **"Follow up with recruiter"** → draft Slack message with their @handle from their person file
- **"Review PR"** → link to the PR if mentioned in interactions or project file

Use available tools (Slack search, Glean, person file contact info) to gather links and context. If a task is self-contained (e.g., "write the design doc"), no extra context is needed — don't force it.

For each item, the user picks one:
- **Done** — mark complete, move to `archive/completed.md`
- **Reschedule** — pick a new date (suggest one based on context — e.g., tomorrow, next available day, before a related meeting)
- **Drop** — remove it (confirm first if it seems important)
- **Nudge needed** — for follow-ups where the other person hasn't delivered, present a draft nudge message, update the nudge trail in the context field and push the due date

Process each decision immediately — update the files as you go so the user doesn't have to revisit.

### 2. Anything new captured today?

Quick scan of today's interactions. If interactions were logged today, check whether they generated tasks or follow-ups that haven't been filed yet. Ask:

> "I see you logged [interaction]. Anything from that still needs tracking?"

If no interactions were logged today, skip this section.

### 3. Tomorrow preview

Briefly note what's coming tomorrow:
- Tasks due tomorrow
- Follow-ups due tomorrow
- Recurring items due tomorrow
- Any meetings noted in recent interactions

Frame it as awareness, not planning: "Here's what's on deck for tomorrow" — not "let's plan tomorrow." Planning happens in the morning.

### 4. Slip pattern check (brief)

If the same task has been rescheduled 3+ times, or if multiple items are consistently slipping day over day, flag it in one line:

> "Task X has been rescheduled 3 times now — worth deciding: commit to it or drop it?"

This is the daily equivalent of the weekly wrap's reflection section. Keep it to one observation max. Most days there's nothing to flag — that's fine.

## After the user reviews

Update all files based on their decisions:
- Completed items to `archive/completed.md`
- Rescheduled items get new due dates
- Dropped items get removed (or archived if they had significant context)
- Nudged follow-ups get updated context and pushed dates

**Do not save a daily wrap file.** Unlike the weekly wrap, daily wraps don't get persisted — they're ephemeral. The value is in the file updates (clean task lists, accurate dates), not in a record of the review itself. The weekly wrap provides the historical record.

## Design principles

- **Speed over thoroughness** — this is a shutdown ritual, not an analysis session. 5 minutes max.
- **Decisions, not discussion** — present items, get a verdict, move on.
- **Clean state for tomorrow** — the measure of success is that tomorrow's morning starts with an accurate, current task list.
- **Catch drift early** — the slip pattern check means problems surface Tuesday, not Friday.
- **Complement the weekly wrap** — daily wraps keep the data clean; the weekly wrap does the strategic thinking. They work together.
