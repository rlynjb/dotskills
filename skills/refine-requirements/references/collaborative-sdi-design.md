# Collaborative SDI Design Track

This reference defines the default recommendation-first, interactive **real engineering design** extension to Refine Requirements. Read it when starting or continuing the four-step System Design Interview (SDI) track. The requirements checklist in **refine-requirements.md** remains authoritative for requirements investigation and the requirements-only handoff. Its prohibition on technical designs applies **while performing the requirements phase**; this reference controls the separately identified design phase. Neither reference authorizes editing application code or invoking an implementation agent.

## Purpose and boundaries

Work with the developer to design a **real** feature or change while repeatedly practicing the reasoning of a system design interview. Produce a reviewable design supported by actual ticket/code evidence, appropriate architectural sketches, options, decisions, and trade-offs. **Engineering and learning are one activity**: explain how and why recommendations work as you help the user choose a feasible design.

The agent is a **researcher, recommending design partner, and optional interviewer**, not the person who grants product approval. The developer decides which technical recommendations to adopt. Real product requirements, service limits, compliance obligations, and stakeholder approvals come from authorized evidence/owners, not the model.

**Read-only execution boundary:** Inspect available code, contracts, tests, docs and tickets only with authorization. Diagrams, interface sketches, pseudocode, and design text are **proposals**, not code changes. Do not edit source, create tickets, contact stakeholders, run migrations, deploy, invoke Superpowers, or instruct an agent to begin coding without a separate, explicit user instruction and capable host authorization. Save design files only when the user separately authorizes writing them.

## Input flexibility and design-first reasoning

This is a **design-first development method**, not just a ticket-review report. Begin with **whatever feature context the user supplied**: a Jira or other issue, pasted user story, acceptance criteria, requirements text, behavior report, feature brief, or informal notes. The input may be pasted directly; a Jira key, special format and tracker integration are **not prerequisites**. Mark draft/uncorroborated statements and missing product decisions as provisional rather than upgrading them to approved requirements.

**Order matters:** SDI Step 1 establishes the problem, desired observable behavior and scope **before solution selection**. Step 2 investigates real architecture/patterns and explains current versus proposed flow; Step 3 reasons through the critical interfaces, data paths and implementation constraints; Step 4 defends the design against risks and trade-offs. Use each step as a reasoning discipline: **evidence → interpretation → options → recommendation → challenge/review → explicit decision**. Do not jump to Step 2/3 technical solutions while essential Step 1 requirements are still unresolved, or mistake the Findings Overview for completed design work.

**Output target:** work toward an **evidence-grounded, explained engineering design** (or a clearly marked provisional design when code/scope is missing), with current/proposed ASCII flow sketches when relevant, ownership/contracts, why existing patterns fit, alternatives, trade-offs and approval status. A design-first workflow happens **before implementation**: it never authorizes code edits, a coding agent or a deploy on its own. The separate approvals/handoff rules below remain mandatory.

## Consistent terminal presentation — one labeled item at a time

**Always use the same screenshot-style vertical format in every terminal width.** The main skill's output-format rule governs all user-facing Findings Overview entries, existing pattern/reuse maps, FR/NFR requirements, proposed options, D-ID decisions, stakeholder questions, and final handoff. **Do not output a Markdown table, ASCII grid, pipe-delimited columns, or a wide-terminal table fallback.** Tables below are internal reference field definitions only; never copy their tabular structure to the user-facing report.

For every material item: start with a brief title/ID (e.g. `**Area: Pan and zoom**`, `**FR-01 — Change layout**`, or `**D-01 — Edit strategy**`), followed by **plain, non-bulleted label/value lines** (`Where it lives:`, `What it does today:`, `Verdict:`, `Why:`, `Requirement:`, `Status:`, `Evidence:`, `Decision:`, etc.). Separate items with a standalone `---` horizontal divider. Keep fields short and include only relevant details. For a lone item omit the separator. Preserve section headings, stable IDs, source status, and the Step 2 **boxed ASCII diagrams** (diagrams are the one place where a monospace box layout is intentional).

