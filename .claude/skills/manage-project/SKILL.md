---
name: manage-project
description: Make sure to use this skill whenever the user discusses projects, wants to create a new project, or asks about project statuses (e.g., "what's the status on [project]?", "what projects am I driving?", or when a new initiative needs tracking), even if they don't explicitly ask to use the skill.
---

## What is a project?

Projects are tactical initiatives being personally driven that have a clear objective, deadline, and multiple moving pieces. They differ from:
- **Areas** - ongoing responsibilities without end dates
- **Tasks** - single discrete actions
- **Follow-ups** - things others committed to

A project has an objective, background context, key people, a task list, and a next action. Each project is stored in its own folder in `projects/`.

## When to create a project:

- Something with multiple steps and people involved is being driven
- It has a clear "done" state and deadline (not an ongoing responsibility — that would be an Area)
- There's enough complexity that context would be lost without a dedicated place to track it

## Project file structure

Every project file should have these sections. The goal is that someone (or a future session) can read the file cold and understand what this project is, why it matters, where things stand, and what happens next.

```markdown
# Project Name

**Objective:** One sentence — what does "done" look like?
**Why it matters:** Why this exists. What happens if it doesn't get done?
**Due:** Target date or timeframe
**Current situation:** 2-3 sentences on where things stand right now. Updated regularly.

## Key People

| Role | Person | Notes |
|------|--------|-------|
| Owner | [Name](path) | Why they're involved |
| Stakeholder | [Name](path) | Their interest or responsibility |

## Tasks

| Due Date | Task | Owner | Status | Context |
|----------|------|-------|--------|---------|
| YYYY-MM-DD | Specific action | Person | pending/done | Why this matters or what it unblocks |

**Next action:** The single most important thing that needs to happen next.
```

Key principles:
- "Current situation" is the most frequently updated section — keep it fresh
- Tasks live here (not in `areas/tasks.md`) because they're project-scoped
- "Next action" forces clarity on what's actually blocking progress
- Key People should include anyone whose actions affect the project, with enough context that you'd know why to contact them

## When a project is mentioned:

1. **Check if it exists** in `projects/` by using Glob to find `projects/*/` directories
2. **If new:** Create `projects/[project-name]/[project-name].md` with:
   - Objective, why it matters, background, key people
   - Empty task table for project-specific tasks
   - Next action
   - Also create `projects/[project-name]/transcripts/` directory
3. **If existing:** Read `projects/[project-name]/[project-name].md`, update status, add new context, update tasks
4. **Cross-reference:**
   - Add an index row to `areas/interactions.md`; put meeting notes/decisions in the project's main file
   - Add follow-ups to `areas/followups.md` with project tag
   - Add project-specific tasks to the project's own task table (not `areas/tasks.md`)

## Project status updates:

When progress on a project is reported:
- Update the relevant tasks and status in the project's main file
- Add new tasks to the project's task table as needed
- Add an index row to `areas/interactions.md`
- If project is complete, move the entire folder from `projects/` to `archive/projects/` with outcome summary added to top of main file

## "What's the status on [project]?" / "Where are we with [project]?"

- Find and read the project file from `projects/[project-name].md`
- Summarize current situation and tasks
- Show any related follow-ups from `areas/followups.md` that are overdue or upcoming
- Surface the next action

## "What projects am I driving?"

- Use Glob to find all files in `projects/`
- Read each project file
- List active projects with current status
- Flag any with overdue tasks or stalled progress
- Highlight next actions
