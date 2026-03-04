# Work-Specific Instructions

This file extends the base memory system with behaviors specific to a professional/management context.

---

## Additional Files

| Path | Purpose |
|------|---------|
| `areas/organization.md` | Company organizational structure, reporting relationships, triad model |
| `areas/leadership-notes/` | Management playbooks, templates, and reference notes |

---

## Work People Categories

Categorize work contacts into these categories. The category affects how interactions are processed:

- **Direct reports:** Track development-relevant observations. Note coaching opportunities. Flag if 1:1s seem infrequent.
- **Cross-functional partners:** Track commitments as dependencies.
- **Leadership/boss:** Flag commitments and requests with higher priority. Note context that might matter for managing up.
- **External contacts:** Track by company/relationship. Note account context.

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
- 2025-02-03: Ran the weekend tasting solo for the first time, great feedback. [Waffles](../waffles/waffles.md) covered backup.
- 2025-01-28: Proactively flagged the vanilla bean shortage before it hit production [perf-evidence: Sprinkles]. Relevant to [Flavor Launch](../../projects/flavor-launch/flavor-launch.md).
```
