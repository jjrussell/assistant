---
name: find-session
description: Search past Claude Code conversation sessions by topic or keyword. Make sure to use this skill whenever the user says "remember when we talked about...", "find the session where...", "which conversation had...", "I was working on something", or wants to resume a previous discussion about a specific topic. Also trigger when the user asks to find an old conversation, look up what was discussed, or says things like "we figured this out before" or "go back to that session".
argument-hint: "<topic or keywords to search for>"
---

## Find a past conversation session

Claude Code stores every conversation as a JSONL file in `~/.claude/projects/<project-dir>/`. This skill searches the full text of those sessions to find conversations matching a query, so the user can resume where they left off.

### Step 1: Run the search

Use the bundled script at `scripts/search_sessions.py` (relative to this skill's directory). It handles all the parsing, noise stripping, and ranking.

```bash
python3 <skill-dir>/scripts/search_sessions.py <search terms> [--project <filter>] [--limit 10]
```

**Choosing the right scope:**
- By default, the script searches ALL projects in `~/.claude/projects/`. This is usually what you want when the user isn't sure where the conversation happened.
- If the user says "in this project" or context makes the project obvious, pass `--project <substring>` to narrow the search (e.g., `--project assistant`, `--project orchestra`). The substring matches against the project directory name.

### Step 2: Present results

Show the user the matching sessions. For each one, include:
- **Date** and **topic** (first user message)
- **Snippets** showing the match in context
- **Resume command**: `claude --resume <session-id>`

If there are many results, highlight the top 2-3 most relevant and mention how many others matched.

### Step 3: Offer next steps

- "Want me to search with different terms?"
- "You can resume any of these with the command shown, or I can read more from a specific session."
