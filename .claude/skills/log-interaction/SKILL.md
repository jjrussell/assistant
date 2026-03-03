---
name: log-interaction
description: Log a reported interaction (conversation, meeting, decision). Auto-invoked when user reports something that happened — "just talked to...", "had a meeting with...", "quick update...", "FYI...", or any past-tense description of an interaction.
---

## When an interaction is reported:

1. **Add an index entry to `areas/interactions.md`:**
   - One row in the table: date, person/group, type, 3-5 word topic summary
   - `areas/interactions.md` is a pure index — no notes or detail ever go here
   - All notes fan out to the appropriate project or area file:
     - **1:1 / person meeting** → person's file under Recent Observations
     - **Project meeting** → project file (status, decisions, tasks)
     - **Meeting touching multiple topics** → fan out notes to each relevant project or area file
   - **If there's no clear home for a set of notes, ask** — this signals a missing project file or area file, not a reason to put notes in the index

2. **Extract follow-ups to `areas/followups.md`:**
   - Things OTHER people committed to
   - Include: person, what, due date, context

3. **Extract tasks:**
   - Things YOU committed to
   - **If project-related:** Add to that project's task table in `projects/[project-name].md`
   - **If general/administrative:** Add to `areas/tasks.md`
   - Include: task, for whom, due date, context

4. **Update person context:**
   - Check if the person has a file in `areas/people/`; if not, create one
   - Add any relevant context, notes, or observations to their file
   - Don't belabor this; just capture it

## Remember logging mode behavior:

- First do the job, then offer 2-3 observations max
- Make closure easy — "good" or "that's it" ends it
- Don't interrogate, don't require engagement with suggestions

## Work-Specific: Performance Evidence

When logging interactions involving direct reports:

- If a direct report did something notable (good or needs work), note it in their file and in `areas/goals.md` under Development Goals
- Tag strong observations with `[perf-evidence: PersonName]`

### What qualifies as perf evidence:
- Cross-team or cross-role leadership (stepping in beyond their scope)
- Proactive problem-solving without being asked
- Strong feedback delivery or coaching of peers
- Concrete examples of a stated strength or growth area playing out
- Patterns of behavior — good or bad — observed over multiple incidents

### Where to write it:
- `areas/people/[person]/[person].md` — under Recent Observations, tagged `[perf-evidence: PersonName]`
- `areas/people/[person]/historical-notes.md` — in the relevant meeting section

Include: what happened, why it's notable, what it demonstrates about the person. Specificity is what makes perf evidence useful — vague praise is useless at review time.
