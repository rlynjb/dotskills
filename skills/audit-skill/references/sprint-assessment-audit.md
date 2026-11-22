# Worked example — Sprint Assessment and Refine Requirements

This is an **illustrative conversation guide** for the [Audit Skill](../SKILL.md) four-step workflow. It is **not** an audit result, an approved integration, a verified skill contract, or authority to run either skill.

## Starting prompt

```text
Use audit-skill on Sprint Assessment and Refine Requirements.

Step 1: inspect both SKILL.md files and their material references,
including agent definitions, relevant permissions, output formats,
failure paths and any existing evaluations. Cite actual source lines.
Perform each skill's Q-01–Q-10 audit independently, show
as-is Mermaid workflows, and compare responsibility overlap.

Step 2: recommend B-xx boundaries with owner, non-owner,
decision authority and alternatives. Stop at Gate A for my input.

When I approve those boundaries, draft C-xx handoff contracts
and stop at Gate B. After approval, prepare the validation
checklist only—do not run either skill or edit files.
```

## Step 1 — inspect the *as-is* responsibilities

Questions to investigate from source (do not presume the answers):

### Sprint Assessment

- How are Jira items discovered, grouped, dispatched, assessed and aggregated?
- Does the actual source direct one worker per ticket? How do dynamic workers differ from reusable agent files?
- What criteria determine estimation and sprint readiness?
- What happens if one ticket is missing evidence, a worker fails or a batch partially completes?
- Does the host enforce read/write restrictions, or are they only written in natural language?

### Refine Requirements

- What triggers the assessment and defines its scope?
- Which requirements, acceptance-criteria, architecture and source-evidence checks does it own?
- What are the declared outputs, stop conditions, human approvals and prohibited actions?
- Does the skill have an actual documented handoff, or only an informal suggestion?

### Relationship comparison

- Who owns requirements **clarity** versus sprint **readiness**?
- Is an acceptance-criteria review shared context or duplicated decision authority?
- Where should unresolved questions, evidence links and confidence information flow?
- Can one item fail without losing successful assessment of other items?
- Which contract parts are host-independent, and which tool/worker operations require a runtime adapter?

Every substantive finding needs direct links to actually inspected source lines. Only mark **OBSERVED RESULT** when a genuine authorized trace exists. A proposed integration is never an as-is workflow diagram.

## Step 2 — example boundary recommendation (not approved)

**B-01 — Requirements clarity versus sprint readiness**

- *Current evidence:* Insert the exact source links after inspecting both skills; otherwise mark NOT VERIFIED.
- *Recommendation:* Refine Requirements owns detailed clarification; Sprint Assessment consumes its conclusions for sprint readiness and reports missing requirements without silently deciding them.
- *Ownership exclusion:* Sprint Assessment does not rewrite acceptance criteria merely to make a ticket appear ready.
- *Alternative:* Both skills independently assess clarity, which increases rework and inconsistent judgments.
- *Status:* PROPOSED.

**Gate A — ask the human:** Approve B-01, revise its owner/exclusion, reject it, or defer it. If revised, restate the **revised** decision for confirmation. Do not automatically pick a winner because the recommendation sounds reasonable.

## Step 3 — example contract (conditional on B-01)

**C-01 — Refine Requirements → Sprint Assessment**

- *Trigger:* the relevant requirements assessment and human decisions are available.
- *Required inputs:* ticket identity, assessed requirements/acceptance criteria, original evidence links, unresolved questions, explicit readiness/clarity conclusions, and approval state where relevant.
- *Output/consumer behavior:* Sprint Assessment can determine sprint readiness using this evidence, or mark the ticket BLOCKED/NEEDS HUMAN when critical inputs are missing.
- *Invariants:* preserve original ticket identity, evidence provenance, open questions and decisions; do not fabricate missing acceptance criteria.
- *Error behavior:* if the upstream output is absent or incompatible, preserve the failure with a human-facing reason rather than silently continue.
- *Security:* least privilege, no unapproved Jira writes or transfer of confidential source data.
- *Status:* PROPOSED if B-01 was explicitly approved; otherwise CONDITIONAL — BLOCKED BY B-01.

**Gate B — ask the human:** Approve C-01, revise its fields/guarantees, reject it, or defer it. Don't claim approval or implementation from a proposed contract.

## Step 4 — example validation handoff (not executed)

With approved B/C decisions, construct a **sanitized** representative Jira fixture with at least:

- One ticket with adequate evidence.
- One ticket missing a required acceptance criterion.
- One simulated partial failure or missing downstream dependency, when applicable.

For a separately authorized Codex or Evaluate Skill run, check:

- Correct decisions are made by the correct skill.
- Required handoff fields, citations and open questions survive.
- The incomplete ticket remains explicitly BLOCKED or NEEDS HUMAN rather than repaired by guesswork.
- A failed item does not silently erase successful items.
- Tool permissions and human approvals remain respected.
- The output records trace and error evidence where available.

Audit Skill can later **read** the genuine run artifacts and compare observed-versus-expected behavior, but it **cannot execute** these cases itself. Check [Evaluate Skill](../../evaluate-skill/SKILL.md) for the current authorization and execution constraints.

## Acceptance criteria for the guided review

- Each accessible skill receives its own ten-check Q-01–Q-10 assessment and ten six-field findings.
- As-is flows, evidence, proposals, human approvals and observed results remain distinct.
- Boundary decisions have B-xx IDs, options and a real Gate A; contract decisions have C-xx IDs and a real Gate B.
- No approval is inferred from a checkbox, a favorable recommendation or a non-specific human remark.
- Open and deferred decisions block only dependent final contracts/readiness.
- No target execution, unauthorized source edits or live business-system effects occur within Audit Skill.
