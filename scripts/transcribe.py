#!/usr/bin/env python3
"""
transcribe.py

Finds unprocessed Voice Memo recordings, transcribes them with mlx-whisper
(Apple Silicon GPU) and optionally diarizes with Sortformer via mlx-audio.

Output goes to inbox/transcripts/ as a single .txt file with a header block,
ready for process-interaction to pick up.

Usage:
    python3 transcribe.py              # process all new recordings
    python3 transcribe.py --limit 3    # process only first 3 new recordings
    python3 transcribe.py --list       # show what's been processed
    python3 transcribe.py --reprocess  # reprocess the latest recording
    python3 transcribe.py --reprocess --all  # reprocess everything
    python3 transcribe.py --no-diarize # skip speaker diarization
    python3 transcribe.py /path/to/file.m4a  # process a specific file

Requires:
    - mlx-whisper and mlx-audio installed in ~/.whisperx-env
    - HF_TOKEN environment variable (for speaker diarization model download)
"""

import os
import sys
import json
import time
import logging
import traceback
from pathlib import Path
from datetime import datetime

# --- Load .env from project root ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

# --- Configuration ---
RECORDINGS_DIR = PROJECT_ROOT / "inbox/recordings"
OUTPUT_DIR = PROJECT_ROOT / "inbox/transcripts"
LOG_FILE = PROJECT_ROOT / "inbox/transcribed.log"
PID_FILE = PROJECT_ROOT / "inbox/.transcribe.pid"
TRANSCRIBE_LOG = PROJECT_ROOT / "inbox/transcription-logger-output.log"
VENV_PYTHON = Path.home() / ".whisperx-env/bin/python"
MODEL = os.environ.get("WHISPER_MODEL", "mlx-community/whisper-medium-mlx")

# --- Logging setup ---
log = logging.getLogger("transcribe")
log.setLevel(logging.DEBUG)
_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(logging.Formatter("%(message)s"))
log.addHandler(_console)
TRANSCRIBE_LOG.parent.mkdir(parents=True, exist_ok=True)
_file = logging.FileHandler(TRANSCRIBE_LOG)
_file.setLevel(logging.DEBUG)
_file.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
log.addHandler(_file)


def write_pid(total_files=0, total_size_mb=0, total_audio_est_min=0):
    """Write PID file with process info and estimated runtime."""
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    info = {
        "pid": os.getpid(),
        "started_at": datetime.now().isoformat(),
        "total_files": total_files,
        "total_size_mb": round(total_size_mb, 1),
        "est_audio_minutes": round(total_audio_est_min),
        "est_runtime_minutes": round(total_audio_est_min / 2),
    }
    PID_FILE.write_text(json.dumps(info, indent=2) + "\n")


def remove_pid():
    """Remove the PID file."""
    try:
        PID_FILE.unlink(missing_ok=True)
    except OSError:
        pass


