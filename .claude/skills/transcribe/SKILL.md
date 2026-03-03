---
name: transcribe
description: "Transcribe voice memos — fires off local transcription in the background using Apple Silicon GPU. No audio leaves the machine."
---

# /transcribe - Transcribe Voice Memos

Launches the local transcription script in the background. Uses mlx-whisper on Apple Silicon GPU with Sortformer speaker diarization — all on-device, no audio leaves the machine. When done, run `/process-voicememos` to extract meeting data.

This pipeline is separate from `/process-transcripts` (which handles clipboard-pasted transcripts in `inbox/transcripts/`).

## Trigger

`/transcribe`, "transcribe my meetings", "transcribe voice memos", etc.

**Optional argument:** a number to limit how many recordings to transcribe. E.g., `/transcribe 1` transcribes only the first new recording. Without a number, transcribes all new recordings.

## What to Do

### 1. Show pipeline status

Run these checks and show a one-line summary for each stage:

```bash
~/.whisperx-env/bin/python scripts/transcribe.py --status

ls inbox/transcribed/*.json 2>/dev/null | wc -l

ls inbox/reviews/*.json 2>/dev/null | wc -l
```

Display as:
```
PIPELINE STATUS
  Transcribe: not running (or: running, X files, ~Y min remaining)
  Process: N transcript(s) ready → run /process-voicememos
  Review: N meeting(s) ready → run /review-voicememos
```

If transcription is already running, report that and stop. Don't launch a second instance.

### 2. Launch transcription in background

```bash
~/.whisperx-env/bin/python scripts/transcribe.py [--limit N]
```

Run this with the Bash tool using `run_in_background: true`. Include `--limit N` if a number was specified.

**Timeout:** Set to `600000` (10 min) as a minimum. For large batches, estimate ~30 min per hour of audio on Apple Silicon.

### 3. Report and return immediately

Tell the user:
- Transcription is running in the background
- Rough time estimate based on what was found
- "Run `/process-voicememos` when it's done to extract meeting data, or I'll let you know if I notice it's finished."

**That's it.** Do not poll. Do not wait. Do not try to run `/process-voicememos` — that's a separate step.

## Checking on progress later

If asked "is transcription done?" or "how's the transcription going?":

```bash
~/.whisperx-env/bin/python scripts/transcribe.py --status
```

If not running, check for pending transcripts:
```bash
ls inbox/transcribed/*.json 2>/dev/null | wc -l
```

## Important Notes

- **Fire and forget**: The script writes a PID file (`inbox/.transcribe.pid`) on start and removes it on exit.
- **Don't run /process-voicememos** — that's a separate command.
- **First run** will download models (~60s for whisper + Sortformer), then cached.
