# Worked example — Sprint Assessment and Refine Requirements

This is an **illustrative conversation guide** for the [Audit Skill](../SKILL.md) four-step workflow. It is **not** an audit result, an approved integration, a verified skill contract, or authority to run either skill.

**Audience:** a junior developer. A senior-engineer-style review should explain what each issue means, why it affects the workflow, the recommended solution and what the developer should decide or test. Explain terms such as *owner*, *handoff*, *invariant* and *trace* when first used; don't simply output labels.

## Starting prompt

```text
Use audit-skill on Sprint Assessment and Refine Requirements.

Treat me as a junior developer learning these skills.
Explain important findings and recommendations like a senior
engineer: what you found, why it matters, a proposed improvement,
and how I can decide or verify it.

Step 1: inspect both SKILL.md files and their material references,
including agent definitions, relevant permissions, output formats,
failure paths and any existing evaluations. Cite actual source lines.
For each skill, explicitly organize Step 1 into:
Inputs, Responsibilities, Outputs, Handoffs, Boundaries,
Feedback. Use Observed / Evidence / Open question for each.
Then do Q-01–Q-10, as-is Mermaid flows and cross-skill comparison.

Step 2: recommend B-xx boundaries with owner, non-owner,
decision authority and alternatives.
Step 3: also draft C-xx handoff contracts based on those
proposed boundaries. Label each dependency as CONDITIONAL.

Show Steps 1, 2 and 3 together BEFORE asking for my feedback.
Then let me approve, revise, reject or defer B/C decisions.
After the consolidated review, show a brief Step 4
Validation Readiness (NOT EXECUTED) summary. Prepare
detailed validation after relevant decisions are approved;
do not run either skill or edit files.
```

## Step 1 — Skill Responsibility & Overlap Assessment (example structure)

**Use the same six headings for EACH skill.** These questions guide evidence gathering; they are **not** verified answers. Under each heading in a real audit, fill out `Observed`, `Evidence` (actual source links/lines), and `Open question`. Start by observing, questioning assumptions and validating the source—**don't choose an architecture here**.

### Sprint Assessment — six considerations to investigate

**01 — Inputs:** Where do Jira items, prior assessments, evidence and worker configuration come from? Which are truly required?

**02 — Responsibilities:** Does this skill decide sprint readiness, estimates, or both? Who owns any delegated work and its aggregation?

**03 — Outputs:** What assessment, score/status, evidence, unresolved issues or error results does it promise to return?

**04 — Handoffs:** Does it consume another skill's output, and what fields must remain intact? Is its result passed to another stage or only reported to a human?

**05 — Boundaries:** Which decisions need human approval? Are Jira modifications prohibited in instructions only, or technically enforced by the runtime?

**06 — Feedback:** If requirements or dependencies are insufficient, who receives the issue? Is that return/escalation path documented or still unknown?

### Refine Requirements — six considerations to investigate

**01 — Inputs:** What triggers refinement, and which tickets, documents, code, evidence or previous outputs are needed?

**02 — Responsibilities:** Does it assess requirements completeness and technical concerns, or also authorize product decisions?

**03 — Outputs:** What findings, functional/nonfunctional requirements, acceptance criteria, assumptions or open questions does it produce?

**04 — Handoffs:** How could its assessment be consumed by Sprint Assessment or another skill? Is such a relationship actually documented?

**05 — Boundaries:** What changes or approvals are excluded? What should happen when a stakeholder decision remains unresolved?

**06 — Feedback:** If a later stage finds a missing or contradictory requirement, is there an identified owner and evidence-based return path?

### Cross-skill Responsibility & Overlap

After the two independent six-consideration summaries, compare the source-backed relationship:

- Who owns **requirements clarity** versus **sprint readiness**?
- Is reviewing acceptance criteria **shared information** or **duplicated final decision authority**?
- Which identity, evidence links, unresolved questions and permission state must survive a handoff?
- If one item or worker fails, is its result clearly separated from the rest?
- If Sprint Assessment finds a requirements gap, does the documented flow identify who reconsiders it? If not, report **feedback-routing gap / NOT VERIFIED** and propose a route later, not as a fact.

