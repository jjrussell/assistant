#!/bin/bash
# Move or delete files in this project. Use this instead of raw mv/rm
# because paths contain spaces that break Claude Code permission matching.
#
# Usage:
#   move-transcript.sh move <source> <dest-dir>            # mkdir -p dest-dir && mv source dest-dir/
#   move-transcript.sh move <source> <dest-dir> <new-name> # mkdir -p dest-dir && mv source dest-dir/new-name
#   move-transcript.sh delete <source>                     # rm source (for duplicates)
#
# Examples:
#   ./move-transcript.sh move inbox/transcripts/2026-03-13.txt areas/people/lisa/transcripts/
#   ./move-transcript.sh move inbox/transcripts/2026-03-13.txt areas/people/lisa/transcripts/ 2026-03-13-1on1.txt
#   ./move-transcript.sh delete inbox/transcripts/2026-03-13.txt

set -euo pipefail

ACTION="${1:-}"
SOURCE="${2:-}"

if [ -z "$ACTION" ] || [ -z "$SOURCE" ]; then
  echo "Usage: move-transcript.sh <move|delete> <source> [dest-dir]" >&2
  exit 1
fi

if [ ! -f "$SOURCE" ]; then
  echo "Error: Source file not found: $SOURCE" >&2
  exit 1
fi

case "$ACTION" in
  move)
    DEST="${3:-}"
    NEWNAME="${4:-}"
    if [ -z "$DEST" ]; then
      echo "Error: dest-dir required for move" >&2
      exit 1
    fi
    mkdir -p "$DEST"
    if [ -n "$NEWNAME" ]; then
      mv "$SOURCE" "$DEST/$NEWNAME"
      echo "Moved $SOURCE → $DEST/$NEWNAME"
    else
      mv "$SOURCE" "$DEST/"
      echo "Moved $SOURCE → $DEST/"
    fi
    ;;
  delete)
    rm "$SOURCE"
    echo "Deleted $SOURCE"
    ;;
  *)
    echo "Error: Unknown action '$ACTION'. Use 'move' or 'delete'." >&2
    exit 1
    ;;
esac
