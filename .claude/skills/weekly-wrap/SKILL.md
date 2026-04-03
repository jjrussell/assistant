---
name: weekly-wrap
description: Make sure to use this skill whenever the user asks for a weekly wrap, weekly reflection, end-of-week summary, or "how did my week go". Also trigger on Fridays when the user says "wrap up the week", "what happened this week", "Friday reflection", or wants to get their head clear for next week. This is the reflective skill — for mechanical file cleanup, use weekly-housekeeping instead.
---

# Weekly Wrap

A Friday ritual to zoom out from the daily grind, take stock, and set up next week. The output is a dated file in `areas/weekly-wraps/` that builds a history useful for quarterly reviews, goal-setting, and pattern recognition.

Target: 10-15 minutes of the user's time. Come prepared with data so they're reacting and refining, not generating from scratch.

## Before starting

**Step 1: Process any open plate file.** Check `outbox/` for a `plate-*.md` file. If one exists, process it before doing anything else — the user may have checked off items and added notes throughout the day that haven't been synced back to the source files yet. Follow the same processing logic as `/whats-on-my-plate` Step 0:
- Checked items (`- [x]`): mark complete in source files (tasks.md, followups.md, project files) and move to `archive/completed.md`
- User-added notes (text below items, modified items): incorporate into relevant files (person files, project files, etc.)
- User-added unchecked items (`- [ ]`): create in the appropriate source file
- Delete the plate file after processing
- Briefly tell the user what you processed: "Processed today's plate: marked N items complete, incorporated notes on X."

**Step 2: Run housekeeping.** Offer to run `/weekly-housekeeping` before the review begins. The review should be built on clean, current data — stale tasks and cluttered files undermine the planning step. If the user declines, proceed anyway.

**Step 3: Gather context.** Do this in parallel — read everything, then synthesize.

- `areas/interactions.md` — this week's rows (filter by date)
- `areas/tasks.md` — tasks due this week (completed and overdue)
- All `projects/*/` files — project-specific tasks due this week
- `areas/followups.md` — follow-ups due this week (resolved and overdue)
- `areas/goals.md` — all active goals
- `areas/recurring.md` — anything that occurred this week
- `areas/people/` — recent observations for direct reports (skim the last entry in each person's file)
- `areas/weekly-wraps/` — last 2-3 wraps for pattern detection

## Present the wrap

Write a draft and present it for the user to react to. Frame it as "here's what I see — correct me where I'm wrong." The sections below are the structure, but adapt the content to what actually happened. Skip sections that have nothing meaningful to say.

### 1. The week in review

Synthesize from interactions. Not a meeting list — a narrative of what moved, what didn't, and what was surprising. Group by theme rather than chronology when possible.

**Example tone:** "The team sync surfaced that data ownership is still unresolved — nobody's claimed it. Meanwhile, the senior hire is progressing fast (hiring committee this week). You spent a lot of time on incident postmortem prep."

### 2. Commitments check

Pull tasks that were due this week. For each:
- Done? Acknowledge briefly.
- Slipped? Say so plainly. No judgment — just visibility. **Include an actionable next step** — a draft message to send, a link to the relevant doc or Slack thread, or a concrete suggestion for what to do next. (See "Make items actionable" principle in CLAUDE.md.)
- New tasks added this week that weren't there Monday? Note them — scope creep is worth seeing.

Same for follow-ups: who came through, who didn't, where nudges are needed. For overdue nudges, draft the nudge message using the person's Slack handle from their person file.

### 3. People pulse

For direct reports and key relationships:
- Who did you connect with this week? (from interactions)
- Anyone you haven't talked to in 2+ weeks? Flag them.
- Notable signals — wins to celebrate, concerns to probe, patterns emerging

Keep this brief. One line per person, only if there's something worth noting.

### 4. Goal momentum

For each active goal, one assessment: **moving**, **stalled**, or **blocked**.

Back it up with specifics from the week — a completed task, a relevant conversation, or the absence of either. Goals with long timelines (months out) can be "on track — no action needed this week" but still list them so nothing is invisible.

### 5. Next week's priorities

Propose 2-3 priorities for next week based on:
- Overdue tasks that need attention
- Follow-ups that need nudges
- Upcoming recurring items or deadlines
- Goal areas that are stalling

Frame as outcomes, not activities: "Get the hiring decision finalized for the senior role" rather than "Follow up with the recruiter about hiring committee."

For each priority, include a concrete first action — a draft message, a link to the relevant doc or thread, or a specific next step that makes it easy to start on Monday.

### 6. Energy check

Ask a simple question: **"How are you feeling heading into next week?"** This isn't therapy — it's data. Over time, energy patterns reveal useful signals:
- Heavy meeting weeks preceding low-output weeks
- Sustained high-intensity periods that need a lighter week
- Specific types of work that drain vs. energize

Capture their answer briefly in the wrap file. When reviewing past wraps, look for energy patterns worth surfacing in Section 7.

### 7. One reflection

Offer one observation — a pattern you're noticing across weeks, something the user might want to think about, or a question worth sitting with. This is the compounding part. Examples:
- "You've had 3 weeks in a row where task X keeps slipping — worth asking whether it's actually a priority or should be dropped."
- "Three different people raised quality concerns independently this week. Might be time for a cross-cutting conversation."
- "You didn't have any 1:1s with [person] this month — intentional or oversight?"
- "Last two wraps you flagged low energy after back-to-back meeting days — might be worth protecting a focus block mid-week."

If nothing stands out, skip it. Forced reflection is worse than no reflection.

## After the user reviews

Make whatever edits they request, then save the final version to:
```
areas/weekly-wraps/YYYY-MM-DD.md
```

Create the directory if it doesn't exist.

The file format:
```markdown
# Weekly Wrap — YYYY-MM-DD

## The week in review
[narrative]

## Commitments
[tasks and follow-ups status]

## People
[pulse check]

## Goals
[momentum assessment]

## Next week
[priorities]

## Energy
[how the user is feeling, brief]

## Reflection
[observation, if any]
```
