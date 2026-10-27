# Requirements Refinement Interview Playbook

This is the interactive teaching and practice format for the Refine Requirements skill. Pair it with the preserved source reference, [refine-requirements.md](refine-requirements.md). That source is the requirements checklist and final-handoff contract; this playbook controls the interview experience. Neither document authorizes code changes, external communications, or running Superpowers.

## Why these interview techniques apply

| Interview pattern | Adaptation to requirements refinement | Boundary |
| --- | --- | --- |
| System design: clarify the problem and scope before drawing architecture | Clarify actors, product goal, in/out of scope, functional and non-functional requirements | This skill prepares a design brief; it does not choose the architecture |
| System design: prioritize the critical requirements and explore scale and trade-offs | Identify core user journeys, critical quality attributes, constraints, and explicit trade-off questions | Do not fabricate performance, traffic, consistency, or compliance targets |
| DSA: restate inputs/outputs and test small examples and boundary cases | Restate triggers and expected outcomes, then trace happy path, empty/invalid input, duplicates, repeated actions, permission denials, and failures | Do not turn the task into a coding challenge |
| DSA: start from a clear baseline, expose assumptions, then refine | Start from the simplest observable behavior supported by the ticket and nearby code; refine it using scenarios and evidence | Existing behavior is not automatically an approved requirement |
| Both: explain reasoning and respond to interviewer follow-ups | Ask a precise question, justify an answer, consider a changed constraint, and improve the FR, NFR, or acceptance statement | A model-generated worked answer is a proposal, not stakeholder approval |

These are adaptations, not claims that any interview guide prescribes this exact skill workflow.

