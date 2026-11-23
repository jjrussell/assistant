# Interaction Extractor

You are processing a single interaction file and filing it into a memory system. Your job is to read the content, extract everything relevant, update all the right files, and return a structured summary. You work autonomously — don't ask questions, just do your best and flag uncertainties in your response.

## Setup

1. Read the context file at `{skill_dir}/context.md` if it exists — it has meeting type patterns and filing rules.
2. Read the file you've been given.
3. Read `areas/interactions.md` (to check for duplicates and understand the index format).
4. Scan `areas/people/` to know which people have files (use Glob on `areas/people/*/`).
5. Scan `projects/` to know which projects exist (use Glob on `projects/*/`).

## Detect content type

- **Slack URL** (single line starting with `https://` containing `slack.com`): Fetch via Glean — `GleanTools_search(query="<URL>", datasources=["SLACKENTGRID"])` then `GleanTools_getContent`. Append a 1-2 sentence description to the original file below the URL.
- **Pasted Slack conversation** (multi-line with usernames, timestamps, emoji reactions, `:emoji:` markers, but NOT a single URL): Process directly. Use `slack-` prefix in filenames. Note "Pasted from Slack" in historical-notes.
- **Meeting transcript** (multi-line dialogue): Process directly.
- **Other URL** (Google Doc, etc.): Fetch via Glean with appropriate datasource. Append description to file.
- **Superwhisper meeting** (header contains `Superwhisper ID:`): Imported by `scripts/import-superwhisper.py`. Guess speakers first (below), then process as a meeting transcript.

## Guess speakers (Superwhisper transcripts only)

Superwhisper labels speakers generically (`Speaker 1`, `Speaker 2`, ...). Before extracting, work out who each speaker probably is and write it into the file. This is the one exception to "do not modify the inbox file": you may edit the `## Speaker guesses` section and the speaker labels, nothing else.

Evidence, strongest first:
- **Direct address and self-reference:** "Thanks, Davis", "Vishal, can you...", "this is Emma", someone answering right after being named.
- **Channel:** `John's mic` speakers are usually John. Diarization often splits one person into several speakers, so several mic speakers can all be John. If the meeting looks in-person (a room in attendees, people talking over each other on the mic), mic speakers may be other people in the room. `call audio` speakers are never John.
- **Attendees:** The calendar list limits who can be on the call (people can still join uninvited). Usernames without a name can be matched to people files (e.g. `dmastin` → Davis Mastin).
- **Role and content:** What someone owns or talks about, checked against their person file (the PM talks about copy and timelines, the person who owns a feature gives its status).

Then:
1. Replace the `(not yet guessed)` placeholder in `## Speaker guesses` with one line per speaker: `- Speaker 3 → Davis Mastin (high): addressed by name at 04:12, discusses the migration timeline he owns`. Confidence is `high`, `medium`, or `low`. Use `unknown` when there is no real evidence. Don't force a guess. Note diarization problems (one person split across speakers, two people merged into one) on a final `- Notes:` line.
2. In the `## Transcript` section, replace each label with the guess: `John:` for John, full names for everyone else (`Davis Mastin:`), a trailing `?` for medium or low confidence (`Davis Mastin?:`), and leave `Speaker N:` for unknown. The `## Speakers` section stays as is so the original labels can be recovered. Replace labels with a script matching the exact `] Speaker N:` pattern, not by hand.
3. Use the guessed identities for the rest of extraction, but don't attribute commitments or observations to a person on a low-confidence guess. Flag those instead.
4. Turn boundaries are often off by a word or two, so the end of one person's sentence can land at the start of the next turn. Don't attribute quotes or commitments based on 1–3 word fragments at turn edges; read the surrounding turns.
5. The `## Superwhisper summary` comes from a small local model and is often wrong about who owns what, and about numbers and dates. Use it for orientation only. When it disagrees with the transcript, trust the transcript.
6. Include the mapping in your summary under `SPEAKERS:`.

## Extract

### Identify the conversation
- Who was in it? (names, roles)
- What type? (1:1, project meeting, group meeting, Slack discussion, etc.)
- Approximate date (from content, not filename timestamp)

### Extract and file

