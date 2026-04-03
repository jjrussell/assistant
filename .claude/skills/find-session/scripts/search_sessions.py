#!/usr/bin/env python3
"""Search past Claude Code conversation sessions by keyword.

Usage:
    python search_sessions.py <query> [--project <substring>] [--limit <n>]

Arguments:
    query           Space-separated search terms (all must match, case-insensitive)
    --project       Filter to project dirs containing this substring (default: search all)
    --limit         Max results to show (default: 10)

Examples:
    python search_sessions.py "auth migration"
    python search_sessions.py "obsidian checkboxes" --project assistant
    python search_sessions.py "kafka worker" --project orchestra --limit 5
"""

import json
import glob
import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path

CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"

# Noise patterns to strip before matching -- these are injected by the harness
# and would cause false positives on nearly every session
NOISE_PATTERNS = [
    re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL),
    re.compile(r"<command-name>.*?</command-name>", re.DOTALL),
    re.compile(r"<command-message>.*?</command-message>", re.DOTALL),
]


def extract_text(message: dict) -> str:
    """Pull plain text out of a message's content field."""
    content = message.get("content", "")
    if isinstance(content, list):
        return " ".join(
            c.get("text", "")
            for c in content
            if isinstance(c, dict) and c.get("type") == "text"
        )
    return str(content)


def strip_noise(text: str) -> str:
    """Remove system-injected markup that would cause false matches."""
    for pattern in NOISE_PATTERNS:
        text = pattern.sub("", text)
    return text


def search_session(fpath: str, terms: list[str]) -> dict | None:
    """Search a single session file for matching terms. Returns a result dict or None.

    Matching strategy:
    - ALL terms must appear somewhere in the session (across any messages)
    - Snippets are extracted from individual messages that contain at least one term
    - Messages containing more terms are scored higher
    """
    sid = os.path.basename(fpath).replace(".jsonl", "")
    mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d %H:%M")

    first_user_msg = None
    msg_count = 0
    session_terms_found: set[str] = set()
    # Collect per-message hits: (type, snippet, timestamp, term_count)
    message_hits: list[dict] = []

    with open(fpath) as f:
        for line in f:
            try:
                obj = json.loads(line.strip())
            except (json.JSONDecodeError, ValueError):
                continue

            if obj.get("type") not in ("user", "assistant"):
                continue

            msg_count += 1
            text = strip_noise(extract_text(obj.get("message", {})))

            # Grab the first real user message as the session "title"
            if (
                obj.get("type") == "user"
                and not obj.get("isMeta")
                and not first_user_msg
            ):
                clean = text.strip()
                if clean and len(clean) > 10:
                    first_user_msg = clean[:200]

            # Check which terms appear in this message
            text_lower = text.lower()
            msg_terms = [t for t in terms if t in text_lower]
            if msg_terms:
                session_terms_found.update(msg_terms)
                # Build snippet around the first matching term
                first_term = msg_terms[0]
                idx = text_lower.find(first_term)
                start = max(0, idx - 60)
                end = min(len(text), idx + len(first_term) + 60)
                snippet = text[start:end].replace("\n", " ").strip()
                message_hits.append(
                    {
                        "type": obj.get("type"),
                        "snippet": snippet,
                        "timestamp": obj.get("timestamp", ""),
                        "term_count": len(msg_terms),
                    }
                )

    # ALL terms must appear somewhere in the session
    if session_terms_found != set(terms):
        return None

    # Score: prefer sessions where terms co-occur in the same message,
    # but still match when terms are spread across messages
    user_match_count = sum(1 for h in message_hits if h["type"] == "user")
    # Bonus for messages that contain multiple terms
    cooccurrence_bonus = sum(h["term_count"] - 1 for h in message_hits)

    # Sort hits: messages with more terms first, then user messages first
    message_hits.sort(key=lambda h: (h["term_count"], h["type"] == "user"), reverse=True)

    return {
        "session_id": sid,
        "date": mtime,
        "title": first_user_msg or "(no title)",
        "msg_count": msg_count,
        "match_count": len(message_hits),
        "user_match_count": user_match_count,
        "score": user_match_count * 2 + len(message_hits) + cooccurrence_bonus * 3,
        "top_snippets": [
            {"type": h["type"], "snippet": h["snippet"], "timestamp": h["timestamp"]}
            for h in message_hits[:3]
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Search Claude Code session history")
    parser.add_argument("query", nargs="+", help="Search terms")
    parser.add_argument(
        "--project",
        default=None,
        help="Filter to project dirs containing this substring",
    )
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    args = parser.parse_args()

    # Split all query args into individual words so that
    # "zhilong staff promotion" (quoted) works the same as
    # zhilong staff promotion (unquoted)
    terms = [w.lower() for arg in args.query for w in arg.split()]

    # Find project directories to search
    if not CLAUDE_PROJECTS.exists():
        print("No Claude projects directory found at ~/.claude/projects/")
        sys.exit(1)

    project_dirs = sorted(CLAUDE_PROJECTS.iterdir())
    if args.project:
        project_dirs = [d for d in project_dirs if args.project.lower() in d.name.lower()]

    if not project_dirs:
        print(f"No project directories matched filter: {args.project}")
        sys.exit(1)

    # Search all session files
    results = []
    files_searched = 0
    for pdir in project_dirs:
        for fpath in glob.glob(str(pdir / "*.jsonl")):
            files_searched += 1
            result = search_session(fpath, terms)
            if result:
                result["project"] = pdir.name
                results.append(result)

    # Sort by relevance (score), then recency (date)
    results.sort(key=lambda r: (r["score"], r["date"]), reverse=True)

    # Output
    print(f"\nSearched {files_searched} sessions across {len(project_dirs)} project(s)")
    print(f"Query: {' '.join(terms)}")
    print(f"Found: {len(results)} matching sessions\n")

    for r in results[: args.limit]:
        print("=" * 70)
        print(f"Session:  {r['session_id']}")
        print(f"Project:  {r['project']}")
        print(f"Date:     {r['date']}  |  Messages: {r['msg_count']}  |  Matches: {r['match_count']}")
        print(f"Topic:    {r['title'][:120]}")
        print("Snippets:")
        for s in r["top_snippets"]:
            print(f"  [{s['type']}] ...{s['snippet']}...")
        print(f"\n  → claude --resume {r['session_id']}")
        print()


if __name__ == "__main__":
    main()