## Entry: findings first, recommendation first

1. Inspect the relevant existing feature and available evidence before recommending architectures. Record revision, known boundaries, code paths, contracts and uncertainty. If inaccessible, mark **NOT VERIFIED**; do not invent an existing implementation.
2. Show the familiar **Findings Overview first**: feature snapshot, evidence/pattern map, all material FRs and NFRs, constraints/gaps, and readiness. Add a **Four-step SDI roadmap** and **Recommended next explorations** within the overview's review-navigation section, **before** the final stakeholder-question queue. For each meaningful design opportunity use a stable D-ID, brief options, a preliminary recommendation, and its condition/evidence limit. Do not begin a lesson or force questions automatically.
3. Recommend an approach **before asking the developer to choose or answer design questions**. In Step 1, this can be a recommended requirements priority or reuse direction; in Steps 2–4 it can be concrete technical options. Ground recommendations in the confirmed scope and existing implementation patterns; conditional recommendations are explicitly provisional.
4. Invite the user to select an FR-ID, NFR-ID, D-ID, a step, an alternate option, or "recommended next". The user may choose another order, explore a concept, ask "how does it work?", request an architecture sketch, or switch modes. Do not infer approval from selection.

Keep post-interview **Questions to ask stakeholders** as the final section of the initial overview and completed full handoff; keep interim responses focused without duplicating the whole queue unless it changed or is needed to make a blocker visible.

## Five-book engineering lens integration

**Alex Xu's System Design Interview (SDI) is the process scaffold, not the only source of reasoning.** Use the four named SDI stages in order, then apply the following books selectively to **real engineering recommendations**, technical alternatives and worked traces. Explain concepts while producing engineering artifacts, not as a detached quiz. The imported requirements checklist is still requirements-only; these lenses may inform architecture in the explicit collaborative design phase.

| Lens | When it helps | How to apply it to design options |
| --- | --- | --- |
| **System Design Interview (SDI) — Alex Xu** | Scoping, architectural boundaries, critical components, and wrap-up | Use Step 1–4 to structure the conversation, recommendations and review. |
| **Designing Data-Intensive Applications, 2nd ed. (DDIA)** | Storage/query choices, read/write workloads, consistency, transactions, concurrency, recovery, scaling | Explain guarantees and failure modes; compare alternatives under evidenced access patterns. Do not claim a database, index or transaction provides an unverified guarantee. |
| **Algorithmic Thinking — Daniel Zingaro** | Transformations, selection/ranking, deduplication, ordering, data structures, or heavy computations | Define input/output and invariants; trace an example and compare actual complexity or limits when relevant. Do not force big-O analysis onto simple glue code or mistake network latency for constant-time computation. |
| **A Philosophy of Software Design (APOSD) — John Ousterhout** | Module boundaries, abstractions, interfaces, coupling, information hiding, evolving contracts | Compare where complexity lives and how a future change propagates; favor comprehensible responsibilities without inventing unnecessary abstraction. |
| **Fundamentals of Data Engineering (FODE) — Joe Reis and Matt Housley** | Ingestion, transformations, data quality, pipeline/consumer contracts, lifecycle and operations | Trace source → ingestion → storage/transformation → serving and failure/recovery; identify ownership and data quality boundaries. |

**Selection rule:** Choose the most relevant lens or two per material decision based on the inspected implementation and its constraints; mention others only if a distinct concern appears. For a frontend-only change, DDIA or FODE might be NOT APPLICABLE. For a transactional Go API, DDIA plus APOSD may matter; for a data import, FODE plus DDIA or Algorithmic Thinking might matter. Explain why the lens fits, its practical concept, a small worked example and the resulting trade-off. Never present a book-inspired suggestion as a quote or as proof that a particular architecture is correct. If no book is relevant, skip the label.