Further reading:
- [Hello Interview: System Design Requirements Gathering](https://www.hellointerview.com/blog/system-design-requirements)
- [Hello Interview: System Design Delivery Framework](https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery)
- [Duke Career Hub: How to Answer System Design Questions](https://careerhub.students.duke.edu/blog/2023/03/24/how-to-answer-system-design-questions/)
- [Engineering Foundry: Coding Interview Strategy](https://engineeringfoundry.dev/dsa/strategy)

## Interview roles and evidence

- The **learner** is the candidate: they practice framing, questioning, analyzing, and explaining a real ticket or a clearly labeled hypothetical.
- The **assistant** is interviewer and coach, not the real product owner. In Guided mode it teaches with evidence-based worked answers; in Practice mode it waits for the candidate first.
- The **codebase** is inspected context, not a source of authority on product decisions. The ticket, approved specs, and recorded stakeholder decisions establish confirmed requirements.
- The **stakeholder or developer** is the actual owner of any unresolved question. Do not invent their answers, quotes, signoff, or historical reasons.
- The **Superpowers/design agent** receives the refined brief and selects a design later; do not invoke it or preempt its implementation decisions.

Start by inspecting the feature ticket and relevant existing code, tests, interfaces, and nearby patterns. Summarize a small pattern map before asking discovery questions. If code is inaccessible, mark pattern fit NOT VERIFIED and use provisional ticket-grounded questions.

## Default interview progression

Use this order as a guide, not a rigid script. Select the next question that resolves the most consequential gap. Skip topics already answered by reliable evidence. Do not insist on a fixed number of questions.

### 1. Frame and clarify the problem

Ask the candidate to restate: who has the problem, what triggers the feature, what observable outcome matters, what is explicitly outside scope, and what remains ambiguous.

Possible prompts:
- What does success look like from the user's perspective?
- Which product decision would change the scope or acceptance criteria?
- Is this a new capability, a variation on a known feature, or a behavior change?

### 2. Establish the current baseline (codebase first)

Show the smallest relevant comparable feature, code symbol, test, contract, and known difference. Ask whether the ticket can FOLLOW, ADAPT, or cannot rely on that pattern. Mark missing access NOT VERIFIED. Ask a developer about historical intent only if evidence cannot answer it.

Possible prompts:
- Which existing behavior could we reuse, and what evidence supports that?
- Is the difference a product requirement or merely an implementation detail?
- What existing contract must remain compatible?

### 3. Define and prioritize functional requirements (FR)

Describe **what actors must be able to do**, including triggering conditions, user-visible output, business rules, permissions, and exclusions. Distinguish core Must behavior from optional Should/Could behavior and unresolved priorities. Prioritization without approval is a proposal.

Record each material FR:

| Field | Requirement |
| --- | --- |
| ID | FR-01, FR-02, etc. |
| Statement | Actor + trigger + observable behavior/result |
| Priority | Confirmed or proposed Must / Should / Could / Out of scope |
| Status | CONFIRMED REQUIREMENT / PROPOSED / ASSUMED / UNKNOWN |
| Evidence | Ticket/spec/decision and relevant inspected code or test |
| Acceptance | Given / When / Then, including meaningful failure behavior |
| Open decision | Question ID, owner, or none |

Possible prompts:
- Which one or two user journeys must work for this feature to be useful?
- Who is allowed to start the action? What happens after a retry?
- What exactly would QA verify, and what existing feature behaves similarly?

### 4. Probe examples, edge cases, and correctness (DSA-style)

Use a small, explicit scenario walkthrough: initial state -> actor/action -> guards/rules -> visible result -> state change -> recovery. Distinguish a manually reasoned example from a test actually run.

Select relevant cases: empty/missing data, malformed input, duplicates, concurrent edits, repeated actions, permissions, timeouts, stale data, cancellation, partial failure, and recovery. Ask about ties, ordering, limits, and idempotency only where behavior or contracts require clarity.

Possible prompts:
- What would happen if this action occurs twice or while another user edits the same record?
- What is the simplest correct outcome for the unhappy path?
- What invariant must still be true when an external dependency fails?

Turn the answer into FR acceptance criteria or an owned unresolved product question. Do not invent algorithmic complexity or design an algorithm.

### 5. Define and prioritize non-functional requirements (NFR)

Describe **how well**, under **which conditions**, the required behavior must operate. Use only applicable concerns and link each to a user journey or FR.

| Dimension | Requirement-level interview question |
| --- | --- |
| Scale / workload | How many users, records, operations, concurrency, peak bursts, or growth must the product support? Is the workload read-heavy or write-heavy? |
| Latency / throughput | Which user action needs a response target, and which percentile or measurement window matters? |
| Availability / resilience | What downtime or degraded behavior can users tolerate? What happens if a dependency fails? |
| Data correctness / consistency | How fresh must displayed data be? What ordering, uniqueness, or read-after-write guarantee matters? |
| Durability / recovery | What must never be lost? Are retries, duplication, recovery windows, or audit trails expected? |
| Authorization / privacy | Which roles can read or change what? Are there sensitive fields, retention, or approval expectations? |
| Accessibility / clients | Which devices, browsers, assistive-technology experiences, or offline cases matter? |
| Operability / cost | What visibility, support process, maintenance constraint, or budget limit is required? |

Record each material NFR:

| Field | Requirement |
| --- | --- |
| ID | NFR-01, NFR-02, etc. |
| Quality + scope | Which behavior/FR is affected, and why users care |
| Target | Source-backed value, or exactly: target requires confirmation |
| Verification | How a tester or owner could verify it |
| Priority + status | Confirmed or proposed priority; CONFIRMED REQUIREMENT / PROPOSED / ASSUMED / UNKNOWN |
| Evidence + owner | Source, applicable existing-contract baseline, or owner of missing decision |

Do not turn examples or guessed traffic numbers into commitments. In a **mock system-design interview**, explicitly labeled illustrative assumptions may be used for estimation practice, but remain separate from actual requirements and handoff facts.

Possible prompts:
- Which single NFR would most change the eventual design?
- If immediate consistency costs responsiveness, which business operation must stay correct?
- Is the baseline from the similar feature sufficient, or does this ticket need a different guarantee?

### 6. Build a system-design-ready brief (without implementing design)

These are design-input questions, **not** an instruction to complete a system design:

- **Actors and external clients:** who initiates actions, which roles, and what permission boundaries exist?
- **Core domain concepts:** what data/entities and user-visible state transitions matter?
- **Interfaces and contracts:** what operations, responses, error outcomes, events, or integration requirements must consumers observe?
- **Data ownership and lifecycle:** source of truth, freshness, update, deletion, concurrent edits, and retention expectations.
- **Dependencies and compatibility:** existing components, upstream/downstream systems, migration or backwards-compatibility requirements.
- **Workload and sizing inputs:** users, request patterns, data volume, peak load, regions, supported clients; note what must be measured or confirmed.
- **Failure and recovery semantics:** retry and duplicate behavior, partial success, restoration, user communication, and audit needs.
- **Security and accessibility:** relevant authorization, privacy, accessibility, and compliance requirements only when supported or needing owner confirmation.
- **Trade-off questions:** latency vs freshness, availability vs stronger consistency, usability vs stricter controls, cost vs quality, and scope vs delivery date, only if relevant.
- **Validation:** which FR/NFR has a clear acceptance test, and what remains unmeasured?

For each materially relevant topic, document the constraint, evidence, uncertainty, and owner. Defer service topology, specific databases, queues, caches, APIs' internal implementation, detailed sizing calculations, technology choice, and code to the later design process. When the user separately requests a **mock full system-design round**, permit a hypothetical architecture phase but label it practice and do not include it as the authoritative product handoff.

### 7. Challenge assumptions, verify, and close

Use a realistic interviewer follow-up: change an input or constraint and ask how the proposed requirement or acceptance condition should change. Example: "What if the user retries the action after a network timeout?" Record the new edge case and affected FR/NFR. A good answer can be "We need the product owner to decide."

Before finishing, check:
- Are core FRs observable and traceable to evidence?
- Are material NFRs tied to behaviors and either measurable or explicitly awaiting targets?
- Are edge/failure cases and ownership rules covered?
- Did we avoid assuming the codebase or the model can approve product policy?
- Are unverified system-design inputs visible for the handoff?
- Can a design agent start without guessing a blocking product decision?

## Response contract for one guided interview question

Use the same learning rhythm as Code Review while keeping the requirements task distinct:

1. **What and why:** teach the relevant requirements or system-design concept in plain English.
2. **Problem question N — [specific feature scenario]:** one focused question grounded in ticket and code evidence.
3. **How to reason:** ask what the candidate should inspect, compare, or clarify.
4. **Worked answer:** provide an evidence-backed answer or a clearly labeled proposal, noting unknowns.
5. **Scenario walkthrough:** a small happy path, edge case, or failure trace.
6. **Trade-off and interviewer follow-up:** one changed constraint and what it means for FR/NFR.
7. **Refined requirement:** add or revise a relevant FR, NFR, acceptance scenario, or decision; show an ID and source/status.
8. **Takeaway:** one transferable lesson.
9. **LEARNING CHECKPOINT — Next question or explore this one?** Pause in default mode.
10. **Post-interview — Questions to ask stakeholders:** final section, using the rules below.

Practice mode initially shows only the scenario and candidate question. Wait for the learner to respond before showing the worked answer, follow-up analysis, refinement, or stakeholder questions. Resume the same question when the learner asks for a hint or clarification.

## Post-interview — Questions to ask stakeholders

End each completed guided question and each completed report with this section; in Practice mode, show it only after the learner responds and feedback is given. **This replaces code-review comments**. No inline code-review comments should be generated.

Only include questions unresolved by evidence and meaningful to scope, behavior, acceptance, or important quality targets. Group product decisions first; optionally include a separate developer/history group when material.

For each question provide:
- **Q-01 / owner:** product owner, designer, security/privacy owner, or developer/history owner as appropriate.
- **Ready-to-ask wording:** one neutral, concise question.
- **Why it matters:** FR/NFR, scenario, or ticket-vs-code conflict; summarize the decision's impact.
- **Priority / blocks handoff:** yes or no and why. Include choices only when useful, not as invented approvals.

If none remains, say: **No unresolved stakeholder questions for this topic.**

Do not fabricate replies, suggest posting the questions automatically, or silently open/update tickets. The candidate may request ready-to-send wording, but that does not authorize sending.

## Final interview report / Superpowers handoff

On completion or request, produce one concise synthesis, not a repetition of every teaching question:

1. Feature goal, actor, scope/exclusions, codebase revision and evidence limits.
2. Existing-pattern map (FOLLOW / ADAPT / NO SUITABLE PATTERN FOUND / NOT VERIFIED), and ticket-to-current-behavior alignment.
3. Prioritized FR table with source/status and Given/When/Then acceptance criteria.
4. Prioritized NFR table with confirmed targets or "target requires confirmation", verification methods, and owners.
5. Key user flows, meaningful edge/failure scenarios, dependencies, business invariants, and permissions.
6. **System-design readiness:** domain concepts, required interfaces/data contracts, source-of-truth and consistency expectations, sizing inputs, integrations, trust boundaries, operational expectations, and explicitly deferred technical choices.
7. Coverage: reviewed / not applicable with reason / unverified, and tests inspected vs actually executed.
8. READY / CONDITIONAL / BLOCKED verdict with minimum outstanding decisions. BLOCKED still gets a provisional brief; no claim of implementation readiness.
9. **Post-interview — Questions to ask stakeholders** as the last section, after the readiness and verification summaries.

## Small hypothetical example (not a real product decision)

**Ticket:** "Let users change notification preferences."

**Interviewer:** "What happens when a preference update succeeds but a second device has stale settings?"

**Candidate reasoning:** The visible behavior and freshness expectation are not explicit. A similar settings feature could reveal existing UI behavior, but that is not proof of policy.

**Worked requirement:** FR-01 (PROPOSED): "When a signed-in user saves a supported preference, the next successful preferences read returns the saved choice." Acceptance (PROPOSED): Given a supported choice, when the user saves it and reopens preferences, then the saved choice is displayed. The phrase "next successful read" requires confirmation before becoming an accepted guarantee.

**NFR:** NFR-01 (UNKNOWN): "Cross-device update freshness for preference reads"; target requires confirmation; linked to FR-01.

**Scenario:** Device A saves; device B immediately loads preferences. The expected observation is unknown until the product owner confirms whether temporary staleness is acceptable.

**Post-interview — Questions to ask stakeholders:** Q-01 / Product owner: "After a user saves a preference, should every signed-in device show it immediately, or is a short propagation delay acceptable?" This could change consistency expectations and blocks confirming NFR-01.

This scenario teaches the distinction between product behavior, quality expectation, evidence, and a later design trade-off without pretending to design the implementation.
