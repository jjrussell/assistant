---
name: process-interaction
description: Make sure to use this skill whenever the user says "process transcripts", "process inbox", or reports any interaction (e.g., "just talked to...", "had a meeting with...", "quick update...", "FYI..."). This handles meeting transcripts, Slack threads, Google Docs, or conversational reports.
---

# Process Interaction

This skill has two paths depending on where the input comes from. The key design decision: file-based input (transcripts, URLs) gets delegated to a subagent so large file contents don't consume the main conversation's context. Conversational input stays in the main conversation since it's already here and small.

## Path A: File-based input (inbox/transcripts/)

For each file in `inbox/transcripts/`, spawn a subagent using the Agent tool:

1. Read `agents/extractor.md` from this skill's directory
2. For each inbox file, spawn a subagent with this prompt:

```
You are an interaction extractor. Follow the instructions in {skill_dir}/agents/extractor.md.

Process this file: {file_path}
Skill directory: {skill_dir}
Working directory: {working_dir}
Today's date: {date}
```

3. If there are multiple files, spawn subagents in parallel (one per file) using background mode
4. As each subagent completes, collect its structured summary
5. Present each summary to the user following logging mode behavior (see below)
6. **Move transcripts immediately after presenting each summary.** Don't wait for flag resolution — move as soon as you present the summary, unless the `FILED TO:` destination itself is flagged as ambiguous. Use `scripts/move-transcript.sh` to move or delete files:
   - Move: `./.claude/skills/process-interaction/scripts/move-transcript.sh move <source> <dest-dir>`
   - Delete (duplicates): `./.claude/skills/process-interaction/scripts/move-transcript.sh delete <source>`

**For filing ambiguities** (subagent flagged destination as uncertain): present to the user and wait for a response before moving.

**For new people** flagged by the subagent: ask for enough context to create their file, then create it. This does NOT block the transcript move.

**For other flags** (observations, questions): present them but don't block on them. The user can engage or dismiss.

## Path B: Conversational input

The user reports something in chat — "just talked to Lisa about X", "had a meeting with the team", "quick update: Davis agreed to...". Handle this inline since the content is already in context and typically small.

### Extraction steps (inline)

1. **Identify:** Who, what type, approximate date
2. **Extract and file** (all entity mentions as `[Name](path)` links):
   - Tasks you committed to → `areas/tasks.md` or relevant project file
   - Follow-ups others committed to → `areas/followups.md`
   - Key observations about people → their `[person].md`
   - Project decisions → relevant project file
   - Log the interaction → `areas/interactions.md` (index row only)
3. **Update person context** — add observations to person files
4. **Historical notes** — if substantive enough, add to the relevant `historical-notes.md`
5. **Performance evidence** — for direct reports, watch for notable behavior (cross-team leadership, proactive problem-solving, coaching). Tag as `[perf-evidence: PersonName]` in their file.

For brief updates ("quick update: Lisa agreed to do X by Friday"), extraction alone is sufficient — skip historical notes.

### Task format
`| Due Date | Task | For | Context | Related Goal | Category | Status |`

### Follow-up format
`| Due Date | Person | What | Context | Related Goal | Category | Status |`

### Date handling
Resolve fuzzy dates to specific weekdays (YYYY-MM-DD). Saturday → Monday, Sunday → Monday.

## Behavior mode

Follow **logging mode**:
- First do the job — log the interaction, extract tasks and follow-ups, confirm what was captured
- Then offer 2-3 observations max (connections to goals, suggested follow-ups, patterns)
- Make closure easy — "good" or "that's it" ends the interaction
- Don't interrogate, don't require engagement with suggestions

**Multiple inbox items:** Process in parallel via subagents, then present summaries one at a time. Confirm each before moving to the next.

## Context file

`context.md` in this skill directory contains meeting type patterns and filing rules specific to the work environment. The subagent reads it directly. For Path B, read it yourself if the interaction matches a recurring meeting type.

## Script location

`scripts/save-transcript.sh` — reads clipboard, saves to `inbox/transcripts/YYYY-MM-DD-HHMMSS.txt`.