def read_pid_info():
    """Read and parse the PID file. Returns dict or None."""
    if not PID_FILE.exists():
        return None
    try:
        return json.loads(PID_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def is_transcribe_running():
    """Check if another transcribe.py process is running via PID file."""
    info = read_pid_info()
    if info is None:
        return False
    try:
        os.kill(info["pid"], 0)
        return True
    except (ProcessNotFoundError, PermissionError, OSError):
        remove_pid()
        return False


def load_log():
    """Load the set of already-processed filenames from the log."""
    if not LOG_FILE.exists():
        return {}
    entries = {}
    for line in LOG_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            entry = json.loads(line)
            entries[entry["source_file"]] = entry
        except (json.JSONDecodeError, KeyError):
            continue
    return entries


def append_log(entry):
    """Append a processed file entry to the log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def get_file_timestamp(filepath):
    """Get the file's modification time as a datetime."""
    return datetime.fromtimestamp(filepath.stat().st_mtime)


AUDIO_EXTENSIONS = {".m4a", ".mp3", ".wav", ".ogg", ".flac", ".webm", ".mp4"}


def find_new_recordings(log):
    """Find audio files in inbox/recordings that haven't been processed yet."""
    if not RECORDINGS_DIR.exists():
        RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
        log.info(f"Created recordings directory: {RECORDINGS_DIR}")

    new_files = []
    for f in sorted(RECORDINGS_DIR.iterdir()):
        if f.suffix.lower() in AUDIO_EXTENSIONS and f.name not in log:
            new_files.append(f)
    return new_files


def transcribe_audio(filepath):
    """Transcribe audio using mlx-whisper. Returns segments with timestamps."""
    import mlx_whisper

    result = mlx_whisper.transcribe(
        str(filepath),
        path_or_hf_repo=MODEL,
        word_timestamps=True,
    )
    return result


def convert_to_wav(filepath):
    """Convert audio file to 16kHz mono wav for diarization."""
    import subprocess
    import tempfile

    wav_path = tempfile.mktemp(suffix=".wav")
    subprocess.run(
        ["ffmpeg", "-i", str(filepath), "-ar", "16000", "-ac", "1", wav_path, "-y"],
        capture_output=True, check=True,
    )
    return wav_path


CHUNK_DURATION = 600  # 10 minutes per chunk
CHUNK_OVERLAP = 60    # 60 seconds overlap between chunks
CHUNK_THRESHOLD = 480  # 8 minutes - files under this are diarized in one pass


def get_wav_duration(wav_path):
    """Get duration of a wav file in seconds."""
    import soundfile as sf
    info = sf.info(wav_path)
    return info.duration


def split_wav_chunks(wav_path, chunk_duration=CHUNK_DURATION, overlap=CHUNK_OVERLAP):
    """Split a wav file into overlapping chunks. Returns list of (chunk_path, offset)."""
    import subprocess
    import tempfile

    duration = get_wav_duration(wav_path)
    if duration <= chunk_duration + overlap:
        return [(wav_path, 0.0)]

    chunks = []
    start = 0.0
    while start < duration:
        end = min(start + chunk_duration + overlap, duration)
        chunk_path = tempfile.mktemp(suffix=".wav")
        subprocess.run(
            ["ffmpeg", "-i", wav_path, "-ss", str(start), "-to", str(end),
             "-ar", "16000", "-ac", "1", chunk_path, "-y"],
            capture_output=True, check=True,
        )
        chunks.append((chunk_path, start))
        start += chunk_duration
        if end >= duration:
            break
    return chunks


def match_speakers_across_chunks(prev_segments, curr_segments, prev_offset, curr_offset, overlap_start, overlap_end):
    """Map speaker IDs from curr chunk to prev chunk's IDs using the overlap region."""
    def speaking_intervals(segments, offset, t_start, t_end):
        totals = {}
        for seg in segments:
            abs_start = seg.start + offset
            abs_end = seg.end + offset
            o_start = max(abs_start, t_start)
            o_end = min(abs_end, t_end)
            if o_start < o_end:
                totals[seg.speaker] = totals.get(seg.speaker, 0) + (o_end - o_start)
        return totals

    prev_totals = speaking_intervals(prev_segments, prev_offset, overlap_start, overlap_end)
    curr_totals = speaking_intervals(curr_segments, curr_offset, overlap_start, overlap_end)

    if not prev_totals or not curr_totals:
        return {}

    mapping = {}
    bin_size = 1.0
    t = overlap_start
    cooccurrence = {}
    while t < overlap_end:
        t_end = min(t + bin_size, overlap_end)
        prev_spk = _dominant_speaker_in_window(prev_segments, prev_offset, t, t_end)
        curr_spk = _dominant_speaker_in_window(curr_segments, curr_offset, t, t_end)
        if prev_spk is not None and curr_spk is not None:
            key = (curr_spk, prev_spk)
            cooccurrence[key] = cooccurrence.get(key, 0) + (t_end - t)
        t += bin_size

    assigned_prev = set()
    sorted_pairs = sorted(cooccurrence.items(), key=lambda x: x[1], reverse=True)
    for (curr_spk, prev_spk), duration in sorted_pairs:
        if curr_spk not in mapping and prev_spk not in assigned_prev:
            mapping[curr_spk] = prev_spk
            assigned_prev.add(prev_spk)

    unmatched_curr = [s for s in curr_totals if s not in mapping]
    unmatched_prev = [s for s in prev_totals if s not in assigned_prev]
    if unmatched_curr and unmatched_prev:
        unmatched_curr.sort(key=lambda s: curr_totals[s], reverse=True)
        unmatched_prev.sort(key=lambda s: prev_totals[s], reverse=True)
        for c, p in zip(unmatched_curr, unmatched_prev):
            mapping[c] = p

    return mapping


def _dominant_speaker_in_window(segments, offset, t_start, t_end):
    """Find which speaker has the most overlap in a time window."""
    totals = {}
    for seg in segments:
        abs_start = seg.start + offset
        abs_end = seg.end + offset
        o_start = max(abs_start, t_start)
        o_end = min(abs_end, t_end)
        if o_start < o_end:
            totals[seg.speaker] = totals.get(seg.speaker, 0) + (o_end - o_start)
    if not totals:
        return None
    return max(totals, key=totals.get)


class UnifiedDiarization:
    """Mimics DiarizationOutput interface with unified segments from chunked diarization."""
    def __init__(self, segments, num_speakers):
        self.segments = segments
        self.num_speakers = num_speakers


class UnifiedSegment:
    """A diarization segment with absolute timestamps and unified speaker ID."""
    def __init__(self, start, end, speaker):
        self.start = start
        self.end = end
        self.speaker = speaker


def _merge_tiny_speakers(segments, min_fraction=0.01):
    """Merge speakers with < min_fraction of total talk time into the nearest real speaker."""
    from collections import defaultdict

    totals = defaultdict(float)
    for seg in segments:
        totals[seg.speaker] += seg.end - seg.start
    total_time = sum(totals.values())
    if total_time == 0:
        return segments

    tiny = {spk for spk, t in totals.items() if t / total_time < min_fraction}
    if not tiny:
        return segments

    real = {spk for spk in totals if spk not in tiny}
    if not real:
        return segments

    real_mids = [(seg, (seg.start + seg.end) / 2) for seg in segments if seg.speaker in real]

    result = []
    for seg in segments:
        if seg.speaker in tiny:
            seg_mid = (seg.start + seg.end) / 2
            nearest = min(real_mids, key=lambda x: abs(x[1] - seg_mid))
            result.append(UnifiedSegment(seg.start, seg.end, nearest[0].speaker))
        else:
            result.append(seg)
    return result


def diarize_audio(filepath):
    """Run Sortformer speaker diarization via mlx-audio (Metal GPU)."""
    from mlx_audio.vad import load

    wav_path = convert_to_wav(filepath)
    try:
        duration = get_wav_duration(wav_path)

        if duration <= CHUNK_THRESHOLD:
            model = load("mlx-community/diar_sortformer_4spk-v1-fp32")
            result = model.generate(wav_path, threshold=0.5, verbose=False)
            if not result.segments:
                return None
            return result

        log.info(f"  Audio is {duration/60:.0f}min, chunking for diarization...")
        chunks = split_wav_chunks(wav_path)
        log.info(f"  Split into {len(chunks)} chunks")

        model = load("mlx-community/diar_sortformer_4spk-v1-fp32")
        chunk_results = []
        chunk_paths_to_clean = []

        for i, (chunk_path, offset) in enumerate(chunks):
            if chunk_path != wav_path:
                chunk_paths_to_clean.append(chunk_path)
            result = model.generate(chunk_path, threshold=0.5, verbose=False)
            chunk_results.append((result, offset))
            log.info(f"    Chunk {i+1}/{len(chunks)} done ({len(result.segments)} segments)")

        for cp in chunk_paths_to_clean:
            if os.path.exists(cp):
                os.unlink(cp)

        all_segments = []
        global_map = {}
        next_global_id = 0

        for chunk_idx, (result, offset) in enumerate(chunk_results):
            if not result.segments:
                continue

            if chunk_idx == 0:
                for seg in result.segments:
                    if seg.speaker not in global_map.get(0, {}):
                        if 0 not in global_map:
                            global_map[0] = {}
                        global_map[0][seg.speaker] = next_global_id
                        next_global_id += 1
                for seg in result.segments:
                    all_segments.append(UnifiedSegment(
                        start=seg.start + offset,
                        end=seg.end + offset,
                        speaker=global_map[0][seg.speaker],
                    ))
            else:
                prev_result, prev_offset = chunk_results[chunk_idx - 1]
                overlap_start = offset
                overlap_end = offset + CHUNK_OVERLAP

                speaker_map = match_speakers_across_chunks(
                    prev_result.segments, result.segments,
                    prev_offset, offset,
                    overlap_start, overlap_end,
                )

                global_map[chunk_idx] = {}
                prev_chunk_global = global_map.get(chunk_idx - 1, {})

                for local_spk in set(seg.speaker for seg in result.segments):
                    if local_spk in speaker_map:
                        prev_local = speaker_map[local_spk]
                        global_map[chunk_idx][local_spk] = prev_chunk_global.get(prev_local, next_global_id)
                        if prev_local not in prev_chunk_global:
                            next_global_id += 1
                    else:
                        global_map[chunk_idx][local_spk] = next_global_id
                        next_global_id += 1

                for seg in result.segments:
                    abs_start = seg.start + offset
                    abs_end = seg.end + offset
                    if abs_start >= overlap_end:
                        all_segments.append(UnifiedSegment(
                            start=abs_start,
                            end=abs_end,
                            speaker=global_map[chunk_idx][seg.speaker],
                        ))
                    elif abs_end > overlap_end:
                        all_segments.append(UnifiedSegment(
                            start=overlap_end,
                            end=abs_end,
                            speaker=global_map[chunk_idx][seg.speaker],
                        ))

        if not all_segments:
            return None

        all_segments = _merge_tiny_speakers(all_segments, min_fraction=0.01)

        num_speakers = len(set(seg.speaker for seg in all_segments))
        log.info(f"  Unified: {len(all_segments)} segments, {num_speakers} speakers")
        return UnifiedDiarization(all_segments, num_speakers)

    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)


