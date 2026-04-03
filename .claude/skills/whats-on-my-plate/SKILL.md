---
name: whats-on-my-plate
description: Make sure to use this skill whenever the user asks "what's on my plate", "what do I need to do", "what's due today/this week", or "what's coming up". Use it to show a consolidated view of their tasks, follow-ups, and goals.
argument-hint: "[today|this week|next week] (optional, defaults to today)"
---

## "What's on my plate today?" / "What do I need to do?"

### Step 0: Check for existing plate files

Before gathering fresh data, check `outbox/` for any existing `plate-*.md` files (today's or previous days').

**If an existing plate file is found:**
1. Read the file
2. Look for checked items (`- [x]`) and any notes the user added (text the user typed below items, or items they modified)
3. **Process completed items** - for each checked-off item:
   - If it's a task: mark it complete in `areas/tasks.md` or the relevant project file, and move to `archive/completed.md`
   - If it's a follow-up: mark it complete in `areas/followups.md` and move to `archive/completed.md`
   - If it's a recurring item: update next occurrence in `areas/recurring.md`
   - If the user added notes to an item: incorporate those notes into the relevant file (person file, project file, etc.)
4. **Process user-added items** - if the user added new unchecked items (`- [ ]`) that don't exist in the system, create them in the appropriate file (tasks.md, followups.md, or project file)
5. **Carry forward unchecked items** - items left unchecked from a previous day should be treated as still open (they'll naturally appear again when you gather fresh data)
6. Delete the old plate file after processing (the new one will replace it)
7. Tell the user what you processed: "Processed plate from [date]: marked N items complete, carried forward M items, incorporated notes on X."

**If no plate file exists**, proceed directly to Step 1.

### Step 1: Gather everything

1. **Pull general tasks** from `areas/tasks.md` due today or overdue
2. **Pull project tasks** by:
   - Using Glob to find all `projects/*.md` files
   - Reading each project file
   - Extracting tasks from each project's task table due today or overdue
3. **Pull follow-ups** from `areas/followups.md` due today or overdue
4. **Mention any goals** with imminent milestones from `areas/goals.md`
5. **Check recurring items** from `areas/recurring.md` due today

### Step 2: Enrich each item with actionable context

The goal is to leave a **thread to pull** on every task -- a link, a draft message, a concrete next step. The user should be able to look at any item and immediately start acting on it without having to go find things first.

**First, carry forward everything already in the source data.** The Context columns in `tasks.md`, `followups.md`, and project task tables often already contain Google Doc links, Slack thread URLs, Loom links, Figma links, and other references. **These MUST appear on the plate item.** Do not summarize away a URL that exists in the source -- surface it. This is the most common and most valuable form of enrichment.

**Then, use available tools** (Slack search, Glean, person file contact info) to fill gaps:
- **Draft Slack messages** with @handles for items requiring outreach
- **Links to relevant Slack threads** where the topic was last discussed
- **Links to documents**, PRs, Google Docs, or Confluence pages not already in the context
- **Loom links** if a video needs to be watched
- **Suggested wording** for responses or feedback
- **Person context** - pull from their person file (Slack handle, recent observations) to inform drafts
- If the item is self-contained (e.g., "write the design doc") and has no links in the source, no extra context needed - don't force it

### Step 3: Write the output file

Write the consolidated view to `outbox/plate-YYYY-MM-DD.md` (using today's date). Any existing plate file will have already been processed and removed in Step 0.

**Use Obsidian-compatible checkboxes** (`- [ ]`) so the user can check items off during the day. Nest supporting context under each checkbox as indented body text (not as sub-checkboxes).

**File format:**

```markdown
# What's on my plate - YYYY-MM-DD

## Tasks

### General
- [ ] **Task description** (due: date | overdue from: date)
  Context or background for this task.
  → Draft message: "Hey @person, ..."
  → [Link to relevant doc/thread](url)

### Project: [Project Name]
- [ ] **Task description** (owner: person | due: date)
  → [Actionable next step or link]

## Follow-ups (waiting on others)
- [ ] **What** - waiting on [Person](path) (due: date)
  Last discussed: [link to Slack thread or date of last nudge]
  → Draft nudge: "Hey @handle, following up on [thing] - any update?"
  Nudge history: [if applicable, list prior nudge dates]

## Recurring
- [ ] **Item** (due: date | frequency)
  Prep needed: [what prep is required]

## Goals check-in
- **Goal name**: [status or upcoming milestone]

---

*Check items off as you complete them during the day. At EOD, ask Claude to process this file to update tasks, follow-ups, and interactions.*
```

### Step 4: Confirm to the user

After writing the file, tell the user:
- The file path (so they can open it in Obsidian)
- A brief summary of what's on the list (count of tasks, follow-ups, etc.)
- Remind them to ask you to process the file at end of day

**Keep work and personal items in separate sections** if both exist.

## "What's coming up this week?" / "What's coming up next week?"

If $ARGUMENTS includes "week" or "next week":

1. **Pull tasks** from both `areas/tasks.md` and all `projects/*.md` files due this/next week
2. **Pull follow-ups** from `areas/followups.md` for the week
3. **Check recurring items** from `areas/recurring.md` that fall in this window
4. **Any scheduled milestones** from `areas/goals.md`
5. **Flag if prep is overdue or coming due** for recurring items
6. **Flag anything** that looks at risk
7. **Write to `outbox/plate-YYYY-MM-DD.md`** using the same checkbox format, grouped by day
8. **Enrich each item** with the same actionable context as the daily view
