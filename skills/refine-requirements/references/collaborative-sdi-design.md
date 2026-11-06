# Collaborative SDI Design Track

This reference defines the default recommendation-first, interactive **real engineering design** extension to Refine Requirements. Read it when starting or continuing the four-step System Design Interview (SDI) track. The requirements checklist in **refine-requirements.md** remains authoritative for requirements investigation and the requirements-only handoff. Its prohibition on technical designs applies **while performing the requirements phase**; this reference controls the separately identified design phase. Neither reference authorizes editing application code or invoking an implementation agent.

## Purpose and boundaries

Work with the developer to design a **real** feature or change while repeatedly practicing the reasoning of a system design interview. Produce a reviewable design supported by actual ticket/code evidence, appropriate architectural sketches, options, decisions, and trade-offs. **Engineering and learning are one activity**: explain how and why recommendations work as you help the user choose a feasible design.

The agent is a **researcher, recommending design partner, and optional interviewer**, not the person who grants product approval. The developer decides which technical recommendations to adopt. Real product requirements, service limits, compliance obligations, and stakeholder approvals come from authorized evidence/owners, not the model.

**Read-only execution boundary:** Inspect available code, contracts, tests, docs and tickets only with authorization. Diagrams, interface sketches, pseudocode, and design text are **proposals**, not code changes. Do not edit source, create tickets, contact stakeholders, run migrations, deploy, invoke Superpowers, or instruct an agent to begin coding without a separate, explicit user instruction and capable host authorization. Save design files only when the user separately authorizes writing them.

## Entry: findings first, recommendation first

1. Inspect the relevant existing feature and available evidence before recommending architectures. Record revision, known boundaries, code paths, contracts and uncertainty. If inaccessible, mark **NOT VERIFIED**; do not invent an existing implementation.
2. Show the familiar **Findings Overview first**: feature snapshot, evidence/pattern map, all material FRs and NFRs, constraints/gaps, and readiness. Add a **Four-step SDI roadmap** and **Recommended next explorations** within the overview's review-navigation section, **before** the final stakeholder-question queue. For each meaningful design opportunity use a stable D-ID, brief options, a preliminary recommendation, and its condition/evidence limit. Do not begin a lesson or force questions automatically.
3. Recommend an approach **before asking the developer to choose or answer design questions**. In Step 1, this can be a recommended requirements priority or reuse direction; in Steps 2–4 it can be concrete technical options. Ground recommendations in the confirmed scope and existing implementation patterns; conditional recommendations are explicitly provisional.
4. Invite the user to select an FR-ID, NFR-ID, D-ID, a step, an alternate option, or "recommended next". The user may choose another order, explore a concept, ask "how does it work?", request an architecture sketch, or switch modes. Do not infer approval from selection.

Keep post-interview **Questions to ask stakeholders** as the final section of the initial overview and completed full handoff; keep interim responses focused without duplicating the whole queue unless it changed or is needed to make a blocker visible.

## Four steps — named and ordered after selection

Use Alex Xu's four-step SDI framing, adapted to a real feature. Show **Step X of 4**, current D-ID/FR-ID, statuses, and the next checkpoint. For tiny tickets stay proportionate; do not invent a distributed system or force three options when only one sensible approach exists.

### Step 1 — Understand the problem and establish design scope

Inspect feature goals and existing patterns. Recommend the smallest useful scope, FR priorities, relevant NFRs, key failure/permission cases, and uncertainties. Explain alternatives (e.g. reuse vs adapt vs new behavior) and where product approval is needed. Refine FR/NFR/acceptance register with the user. Surface unresolved product questions by owner; a coding/design agent cannot decide product policy. **Output:** requirements baseline, acceptance, constraints, pattern map, candidate D-IDs and scope decisions.

### Step 2 — Propose high-level design and obtain review

Ground the proposal in verified requirements and codebase constraints. Present **two or three viable options when meaningful**, each with architecture/components, external interfaces, data flow, fit with existing code, complexity, benefit/cost, and principal risk. Clearly identify **recommended option + why + what evidence would change it**. Offer a small diagram (Mermaid or clear textual sketch) with labeled hypothetical/unverified components; trace the normal request/data path. Invite exploration and changes, then develop a proposed high-level architecture for review. **Output:** architecture sketch, component responsibilities, main contracts/data movement, D-IDs with tentative direction. "Obtain review" is technical alignment, not permission to implement.