def merge_transcript_and_speakers(transcription, diarization):
    """Merge mlx-whisper segments with Sortformer speaker labels."""
    if diarization is None:
        lines = []
        for seg in transcription["segments"]:
            start = format_time(seg["start"])
            end = format_time(seg["end"])
            text = seg["text"].strip()
            lines.append(f"[{start} - {end}] {text}")
        return "\n".join(lines)

    lines = []
    for seg in transcription["segments"]:
        seg_start = seg["start"]
        seg_end = seg["end"]
        text = seg["text"].strip()

        speaker = get_speaker_for_segment(diarization, seg_start, seg_end)
        start_str = format_time(seg_start)
        end_str = format_time(seg_end)

        if speaker is not None:
            lines.append(f"[{start_str} - {end_str}] SPEAKER_{speaker:02d}: {text}")
        else:
            lines.append(f"[{start_str} - {end_str}] {text}")

    return "\n".join(lines)


def get_speaker_for_segment(diarization, seg_start, seg_end):
    """Find which speaker has the most overlap with a transcript segment."""
    overlap = {}
    for dseg in diarization.segments:
        overlap_start = max(seg_start, dseg.start)
        overlap_end = min(seg_end, dseg.end)
        if overlap_start < overlap_end:
            duration = overlap_end - overlap_start
            overlap[dseg.speaker] = overlap.get(dseg.speaker, 0) + duration

    if not overlap:
        return None
    return max(overlap, key=overlap.get)


