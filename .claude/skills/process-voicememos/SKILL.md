---
name: process-voicememos
description: "Make sure to use this skill whenever the user asks to process transcribed voice memos, extract summaries, tasks, or follow-ups from them. Trigger this to prepare meetings for review."
---

# /process-voicememos - Process Transcribed Voice Memos

Reads pending transcripts from `inbox/transcribed/`, extracts summaries and action items, and writes review files to `inbox/reviews/`.

This is separate from `/process-transcripts` (which handles clipboard-pasted transcripts in `inbox/transcripts/`).

## Trigger

`/process-voicememos`, "process voice memos", etc.

**Optional argument:** a number to limit how many transcripts to process.

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
  Process: N transcript(s) ready ← you are here
  Review: N meeting(s) ready → run /review-voicememos
```

### 2. Find pending transcripts

Read all `.json` files in `inbox/transcribed/`. Every file here is pending — completed files get archived out of this directory. Sort by `recorded_at` ascending (oldest first).

If a limit was specified, take only the first N.

If none found and transcription is running: "Transcription is still in progress. No completed transcripts to process yet — try again shortly." Stop.

If none found and transcription is not running: "No pending transcripts to process." Stop.

### 3. For each pending transcript

#### a. Read the transcript

Read the `.txt` file referenced in `transcript_path` from the metadata JSON.

#### b. Identify people

Check `areas/people/` for known people. Try to match SPEAKER_XX labels to known people based on:
- Conversational context (names mentioned, topics discussed)
- Relationship context from person files
- The number of speakers detected vs. expected meeting size

#### c. Summarize and extract

From the transcript text:

- **Meeting title**: infer from content (topic, participants)
- **People involved**: from speaker identification. Map SPEAKER_XX to real names where possible.
- **Date**: from `recorded_at` in the metadata
- **Category**: infer (1on1, team, cross-functional, external, etc.)
- **Summary**: 1-2 sentence overview
- **Key points**: 3-6 bullet points of what was discussed/decided
- **Proposed tasks**: things the user committed to doing. Include:
  - `description`: what needs to be done
  - `due`: date if mentioned or inferrable, otherwise null
  - `trigger`: "date" or "conversation"
- **Proposed follow-ups**: things others committed to doing. Include:
  - `description`: what the person committed to
  - `person`: who owns it
  - `trigger`: "date" or "conversation"
- **Questions**: anything ambiguous that needs human input:
  - Unidentified speakers (SPEAKER_01, etc.)
  - Unclear project/goal connections
  - Ambiguous commitments

#### d. Write review file

Write to `inbox/reviews/` using the same base name as the transcript:
```
inbox/reviews/meeting_2026-02-11_1135.json
```

Structure:
```json
{
  "transcript_path": "inbox/transcribed/meeting_2026-02-11_1135.txt",
  "metadata_path": "inbox/transcribed/meeting_2026-02-11_1135.json",
  "source_path": "/path/to/original/recording.m4a",
  "recorded_at": "2026-02-11T11:35:00",
  "duration_seconds": 1800,
  "proposed": {
    "title": "Product Team Sync",
    "people": ["Sarah", "Noah"],
    "date": "2026-02-11",
    "category": "team",
    "summary": "Discussed roadmap priorities...",
    "key_points": "- Point one\n- Point two",
    "tasks": [
      {"description": "Review demo prep", "due": "2026-02-13", "trigger": "date"}
    ],
    "follow_ups": [
      {"description": "Send updated timeline", "person": "Sarah", "trigger": "conversation"}
    ]
  },
  "questions": [
    "SPEAKER_01 couldn't be identified — was anyone else in this meeting?"
  ]
}
```

### 4. Report results

After all files are processed:
- How many meetings were processed
- Brief one-line summary of each (title/people/date)
- If transcription is still running: "Transcription is still in progress — more recordings may be coming. Run `/process-voicememos` again when it finishes."
- "Run `/review-voicememos` to review and save them."

## Important Notes

- **No logging yet** — that happens in `/review-voicememos` after the user confirms.
- **Parallel processing**: If multiple transcripts are pending, process them in parallel using Task agents.
- The transcript stays in `inbox/transcribed/` until `/review-voicememos` archives it.
