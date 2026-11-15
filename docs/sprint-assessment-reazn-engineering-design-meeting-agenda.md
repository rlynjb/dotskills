# Sprint Assessment × REAZN — Proposed Engineering Design Meeting Agenda

**Meeting objective:** Understand the current state of Sprint Assessment, discuss whether integrating REAZN aligns with the project's direction, and identify opportunities to contribute to its design, reliability, and evaluation.

**Approach:** Discovery first → Clarify requirements → Discuss options → Agree on next steps.

---

## 1. Sprint Assessment + REAZN Integration

### Context

Sprint Assessment processes Jira tickets in batches, potentially 10, 20, or 50 tickets.

Before assuming that REAZN should be integrated into the workflow, I'd like to understand how Sprint Assessment currently processes these tickets, what its existing assessment capabilities are, and what problems we want the integration to solve.

### Questions to discuss

**Main question:**

> Can we walk through how Sprint Assessment currently processes Jira tickets in a batch, and where we see REAZN potentially fitting into that workflow?

**Follow-up questions:**

- How does Sprint Assessment currently assess each ticket? Does it perform a deeper analysis or primarily evaluate ticket readiness?
- What does Sprint Assessment currently return for each ticket? A score, individual findings, recommendations, or a consolidated batch report?
- What specific gap or limitation are we hoping REAZN will address?
- Are we considering dispatching REAZN for every ticket, or only for tickets that require deeper analysis?
- If selective dispatch is preferred, how would Sprint Assessment determine which tickets need REAZN?
- Are there any performance, cost, or execution constraints we should consider when processing larger batches?

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

If we decide to integrate both skills, I think it would be useful to define their responsibilities and the contract governing how they communicate.

In particular, I'd like to understand what Sprint Assessment would pass to REAZN, what REAZN is expected to return, and how Sprint Assessment would consume those results.

### Questions to discuss

**Main question:**

> If we move forward with integrating Sprint Assessment and REAZN, what contracts would we need to establish between the two skills, and are any of these contracts already defined?

**Follow-up questions:**

- Which skill should own the overall assessment workflow?
- What information does REAZN need to perform a reliable assessment?
- Should REAZN return its complete SDI report or a smaller structured result?
- How would Sprint Assessment incorporate REAZN's findings into the final assessment?
- What should happen when required context is missing or REAZN cannot complete an assessment?
- What existing conventions or contracts should we reuse?

### Proposed contract areas for discussion

These are illustrative definitions, not agreed requirements or confirmed existing behavior.

| Contract area | Proposed definition | Example |
| --- | --- | --- |
| **Trigger** | Conditions determining whether REAZN should be invoked. | A Jira ticket lacks clear acceptance criteria or involves changes across multiple services. |
| **Input** | Information Sprint Assessment passes to REAZN. | Ticket ID, description, acceptance criteria, relevant repository context, and requested scope. |
| **Processing** | The assessment REAZN is expected to perform. | Evaluate the ticket using the four SDI steps, identifying requirements, architecture, contracts, and risks. |
| **Output** | Information REAZN returns for Sprint Assessment to consume. | Requirements gaps, architectural findings, interface considerations, risks, and supporting evidence. |
| **Status** | How completion, uncertainty, and failures are represented. | completed, incomplete, needs_review, or failed. |
| **Traceability** | How findings are associated with the original ticket and assessment execution. | Ticket ID, skill version, source revision, and references supporting each finding. |
| **Ownership** | Which skill is responsible for specific decisions and outputs. | Sprint Assessment owns batch aggregation; REAZN owns its detailed design findings. |
| **Failure behavior** | Expected behavior when one assessment cannot finish. | An unavailable repository produces an incomplete result rather than fabricated architecture findings; other tickets continue where safe. |

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

I've been developing REAZN as an input-agnostic, evidence-based engineering assessment skill using the four-step System Design Interview (SDI) framework.

I've also developed Audit Skill to review the engineering design, responsibilities, contracts, trust boundaries, and limitations of skills.

Before suggesting changes or using audit findings to guide the integration, I'd like to share how REAZN is structured and understand whether its current capabilities align with what Sprint Assessment needs.

### Questions to discuss

**Main question:**

> Would it be helpful if I walked through how I've structured REAZN and the engineering review approach I've been using, so we can evaluate whether its capabilities fit Sprint Assessment's needs?

**Follow-up questions:**

- What level of requirements or design analysis would be useful for Sprint Assessment?
- Does REAZN's existing four-step approach provide that level of analysis, or would we need a more focused output?
- Are there already standards or review criteria that our team follows when developing skills?
- Would reviewing the two skills together help us identify overlapping responsibilities or missing contracts?
- Which parts of the integration would benefit most from a source-based engineering audit?

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

### How Audit Skill could contribute

Audit Skill performs a read-only engineering review using ten criteria, including:

- Activation and discovery
- Workflow and orchestration
- Contracts and outputs
- Context and trust
- Permissions and side effects
- Failure handling
- Evals and observability
- Lifecycle and portability

For the integration, I think the most relevant areas would be orchestration, contracts, trust boundaries, failures, and evaluation evidence.

**Important distinction:** Audit Skill can identify documented capabilities and evidence gaps. It doesn't automatically establish that a skill behaves correctly during execution.

A previous audit of Refine Requirements Light can serve as historical context, but the current REAZN version should be reviewed separately before treating those findings as current.

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

I've been collecting technical materials from AgentCon/MCP Con 2026 covering agent security, trust boundaries, context management, interface contracts, governance, and reliability.

I think some of those practices could be useful as we develop our skills, but I'd like to understand what security and reliability expectations already exist and whether further investigation would be valuable.

### Questions to discuss

**Main question:**

> Have we established any security, trust-boundary, or reliability requirements for Sprint Assessment and our other skills, or is that something we're considering as part of their development?

**Follow-up questions:**

- What protections or security practices are currently in place?
- Are Jira tickets, repository content, and other retrieved information treated as untrusted input?
- What permissions do these skills currently have, and how are those permissions enforced?
- Are there established standards for delegation between skills or agents?
- Are we planning to formalize these boundaries, or is this outside the current project scope?
- Would it be helpful for me to review my AgentCon/MCP Con materials and bring back relevant findings?

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

I've been developing Evaluate Skill to support repeatable, evidence-based evaluations for agent skills.

My longer-term goal is to move beyond manually inspecting generated outputs and begin measuring whether skills behave correctly, follow their contracts, and handle edge cases reliably.

However, I'd first like to understand the team's current evaluation approach and whether writing executable evals aligns with the project's priorities.

### Questions to discuss

**Main question:**

> How are we currently validating Sprint Assessment and our other skills, and are we considering introducing automated or repeatable evaluations as part of the development process?

**Follow-up questions:**

- What tests or evaluations already exist for Sprint Assessment?
- Are we primarily reviewing generated outputs manually, or do we have executable test cases?
- How do we determine whether a generated assessment is correct?
- Do we have representative Jira tickets and expected outcomes that we could use for evaluation?
- Would we want to test individual skills first, or the entire Sprint Assessment–REAZN workflow?
- Are we interested in measuring the consistency of dispatch decisions, not just the final results?
- Would it be useful for me to demonstrate the Evaluate Skill workflow and discuss how it could support our existing process?

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