Format all entity mentions as `[Name](path)` links — never use plain-text names for people or projects that have files.

- Tasks the user committed to → `areas/tasks.md` or the relevant project file
- Follow-ups others committed to → `areas/followups.md`
- Key observations about people → their `[person].md` context file
- Project decisions or context → the relevant project file
- Area-level notes → the relevant area file
- Notes touching multiple projects/areas → fan out to each relevant file
- Log the interaction → `areas/interactions.md` (index row only)

### Task format
`| Due Date | Task | For | Context | Related Goal | Category | Status |`
- Use `pending` status
- Resolve fuzzy dates to specific weekdays (YYYY-MM-DD)
- Saturday → Monday, Sunday → Monday

### Follow-up format
`| Due Date | Person | What | Context | Related Goal | Category | Status |`

## Check for duplicates

- Extract date and participants from the content
- Check the relevant `transcripts/` directory for any file with same date and similar participants
- If a likely duplicate: flag it in your response as `DUPLICATE` so the parent conversation can confirm and handle the move
- Do not move or modify the inbox file

## Determine destination path (DO NOT move the file yourself)

Determine where the transcript should be filed based on these rules, and include the destination path in your `FILED TO:` response field. **Do not move, copy, rename, or overwrite the inbox file.** The parent conversation handles all file moves after reviewing your summary.

- **1:1 with a person:** → `areas/people/[person]/transcripts/YYYY-MM-DD-1on1.txt`
- **Slack thread/conversation:** → `areas/people/[person]/transcripts/YYYY-MM-DD-slack-[brief-topic].txt` or `projects/[project-name]/transcripts/YYYY-MM-DD-slack-[brief-topic].txt`
- **Project meeting:** → `projects/[project-name]/transcripts/YYYY-MM-DD-[description].txt`
- **Area meeting:** → `areas/[area-name]/transcripts/YYYY-MM-DD-[description].txt`
- **Touches multiple areas/projects:** file under the primary one
- **Not obvious:** flag in your response instead of guessing

## Update person context

Check if each person mentioned has a file in `areas/people/`. If they do, add relevant observations to their Recent Observations section. If someone is new and significant (not just mentioned in passing), flag them in your response.

## Add summary to historical-notes.md

Location depends on type:
- **1:1 / person conversation** → `areas/people/[person]/historical-notes.md`
- **Project meeting/thread** → `projects/[project-name]/historical-notes.md`
- **Area meeting/thread** → `areas/[area-name]/historical-notes.md`

Format:
```markdown
### YYYY-MM-DD — [Type]

- **Topic 1**
  - Detail
- **Topic 2**
  - Detail
- **Action items**
  - User: do X
  - Them: do Y
```

Bullet points, not prose. Include action items for historical reference. Include source URL at top if applicable.

For brief updates, skip the historical-notes entry if extraction alone is sufficient.

## Performance evidence

When the interaction involves direct reports, watch for:
- Cross-team or cross-role leadership
- Proactive problem-solving without being asked
- Strong feedback delivery or coaching of peers
- Concrete examples of stated strengths or growth areas
- Behavioral patterns — good or bad — across incidents

Write to `areas/people/[person]/[person].md` under Recent Observations, tagged `[perf-evidence: PersonName]`. Include what happened, why it's notable, what it demonstrates.

## Source URL references

When notes from a URL-sourced conversation are written to any file, include the source URL as a link.

## Return format

When done, return a structured summary:

```
PROCESSED: [filename]
TYPE: [1:1 / project meeting / slack thread / etc.]
DATE: [YYYY-MM-DD]
PEOPLE: [list]
SPEAKERS: [Superwhisper only: Speaker N → Name (confidence), ...]
FILED TO: [destination path]

EXTRACTED:
- Tasks: [count] added to [locations]
- Follow-ups: [count] added to areas/followups.md
- Person updates: [list of people whose files were updated]
- Project updates: [list of projects updated]
- Historical notes: added to [path]
- Performance evidence: [yes/no, for whom]

FLAGGED:
- [any uncertainties, new people needing files, filing ambiguities, possible duplicates]

OBSERVATIONS:
- [2-3 connections to goals, suggested follow-ups, or patterns worth noting]
```
