# Quality Review Questions — Q-01–Q-10

Optional reference for `skill-responsibility-overlap-audit`. The default responsibility investigation does **not** load or print these questions. This is a reference, not another skill or mandatory report section.

**Source:** Original wording copied verbatim from `skills/audit-skill/SKILL.md`, “Canonical engineering questions,” inspected November 23, 2026. Consideration mappings and evidence prompts below are new organizational suggestions, not part of the original questions.

## Original ten questions — exact wording

- **Q-01 — Purpose & boundaries:** Does the skill explain its job, intended users, when not to use it and prohibited actions?
- **Q-02 — Activation & discovery:** Are discovery, invocation, trigger conditions and incorrect-trigger handling defined for its intended host?
- **Q-03 — Structure, inputs & dependencies:** Are entry points, required inputs, resources/context, tools, environment assumptions and unavailable-source handling established?
- **Q-04 — Workflow & orchestration:** Are workflow stages, decision rules, applicable delegation/aggregation and human gates defined?
- **Q-05 — Contracts & outputs:** Are required inputs, outputs, validation, invariants, ownership and failed handoffs defined?
- **Q-06 — Context & trust:** Are evidence provenance, freshness, contradictions, untrusted input treatment and source-backed conclusions addressed?
- **Q-07 — Permissions & effects:** Are permitted effects, authorization boundaries, least privilege and applicable host/tool/server enforcement evidenced?
- **Q-08 — Failure & stop behavior:** Are missing resources, errors, partial outcomes, relevant retries/timeouts, stopping and escalation handled?
- **Q-09 — Evals & observability:** Are evaluation cases, existing runs/traces, grading, known gaps and regression evidence identified accurately?
- **Q-10 — Lifecycle & portability:** Are ownership, versions, review/rollback, dependencies and claimed harness compatibility supported?

## Mapping into the six considerations

### Q-01 — Purpose & boundaries

- **Maps to:** C2 Responsibilities; C5 Boundaries.
- **Inspect:** purpose, non-use conditions and prohibited actions.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-02 — Activation & discovery

- **Maps to:** C1 Inputs; C2 Responsibilities.
- **Inspect:** triggers, invocation and incorrect-trigger handling.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-03 — Structure, inputs & dependencies

- **Maps to:** C1 Inputs; C4 Handoffs.
- **Inspect:** required inputs, resources, tools and inaccessible sources.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-04 — Workflow & orchestration

- **Maps to:** C2 Responsibilities; C4 Handoffs; C6 Feedback.
- **Inspect:** documented workflow, delegation and human gates.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-05 — Contracts & outputs

- **Maps to:** C3 Outputs; C4 Handoffs.
- **Inspect:** current input/output guarantees and missing handoff behavior.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-06 — Context & trust

- **Maps to:** C1 Inputs; C5 Boundaries.
- **Inspect:** provenance, freshness, contradictions and untrusted input treatment.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-07 — Permissions & effects

- **Maps to:** C5 Boundaries.
- **Inspect:** host/tool permission evidence and actual authorization versus prompt-only statements.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-08 — Failure & stop behavior

- **Maps to:** C5 Boundaries; C6 Feedback.
- **Inspect:** missing inputs, errors, stop rules and escalation.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-09 — Evals & observability

- **Maps to:** C3 Outputs; C6 Feedback.
- **Inspect:** eval definitions versus completed runs/traces, grading and regressions.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

### Q-10 — Lifecycle & portability

- **Maps to:** Cross-cutting C2/C4/C5/C6, as applicable.
- **Inspect:** ownership, revisions, rollback and tested host compatibility.
- **Stage 2 limit:** Identify currently documented behavior or uncertainty; do not finalize decisions or infer runtime execution.

## Optional Q review operation

- Run the full Q-01–Q-10 checklist only when **quality_review: on** or a full quality review is explicitly requested. For selected Q IDs, inspect **only** those requested, in Q order. A lens-only review does not trigger the Q checklist.
- For each inspected skill and selected Q, report a short **Quality review coverage (optional)** line *after* Section 2's Supporting table and its findings. Preserve the six C1–C6 rows and seven report headings. Put evidence-linked material findings into the existing F-xx vertical notes (do not create separate duplicate findings).
- Use **PRESENT** for evidence sufficiently supporting the applicable documentation claim, **PARTIAL** for incomplete applicable coverage, **MISSING** for demonstrably absent guidance in an adequately inspected scope, **NOT VERIFIED** for unavailable source or runtime evidence, and **NOT APPLICABLE** only if the entire question does not apply.
- Documented text is not observed behavior. Under Q-07, claimed permissions do not prove actual tool/server enforcement. Under Q-09, eval definitions do not prove the evaluations ran or passed. Q-05 checks existing contracts but does not draft Stage 3 contracts. **NOT VERIFIED Q status does not automatically require an F-xx VERIFY**. Ordinary missing traces are coverage limits unless a material runtime claim, explicit assurance request or concrete safety/reliability risk makes verification actionable.
- Cite actual inspected skill files, lines or sections. A brief status example: `Q-07 — NOT VERIFIED — C5; F-02; host permission evidence unavailable.` Never invent a numeric score or production-readiness badge.
