---
name: whats-on-my-plate
description: Show a consolidated view of tasks, follow-ups, and goals due today or this week. Use when asked "what's on my plate", "what do I need to do", or "what's due today/this week".
argument-hint: "[today|this week|next week] (optional, defaults to today)"
---

Follow the query behavior defined in CLAUDE.md for "What's on my plate today?" — or if $ARGUMENTS includes "week", use the "What's coming up this week?" behavior instead.

Pull tasks from both `areas/tasks.md`, all `projects/*.md` files, and any third party todo apps available through MCP servers. Include follow-ups and any recurring items in scope. Separate work and personal items. Generate Slack messages for any follow-ups where something is needed from internal people.