**Decision record addition:** For each D-ID, optionally add `Engineering lens / principle / evidence`, showing which idea shaped the recommendation and what actual repository/ticket evidence or unverified assumption supports it. Principles do **not** override explicit user approval, stakeholder authority, or tested behavior.

## Four steps — named and ordered after selection

Use Alex Xu's four-step SDI framing, adapted to a real feature. Show **Step X of 4**, current D-ID/FR-ID, statuses, and the next checkpoint. For tiny tickets stay proportionate; do not invent a distributed system or force three options when only one sensible approach exists.

### Step 1 — Understand the problem and establish design scope

Inspect the supplied feature input—ticket, user story, ACs, brief or notes—and relevant existing patterns. **Stay with problem framing before choosing technical solutions:** establish actor, trigger, expected observable behavior, scope/out-of-scope, FR priorities, relevant NFRs, key failure/permission cases and unknown product decisions. Recommend the smallest useful scope and explain which clarifications materially change the design. Treat early reuse/adapt/new observations as **candidates**, not approved architecture. Refine the FR/NFR/acceptance register with the user. **Always present separate Functional Requirements (FRs) and Non-Functional Requirements (NFRs) sections**, with each requirement as a **separate labeled block and a `---` divider between items (never a table)**, using stable, visible `FR-01`, `FR-02` and `NFR-01`, `NFR-02` IDs for every material requirement; include source/status and linked acceptance or questions, and reuse the same IDs in subsequent prose, diagrams/decisions and handoff. When a category has no evidenced items, say **None identified from supplied evidence** rather than inventing requirements. Keep assumptions and out-of-scope statements separate from requirements. Surface unresolved product questions by owner; a coding/design agent cannot decide product policy. **Output:** explicitly labeled FR and NFR registers with stable IDs and evidence/status, requirements baseline, acceptance linked to IDs, constraints, pattern map, candidate D-IDs and scope decisions.

### Step 2 — Verify existing patterns, explain why they work, and propose a high-level design for review

Use the Step 1 requirements baseline and the already-inspected pattern map as a starting point. Investigate relevant code, callers, interfaces, tests, company conventions and decision records as needed; **verify before recommending reuse**. For each material pattern/area:

1. **Existing pattern and evidence:** identify the verified path/symbol/test, the component's responsibility, its callers, contracts, and what it **OBSERVABLY** does today. Note fit with linked FRs/NFRs and use **FOLLOW / ADAPT / NEW REQUIRED / NO SUITABLE PATTERN FOUND IN INSPECTED SCOPE / NOT VERIFIED** as an explicit, explained verdict; never call a bounded unsuccessful search proof of absence.
2. **Purpose and reasoning:** explain in plain English *what problem this pattern addresses*, *why the separation of responsibilities and data/request flow is useful here*, and the relevant benefits/costs or constraints. Distinguish **CONFIRMED documented design rationale** (supported by ADRs, docs or authoritative decisions) from **OBSERVED code behavior** and **ASSUMED architectural interpretation**. Code proves how it currently works, **not why its original authors made that choice**. When historical intent is unknown say **NOT VERIFIED** rather than inventing it. Support material claims with actual file/symbol/test/docs links.
3. **Fit with this ticket:** explain *why* to follow/adapt this pattern, *why not* when it conflicts with the ticket, or *which evidence is missing*; don't leave the verdict unexplained. Prefer the smallest coherent reuse-first extension that respects verified ownership and contracts.

Then present the high-level design in the following approachable order, with detail proportional to the ticket:

