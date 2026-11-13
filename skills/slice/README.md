# SLICE

**Tracker-agnostic delivery planning after requirements and design reasoning.**

Use this skill to turn a feature brief or a [REAZN](../reazn/SKILL.md) assessment into a reviewable plan of **stories, subtasks, and an optional epic/parent**. It doesn't need Jira, an API connection, or a particular ticketing system.

## Where it fits

```text
Feature request
  → REAZN (SDI: requirements, verified design and contracts)
  → SLICE (outcome-based work decomposition)
  → Team reviews and accepts plan
  → Separate tracker publishing / implementation
```

This is a **delivery handoff**, not a fifth SDI step. REAZN's proposed design does not become an approved decision by being copied into tickets.

## How decisions are made

- **One independently testable outcome:** normally one story. Add subtasks only when helpful; explain the boundary in a short **Slicing rationale**.
- **Several independently testable outcomes:** multiple stories.
- **Broader initiative or release grouping:** consider a parent/epic if team conventions support it.
- **Cross-component implementation:** often subtasks inside one story, not separate frontend/backend/database stories.
- **Standalone technical Task:** use only when the prerequisite or operational work has independent completion evidence and a justified reason to track it separately; otherwise it's a subtask or implementation note. The final Jira type depends on team conventions.
- **Uncertain design or missing source:** show provisional tickets and the questions to resolve, not fabricated architecture or capabilities.

**Decision order:** **vertical slicing** defines outcome boundaries → **Story/Task/Subtask** classification follows independent completion evidence → **INVEST** checks whether each proposed Story is well formed → **Slicing rationale** explains why that boundary was chosen. INVEST means Independent, Negotiable, Valuable, Estimable, Small, Testable; it is a qualitative guideline, not an official Jira mandate or a scoring formula. Mark weak or unverified dimensions instead of inventing clarity.

System size and dependencies affect **complexity, sequencing and confidence**, not the story count by themselves.

## What you get

1. Delivery Snapshot with recommended structure and rationale.
2. Proposed Ticket Tree with stable draft identifiers (`ST-xx` stories, `TK-xx` standalone tasks, `SUB-xx` subtasks, etc.), not real tracker IDs.
3. Jira/Linear/GitHub-issue-friendly drafts including each Story's **Slicing rationale** and compact **INVEST quality check**, outcome, **keyed acceptance criteria (`AC-01`, `AC-02`, ... per ticket)**, technical notes, dependencies and readiness.
4. Source-to-ticket traceability using `FR/NFR/D` and contract identifiers from the supplied design assessment, with unambiguous ticket/criterion references such as `ST-01/AC-01`.
5. Open decisions or blockers for a team to resolve.

## Example

If the source says **"Export assessment results as CSV"**, the default is **one export story** (plus implementation subtasks if useful), even when UI and backend both change.

Only add separate stories such as export history or export scheduling if those are **explicitly supported additional requirements**. A large system doesn't authorize adding features.

## Story-quality review — INVEST

Check all six letters for each proposed **Story**: **I**ndependent, **N**egotiable, **V**aluable, **E**stimable, **S**mall and **T**estable. A Story can span UI, API and storage while remaining one outcome. If the story boundary is wrong, revise it; if requirements are missing, preserve the uncertainty and mark the item provisional.

Output only **one concise** `_INVEST:_` field per Story: `ALIGNED` with a grounded reason, `NEEDS REFINEMENT` naming the weak letter(s), or `NOT VERIFIED` explaining what cannot be judged. This complements `_Slicing rationale:_`, which explains the boundary. Neither INVEST nor the rationale automatically approves a Jira item. For standalone technical Tasks, justify independent completion/tracking rather than forcing user-story INVEST criteria.

## Acceptance criterion labels

Within each Ticket Draft, output each acceptance check as `AC-01:`, `AC-02:`, etc. instead of repeating `Acceptance:`. Number sequentially from `AC-01` **inside each story**, restarting for the next ticket. Use `ST-01/AC-01` when cross-referencing a particular criterion. Keep the same compact, consecutive field layout and match other labels' Markdown styling (for example, `_AC-01:_` when labels are italic). Do not replace existing source criteria identifiers or claim these draft IDs are live tracker IDs.

```markdown
**ST-01 — Export assessment results as CSV**  
_Type:_ Story  
_Outcome:_ Users can export assessment results as CSV.  
_Slicing rationale:_ One end-to-end user outcome; UI and API pieces are implementation steps of the same story.  
_INVEST:_ NEEDS REFINEMENT — T: the required CSV fields need confirmation.  
_AC-01:_ The export produces a CSV file.  
_AC-02:_ The CSV contains the requested assessment results.  
_Readiness:_ PROVISIONAL
```

## Invocation

```text
Run slice using my feature requirements and
reazn report. Create a tracker-agnostic
draft plan with stories, subtasks and an epic only if justified.
Use vertical slicing for ticket boundaries; give each Story a
slicing rationale and a concise INVEST quality result.
Key acceptance criteria as AC-01, AC-02, etc. per ticket; trace them to source FR/NFR and design/contract decisions.
Mark anything unverified or awaiting approval.
Do not publish or modify actual tickets.
```

## Limits

This skill drafts delivery tickets; it does **not** create them, estimate story points, assign developers, change code, or approve designs. Tracker publishing is a separately authorized workflow. The canonical instructions are in [`SKILL.md`](SKILL.md); [`evals/evals.json`](evals/evals.json) contains proposed behavioral evaluation cases (not claims of executed tests).
