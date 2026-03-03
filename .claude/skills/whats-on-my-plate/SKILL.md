---
name: whats-on-my-plate
description: Show a consolidated view of tasks, follow-ups, and goals due today or this week. Use when asked "what's on my plate", "what do I need to do", "what's due today/this week", "what's coming up", or similar.
argument-hint: "[today|this week|next week] (optional, defaults to today)"
---

## "What's on my plate today?" / "What do I need to do?"

1. **Pull general tasks** from `areas/tasks.md` due today or overdue
2. **Pull project tasks** by:
   - Using Glob to find all `projects/*.md` files
   - Reading each project file
   - Extracting tasks from each project's task table due today or overdue
3. **Pull follow-ups** from `areas/followups.md` due today or overdue
4. **Pull from third-party todo apps** available through MCP servers
5. **Mention any goals** with imminent milestones from `areas/goals.md`
6. **Present consolidated view:**
   ```
   ## Tasks Due Today

   ### General Tasks
   - Task 1
   - Task 2

   ### Project: [Project Name]
   - Project task 1
   - Project task 2

   ### Project: [Another Project]
   - Project task 3

   ## Follow-ups Due Today
   - Follow-up 1
   - Follow-up 2
   ```
7. **Keep it scannable**
8. **Separate work and personal items**
9. **Generate ready-to-send messages:** For any follow-ups where something is needed from people who have contact handles in their `areas/people/` files, provide ready-to-send Slack messages at the end

## "What's coming up this week?" / "What's coming up next week?"

If $ARGUMENTS includes "week" or "next week":

1. **Pull tasks** from both `areas/tasks.md` and all `projects/*.md` files due this/next week
2. **Pull follow-ups** from `areas/followups.md` for the week
3. **Check recurring items** from `areas/recurring.md` that fall in this window
4. **Any scheduled milestones** from `areas/goals.md`
5. **Flag if prep is overdue or coming due** for recurring items
6. **Flag anything** that looks at risk
