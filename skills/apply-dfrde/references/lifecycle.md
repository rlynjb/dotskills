# Lifecycle guide — stages, evidence, gates and loops

Read when teaching or coordinating an active stage. The six stages express a **default decision sequence**, not a requirement for six heavyweight documents. Favor the smallest durable artifact capable of supporting an informed review. For riskier work, add assurance depth rather than blindly multiplying paperwork.

## Stage 1 — Discover

**Aim:** establish problem, current state and evidence sufficiency before proposing a change.

- Identify intended users and outcomes, scope/non-goals, inputs, existing owner, repository/application/service/harness boundaries, and domain-specific standards.
- For existing work, trace relevant data, call graph, decision flow, dependencies and affected callers; identify assumptions and uninspected surfaces. For greenfield work, record known needs and explicit unknowns—do not invent an existing architecture.
- Decide whether an agent or new component is necessary, or a smaller deterministic/scripted solution suffices.
- Label source claims **OBSERVED**, **DOCUMENTED**, **INFERRED** or **UNVERIFIED**; quote paths/locations where available. Avoid executing live effects merely to discover state.

**Deliverable:** current-state summary and optional as-is Mermaid diagram, scope, constraints, risks, open questions and candidate success criteria.

**Checkpoint:** evidence sufficient to consider designs, or **BLOCKED** with specific missing inputs. A reviewed discovery summary is not proof that every assumption is true.

## Stage 2 — Design and review

**Aim:** compare approaches and decide direction, not just accept the first generated plan.

- Show a high-level design grounded in discovered constraints. State decision ownership and important component boundaries.
- Provide at least one materially different option when a real trade-off exists (including keep-as-is / simplest adequate solution), noting benefits, complexity, coupling, operability, cost, portability and blast radius as relevant.
- Use diagrams only where they improve review; mark them **PROPOSED** rather than pretending implementation exists.
- Identify critical design decisions and who needs to participate in review. Capture rejected alternatives and rationale.

**Deliverable:** design options, recommendation, chosen direction (if approved), decision record with unresolved issues.

**HUMAN REVIEW REQUIRED — Design:** ask the user/appropriate owner to confirm a direction before writing implementation. If the team is undecided, keep options OPEN and do not silently pick one.

## Stage 3 — Contracts and evaluation plan

**Aim:** turn the chosen direction into testable, bounded commitments.

Define whichever contracts are relevant, without assuming every domain uses JSON:
- **Functional behavior:** interfaces, events, inputs, outputs, pre/postconditions, acceptance criteria and invariants.
- **Nonfunctional behavior:** latency/performance, reliability, resource budgets, usability, scalability, compatibility and support level where relevant.
- **Security/trust:** data origin, access scope, runtime enforcement, identity, approvals, confidentiality, safe defaults and forbidden effects.
- **Failure behavior:** timeouts, retries, idempotency, partial success, errors, rollback and recovery.
- **Handoffs:** producer/consumer, responsible owner, format, schema version, provenance, uncertainties, failure/stop signals.
- **Evaluation plan:** representative success, failure and misuse cases; objective or calibrated grading; expected evidence, baseline where available and applicable runtime/environment.

Distinguish **interface contract** (how components interact) from **implementation design** (how each component fulfills it); distinguish prose policy from externally enforced authorization.

**Deliverable:** minimum reviewed contracts, measurable acceptance checks and test/safety plan; record unresolved choices.

**HUMAN REVIEW REQUIRED — Contract:** request confirmation for behavior, owner and authority boundaries. Revisit Stage 2 if the contract exposes an architecture flaw.

## Stage 4 — Implement (only when separately authorized)

**Aim:** make the smallest coherent change within the reviewed scope.

- Describe exact affected files/services/environments, expected effects, incremental sequence and rollback.
- Confirm permissions, workspace, target branch/source revision, external tool availability and the user's approval for these specific writes.
- Keep changes reviewable; follow existing conventions. Never broaden to unrelated refactors, external writes, deployment or secrets because an agent suggests it.
- Record departures from the approved contract as **deviations**, and pause for design/contract re-review when material. Distinguish draft proposals from real modifications.

**Deliverable:** approved change set, relevant source/commit references, what actually changed and unimplemented items.

**HUMAN REVIEW REQUIRED — Implementation scope:** no edits or execution until scope and tools are authorized. A review of the design is not implicit authorization to write files or access production.

## Stage 5 — Evaluate and diagnose

**Aim:** prove outcomes, not just obtain a plausible model response.

- **Before code changes** in existing systems, capture safe baseline evidence when available. A missing baseline is explicitly **UNVERIFIED**, not zero defects.
- Run only approved, adequately isolated tests. Check the intended user journey, component contracts, negative paths, permissions/side effects, and previously passing behavior.
- Select domain-appropriate checks: deterministic tests and contract/integration tests for tools; behavior/trajectory evals and security scenarios for agents; isolation/retry/recovery tests for harnesses; unit/integration/E2E for apps; fault/recovery/load tests for infrastructure.
- Keep **expected**, **observed** and **not run** separate. Review test/fixture quality and environmental failures independently of implementation defects.
- Diagnose before changing; if failures reveal new requirements or flawed contracts, return to Stage 1, 2 or 3 and repeat review gates. Never excuse a safety failure by averaging it into a quality score.

**Deliverable:** test plan/results, source/trace evidence, regressions, unknowns and go/no-go implications.

**HUMAN REVIEW REQUIRED — Evaluation evidence:** approval needed before risky evaluations; users review results and unresolved risks before promoting.

## Stage 6 — Review, release and operate

**Aim:** ensure responsibility continues after implementation.

- Present what was intended, implemented and actually verified; scope of test coverage; unresolved risks; stakeholder sign-offs.
- Agree on version, release/rollout strategy, ownership, monitoring signals, incident and rollback procedure, and feedback cycle.
- For non-deployment work, **release** may mean documentation approval, acceptance of an internal artifact or recommendation to defer. Label it appropriately.
- A go decision does not certify all possible contexts, harnesses or future changes.

**Deliverable:** decision (READY FOR APPROVAL / BLOCKED / DEFERRED / RELEASED only if observed), release/rollback plan and monitoring follow-ups.

**HUMAN REVIEW REQUIRED — Release:** no production deploy, publish, merge or external write without explicit new authorization and actual supported tooling.

## Practical transition rules

- **Default flow:** 1 → 2 → 3 → 4 → 5 → 6.
- **Baseline before mutation** for existing systems if safe/feasible, even though the formal evaluation review is Stage 5.
- **Failure loop:** 5 → 1, 2 or 3 when evidence invalidates a prior assumption/contract; obtain fresh approvals for materially changed scopes.
- **Small task:** combine documentation where safe, never manufacture approval or verification.
- **Explicit user direction:** the user can focus on a later stage; summarize prerequisite unknowns and blockers rather than forcing a lengthy tutorial.
- **Specialist handoffs:** optional; output and execution evidence must be verified, and the specialist's own safety contract must be honored.
