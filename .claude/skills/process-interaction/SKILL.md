---
name: process-interaction
description: Process any interaction — meeting transcripts, Slack threads, pasted Slack conversations, Google Doc links, or conversational reports. Auto-invoked when the user says "process transcripts", "process inbox", or reports an interaction ("just talked to...", "had a meeting with...", "quick update...", "FYI...").
---

## Pre-processing: Load context

If a `context.md` file exists in this skill directory, read it first. It contains meeting type patterns, filing rules, and participant matching hints specific to the current work environment.

## Step 0: Determine input source and content type

There are two input paths:

### Path A: File-based input (inbox/transcripts/)

Read each file from `inbox/transcripts/`. Detect what it is:

- **Slack URL** (single line starting with `https://` and containing `slack.com`): Fetch the thread content via Glean using `GleanTools_search(query="<URL>", datasources=["SLACKENTGRID"])` then `GleanTools_getContent`. After fetching, append a 1-2 sentence description of the thread to the original file (below the URL) so the file is self-describing without needing to visit Slack.
- **Pasted Slack conversation** (multi-line text with Slack message patterns — lines with usernames, timestamps, emoji reactions, or Slack-style formatting like `:emoji:` markers, but NOT a single URL): Process the text directly, treating it the same as a Slack thread. When filing, use the `slack-` prefix in filenames (e.g., `YYYY-MM-DD-slack-[brief-topic].txt`). Since there's no source URL, note "Pasted from Slack" in historical-notes entries instead of a link.
- **Meeting transcript** (multi-line text with dialogue): Process the text directly.
- **Other URL** (Google Doc, etc.): Fetch via Glean with appropriate datasource. After fetching, append a 1-2 sentence description to the original file below the URL.

After fetching (if needed), proceed to the Extraction Workflow below.

### Path B: Conversational input (user reports an interaction in chat)

The user tells you about something that happened — "just talked to Lisa about X", "had a meeting with the team", "quick update: Davis agreed to...". The content is whatever they share in the conversation. There are no files to manage — skip duplicate detection (Step 3) and file management (Step 4). Proceed directly to the Extraction Workflow.

---

## Extraction Workflow (all input types):

### 1. Identify the conversation
- Who was in it? (names, roles)
- What type? (1:1, project meeting, group meeting, Slack discussion, ad hoc update, etc.)
- Approximate date (from content — for inbox files, **not** the filename timestamp, which only reflects when it was pasted)

### 2. Extract and file

Every entity mention in every edit must be a `[Name](path)` link — no plain-text names for people or projects that have files.

- Tasks YOU committed to → `areas/tasks.md` or the relevant project file
- Follow-ups others committed to → `areas/followups.md`
- Key observations about people → their `[person].md` context file
- Project decisions or context → the relevant project file
- Area-level notes (relevant to an ongoing responsibility) → the relevant area file
- Notes touching multiple projects/areas → fan out to each relevant file
- Log the interaction → `areas/interactions.md` (index row only — no notes here)

### 3. Check for duplicates (file-based input only)

Skip this step for conversational input.

- Extract the date and participants from the content
- Check the relevant `transcripts/` directory (person or project) for any file with the same date and similar participants
- If a likely duplicate is found, **do not process it** — move it to `inbox/possible-duplicates/` (create the folder if it doesn't exist), keeping the original filename
- At the end of the batch, list every file moved to `inbox/possible-duplicates/` and explicitly state which already-processed item you believe it duplicates
- Wait for confirmation before doing anything further with those files
- **NEVER DELETE AN INBOX FILE** — even confirmed duplicates stay in `inbox/possible-duplicates/` until you explicitly say to remove them

### 4. Move and rename the file (file-based input only)

Skip this step for conversational input.

- **1:1 with a person:** → `areas/people/[person]/transcripts/YYYY-MM-DD-1on1.txt`
- **Slack thread or pasted Slack conversation:** → `areas/people/[person]/transcripts/YYYY-MM-DD-slack-[brief-topic].txt` or `projects/[project-name]/transcripts/YYYY-MM-DD-slack-[brief-topic].txt`
- **Project meeting:** → `projects/[project-name]/transcripts/YYYY-MM-DD-[description].txt` (create the `transcripts/` dir if needed)
- **Area meeting:** → `areas/[area-name]/transcripts/YYYY-MM-DD-[description].txt` (create the `transcripts/` dir if needed; create the area file too if it doesn't exist)
- **Touches multiple areas/projects:** file it under the primary one and note in the index where notes were fanned out
- **Not obvious where it belongs:** Ask before moving

### 5. Update person context

Check if the person has a file in `areas/people/`; if not, create one. Add any relevant context, notes, or observations to their file.

### 6. Add a summary to `historical-notes.md`

Create the file if it doesn't exist. The location depends on the type:

- **1:1 / person conversation** → `areas/people/[person]/historical-notes.md`
- **Project meeting/thread** → `projects/[project-name]/historical-notes.md`
- **Area meeting/thread** → `areas/[area-name]/historical-notes.md`

Use this format:

```markdown
### YYYY-MM-DD — [Type, e.g. 1:1, Slack thread, meeting title]

- **Topic 1**
  - Detail or key point
  - Another detail
- **Topic 2**
  - Detail
- **Action items**
  - John: do X
  - Them: do Y
```

Write in bullet points, not prose. Include action items for historical reference even though they are captured elsewhere. When the source is a URL (Slack, Google Doc, etc.), include the source URL as a link at the top of the summary. For pasted Slack conversations with no URL, note "Pasted from Slack" instead. For conversational input, note "Reported in chat" instead.

**Note on conversational input:** For brief ad hoc updates ("quick update: Lisa agreed to do X by Friday"), a historical-notes entry may be overkill — use judgment. If there's enough substance to warrant a summary, write one. If it's just a single follow-up or task, the extraction in Step 2 is sufficient.

### 7. Performance evidence (when applicable)

When logging interactions involving direct reports, check for notable behavior:

- Cross-team or cross-role leadership (stepping in beyond their scope)
- Proactive problem-solving without being asked
- Strong feedback delivery or coaching of peers
- Concrete examples of a stated strength or growth area playing out
- Patterns of behavior — good or bad — observed over multiple incidents

**Where to write it:**
- `areas/people/[person]/[person].md` — under Recent Observations, tagged `[perf-evidence: PersonName]`
- `areas/people/[person]/historical-notes.md` — in the relevant meeting section

Include: what happened, why it's notable, what it demonstrates about the person. Specificity is what makes perf evidence useful — vague praise is useless at review time.

---

## Source URL references

Any time notes from a URL-sourced conversation are written to any file (historical-notes, person files, project files, followups, tasks), include the source URL as a link so the original content is always one click away. For pasted Slack conversations with no URL, note "Pasted from Slack" instead. For conversational input, no source link is needed.

## Behavior mode

Follow **logging mode** behavior:
- First do the job — log the interaction, extract tasks and follow-ups, confirm what you captured
- Then offer 2-3 observations max (connections to goals, suggested follow-ups, patterns)
- Make closure easy — "good" or "that's it" ends the interaction
- Don't interrogate, don't require engagement with suggestions

**When processing multiple inbox items:** Work through them one at a time. After each one, confirm what was extracted and where the file was moved before continuing to the next.

## Script location

`scripts/save-transcript.sh` — reads clipboard, saves to `inbox/transcripts/YYYY-MM-DD-HHMMSS.txt`. Silent, no UI. Works for transcripts, URLs, and pasted Slack conversations.
