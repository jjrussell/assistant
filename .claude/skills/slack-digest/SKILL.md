---
name: slack-digest
description: "Summarize Slack channels by named group, filtering noise from substance. Make sure to use this skill whenever the user asks for a Slack digest, Slack summary, channel recap, 'what happened in Slack', 'catch me up on channels', or wants to summarize a group of Slack channels. Also trigger when used with /loop for periodic Slack monitoring."
---

# Slack Digest

Summarize recent Slack activity across a named group of channels, filtering out noise (individual Q&A, troubleshooting threads) and surfacing substance (debates, decisions, announcements, action items, escalations, org/project updates).

## Invocation

```
/slack-digest <group-name> [time-window]
```

- **group-name** (required): A named group from `channel-groups.md` (e.g., `projects`, `leadership`)
- **time-window** (optional): How far back to look. Defaults to `24h`. Examples: `48h`, `3d`, `1w`

If no arguments are provided, list the available groups from `channel-groups.md` and ask which one to run.

## Channel Groups

Channel groups are defined in `channel-groups.md` (sibling file to this skill). Read it to find the channels for the requested group.

Each group is an `## H2` heading followed by a bullet list of `#channel-name` entries. To add or modify groups, edit that file directly.

## Step 1: Calculate the date range

Convert the time window into a Slack-compatible `after:YYYY-MM-DD` date string. For example, if today is 2026-03-18 and the window is `24h`, use `after:2026-03-17`. For `3d`, use `after:2026-03-15`.

## Step 2: Fetch messages from each channel

For each channel in the group, use the `SlackTools_searchSlack` tool:

```
searchQuery: "in:#channel-name after:YYYY-MM-DD"
maxResults: 50
includeFullUserInfo: true
```

**Parallelization**: Launch searches for all channels in the group simultaneously using parallel tool calls. This is critical for performance — do not search channels one at a time.

If a channel returns no results, note it as "No activity" and move on.

## Step 3: Filter and classify messages

For each channel's results, classify every message into one of two buckets:

### KEEP — Substantive messages
- Announcements or broadcasts to the channel
- Decisions made or communicated
- Status updates on projects, launches, migrations
- Action items assigned or completed
- Escalations, blockers, or risk callouts
- Organizational changes (team moves, role changes, new hires)
- Links to important docs, PRs, or artifacts shared for broad awareness
- Meeting summaries or recaps posted to the channel
- Strategic direction or priority shifts

### SKIP — Noise
- One person asking another person a specific question (and the answer thread)
- Individual troubleshooting or debugging threads
- "Can someone help me with X?" + responses
- Bot-generated notifications (deploy alerts, CI results, PR notifications) unless they indicate something significant
- Social chatter, emoji reactions, thank-yous
- Questions that were fully resolved in-thread with no broader implications

**When in doubt, KEEP it.** The user would rather skim an extra bullet than miss something important. But a thread where Alice asks Bob how to configure a setting and Bob answers — that's noise. A thread where someone announces a new architecture decision that affects multiple teams — that's substance.

### Thread grouping — one entry per thread

Messages sharing the same `thread_ts` belong to one Slack thread and must be consolidated into a single digest entry. Never create separate entries for messages within the same thread, even if the thread covers multiple subtopics. Instead, summarize the full thread as one entry:
- Link the headline to the thread root (the message whose timestamp matches `thread_ts`)
- Credit all substantive contributors in the **Who** line
- Cover the key points, proposals, and decisions from the entire thread in the summary body
- If the thread has distinct subtopics, use bullet points within the single entry rather than splitting into multiple entries

## Step 4: Write the digest

Write the digest to:

```
outbox/slack-digests/YYYY-MM-DD-<group-name>.md
```

Use this format:

```markdown
# Slack Digest: <Group Name>
**Period**: <start date> to <end date>
**Generated**: <today's date and time>

---

## #channel-name

### [Brief topic headline](slack-message-url)
**Type**: Decision | Debate | Proposal | Announcement | Blocker | FYI<br>
**Who**: @person
[1-3 sentence summary of the substantive message or thread. Include what was decided, announced, or requested. If there's an action item, call it out.]

### [Another topic]
...

---

## #another-channel

...

---

## Quiet Channels
- #channel-with-no-activity
- #channel-with-only-noise
```

### Writing guidelines

- **Lead with what matters**: Put the most important/actionable items first within each channel
- **Name names**: Always include who said/decided/announced something
- **Be specific**: "Jamie announced the unified builder launch is delayed to April 2" not "There was a discussion about timelines"
- **Call out action items explicitly**: If someone is expected to do something, make it clear
- **Link back**: If a message contains a link to a doc, PR, or artifact, include it
- **Keep it scannable**: Short paragraphs, clear headlines. The user should be able to skim this in 2 minutes per channel
- **Classify every entry**: Each entry gets a **Type** tag that tells the reader why it matters at a glance. Pick exactly one:
  - **Decision** — something was decided or agreed upon in this thread
  - **Debate** — active disagreement or an open question still being hashed out, no resolution yet
  - **Proposal** — someone put forward an idea or design that hasn't been resolved
  - **Announcement** — broadcast of a change, deploy, new feature, or team update
  - **Blocker** — something is stuck, blocked, or at risk
  - **FYI** — informational, no action needed but worth knowing about
- **Use `<br>` for line breaks**: Markdown renderers collapse adjacent lines into one paragraph. Always put `<br>` at the end of the **Type** line so it renders on its own line above **Who**. Same for the **Who** line before the summary body.
- **Always link to Slack**: Make the topic headline itself a clickable link to the originating message or thread root using the `messageUrl` from search results. Use the format `### [Headline text](slack-url)`. If a topic spans multiple messages, link to the thread root (the message with `thread_ts` matching its own timestamp). This lets the user click straight into Slack for context.

## Step 5: Present to the user

After writing the file, give a brief verbal summary:
- Which channels had substantive activity
- The 2-3 most important items across all channels (the "if you read nothing else" highlights)
- Which channels were quiet

Keep this conversational summary very short — the detail is in the file.

## Handling edge cases

- **Channel not found**: If `searchSlack` returns no results and you suspect the channel name is wrong, mention it to the user
- **Very high volume channel**: If a channel has 50+ substantive messages, group related messages into themes rather than listing each one individually
- **Duplicate topics across channels**: If the same topic appears in multiple channels, note the cross-channel discussion but don't repeat the full summary — summarize once and reference it
- **Time zone**: Use the user's local context. Dates in file names are YYYY-MM-DD format

## Appending to an existing digest

If a digest file already exists for today and the same group, append to it with a separator:

```markdown
---
**Updated**: <time>
(New activity since last digest)

## #channel-name
...
```
