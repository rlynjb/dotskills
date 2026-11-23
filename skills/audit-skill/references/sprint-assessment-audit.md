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
Perform each skill's Q-01–Q-10 audit independently, show
as-is Mermaid workflows, and compare responsibility overlap.

Step 2: recommend B-xx boundaries with owner, non-owner,
decision authority and alternatives.
Step 3: also draft C-xx handoff contracts based on those
proposed boundaries. Label each dependency as CONDITIONAL.

Show Steps 1, 2 and 3 together BEFORE asking for my feedback.
Then let me approve, revise, reject or defer B/C decisions.
After relevant decisions are approved, prepare Step 4 validation
only—do not run either skill or edit files.
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

Every substantive finding needs direct links to actually inspected source lines. **Explain the consequence of each material overlap**: for example, two skills reading the same ticket can be fine, but two independently rewriting it may lead to inconsistent decisions. Only mark **OBSERVED RESULT** when a genuine authorized trace exists. A proposed integration is never an as-is workflow diagram.

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

- Each accessible skill receives its own ten-check Q-01–Q-10 assessment and ten six-field findings.
- As-is flows, evidence, proposals, human approvals and observed results remain distinct.
- The first response shows Step 1 findings, Step 2 B-xx proposals, and Step 3 C-xx proposals together before any approval request.
- One consolidated review accepts individual B/C approvals, revisions, rejections or deferrals and tracks dependencies. No approval is inferred from a checkbox, a favorable recommendation or a non-specific human remark.
- Open and deferred decisions block only dependent final contracts/readiness.
- No target execution, unauthorized source edits or live business-system effects occur within Audit Skill.
