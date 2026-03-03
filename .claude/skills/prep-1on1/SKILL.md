---
name: prep-1on1
description: Prepare for a 1:1 meeting with a person, answer "what do I know about [person]?" queries, work on development plans, or answer "what should I be thinking about with my team?". Use when asked to prep for a 1:1, asked about a person's context, or asked about team oversight.
argument-hint: "[person name]"
---

## Preparing for a 1:1

For: $ARGUMENTS

### 1. Gather Context from All Sources

Pull information from:
- **Their person file** (`areas/people/[person]/[person].md`) - Current focus, strengths, growth areas, recent observations
- **Historical notes** (`areas/people/[person]/historical-notes.md`) - Past meeting summaries
- **Interactions index** (`areas/interactions.md`) - Last 1:1 date; detailed notes are in their person file under Recent Observations
- **Goals file** (`areas/goals.md`) - Their development goals and progress
- **Follow-ups** (`areas/followups.md`) - Open commitments from them or to them
- **Tasks** (`areas/tasks.md` and all `projects/*.md` files) - Work involving them
- **Projects** - Check if they're a key person in any active project
- **External sources** - If Glean/Slack/etc. are available, search for their Google Docs and recent Slack activity

### 2. Identify Key Themes

Analyze the gathered context to identify:
- **Action items from last meeting** - What was supposed to happen? Did it?
- **Current priorities** - What are they working on right now?
- **Recent activity patterns** - Are they engaged? Stuck? Overloaded?
- **Growth opportunities** - Chances to coach, delegate, or develop them
- **Red flags** - Signs of burnout, disengagement, blocked work, or misalignment
- **Green flags** - Wins to celebrate, good decisions, growth demonstrated

#### Red flags to watch for (especially in Slack/activity):
- Late night/weekend messages — potential burnout
- Short, terse responses — possible disengagement or stress
- Repeatedly asking for same information — blocked or unclear on direction
- No activity in key channels — disconnected from important work
- Only tactical discussions — not operating at the right level
- Conflict or tension in threads — team dynamics issues

#### Green flags to watch for:
- Helping others — mentorship, unblocking teammates
- Strategic questions — thinking beyond immediate implementation
- Cross-team collaboration — building relationships
- Thoughtful responses — taking time to explain "why"
- Pattern recognition — connecting current work to past learnings

### 3. Structure the Prep Document

```markdown
## 1:1 Prep: [Person Name]

### Last 1:1 ([Date]) - Key Points
- Personal updates
- Work topics discussed
- Action items from last time

### Current Context
- Q1/current priorities
- Recent projects/work
- Team dynamics or concerns

### Recent Activity Analysis
[If external sources available, summarize recent discussions, contributions, patterns]

### Suggested Agenda
1. **Check-in on action items** (5 min)
2. **Topic 1** (10 min) - Context and questions
3. **Topic 2** (10 min) - Context and questions
4. **Growth/Development** (10 min)
5. **Personal/Life** (5 min)

### Things to Watch For
- Red flags to probe
- Green flags to celebrate

### Key Messages to Reinforce
- Specific feedback or encouragement

### Questions to Ask Yourself
- Am I setting them up for success?
- Are there blockers I need to remove?
```

### 4. Connect Patterns Across Sources

Look for alignment or disconnects between:
- What they said they'd do vs. what actually happened
- Their stated priorities vs. where time is actually going
- Growth areas identified vs. opportunities being given
- What's written in notes vs. what's visible in activity

**Use specific examples, not vague observations.** Don't say "you should delegate more" — say "I saw you were hands-on with [specific thing]. Walk me through — is this the right use of your time?"

### 5. Make It Actionable

The prep should enable:
- **Concrete discussion topics** - Not vague check-ins
- **Specific coaching moments** - Based on recent examples
- **Clear asks** - What you need from them, what they need from you
- **Follow-through** - Tracking on previous commitments

### 6. Balance Directive and Discovery

- Come prepared with observations and topics
- But leave space to discover what's on their mind
- Use prep to inform questions, not to script the conversation
- Be ready to pivot based on what they share

---

## "What do I know about [person]?"

When asked about a person's context:
- Check `areas/people/[person]/[person].md` for their context
- Pull recent interactions from `areas/interactions.md`
- Show open follow-ups or tasks involving them
- Check any environment-specific data sources

When the person is a direct report, also show:
- Development focus and recent observations
- Performance evidence captured (tagged `[perf-evidence: PersonName]`)
- Last 1:1 date and topics

---

## People Development Conversations

When development plans for a direct report need to be worked on:

1. **Pull up current context** from their file in `areas/people/` and from `areas/goals.md`
2. **Explore the development area:**
   - What's the gap or opportunity?
   - What does "better" look like?
   - What situations or experiences would help them grow?
   - How will progress be recognized?
3. **Make it actionable:** What's the next thing to do? Create an opportunity? Have a conversation? Give feedback?
4. **Connect to ongoing work:** Are there upcoming projects or interactions where this development focus is relevant?
5. **Confirm and save** to both `areas/people/[person].md` (development focus) and `areas/goals.md` (development goals section)

---

## "What should I be thinking about with my team?"

- Review development goals for each direct report
- Flag anyone who hasn't had a logged interaction recently
- Surface any patterns (someone consistently missing commitments, someone ready for a stretch opportunity)
