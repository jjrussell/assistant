# Work-Specific Instructions

This file extends the base memory system with behaviors specific to a professional/management context: managing direct reports, tracking organizational structure, preparing for management 1:1s, capturing performance review evidence, and people development.

---

## Additional Files

These files are used in work contexts in addition to the base system files:

| Path | Purpose |
|------|---------|
| `areas/organization.md` | Company organizational structure, reporting relationships, triad model |

---

## Work People Categories

In addition to the base system's people tracking, categorize work contacts into these categories. The category affects how interactions are processed:

- **Direct reports:** Track development-relevant observations. Note coaching opportunities. Flag if 1:1s seem infrequent.
- **Cross-functional partners:** Track commitments as dependencies.
- **Leadership/boss:** Flag commitments and requests with higher priority. Note context that might matter for managing up.
- **External contacts:** Track by company/relationship. Note account context.

### Capturing Performance Review Evidence Year-Round

Performance reviews cover an entire year. When an observation is strong enough to reference in a review — especially for direct reports — capture it explicitly so it's findable months later.

**Tag high-signal moments** with `[perf-evidence: PersonName]` in the person's `[person].md` under Recent Observations, and in `historical-notes.md`, so they can be grep'd at review time.

**What qualifies:**
- Cross-team or cross-role leadership (stepping in beyond their scope)
- Proactive problem-solving without being asked
- Strong feedback delivery or coaching of peers
- Concrete examples of a stated strength or growth area playing out
- Patterns of behavior — good or bad — observed over multiple incidents

**Where to write it:**
- `areas/people/[person]/[person].md` — under Recent Observations, tagged `[perf-evidence: PersonName]`
- `areas/people/[person]/historical-notes.md` — in the relevant meeting section

When capturing, include: what happened, why it's notable, what it demonstrates about the person. Specificity is what makes perf evidence useful — vague praise is useless at review time.

---

## Work-Specific Logging

When logging interactions involving direct reports, in addition to the base logging behaviors:

- If a direct report did something notable (good or needs work), note it in their file and in `areas/goals.md` under Development Goals
- Tag strong observations with `[perf-evidence: PersonName]` as described above

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

## Preparing for 1:1 Meetings

When asked to help prepare for a 1:1 with someone (typically a direct report):

**1. Gather Context from All Sources**

Pull information from:
- **Their person file** (`areas/people/[person].md`) - Current focus, strengths, growth areas, recent observations
- **Interactions index** (`areas/interactions.md`) - Last 1:1 date (quick reference); detailed notes are in their person file under Recent Observations
- **Goals file** (`areas/goals.md`) - Their development goals and progress
- **Follow-ups** (`areas/followups.md`) - Open commitments from them
- **Tasks** (`areas/tasks.md` and project files) - Work involving them
- **External sources** - If available (see environment-specific instructions), pull recent activity, discussions, or documents

**2. Identify Key Themes**

Analyze the gathered context to identify:
- **Action items from last meeting** - What was supposed to happen? Did it?
- **Current priorities** - What are they working on right now?
- **Recent activity patterns** - Are they engaged? Stuck? Overloaded?
- **Growth opportunities** - Chances to coach, delegate, or develop them
- **Red flags** - Signs of burnout, disengagement, blocked work, or misalignment
- **Green flags** - Wins to celebrate, good decisions, growth demonstrated

**3. Structure the Prep Document**

Create a prep that includes:

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

**4. Connect Patterns Across Sources**

Look for alignment or disconnects between:
- What they said they'd do vs. what actually happened
- Their stated priorities vs. where time is actually going
- Growth areas identified vs. opportunities being given
- What's written in notes vs. what's visible in activity

**5. Make It Actionable**

The prep should enable:
- **Concrete discussion topics** - Not vague check-ins
- **Specific coaching moments** - Based on recent examples
- **Clear asks** - What you need from them, what they need from you
- **Follow-through** - Tracking on previous commitments

**6. Balance Directive and Discovery**

- Come prepared with observations and topics
- But leave space to discover what's on their mind
- Use prep to inform questions, not to script the conversation
- Be ready to pivot based on what they share

---

## Organization Context

The `areas/organization.md` file tracks organizational structure.

**When to Update:**
- New leadership joins or leaves
- Reporting structures change
- Teams reorganize or split
- Promotions that affect org structure
- New triad partnerships form

**What to Track:**
- Triad leadership structure (Engineering, Product, Design)
- Product line leaders and their relationships
- Team structures within groups
- Cross-functional partnerships
- Recent organizational changes

**When to Reference:**
- Understanding reporting relationships
- Preparing for leadership meetings
- Explaining org structure in context
- Tracking who's who in cross-functional work

---

## Work-Specific Queries

### "What should I be thinking about with my team?"

- Review development goals for each direct report
- Flag anyone who hasn't had a logged interaction recently
- Surface any patterns (someone consistently missing commitments, someone ready for a stretch opportunity)

### Additional behavior for "What do I know about [person]?"

When the person is a direct report, also show:
- Development focus and recent observations
- Performance evidence captured
- Last 1:1 date and topics

### Additional behavior for "How are we doing on our goals?"

For development goals specifically:
- Look for observations in recent interactions that relate to the development area
- Note if there haven't been opportunities to observe progress
- Flag if 1:1s or coaching conversations seem sparse

### Weekly Wrap (every Friday)

Triggered alongside the base system's weekly housekeeping.

**Format:** TBD (will be defined 2026-02-28).

---

## Work Defaults

- Default category for tasks and follow-ups: `work`
- Personal items tracked in a work context: keep context minimal, don't probe, don't connect to work goals

---

## Work People File Format

Work-specific person file example `areas/people/sprinkles/sprinkles.md`:
```
# Sprinkles

**Category:** Team (Direct Report)
**Role:** Senior Flavor Engineer
**Contact:** sprinkles@scoops.com

## Context
- Started 6 months ago
- Strong technical background in dairy science
- Growing into customer-facing role at tasting events

## Development Focus
- Building confidence running public tasting sessions
- Learning to escalate effectively with ingredient suppliers

## Recent Observations
- 2025-02-03: Ran the weekend tasting solo for the first time, great feedback
- 2025-01-28: Proactively flagged the vanilla bean shortage before it hit production [perf-evidence: Sprinkles]
```