**Diagram readability:** For each skill's as-is Mermaid flow, use complete 2–4-word node labels, split longer labels with quoted `<br/>` line breaks, and explain abbreviated nodes under **Node explanations**. Do not shrink fonts or omit decisions to fit a narrow viewer.

Every real observation requires actual inspected source lines. Explain the consequence of each material gap in junior-friendly language. Only mark **OBSERVED RESULT** when a genuine authorized trace exists. Keep proposed integration separate from the as-is flow.

### Supporting Quality Checks (Q-01–Q-10)

Include each target's ten Q-01–Q-10 statuses and material source-backed explanations. These are evidence/quality checks **supporting the six considerations**, not a second six-part investigation. Keep detailed six-field findings available for justified gaps or follow-up.

## Step 2 — example boundary recommendation (not approved)

**B-01 — Requirements clarity versus sprint readiness**

- *Current evidence:* Insert the exact source links after inspecting both skills; otherwise mark NOT VERIFIED.
- *Recommendation:* Refine Requirements owns detailed clarification; Sprint Assessment consumes its conclusions for sprint readiness and reports missing requirements without silently deciding them.
- *Ownership exclusion:* Sprint Assessment does not rewrite acceptance criteria merely to make a ticket appear ready.
- *Why this matters:* If both skills can change what the requirements mean, the next person may not know which conclusion to trust. Giving one skill the clarification responsibility makes that decision easier to trace.
- *Alternative:* Both skills independently assess clarity, which may be flexible but increases rework and the chance of inconsistent judgments.
- *Status:* PROPOSED.

**Continue directly to Step 3:** show the proposed contract that would result from this B-01 recommendation. Do not pause for a decision yet.

## Step 3 — example contract (conditional on B-01)

**C-01 — Refine Requirements → Sprint Assessment**

- *Trigger:* the relevant requirements assessment and human decisions are available.
- *Required inputs:* ticket identity, assessed requirements/acceptance criteria, original evidence links, unresolved questions, explicit readiness/clarity conclusions, and approval state where relevant.
- *Output/consumer behavior:* Sprint Assessment can determine sprint readiness using this evidence, or mark the ticket BLOCKED/NEEDS HUMAN when critical inputs are missing.
- *Invariants (things that must stay true):* preserve original ticket identity, evidence provenance, open questions and decisions; do not fabricate missing acceptance criteria.
- *Error behavior:* if the upstream output is absent or incompatible, preserve the failure with a human-facing reason rather than silently continue.
- *Security:* least privilege, no unapproved Jira writes or transfer of confidential source data.
- *Why this matters:* If a ticket has an unresolved question and the next skill does not receive it, the workflow might incorrectly mark the ticket ready. This contract makes the question visible at the next step.
- *Status in initial overview:* PROPOSED — CONDITIONAL ON B-01 (not approved).

**Consolidated human review — after Step 3:** present B-01 and C-01 together, with dependencies. Explain that *approve* accepts the exact proposal, *revise* changes it, *reject* declines it and *defer* leaves it open. The human may decide on either item or explicitly approve both as a compatible set. If the boundary changes, explain why the dependent contract may also change and request confirmation. Do not claim implementation from design approval.

## Step 4 — example validation handoff (not executed)

With approved B/C decisions, construct a **sanitized** representative Jira fixture with at least the scenarios below. Explain validation as a **Given / When / Then** experiment: given a ticket with missing requirements, when the approved skills process it in a separately authorized environment, then the unresolved question should stay visible and the ticket should not silently become ready.

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

- Each accessible skill receives the same **six numbered considerations**, each with `Observed / Evidence / Open question`, and a separate ten-check Q-01–Q-10 quality assessment. Material findings remain junior-friendly without burying Steps 1–3.
- As-is flows, evidence, proposals, human approvals and observed results remain distinct.
- The first response shows Step 1 findings, Step 2 B-xx proposals, and Step 3 C-xx proposals together before any approval request.
- One consolidated review accepts individual B/C approvals, revisions, rejections or deferrals and tracks dependencies. No approval is inferred from a checkbox, a favorable recommendation or a non-specific human remark.
- Open and deferred decisions block only dependent final contracts/readiness.
- No target execution, unauthorized source edits or live business-system effects occur within Audit Skill.
