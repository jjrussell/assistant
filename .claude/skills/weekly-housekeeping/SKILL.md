---
name: weekly-housekeeping
description: Make sure to use this skill whenever the user asks for system housekeeping, cleanup, or to declutter the memory system. Also trigger for "clean things up", "archive old stuff", "tidy up my system", or any request to keep active files from growing too large. This is the mechanical cleanup skill — for weekly reflection, use weekly-wrap instead.
---

# System Housekeeping

Mechanical cleanup of the memory system. The goal is to keep active files focused on what's current so they're fast to scan and don't accumulate noise. Archived items aren't deleted — they move to `archive/` where they're still searchable.

## Steps

### 1. Archive old interactions

Move index rows older than 30 days from `areas/interactions.md` to `archive/interactions/YYYY-MM.md` (grouped by month). The 30-day window keeps roughly a month of context visible for pattern recognition while preventing the file from growing indefinitely.

If a row is older than 30 days but references an active project or open follow-up, flag it rather than archiving — it may still be useful context.

### 2. Clean completed tasks

Move completed tasks from `areas/tasks.md` to `archive/completed.md`. Also scan project files (`projects/*/`) for completed project-specific tasks and archive those too.

For tasks marked `pending` that are significantly overdue (2+ weeks past due date):
- Flag them with a brief note: "Overdue since [date] — still relevant?"
- Present the list to the user rather than archiving silently, since overdue tasks may need rescheduling rather than removal

### 3. Clean follow-ups

Move resolved follow-ups from `areas/followups.md` to `archive/completed.md`.

For follow-ups that are overdue:
- If 1-2 weeks overdue: leave in place, add a nudge note to context
- If 3+ weeks overdue with no updates: flag for the user — these likely need escalation or a different approach

### 4. Update recurring items

Check `areas/recurring.md`:
- If any item's "next occurrence" has passed, update it to the next future date
- Regenerate the upcoming dates table (next 3 occurrences)
- If a prep task was due and not created, create it

### 5. Scan goals

Check `areas/goals.md` — flag any goals that have had no related interactions, tasks completed, or follow-ups resolved in the past 2 weeks. A stalled goal isn't necessarily a problem (some have long timelines), but surfacing them keeps them from quietly dying.

### 6. Report

Present a summary:
```
HOUSEKEEPING COMPLETE
  Interactions archived: N rows (from [month])
  Tasks cleaned: N completed, N flagged as overdue
  Follow-ups cleaned: N resolved, N flagged as stale
  Recurring items updated: N
  Goals flagged: N with no recent activity
```

If anything was flagged for the user's attention, list those items after the summary.

---

## Archiving (on-demand, not weekly)

These are bigger moves triggered by life events, not routine cleanup:

**Projects:** When a project completes, move its folder from `projects/` to `archive/projects/`. Add an outcome summary at the top of the main file before moving.

**People:** When someone is no longer an active contact, move their directory from `areas/people/[person]/` to `archive/people/[person]/`.

**Goals:** When goals are completed or abandoned, move them from `areas/goals.md` to `archive/goals/`.
