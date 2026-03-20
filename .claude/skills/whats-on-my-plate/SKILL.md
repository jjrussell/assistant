---
name: whats-on-my-plate
description: Make sure to use this skill whenever the user asks "what's on my plate", "what do I need to do", "what's due today/this week", or "what's coming up". Use it to show a consolidated view of their tasks, follow-ups, and goals.
argument-hint: "[today|this week|next week] (optional, defaults to today)"
---

## "What's on my plate today?" / "What do I need to do?"

1. **Pull general tasks** from `areas/tasks.md` due today or overdue
2. **Pull project tasks** by:
   - Using Glob to find all `projects/*.md` files
   - Reading each project file
   - Extracting tasks from each project's task table due today or overdue
3. **Pull follow-ups** from `areas/followups.md` due today or overdue
4. **Mention any goals** with imminent milestones from `areas/goals.md`
6. **Present consolidated view with actionable next steps** (see "Make items actionable" principle in CLAUDE.md):
   ```
   ## Tasks Due Today

   ### General Tasks
   - Task 1
     → [Draft message / link to doc or Slack thread / concrete next step]
   - Task 2
     → [Draft message / link / suggested action]

   ### Project: [Project Name]
   - Project task 1
     → [Actionable next step]

   ## Follow-ups Due Today
   - Follow-up 1 (from Person)
     → Draft nudge: "Hey @person, following up on [thing] — any update?"
   - Follow-up 2
     → [Link to relevant thread or doc]
   ```

   For each item, use available tools (Slack search, Glean, person file contact info) to provide:
   - Draft Slack messages with @handles for items requiring outreach
   - Links to relevant documents, PRs, or Slack threads
   - Suggested wording for responses or feedback
   - If the item is self-contained (e.g., "write the design doc"), no extra context needed — don't force it

7. **Keep it scannable**
8. **Separate work and personal items**

## "What's coming up this week?" / "What's coming up next week?"

If $ARGUMENTS includes "week" or "next week":

1. **Pull tasks** from both `areas/tasks.md` and all `projects/*.md` files due this/next week
2. **Pull follow-ups** from `areas/followups.md` for the week
3. **Check recurring items** from `areas/recurring.md` that fall in this window
4. **Any scheduled milestones** from `areas/goals.md`
5. **Flag if prep is overdue or coming due** for recurring items
6. **Flag anything** that looks at risk
