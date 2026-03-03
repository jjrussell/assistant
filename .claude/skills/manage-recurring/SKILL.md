---
name: manage-recurring
description: Manage recurring items — create, update, and track items that repeat on a schedule. Auto-invoked when recurring responsibilities are discussed or need updating.
---

## Recurring Items

Recurring items are ongoing responsibilities that repeat on a schedule. They are Areas (ongoing responsibilities), not Projects (time-bound). Tracked in `areas/recurring.md`.

**Structure of a recurring item:**
- Frequency (e.g., every 2 weeks, monthly)
- Next occurrence date
- Prep lead time (how far in advance a reminder is needed)
- Category (work/personal)

**Behaviors:**

1. **Prep tasks:** When a recurring item's prep window arrives, create a task in `areas/tasks.md` with the prep due date. Mark it with context linking to the recurring item.

2. **After each occurrence:**
   - Update the "next occurrence" date in `areas/recurring.md`
   - Create the next prep task
   - Keep the upcoming dates table current (show next 3 occurrences)

3. **In "what's coming up" queries:**
   - Check `areas/recurring.md` for items occurring this week or next
   - Flag if prep is overdue or due soon
   - Include in the response alongside tasks and follow-ups

4. **When a recurring item is completed:**
   - Mark the current prep task complete
   - Prompt: "Should I add the prep task for the next occurrence on [date]?"