def format_time(seconds):
    """Format seconds as MM:SS or HH:MM:SS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def format_duration(seconds):
    """Format seconds as human-readable duration."""
    m = int(seconds // 60)
    s = int(seconds % 60)
    if m > 0:
        return f"{m}m {s}s"
    return f"{s}s"


def get_duration_seconds(transcription):
    """Get total audio duration from transcription segments."""
    segments = transcription.get("segments", [])
    if not segments:
        return 0
    return round(segments[-1]["end"])


def build_output(filepath, transcription, diarization):
    """Build the final output: header block + transcript text."""
    timestamp = get_file_timestamp(filepath)
    duration_seconds = get_duration_seconds(transcription)
    speaker_count = diarization.num_speakers if diarization else 0
    diarized = diarization is not None

    header_lines = [
        f"Date: {timestamp.strftime('%Y-%m-%d')}",
        f"Time: {timestamp.strftime('%H:%M')}",
        f"Duration: {format_duration(duration_seconds)}",
        f"Speakers: {speaker_count}" if diarized else "Speakers: unknown (diarization skipped)",
        f"Audio: {filepath}",
        "",
    ]

    transcript_text = merge_transcript_and_speakers(transcription, diarization)

    return "\n".join(header_lines) + "\n" + transcript_text


def transcribe(filepath, do_diarize=True):
    """Full pipeline: transcribe + diarize + merge + save.

    Returns a dict with transcript_path, duration_seconds, speaker_count,
    and diarized flag, or None on failure.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = get_file_timestamp(filepath)
    output_name = f"meeting_{timestamp.strftime('%Y-%m-%d_%H%M')}"
    final_transcript = OUTPUT_DIR / f"{output_name}.txt"

    counter = 1
    while final_transcript.exists():
        final_transcript = OUTPUT_DIR / f"{output_name}_{counter}.txt"
        counter += 1

    # Step 1: Transcribe with mlx-whisper
    t0 = time.time()
    log.info(f"  Transcribing with mlx-whisper ({MODEL.split('/')[-1]})...")
    try:
        transcription = transcribe_audio(filepath)
    except Exception as e:
        log.error(f"  Transcription failed for {filepath.name}: {e}")
        log.debug(traceback.format_exc())
        return None
    t1 = time.time()
    log.info(f"  Transcription done in {t1 - t0:.1f}s")

    duration_seconds = get_duration_seconds(transcription)

    # Step 2: Diarize with Sortformer via mlx-audio (optional)
    diarization = None
    speaker_count = 0
    if do_diarize:
        log.info("  Running speaker diarization (Sortformer/MLX)...")
        try:
            diarization = diarize_audio(filepath)
            t2 = time.time()
            if diarization:
                speaker_count = diarization.num_speakers
                log.info(f"  Diarization done in {t2 - t1:.1f}s ({speaker_count} speakers detected)")
            else:
                t2 = t1
        except Exception as e:
            log.error(f"  Diarization failed for {filepath.name}: {e}")
            log.debug(traceback.format_exc())
            t2 = t1
    else:
        t2 = t1

    # Step 3: Build output with header + transcript and write
    output_text = build_output(filepath, transcription, diarization)
    final_transcript.write_text(output_text)

    total = t2 - t0
    log.info(f"  Total processing time: {total:.1f}s")

    return {
        "transcript_path": final_transcript,
        "duration_seconds": duration_seconds,
        "speaker_count": speaker_count,
        "diarized": diarization is not None,
    }


