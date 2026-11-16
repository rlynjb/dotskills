# Sprint Assessment × REAZN — Proposed Engineering Design Meeting Agenda

**Meeting objective:** Understand the current state of Sprint Assessment, discuss whether integrating REAZN aligns with the project's direction, and identify opportunities to contribute to its design, reliability, and evaluation.

**Approach:** Discovery first → Clarify requirements → Discuss options → Agree on next steps.

## Table of Contents

1. [Sprint Assessment + REAZN Integration](#1-sprint-assessment--reazn-integration)
2. [Contracts Between Sprint Assessment and REAZN](#2-contracts-between-sprint-assessment-and-reazn)
3. [REAZN Design and Audit Skill Findings](#3-reazn-design-and-audit-skill-findings)
4. [Security, Trust Boundaries, and AgentCon/MCP Con 2026](#4-security-trust-boundaries-and-agentconmcp-con-2026)
5. [Evaluation Strategy and Evaluate Skill](#5-evaluation-strategy-and-evaluate-skill)
6. [Closing Discussion — Aligning on Next Steps](#closing-discussion--aligning-on-next-steps)

---

## 1. Sprint Assessment + REAZN Integration

### Context

Sprint Assessment processes Jira tickets in batches of potentially 10–50. I'd like to understand its current workflow and what problem REAZN would solve before discussing integration.

### Questions to discuss

**Main question:**

> Can we walk through how Sprint Assessment currently processes Jira tickets in a batch, and where we see REAZN potentially fitting into that workflow?

**Follow-up questions:**

- How does Sprint Assessment currently assess each ticket, and what does it return?
- What specific problem are we hoping REAZN will solve?
- Is the plan to invoke REAZN for every ticket or only when deeper analysis is needed?

### Possible integration approaches to explore

**Option A — REAZN evaluates every ticket**

Every Jira ticket in the batch receives a complete REAZN assessment.

*Potential benefit:* Consistent design analysis across tickets.

*Potential trade-off:* Increased execution time, token usage, and potentially unnecessary analysis.

**Option B — Selective REAZN dispatch**

Sprint Assessment evaluates each ticket first and invokes REAZN only when predefined criteria are met.

*Possible triggers:*

- Ambiguous or incomplete requirements
- Missing acceptance criteria
- Cross-system dependencies
- Security-sensitive changes
- Unclear interfaces or architectural risks

*Potential benefit:* More focused use of deeper reasoning.

*Potential trade-off:* Sprint Assessment needs a reliable mechanism for determining when REAZN is necessary, and incorrect routing could miss important issues.

**Option C — Keep the skills independent initially**

Continue using Sprint Assessment and REAZN separately while gathering evidence about whether an automated integration would add value.

*Potential benefit:* Avoids introducing orchestration complexity before confirming the need.

### What I'd like us to establish

- The current Sprint Assessment workflow
- The specific problem REAZN integration would solve
- Whether integration is an agreed direction or still exploratory
- Which dispatch approaches are worth evaluating
- What additional evidence is needed before choosing an approach

**My consideration:** I'd lean toward evaluating selective dispatch, but only after understanding Sprint Assessment's current capabilities and the intended integration outcomes.

---

## 2. Contracts Between Sprint Assessment and REAZN

### Context

If integration moves forward, we should clarify what Sprint Assessment sends to REAZN, what REAZN returns, and which skill owns each responsibility.

### Questions to discuss

**Main question:**

> If we move forward with integrating Sprint Assessment and REAZN, what contracts would we need to establish between the two skills, and are any of these contracts already defined?

**Follow-up questions:**

- Which skill owns the workflow and the final assessment?
- What inputs should Sprint Assessment pass to REAZN, and what output should it receive?
- How should the workflow handle missing information or an incomplete REAZN assessment?

### Contract areas to discuss

These are **three discussion categories**, not an official industry-standard framework or agreed requirements. First, check whether the team already has a handoff pattern to reuse.

| Area | Focus | Coverage |
| --- | --- | --- |
| **A. Interface Contract** | Inputs, outputs, and errors | Input, Output, Status |
| **B. Responsibilities & Orchestration** | Dispatch and workflow ownership | Trigger, Processing, Ownership |
| **C. Reliability & Verification** | Failures, evidence, and testing | Traceability, Failure behavior |

### Industry references versus proposed design

**Established practices to consult (when applicable):**

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — describing structured request and response interfaces when an API is actually involved.
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html) — a standardized approach to HTTP error responses, if the integration uses HTTP.
- [Pact documentation](https://docs.pact.io/) — consumer-provider contract testing for independently implemented components.
- [W3C Trace Context](https://www.w3.org/TR/trace-context/) — propagating trace identifiers across services when distributed tracing is relevant.

**Proposed for this project, not prescribed by those standards:** Selective dispatch, the exact ticket-to-REAZN fields, which skill owns aggregation, the assessment status names, and the handling of partial batch failures. These decisions depend on Sprint Assessment's existing implementation and execution environment.

### Example scenario

Suppose a Jira ticket requires users to export assessment results as CSV, but a generated assessment describes PDF export.

We could discuss:

1. Should Sprint Assessment detect that discrepancy independently?
2. Should the discrepancy trigger REAZN?
3. What evidence would REAZN receive?
4. What should REAZN return to indicate the mismatch?
5. Would that result affect Sprint Assessment's score, produce an additional finding, or require human review?

This would help us work through the contract using a concrete example.

### What I'd like us to establish

- Whether a formal handoff contract is necessary for the proposed integration
- Existing contracts or patterns we can reuse
- Responsibility and ownership boundaries
- Required versus optional input/output fields
- Failure-handling expectations
- Any unresolved design decisions

**My consideration:** I would prefer explicit, testable contracts if we proceed with an automated integration, but I want to understand the existing architecture before proposing a specific schema.

---

## 3. REAZN Design and Audit Skill Findings

### Context

REAZN uses the four-step SDI framework, while Audit Skill reviews documented design and evidence gaps. I'd like to see whether these capabilities fit Sprint Assessment's needs.

### Questions to discuss

**Main question:**

> Would it be helpful if I walked through how I've structured REAZN and the engineering review approach I've been using, so we can evaluate whether its capabilities fit Sprint Assessment's needs?

**Follow-up questions:**

- What level of requirements and design analysis does Sprint Assessment need?
- Does REAZN's current four-step approach and output meet that need?

### REAZN's current design

REAZN uses four SDI steps:

**Step 1 — Requirements & Scope**

Identify functional requirements, non-functional requirements, assumptions, missing information, and scope boundaries.

**Step 2 — Existing Patterns & High-Level Design**

Review available evidence about the current system, examine existing patterns, and explain potential architectural approaches.

**Step 3 — Design Deep Dive**

Examine interfaces, responsibilities, data flow, contracts, expected behavior, invariants, and guarantees.

**Step 4 — Risks & Trade-offs**

Identify alternatives, risks, mitigations, unresolved decisions, and verification needs.

REAZN can assess Jira requirements, repository changes, existing implementations, agent skills, or system/workflow descriptions. It is designed to produce a read-only assessment, with evidence and uncertainty explicitly identified.

### Additional Engineering Research (Ongoing)

I'm also developing Audit Skill to review agent skill design and engineering practices, although I haven't evaluated its reliability yet.

Separately, I've been reviewing my AgentCon/MCP Con 2026 session notes and external resources, including [GitHub's guidance on reusable agent skills](https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/), to identify potentially useful engineering practices.

For now, I'd like to prioritize understanding and validating REAZN and Sprint Assessment. If we identify areas where additional research would help, I can bring those findings into future discussions.

### What I'd like us to establish

- Whether REAZN's design meets the integration's intended needs
- Any capabilities that should remain independent
- Whether an audit of both skills would be useful
- Which existing engineering patterns or requirements should take priority
- Which findings deserve further investigation

**My consideration:** I can share the REAZN documentation and relevant audit findings as engineering evidence, without assuming the integration needs to adopt every part of my skill's design.

---

## 4. Security, Trust Boundaries, and AgentCon/MCP Con 2026

### Context

My AgentCon/MCP Con 2026 materials cover security, trust boundaries, and reliability. I'd like to understand existing team practices before recommending additional work.

### Questions to discuss

**Main question:**

> Have we established any security, trust-boundary, or reliability requirements for Sprint Assessment and our other skills, or is that something we're considering as part of their development?

**Follow-up questions:**

- What security and trust boundaries are already established for these skills?
- Are there gaps where additional research or conference findings would be useful?

### Potential conference material

**Don't Share the Database: Interface Contracts Between Isolated AI Agents**

*Possible relevance:* Narrow contracts, context isolation, and explicit handoffs.

**Trustworthy Context Is Untrusted by Default**

*Possible relevance:* Source provenance, stale context, prompt injection, and validation against authoritative sources.

**When Agents Spawn Agents: Securing Recursive Delegation**

*Possible relevance:* Least-privilege delegation and authorization boundaries, if the architecture involves separately authorized agents.

### What I'd like us to establish

- Existing security and reliability requirements
- Whether additional trust-boundary analysis is needed
- Whether the team is open to incorporating relevant conference findings
- Which topics are worth investigating
- Whether this work is appropriate for the current project phase

**My consideration:** If these areas are relevant to our next steps, I can review the original conference sessions, document applicable recommendations, and bring back evidence for the team to consider rather than immediately changing the skills.

---

## 5. Evaluation Strategy and Evaluate Skill

### Context

I'm developing Evaluate Skill for repeatable behavioral testing. I'd like to understand how Sprint Assessment is currently validated and whether executable evals align with team priorities.

### Questions to discuss

**Main question:**

> How are we currently validating Sprint Assessment and our other skills, and are we considering introducing automated or repeatable evaluations as part of the development process?

**Follow-up questions:**

- How are Sprint Assessment and REAZN currently tested or validated?
- What evidence would show that the skills and their integration work as expected?
- Are executable evaluations a priority for this project?

### How Evaluate Skill could contribute

Evaluate Skill is designed to guide evaluation development through a human-reviewed workflow.

It supports:

- Defining expected behavior
- Recommending test cases
- Allowing reviewers to revise or provide their own cases
- Preparing evaluation inputs and assertions
- Configuring controlled evaluation execution
- Reviewing results and failures
- Supporting regression analysis

Its current execution architecture includes Promptfoo and the Codex SDK, with offline-tested components. Live Docker isolation and end-to-end model execution are not yet verified, so I'd present it as ongoing tooling development rather than an established production evaluation system.

### Possible evaluation examples

**Case 1 — Clear requirements**

A ticket contains complete requirements and acceptance criteria.

*Question:* Does Sprint Assessment handle the ticket appropriately without unnecessary additional analysis?

**Case 2 — Ambiguous requirements**

A ticket contains missing or conflicting requirements.

*Question:* If selective dispatch is agreed, does the workflow correctly invoke REAZN?

**Case 3 — Missing context**

A ticket references repository behavior that the skill cannot verify.

*Question:* Does REAZN explicitly report the missing evidence instead of making unsupported assumptions?

**Case 4 — Failed handoff**

REAZN returns an incomplete result or fails during processing.

*Question:* Does Sprint Assessment preserve the failure status and appropriately handle the remaining tickets?

**Case 5 — Batch processing**

Sprint Assessment receives 20 tickets with different levels of complexity.

*Question:* Are the correct tickets assessed, correctly associated with their results, and included in the consolidated output?

These are candidate scenarios, not finalized requirements. Actual expected behavior depends on the integration design we agree to.

### What I'd like us to establish

- Existing evaluation methods and available evidence
- Whether automated evaluations are a current priority
- Whether a small proof of concept would be useful
- Which skill or workflow should be evaluated first
- What success would look like
- How I could contribute to developing evaluation cases and infrastructure

**My consideration:** If the team is interested, I'd suggest starting with a small evaluation suite using representative Jira tickets, comparing expected and observed behavior, and expanding only after we have reliable evidence from those initial tests.

---

## Closing Discussion — Aligning on Next Steps

Before ending the meeting, I'd like to summarize what we've learned and confirm which items, if any, we want to move forward with.

### Questions to close with

1. Based on what we've discussed, what should we prioritize next for Sprint Assessment?
2. Which parts of the REAZN integration are already decided, and which are still open?
3. Are there areas where additional engineering review, conference research, or evaluations would be helpful?
4. What would be the most useful thing for me to contribute before our next discussion?

### Expected meeting outcomes

The goal isn't necessarily to finalize an integration architecture or commit to new development work immediately.

A useful outcome would be a shared understanding of:

- **Current state:** What exists and how it works today.
- **Intended direction:** What the team wants to accomplish.
- **Open questions:** What still needs evidence or decisions.
- **Possible contributions:** Where my work on REAZN, Audit Skill, conference research, or Evaluate Skill could help.
- **Next steps:** Only the follow-up work we've agreed is worthwhile.

**Guiding principle:** Understand the problem and existing system before proposing a solution. Distinguish observed behavior from assumptions, and treat proposed designs as options until they're reviewed and agreed upon.
