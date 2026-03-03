---
name: weekly-housekeeping
description: Run weekly cleanup and archiving of stale tasks, follow-ups, interactions, and goals. Use on Fridays or when explicitly requested.
---

## Weekly Housekeeping

1. **Archive old interactions:** Move index rows older than 30 days from `areas/interactions.md` → `archive/interactions/YYYY-MM.md`
2. **Clean tasks:** Remove completed tasks from `areas/tasks.md`
3. **Clean follow-ups:** Purge resolved or clearly-stale follow-ups from `areas/followups.md`
4. **Scan goals:** Check `areas/goals.md` — flag any goals with no recent activity

## Weekly Wrap (every Friday)

Triggered alongside housekeeping. Format: TBD.

## Archiving

Periodically move inactive items to `archive/` to keep active files manageable:

**Projects:**
- When a project completes, move from `projects/` to `archive/projects/`
- Add an outcome summary at the top before archiving

**People:**
- When someone is no longer an active contact, move their entire directory from `areas/people/[person]/` to `archive/people/[person]/`

**Goals:**
- When goals are completed or abandoned, move from `areas/goals.md` to individual files in `archive/goals/`

**Interactions:**
- Periodically (quarterly/annually) move old interactions to `archive/interactions/`
- Can organize by year: `archive/interactions/2025.md`
