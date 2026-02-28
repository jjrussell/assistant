#!/bin/bash
SCRIPT_PATH="$0"
while [ -L "$SCRIPT_PATH" ]; do
    SCRIPT_DIR=$(cd "$(dirname "$SCRIPT_PATH")" && pwd)
    SCRIPT_PATH=$(readlink "$SCRIPT_PATH")
    [[ "$SCRIPT_PATH" != /* ]] && SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_PATH"
done
SCRIPT_DIR=$(cd "$(dirname "$SCRIPT_PATH")" && pwd)
DEST="$SCRIPT_DIR/../inbox/transcripts"
mkdir -p "$DEST"
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
pbpaste > "$DEST/$TIMESTAMP.txt"