### Step 3 — Design deep dive

Prioritize the components or decisions that materially drive correctness, scale, or complexity. For each D-ID present options and a recommendation **first**, then drill into the user's choice: read/write paths, key APIs and data models, state transitions, retries/idempotency, concurrent actions, failures/recovery, auth/trust boundaries, migration/compatibility, observability, performance and verification **only where relevant**. Explain relevant DDIA (2nd edition), APOSD, FODE, Algorithmic Thinking, or SDI principles in plain language when they help the choice. Contrast observed code guarantees with hypothetical ones. **Output:** implementation-level design decisions (not implementation code), representative traces, test/validation ideas, known unknowns.

### Step 4 — Wrap up: bottlenecks, trade-offs, and review

Challenge the proposal against the important NFRs, failure cases, bottlenecks, costs, operational burdens and changed constraints. Recommend improvements and alternatives, summarize all D-IDs and open blockers, then present the **Engineering Design & Implementation Handoff** for the user's review. Verify internal consistency: FR/NFR -> architecture -> decisions -> acceptance/verification. Invite explicit revisions or a **separate design sign-off**. **Output:** reviewed design candidate and readiness result. Do not imply implementation has started.

## Recommendation-first decision loop (repeat for each meaningful D-ID)

1. **Inspect and recommend:** State the concrete decision, linked FR/NFR, source/evidence or missing measurement, 2–3 credible options when warranted, their advantages, costs/risks, and the agent's **recommended** choice with rationale and confidence/conditions. Include "keep the existing pattern" where viable.
2. **Explore:** The user selects an option to *learn about*, requests examples/diagrams, asks how it works or challenges the recommendation. Explain mechanisms, assumptions, alternatives, failure modes and relevant principles. Selection = interest, **not assent**.
3. **Propose:** The user suggests a direction or requests a refined proposal. Draft architecture and decision details, tie them to actual constraints and acceptance, and identify what must be verified.
4. **Review and revise:** Challenge a changed constraint or counterexample; compare options and resolve/flag disagreements. Loop through explore/propose/review as often as helpful.
5. **Explicit decision approval:** Present a concise decision record; **only** after the user explicitly says they approve **that identified D-ID and revision** mark it **APPROVED**. "Explain B", "choose B to explore", "looks interesting", and the agent's own recommendation never constitute approval.

**Never finalize a technical decision merely because the agent recommended it or the user chose it for exploration.**

### Stable decision record

Keep an in-session decision register with stable IDs, for example:

| Field | Required value |
| --- | --- |
| Decision | D-01: named choice and affected component |
| Links | FR/NFR/acceptance, ticket, existing path or test |
| Options | Alternatives considered; why each fits or fails |
| Recommendation | Agent's conditional recommendation and rationale |
| Draft selection | User's current preferred approach, if any |
| Benefits and costs | Correctness, complexity, reliability, performance, delivery, operability |
| Evidence | OBSERVED, CONFIRMED, PROPOSED, ASSUMED, or NOT VERIFIED with source |
| Unknowns | Blocking product decision, measurement, contract, or validation needed |
| Status | OPTIONS PRESENTED -> EXPLORING -> PROPOSED -> REVIEWING -> APPROVED (or BLOCKED / REJECTED / SUPERSEDED) |
| Approval | Explicit user approval text and approved revision within the accessible session; otherwise NONE |

Do not auto-advance status based on elapsed discussion, a proposed option, a draft diagram, or "continue". Revisiting an **APPROVED** decision after material requirement/evidence change moves its revision back to **REVIEWING** and asks for reapproval; retain the prior decision and note the change. Never label user technical approval as stakeholder approval.

### Interactive modes and navigation

- **Collaborative SDI (default):** Agent offers evidence-backed choices and a recommendation first, then the user explores, asks questions, proposes and approves each meaningful decision. Provide short conceptual explanations naturally, without an unrelated quiz.
- **Interview Practice (on request):** Present a short recommendation/options map up front, but for the chosen step ask the developer to defend or critique a choice **before** showing detailed worked reasoning. Offer hints, then feedback and recommendations; still produce real design artifacts and require explicit approval.
- **Direct Engineering (on request):** Present more complete recommendations, diagrams and proposed decisions in a batch for review; approval gates remain.
- **Requirements-only (on request):** Use the preserved requirements-only playbook and source-locked master; no architecture selection. Existing item-based Guided/Practice/Concise/Full-Walkthrough navigation remains available.

