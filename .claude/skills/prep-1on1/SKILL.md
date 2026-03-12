---
name: prep-1on1
description: Make sure to use this skill whenever the user asks to prep for a 1:1, asks "what do I know about [person]?", works on development plans, or asks about team oversight. Trigger this skill even if they just mention an upcoming meeting with a team member.
argument-hint: "[person name]"
---

# 1:1 Prep and People Context

This skill has several modes. The data-heavy ones (1:1 prep, person lookup, team overview) delegate to a subagent so the raw file contents stay out of the main conversation. The interactive one (development conversations) stays inline.

## Prep for a 1:1

For: $ARGUMENTS

Spawn a subagent using the Agent tool:

```
Follow the instructions in {skill_dir}/agents/researcher.md.

Person: {person_name}
Today's date: {date}
Working directory: {working_dir}
```

When the subagent returns the prep document:
1. Present it to the user
2. Ask if they want to adjust topics, add anything, or go deeper on a section
3. Keep the conversation focused on prep, not on rehashing raw data

The prep is a starting point for the conversation, not a script. Remind the user to leave space for what the person brings.

---

## "What do I know about [person]?"

Spawn the same researcher subagent — same prompt, same sources. When it returns, present the relevant sections:

- Person context (role, relationship, current focus)
- Recent interactions
- Open follow-ups and tasks involving them
- For direct reports: development focus, performance evidence, last 1:1 date

Skip the agenda and coaching sections — this is a lookup, not meeting prep.

---

## "What should I be thinking about with my team?"

Spawn one researcher subagent per direct report, in parallel. Collect the results, then synthesize across the team:

- Who hasn't had a logged interaction recently?
- Anyone with overdue follow-ups or stalled commitments?
- Development goal progress across the team
- Patterns worth noting (someone consistently missing commitments, someone ready for a stretch)

Present as a team-level summary, not individual prep docs.

---

## People Development Conversations

This mode is interactive — keep it in the main conversation. Don't delegate to a subagent.

When development plans for a direct report need to be worked on:

1. **Pull up current context** — read their file in `areas/people/` and check `areas/goals.md` for their development goals. This is a small read, fine to do inline.
2. **Explore the development area:**
   - What's the gap or opportunity?
   - What does "better" look like?
   - What situations or experiences would help them grow?
   - How will progress be recognized?
3. **Make it actionable:** What's the next thing to do? Create an opportunity? Have a conversation? Give feedback?
4. **Connect to ongoing work:** Are there upcoming projects or interactions where this development focus is relevant?
5. **Confirm and save** to both `areas/people/[person].md` (development focus) and `areas/goals.md` (development goals section)
