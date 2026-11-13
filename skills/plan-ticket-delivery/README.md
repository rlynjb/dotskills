# Plan Ticket Delivery

**Tracker-agnostic delivery planning after requirements and design reasoning.**

Use this skill to turn a feature brief or a [REAZN](../reazn/SKILL.md) assessment into a reviewable plan of **stories, subtasks, and an optional epic/parent**. It doesn't need Jira, an API connection, or a particular ticketing system.

## Where it fits

```text
Feature request
  → REAZN (SDI: requirements, verified design and contracts)
  → Plan Ticket Delivery (outcome-based work decomposition)
  → Team reviews and accepts plan
  → Separate tracker publishing / implementation
```

This is a **delivery handoff**, not a fifth SDI step. Light's proposed design does not become an approved decision by being copied into tickets.

## How decisions are made

- **One independently testable outcome:** normally one story. Add subtasks only when helpful.
- **Several independently testable outcomes:** multiple stories.
- **Broader initiative or release grouping:** consider a parent/epic if team conventions support it.
- **Cross-component implementation:** often subtasks inside one story, not separate frontend/backend/database stories.
- **Uncertain design or missing source:** show provisional tickets and the questions to resolve, not fabricated architecture or capabilities.

System size and dependencies affect **complexity, sequencing and confidence**, not the story count by themselves.

## What you get

1. Delivery Snapshot with recommended structure and rationale.
2. Proposed Ticket Tree with stable draft identifiers, not real tracker IDs.
3. Jira/Linear/GitHub-issue-friendly story drafts including outcome, acceptance criteria, technical notes, dependencies and readiness.
4. Source-to-ticket traceability using `FR/NFR/D` and contract identifiers from the supplied design assessment.
5. Open decisions or blockers for a team to resolve.

## Example

If the source says **"Export assessment results as CSV"**, the default is **one export story** (plus implementation subtasks if useful), even when UI and backend both change.

Only add separate stories such as export history or export scheduling if those are **explicitly supported additional requirements**. A large system doesn't authorize adding features.

## Invocation

```text
Run plan-ticket-delivery using my feature requirements and
reazn report. Create a tracker-agnostic
draft plan with stories, subtasks and an epic only if justified.
Trace acceptance criteria to source FR/NFR and design/contract decisions.
Mark anything unverified or awaiting approval.
Do not publish or modify actual tickets.
```

## Limits

This skill drafts delivery tickets; it does **not** create them, estimate story points, assign developers, change code, or approve designs. Tracker publishing is a separately authorized workflow. The canonical instructions are in [`SKILL.md`](SKILL.md); [`evals/evals.json`](evals/evals.json) contains proposed behavioral evaluation cases (not claims of executed tests).