def process_file(filepath, do_diarize=True):
    """Process a single specific file."""
    filepath = Path(filepath)
    if not filepath.exists():
        log.error(f"File not found: {filepath}")
        return

    size_mb = filepath.stat().st_size / (1024 * 1024)
    est_audio_min = size_mb * 2
    write_pid(total_files=1, total_size_mb=size_mb, total_audio_est_min=est_audio_min)
    try:
        timestamp = get_file_timestamp(filepath)
        log.info(f"[1/1] {filepath.name}")
        log.info(f"  Recorded: {timestamp.strftime('%Y-%m-%d %H:%M')}")
        log.info(f"  Size: {size_mb:.1f} MB")

        result = transcribe(filepath, do_diarize=do_diarize)

        if result:
            entry = {
                "source_file": filepath.name,
                "source_path": str(filepath),
                "transcript": str(result["transcript_path"]),
                "recorded_at": timestamp.isoformat(),
                "processed_at": datetime.now().isoformat(),
                "model": MODEL,
                "diarized": result["diarized"],
            }
            append_log(entry)
            log.info(f"  Saved: {result['transcript_path'].name}")
        else:
            log.error(f"  FAILED: {filepath.name}")

        log.info("Done.")
    finally:
        remove_pid()


def process_all(reprocess=False, limit=None, do_diarize=True):
    """Main processing loop."""
    processed_log = {} if reprocess else load_log()
    if reprocess:
        new_files = sorted(
            [f for f in RECORDINGS_DIR.iterdir() if f.suffix.lower() in AUDIO_EXTENSIONS],
            key=lambda f: f.stat().st_mtime, reverse=True,
        )
    else:
        new_files = find_new_recordings(processed_log)

    if not new_files:
        log.info("No new recordings to process.")
        return

    total = len(new_files)
    if limit:
        new_files = new_files[:limit]

    total_size_mb = sum(f.stat().st_size / (1024 * 1024) for f in new_files)
    est_audio_min = total_size_mb * 2
    write_pid(total_files=len(new_files), total_size_mb=total_size_mb, total_audio_est_min=est_audio_min)
    try:
        if limit:
            log.info(f"Found {total} new recording(s), processing first {len(new_files)}:\n")
        else:
            log.info(f"Found {total} new recording(s):\n")

        for i, filepath in enumerate(new_files, 1):
            timestamp = get_file_timestamp(filepath)
            log.info(f"[{i}/{len(new_files)}] {filepath.name}")
            log.info(f"  Recorded: {timestamp.strftime('%Y-%m-%d %H:%M')}")
            log.info(f"  Size: {filepath.stat().st_size / (1024*1024):.1f} MB")

            result = transcribe(filepath, do_diarize=do_diarize)

            if result:
                entry = {
                    "source_file": filepath.name,
                    "source_path": str(filepath),
                    "transcript": str(result["transcript_path"]),
                    "recorded_at": timestamp.isoformat(),
                    "processed_at": datetime.now().isoformat(),
                    "model": MODEL,
                    "diarized": result["diarized"],
                }
                append_log(entry)
                log.info(f"  Saved: {result['transcript_path'].name}")
            else:
                log.error(f"  FAILED: {filepath.name}")

            log.info("")

        log.info("Done.")
    finally:
        remove_pid()


