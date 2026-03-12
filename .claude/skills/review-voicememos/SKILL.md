---
name: review-voicememos
description: Make sure to use this skill whenever the user asks to review voice memos or processed meetings. Also trigger when the user says "what meetings are ready", "anything to review", asks about the voice memo pipeline status, or when inbox/reviews/ has pending files. Use this to confirm or edit summaries and save them to work memory.
---

# /review-voicememos - Review Processed Voice Memo Meetings

Interactive review step. Confirm or adjust extracted meeting data before saving to the memory system.

Final step of the voice memo pipeline: `/transcribe` → `/process-voicememos` → `/review-voicememos`

This is separate from `/process-transcripts` (which handles clipboard-pasted transcripts).

## Trigger

`/review-voicememos`, "review voice memos", "review voice memo meetings", etc.

## What to Do

### 1. Show pipeline status

```bash
~/.whisperx-env/bin/python scripts/transcribe.py --status

ls inbox/transcribed/*.json 2>/dev/null | wc -l

ls inbox/reviews/*.json 2>/dev/null | wc -l
```

Display as:
```
PIPELINE STATUS
  Transcribe: not running
  Process: 0 pending
  Review: N meeting(s) ready ← you are here
```

### 2. Find pending reviews

Read all `.json` files in `inbox/reviews/`. Every file here is pending.

If none found: "No meetings to review. Run `/process-voicememos` first if you have pending transcripts." Stop.

### 3. Present each meeting for review

For each review file, present a concise summary:

```
### Meeting: Product Team Sync
**Date:** 2026-02-11  |  **People:** Sarah, Noah
**Status:** NEW — not yet in work memory

**Summary:** Discussed roadmap priorities...

**Key points:**
- Point one
- Point two

**Proposed tasks (for you):**
- [ ] Review demo prep (due Feb 13)

**Proposed follow-ups (for others):**
- [ ] Sarah: Send updated timeline (conversation trigger)

**Questions:**
- SPEAKER_01 couldn't be identified — was anyone else in this meeting?
```

Then offer options:
- **Save** — log everything as-is
- **Edit** — provide corrections, then save
- **Skip** — leave for later

### 4. On Save

Execute these steps in order:

#### a. Log the interaction

Add a row to `areas/interactions.md`:
```
| YYYY-MM-DD | Person/Group | Type | Topics |
```

Fan out notes to the appropriate files per the memory system rules:
- **1:1 / person meeting** → person's file under Recent Observations
- **Project meeting** → project file (status, decisions, tasks)
- **Meeting touching multiple topics** → fan out to each relevant project or area file

#### b. Extract tasks

Things the user committed to → `areas/tasks.md` or the relevant project file.

Format: `| Due Date | Task | For | Context | Related Goal | Category | Status |`

- Use `pending` status
- Resolve fuzzy dates to specific weekdays (YYYY-MM-DD)
- Connect to related goals where applicable

#### c. Extract follow-ups

Things others committed to → `areas/followups.md`.

Format: `| Due Date | Person | What | Context | Related Goal | Category | Status |`

#### d. Update person context

- Check if each person has a file in `areas/people/`
- Add relevant observations to their Recent Observations section
- If a person is new, ask for enough context to create their file

#### e. Write permanent transcript

Use `build_transcript.py` to create the final `.md` file:

```bash
python scripts/build_transcript.py \
  "<destination_path>" \
  "inbox/transcribed/<raw-transcript>.txt" \
  --title "Meeting Title" \
  --date "YYYY-MM-DD" \
  --time "HH:MM" \
  --people "Person1, Person2" \
  --primary "Person1" \
  --summary "- Key point one\n- Key point two" \
  --audio "/path/to/original/recording.m4a"
```

Transcript destination follows existing conventions:
- **1:1:** `areas/people/[person]/transcripts/YYYY-MM-DD-1on1.md`
- **Project meeting:** `projects/[project-name]/transcripts/YYYY-MM-DD-[description].md`
- **Area meeting:** `areas/[area-name]/transcripts/YYYY-MM-DD-[description].md`
- **Multiple areas/projects:** file under primary, note in interactions where notes fanned out

The `--audio` path comes from `source_path` in the review JSON — the original Voice Memo recording (never deleted or copied).

Use `\n` in the `--summary` argument to separate bullet points — the script decodes them.

#### f. Add summary to historical-notes.md

Location matches the transcript destination:
- **1:1:** `areas/people/[person]/historical-notes.md`
- **Project:** `projects/[project-name]/historical-notes.md`
- **Area:** `areas/[area-name]/historical-notes.md`

Create the file if it doesn't exist. Format:

```markdown
### YYYY-MM-DD — [Meeting type or title]

- **Topic 1**
  - Detail or key point
- **Topic 2**
  - Detail
- **Action items**
  - You: do X
  - Person: do Y
```

#### g. Archive working files

```bash
mv inbox/transcribed/<name>.txt inbox/archive/
mv inbox/transcribed/<name>.json inbox/archive/
mv inbox/reviews/<name>.json inbox/archive/
```

This keeps `inbox/transcribed/` and `inbox/reviews/` clean — only pending files remain. Original Voice Memo recordings are untouched.

### 5. On Edit

User provides corrections (wrong people, adjusted tasks, rephrased points, answers to questions). Apply the edits, re-present the updated summary, then save as above.

### 6. On Skip

Leave the review file untouched. Move to the next meeting.

### 7. After all reviews

Report: "Saved X of Y meetings. Z skipped (still pending review)."

## Important Notes

- **One at a time**: Present meetings sequentially.
- **Be concise**: `/process-voicememos` did the heavy lifting. This should be fast.
- **Questions section**: Present unresolved questions before Save/Edit/Skip. Incorporate answers before saving.
- Move working files to `inbox/archive/` instead of deleting them. This preserves the history in case the user needs to refer back to the intermediate processing steps.
- Preserve original Voice Memo recordings to ensure no source audio is ever lost.
- This pipeline is separate from `/process-transcripts`. Both can coexist.
