---
name: transcribe
description: Make sure to use this skill whenever the user asks to transcribe, transcribe meetings, or transcribe voice memos. Use this skill to securely launch local transcription in the background on Apple Silicon.
---

# /transcribe - Transcribe Voice Memos

Launches the local transcription script in the background. Uses mlx-whisper on Apple Silicon GPU with Sortformer speaker diarization -- all on-device, no audio leaves the machine.

**Input:** Picks up audio files from `inbox/recordings/` (m4a, mp3, wav, ogg, flac, webm, mp4). Drop recordings there from Voice Memos, Zoom, or any source.

**Output:** Writes `.txt` files to `inbox/transcripts/` with a header (date, time, duration, speakers, audio path) followed by the transcript. This is the same inbox that `/process-interaction` reads from, so after transcription finishes you just run "process transcripts" as usual.

## Trigger

`/transcribe`, "transcribe my meetings", "transcribe voice memos", etc.

**Optional argument:** a number to limit how many recordings to transcribe. E.g., `/transcribe 1` transcribes only the first new recording. Without a number, transcribes all new recordings.

## What to Do

### 1. Check status

```bash
~/.whisperx-env/bin/python scripts/transcribe.py --status
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
- "Run 'process transcripts' when it's done, or I'll let you know if I notice it's finished."

**That's it.** Do not poll. Do not wait.

## Checking on progress later

If asked "is transcription done?" or "how's the transcription going?":

```bash
~/.whisperx-env/bin/python scripts/transcribe.py --status
```

If not running, check for pending transcripts:
```bash
ls inbox/transcripts/*.txt 2>/dev/null | wc -l
```

## Important Notes

- **Fire and forget**: The script writes a PID file (`inbox/.transcribe.pid`) on start and removes it on exit.
- **First run** will download models (~60s for whisper + Sortformer), then cached.
- **Dedup**: `inbox/transcribed.log` tracks which Voice Memo files have already been processed, so re-running is safe.
