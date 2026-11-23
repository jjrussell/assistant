#!/usr/bin/env python3
"""Import Superwhisper meeting recordings into inbox/transcripts/.

Only recordings with kind == "meeting" are imported; dictation is ignored.
Interviews are skipped. A recording counts as already imported if its
"Superwhisper ID" header line appears in any .txt file in the memory system,
so filed transcripts keep deduplicating after they leave the inbox.

Usage:
  scripts/import-superwhisper.py            # import new meetings
  scripts/import-superwhisper.py --dry-run  # show what would be imported
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
INBOX = PROJECT_DIR / "inbox" / "transcripts"
SEARCH_DIRS = ["inbox", "areas", "projects", "resources", "archive"]
PEOPLE_DIR = PROJECT_DIR / "areas" / "people"
SELF_USERNAME = "jorussell"
ID_MARKER = "Superwhisper ID:"
INTERVIEW_PATTERN = re.compile(r"\binterview\b", re.IGNORECASE)
GENERIC_SPEAKER = re.compile(r"^Speaker \d+$")
MIN_AGE_SECONDS = 120
CHANNEL_LABELS = {"mic": "John's mic", "sys": "call audio"}


def recordings_dir():
    try:
        base = subprocess.run(
            ["defaults", "read", "com.superduper.superwhisper", "appFolderDirectory"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        base = str(Path.home() / "Documents")
    return Path(base) / "superwhisper" / "recordings"


def already_imported_ids():
    ids = set()
    pattern = re.compile(re.escape(ID_MARKER) + r"\s*(\d+)")
    for d in SEARCH_DIRS:
        for f in (PROJECT_DIR / d).rglob("*.txt"):
            try:
                with f.open(errors="ignore") as fh:
                    head = fh.read(4000)
            except OSError:
                continue
            ids.update(pattern.findall(head))
    return ids


def load_people():
    """Map email usernames and display names to person names from people files.

    Usernames come from emails written in person files, plus first-initial +
    last-name style guesses from the directory slug (davis-mastin -> dmastin).
    """
    by_email, by_name = {SELF_USERNAME: "John Russell"}, {}
    email_re = re.compile(r"[\w.+-]+@hubspot\.com", re.IGNORECASE)
    for person_dir in PEOPLE_DIR.glob("*/"):
        main = person_dir / f"{person_dir.name}.md"
        if not main.exists():
            continue
        text = main.read_text(errors="ignore")
        heading = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        name = heading.group(1).strip() if heading else person_dir.name.replace("-", " ").title()
        by_name[person_dir.name.replace("-", " ")] = name
        for email in email_re.findall(text):
            by_email.setdefault(email.split("@")[0].lower(), name)
        parts = person_dir.name.split("-")
        if len(parts) >= 2:
            first, last = parts[0], parts[-1]
            for guess in (first[0] + last, first + last, f"{first}.{last}", first + last[0]):
                by_email.setdefault(guess, name)
    return by_email, by_name


def describe_attendees(attendees, people):
    by_email, by_name = people
    result = []
    for a in attendees or []:
        a = a.strip()
        if not a or "Zoom]" in a or "Digital Whiteboard" in a:
            continue
        if "@" in a:
            name = by_email.get(a.split("@")[0].lower())
            result.append(f"{name} <{a}>" if name else a)
        else:
            result.append(by_name.get(a.lower(), a))
    return result


def fmt_ts(seconds):
    seconds = int(seconds or 0)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def speaker_labels(meta):
    labels = {}
    for sp in meta.get("speakers") or []:
        labels[sp.get("number")] = sp.get("name") or f"Speaker {sp.get('number', 0) + 1}"
    return labels


def render_turns(meta, labels):
    turns = []
    for seg in meta.get("segments") or []:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        spk = seg.get("speaker")
        if turns and turns[-1]["speaker"] == spk:
            turns[-1]["text"].append(text)
        else:
            turns.append({"speaker": spk, "start": seg.get("start", 0), "text": [text]})
    if not turns:
        return meta.get("result", "").strip()
    lines = []
    for t in turns:
        label = labels.get(t["speaker"], "Unknown") if t["speaker"] is not None else "Unknown"
        lines.append(f"[{fmt_ts(t['start'])}] {label}: {' '.join(t['text'])}")
    return "\n\n".join(lines)


def slugify(text, max_len=50):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-") or "meeting"


def render(rec_id, meta, people):
    started = datetime.fromtimestamp(int(rec_id))
    title = (meta.get("calendarEventTitle") or meta.get("title") or "Untitled meeting").strip()
    duration_min = round((meta.get("duration") or 0) / 60000)
    attendees = describe_attendees(meta.get("attendees"), people)
    labels = speaker_labels(meta)

    speaker_lines = []
    for sp in sorted(meta.get("speakers") or [], key=lambda s: s.get("number", 0)):
        label = labels[sp.get("number")]
        channel = CHANNEL_LABELS.get(sp.get("channel"), "unknown channel")
        note = "" if GENERIC_SPEAKER.match(label) else " (named in Superwhisper)"
        speaker_lines.append(f"- {label}: {channel}{note}")

    header = [
        f"Title: {title}",
        f"Date: {started:%Y-%m-%d %H:%M} (local)",
        f"Duration: {duration_min} min",
        f"Attendees (calendar): {', '.join(attendees) if attendees else 'unknown'}",
        f"Source: Superwhisper meeting recording",
        f"{ID_MARKER} {rec_id}",
        "",
        "## Speakers",
        *(speaker_lines or ["- (no speaker separation)"]),
        "",
        "## Speaker guesses",
        "(not yet guessed)",
        "",
    ]
    summary = (meta.get("llmResult") or "").strip()
    if summary and summary != (meta.get("result") or "").strip():
        header += ["## Superwhisper summary", summary, ""]
    header += ["## Transcript", "", render_turns(meta, labels), ""]

    filename = f"{started:%Y-%m-%d-%H%M}-{slugify(title)}.txt"
    return filename, "\n".join(header)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rec_dir = recordings_dir()
    if not rec_dir.is_dir():
        sys.exit(f"Superwhisper recordings folder not found: {rec_dir}")

    imported = already_imported_ids()
    people = load_people()
    INBOX.mkdir(parents=True, exist_ok=True)
    counts = {"imported": 0, "already": 0, "interview": 0, "pending": 0}

    for meta_path in sorted(rec_dir.glob("*/meta.json")):
        rec_id = meta_path.parent.name
        if not rec_id.isdigit():
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if meta.get("kind") != "meeting":
            continue
        if rec_id in imported:
            counts["already"] += 1
            continue
        title = (meta.get("calendarEventTitle") or meta.get("title") or "").strip()
        if INTERVIEW_PATTERN.search(f"{title} {meta.get('title') or ''}"):
            counts["interview"] += 1
            print(f"skip (interview): {rec_id} {title}")
            continue
        recently_written = time.time() - meta_path.stat().st_mtime < MIN_AGE_SECONDS
        if recently_written or not (meta.get("result") or "").strip():
            counts["pending"] += 1
            continue

        filename, content = render(rec_id, meta, people)
        print(f"{'would import' if args.dry_run else 'imported'}: {filename}")
        if not args.dry_run:
            (INBOX / filename).write_text(content)
        counts["imported"] += 1

    print(
        f"\n{counts['imported']} {'to import' if args.dry_run else 'imported'}, "
        f"{counts['already']} already imported, {counts['interview']} interviews skipped, "
        f"{counts['pending']} still processing"
    )


if __name__ == "__main__":
    main()
