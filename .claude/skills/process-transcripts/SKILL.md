---
name: process-transcripts
description: Process unprocessed items from inbox/transcripts/ — meeting transcripts, Slack thread URLs, or other content. Use when the user says "process transcripts", "process new transcripts", "process inbox", or when unprocessed files are found in the inbox.
---

## Step 0: Determine the content type

Read each file from `inbox/transcripts/`. Detect what it is:

- **Slack URL** (single line starting with `https://` and containing `slack.com`): Fetch the thread content via Glean using `GleanTools_search(query="<URL>", datasources=["SLACKENTGRID"])` then `GleanTools_getContent`. After fetching, append a 1-2 sentence description of the thread to the original file (below the URL) so the file is self-describing without needing to visit Slack.
- **Meeting transcript** (multi-line text with dialogue): Process the text directly.
- **Other URL** (Google Doc, etc.): Fetch via Glean with appropriate datasource. After fetching, append a 1-2 sentence description to the original file below the URL.

After fetching (if needed), follow the same workflow below for all content types.

## Workflow for each item:

1. **Identify the conversation:**
   - Who was in it? (names, roles)
   - What type? (1:1, project meeting, group meeting, Slack discussion, etc.)
   - Approximate date (from content — **not** the filename timestamp, which only reflects when it was pasted)
2. **Extract and file:**
   - Tasks YOU committed to → `areas/tasks.md` or the relevant project file
   - Follow-ups others committed to → `areas/followups.md`
   - Key observations about people → their `[person].md` context file
   - Project decisions or context → the relevant project file
   - Area-level notes (relevant to an ongoing responsibility) → the relevant area file
   - Notes touching multiple projects/areas → fan out to each relevant file
   - Log the interaction → `areas/interactions.md` (index row only)
3. **Check for duplicates before filing:**
   - Extract the date and participants from the content
   - Check the relevant `transcripts/` directory (person or project) for any file with the same date and similar participants
   - If a likely duplicate is found, **do not process it** — move it to `inbox/possible-duplicates/` (create the folder if it doesn't exist), keeping the original filename
   - At the end of the batch, list every file moved to `inbox/possible-duplicates/` and explicitly state which already-processed item you believe it duplicates
   - Wait for confirmation before doing anything further with those files
   - **NEVER DELETE AN INBOX FILE** — even confirmed duplicates stay in `inbox/possible-duplicates/` until you explicitly say to remove them

4. **Move and rename the file:**
   - **1:1 with a person:** → `areas/people/[person]/transcripts/YYYY-MM-DD-1on1.txt`
   - **Slack thread:** → `areas/people/[person]/transcripts/YYYY-MM-DD-slack-[brief-topic].txt` or `projects/[project-name]/transcripts/YYYY-MM-DD-slack-[brief-topic].txt`
   - **Project meeting:** → `projects/[project-name]/transcripts/YYYY-MM-DD-[description].txt` (create the `transcripts/` dir if needed)
   - **Area meeting:** → `areas/[area-name]/transcripts/YYYY-MM-DD-[description].txt` (create the `transcripts/` dir if needed; create the area file too if it doesn't exist)
   - **Touches multiple areas/projects:** file it under the primary one and note in the index where notes were fanned out
   - **Not obvious where it belongs:** Ask before moving
5. **Update the person's context file** if the conversation surfaces new observations, context changes, or notes worth capturing in `[person].md`
6. **Add a summary to `historical-notes.md`** — create the file if it doesn't exist. The location depends on the type:
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

   Write in bullet points, not prose. Include action items for historical reference even though they are captured elsewhere. When the source is a URL (Slack, Google Doc, etc.), include the source URL as a link at the top of the summary.

**Source URL references:** Any time notes from a URL-sourced conversation are written to any file (historical-notes, person files, project files, followups, tasks), include the source URL as a link so the original content is always one click away.

**When processing multiple items:** Work through them one at a time. After each one, confirm what was extracted and where the file was moved before continuing to the next.

**Script location:** `scripts/save-transcript.sh` — reads clipboard, saves to `inbox/transcripts/YYYY-MM-DD-HHMMSS.txt`. Silent, no UI. Works for both transcripts and URLs.