Accept "continue", "recommend next", "D-02", "compare A vs B", "how does B work?", "show diagram", "challenge this", "back to Step 2", "revise D-01", "review decisions", and "request handoff". Continue at the saved in-conversation step/ID without replaying the entire overview. Mark progress **not persisted** if the harness does not provide persistence; do not claim memory across runs.

## Engineering handoff and approval gates

Maintain **two distinct gates**:

1. **Technical decisions:** individual D-IDs are APPROVED only upon explicit developer acceptance of their stated proposal/revision; unresolved or superseded options are clearly labeled.
2. **Overall design sign-off:** after Step 4, show a versioned review package, readiness and blockers. Ask the user explicitly to **approve the design package for implementation handoff**. This is different from approving an individual D-ID. Record sign-off and revision in the current session; do not infer it from "continue" or previous option approvals.

**Engineering Design & Implementation Handoff** includes:
1. Feature goal, actors, scope, exclusions, sources, inspected revision and evidence limits.
2. Approved/remaining provisional FRs and NFRs, owners, quality targets, Given/When/Then acceptance and open product decisions.
3. Existing-pattern map and compatibility/integration constraints.
4. Proposed/approved architecture diagram, components, request/data paths, interfaces/data contracts, ownership/state and security boundaries as applicable.
5. Decision register with D-ID, selected option, alternatives, rationale, costs, assumptions, status and explicit approval evidence.
6. Critical deep dives, edge/concurrency/retry/failure behavior, observability, migration/backfill and capacity concerns where applicable.
7. Verification and test plan mapped to FRs/NFRs/decisions; distinguish inspected tests, actually run checks and proposed tests.
8. Risks, unknowns, blockers, rejected options and scope/verification gaps.
9. **Two separate readiness labels:** requirements READY / CONDITIONAL / BLOCKED, and design DRAFT / REVIEW NEEDED / APPROVED FOR HANDOFF. Only label **APPROVED FOR HANDOFF** with explicit overall sign-off, all material design choices approved, and no unaccepted blocking product/technical decisions. An approved hypothetical design cannot bypass unresolved real product authority.
10. **Post-interview — Questions to ask stakeholders** last: concise deduplicated pending owner decisions with BLOCKS HANDOFF status.

An approved design package is **permission to prepare the handoff**, not permission to write code. Produce the reviewed package in the response; do not silently dispatch Superpowers/Codex/Claude or mutate repositories. A separate explicit instruction is required to invoke an implementation workflow, which must re-check permissions and repository changes before acting. If design is unapproved or blockers remain, share only a clearly marked **DRAFT — NOT AUTHORIZED FOR IMPLEMENTATION** package.

## What to say at each checkpoint

Summarize only the current step, recommendation, a short rationale/evidence status, relevant D-IDs and one action menu: **Explore option / ask how / compare / propose / revise / approve named D-ID / continue / back**. Never ask the user to approve unexamined alternatives or automatically infer sign-off from a selection. Offer a recommended next step when the user says "continue"; progression is a navigation action, not approval.

## Small illustrative example (not a real requirement)

**Task:** export audit records; repository not provided so existing export mechanism is **NOT VERIFIED**.

**D-01:** export execution strategy. Options: synchronous request (simpler, possible timeout) vs. background processing (better for long jobs, extra worker/queue/status/storage). **Conditional recommendation:** first inspect existing export handling and determine actual export size, completion-time requirements and infrastructure; prefer established capabilities when fit is verified. Status: **OPTIONS PRESENTED**, not approved.

If the user asks "How would background jobs work?", explain the queue/worker/status result flow, retry/idempotency and operational cost; set status **EXPLORING**. If they say "Propose the background approach", present a draft diagram and interface/verification options; set **PROPOSED**. If they say "Approve D-01 background job v1", confirm that exact decision **APPROVED**, but do not approve the whole design or invoke Superpowers. Overall handoff still requires Step 4 review and explicit package sign-off.
