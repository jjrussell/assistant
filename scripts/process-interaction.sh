#!/bin/bash
# Process interactions non-interactively via claude -p
# Replicates the /process-interaction skill behavior.
#
# Usage:
#   ./scripts/process-interaction.sh                    # Process inbox/transcripts/
#   ./scripts/process-interaction.sh "just talked to Lisa about X"  # Conversational input
#   echo "transcript text" | ./scripts/process-interaction.sh       # Piped input

SCRIPT_PATH="$0"
while [ -L "$SCRIPT_PATH" ]; do
    SCRIPT_DIR=$(cd "$(dirname "$SCRIPT_PATH")" && pwd)
    SCRIPT_PATH=$(readlink "$SCRIPT_PATH")
    [[ "$SCRIPT_PATH" != /* ]] && SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_PATH"
done
SCRIPT_DIR=$(cd "$(dirname "$SCRIPT_PATH")" && pwd)
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$PROJECT_DIR/.claude/skills/process-interaction"
LOG_DIR="$PROJECT_DIR/outbox/process-interaction"

mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
LOG_FILE="$LOG_DIR/$TIMESTAMP.md"

SKILL_PROMPT=$(cat "$SKILL_DIR/SKILL.md")
CONTEXT_PROMPT=$(cat "$SKILL_DIR/context.md" 2>/dev/null || echo "")

if [ -n "$1" ]; then
  # Conversational input passed as argument
  INPUT="Conversational input from the user:

$*"
elif [ ! -t 0 ]; then
  # Piped input
  INPUT="Conversational input from the user:

$(cat)"
else
  # No argument, no pipe — process the inbox
  INPUT="Process all files in inbox/transcripts/"
fi

FULL_PROMPT="You are running the process-interaction skill. Follow these instructions exactly:

--- SKILL INSTRUCTIONS ---
$SKILL_PROMPT
--- END SKILL INSTRUCTIONS ---

--- CONTEXT ---
$CONTEXT_PROMPT
--- END CONTEXT ---

--- INPUT ---
$INPUT
--- END INPUT ---

Process this now. Follow the extraction workflow step by step.

IMPORTANT: When you need to move or delete files, use the move-transcript script — NEVER raw mv/rm commands. Paths contain spaces that break permission matching.
- Move: ./.claude/skills/process-interaction/scripts/move-transcript.sh move <source> <dest-dir>
- Delete: ./.claude/skills/process-interaction/scripts/move-transcript.sh delete <source>"

# Build log header
{
  echo "# Process Interaction Log"
  echo ""
  echo "**Timestamp:** $TIMESTAMP"
  echo "**Input type:** $(if [ -n "$1" ]; then echo "argument"; elif [ ! -t 0 ]; then echo "piped"; else echo "inbox"; fi)"
  echo ""
  echo "## Input"
  echo ""
  echo '```'
  echo "$INPUT"
  echo '```'
  echo ""
  echo "## Output"
  echo ""
} > "$LOG_FILE"

cd "$PROJECT_DIR" && stdbuf -oL claude -p "$FULL_PROMPT" \
  --allowedTools "Bash,Read,Write,Edit,Glob,Grep,WebFetch,mcp__devex-mcp-server__GleanTools_search,mcp__devex-mcp-server__GleanTools_getContent,mcp__devex-mcp-server__SlackTools_readSlackUrl,mcp__devex-mcp-server__SlackTools_searchSlack" \
  2>&1 | tee -a "$LOG_FILE"

echo ""
echo "---"
echo "Log saved to: $LOG_FILE"