def list_processed():
    """Show what's been processed."""
    processed_log = load_log()
    if not processed_log:
        print("No recordings have been processed yet.")
        return

    print(f"Processed recordings ({len(processed_log)}):\n")
    for entry in processed_log.values():
        recorded = datetime.fromisoformat(entry["recorded_at"]).strftime("%Y-%m-%d %H:%M")
        transcript = Path(entry["transcript"]).name
        print(f"  {recorded}  ->  {transcript}")


if __name__ == "__main__":
    if "--status" in sys.argv:
        if is_transcribe_running():
            info = read_pid_info()
            started = datetime.fromisoformat(info["started_at"])
            elapsed = (datetime.now() - started).total_seconds() / 60
            print(f"Transcription is running (PID {info['pid']})")
            print(f"  Started: {started.strftime('%H:%M')} ({elapsed:.0f} min ago)")
            print(f"  Files: {info['total_files']} ({info['total_size_mb']} MB)")
            print(f"  Est. audio: ~{info['est_audio_minutes']} min")
            print(f"  Est. runtime: ~{info['est_runtime_minutes']} min")
        else:
            print("Transcription is not running")
        sys.exit(0)

    if not VENV_PYTHON.exists():
        print(f"ERROR: Python venv not found at {VENV_PYTHON}")
        print("Install with:")
        print("  python3 -m venv ~/.whisperx-env")
        print("  ~/.whisperx-env/bin/pip install mlx-whisper soundfile")
        print("  ~/.whisperx-env/bin/pip install git+https://github.com/Blaizzy/mlx-audio.git")
        sys.exit(1)

    if is_transcribe_running():
        info = read_pid_info()
        started = datetime.fromisoformat(info["started_at"])
        elapsed = (datetime.now() - started).total_seconds() / 60
        print(f"ERROR: Transcription is already running (PID {info['pid']}, started {elapsed:.0f} min ago)")
        print("Wait for it to finish, or remove the PID file if it's stale:")
        print(f"  rm {PID_FILE}")
        sys.exit(1)

    limit = None
    if "--limit" in sys.argv:
        try:
            limit = int(sys.argv[sys.argv.index("--limit") + 1])
        except (IndexError, ValueError):
            print("ERROR: --limit requires a number (e.g. --limit 3)")
            sys.exit(1)

    do_diarize = "--no-diarize" not in sys.argv

    file_args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in (str(limit),)]
    specific_file = file_args[0] if file_args else None

    if "--list" in sys.argv:
        list_processed()
    elif specific_file:
        process_file(specific_file, do_diarize=do_diarize)
    elif "--reprocess" in sys.argv:
        if "--all" not in sys.argv and limit is None:
            limit = 1
        process_all(reprocess=True, limit=limit, do_diarize=do_diarize)
    else:
        process_all(limit=limit, do_diarize=do_diarize)