- **OBSERVED CURRENT FLOW — boxed ASCII diagram:** for a multi-component or boundary-crossing feature, draw a **visually readable, labeled box-and-arrow diagram**, not a single-line list of bracketed component names. Draw meaningful verified components as boxed nodes with `+---+` borders, arranged vertically or in clearly grouped branches. Connect them with `|`, `v`, and occasional horizontal arrows for real side effects/branches; label important handoffs (e.g., request, transform, save, audit event). Use the **actual verified component names** and ownership/boundaries; label unknown links/nodes `[NOT VERIFIED]`. **Explain the arrows in plain English:** what happens at each handoff today, what each box owns and why its boundary matters to the feature. Distinguish documented architectural intent from an inferred engineering explanation.
- **PROPOSED FLOW — boxed ASCII diagram:** show the same user journey at a **comparable visual level of detail** so the change is easy to spot. Keep existing verified paths recognizable; label every new/modified step `[PROPOSED]` and unverified connection `[NOT VERIFIED]`. Explain **what changes, what remains, where the new responsibility belongs, why it belongs there, and how the change achieves the ticket outcome**. Do **not** introduce a service, queue, database, snapshot, dependency or subsystem solely to make the diagram look complete.
- **Readable diagram conventions:** prefer stacked boxes and concise arrow labels over long, wrapping inline chains like `[A] --> [B] --> [C] --> [D]`. Split read and write flows if a single diagram would be misleading. Keep diagram width manageable in monospaced Markdown code fences; adapt the topology to real verified branches rather than forcing a linear architecture. Diagrams show the high-level design, **not** executable implementation or approved decisions.
- **Illustrative formatting only — not evidence of real code:**

  ```text
  OBSERVED CURRENT FLOW

  +---------------------------+
  | Existing UI               |
  +---------------------------+
               |
               | GET /resource
               v
  +---------------------------+
  | Existing API handler      |
  +---------------------------+
               |
               | reads through
               v
  +---------------------------+
  | Existing service / store  |
  +---------------------------+

  PROPOSED FLOW (CONDITIONAL)

  +---------------------------+
  | Existing UI + new action  |
  | [PROPOSED change]         |
  +---------------------------+
               |
               | save request
               v
  +---------------------------+
  | Existing API handler      |
  +---------------------------+
               |
               | validate changes
               v
  +---------------------------+
  | Existing service / store  |
  | [PROPOSED extension]      |
  +---------------------------+
  ```

  Replace every illustrative name and arrow with the inspected code's real flow. Add a branch only when evidence supports it; don't assume all systems are linear.
- **Design rationale and options:** present **two or three viable options only when meaningful** (including following existing behavior where appropriate). For each, explain the pattern fit, architecture/components, contracts or integration boundaries, benefit, cost/complexity and main risk; clearly state the **recommended option + why + what evidence or changed constraint would alter it**. Explain why a new component is needed rather than invented, and make unverified proposals conditional.
- **Interactive review:** link proposals to stable D-IDs; invite the developer to inspect, challenge, compare and revise both the diagram and its explanation before any explicit technical-decision approval. Selection or curiosity does not imply approval.

**Proportionate output:** a single-component change with no meaningful architecture change can use a short ASCII before/after trace or **Flow unchanged** with an explanation; do not manufacture a distributed flow. Keep this step focused on architectural intent and ownership—defer detailed failure/transaction/code-path mechanics to Step 3.

**Output:** explained existing-pattern/reuse map; visually readable **boxed ASCII OBSERVED CURRENT FLOW and PROPOSED FLOW** diagrams, with short plain-English walkthroughs when warranted; grounded rationale for what exists and what changes; high-level components, responsibilities, contracts/data movement, options, recommended direction and tentative D-IDs. "Obtain review" means technical alignment, **not** permission to implement.

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

Keep an in-session decision register with stable IDs. The field-definition table below is for internal reference only: **output each D-ID as its own vertical labeled block, with plain label/value lines and `---` between items, never in a table**. For example:

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
3. Existing-pattern map with key pattern purpose, reuse verdict, **evidence-backed rationale** (documented intent versus inferred reasoning) and compatibility/integration constraints.
4. **OBSERVED CURRENT FLOW** and **PROPOSED FLOW** as readable boxed ASCII architecture diagrams with brief explained handoffs when relevant, plus proposed/approved architecture, components, request/data paths, interfaces/data contracts, ownership/state and security boundaries as applicable.
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
