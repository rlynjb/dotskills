# Worked Example — Sprint Assessment and Refine Requirements

This file is optional **task-specific guidance** for the single `audit-skill` workflow. It does not define a second review process, a mode, an implemented integration, or authority to run either skill.

## Invocation

```text
Use audit-skill to inspect Sprint Assessment and Refine Requirements.
Read only. Start with the full At a Glance report for EACH skill:
purpose, activation, inputs/context, dependencies, steps/decisions,
agent/tool delegation, outputs, contracts, permissions, failures,
existing safeguards, evaluation evidence and unknowns.

Also supply:
- A current-state Mermaid workflow diagram for each skill.
- The Agent Skills specification conformance matrix, separating
  requirements from recommended or host-specific conventions.
- All Q-01–Q-10 quality criteria with sources and review status.
- An explicit Claude Code / Codex compatibility and adapter matrix,
  marking behavior NOT VERIFIED without actual runtime evidence.
- A responsibility/overlap matrix; unique, duplicated, conflicting and
  missing decisions; candidate handoff/integration options labeled
  PROPOSED, never as already implemented.
- Evidence-backed risk findings and three or more NOT RUN synthetic
  eval scenarios with observable assertions.

Cite paths and line numbers. Do not execute target skills, shell
commands, agent workers, Jira/Confluence effects or eval cases. Do not
edit source files. Preserve gaps and pause for human review.
```

## Target-specific review questions

### Sprint Assessment
- How are Jira tickets discovered, grouped, assigned, assessed and aggregated?
- Does the source explicitly instruct one worker per ticket? Which workers
  are named reusable agents versus ad hoc dynamically delegated agents?
- What requirements, evidence, architecture assumptions and readiness rubric
  determine sizing? Which results are independently verified?
- What happens when an individual ticket lacks evidence, a worker fails,
  Jira is unavailable or the batch partially completes?
- Does the skill rely on Claude-specific tools, shell names, local paths,
  configuration inheritance or agent delegation?
- Are read/write constraints enforced by the runtime/tool permissions, or
  simply written as natural-language instructions?

### Refine Requirements
- What task scope and user approvals govern its requirements refinement?
- How does it establish functional/nonfunctional requirements, acceptance
  criteria, technical evidence and unresolved stakeholder questions?
- What outputs, side effects and stop conditions are specified?
- Does any design handoff (including Superpowers, if referenced) actually
  exist and have a verifiable input/output contract?

### Relationship
- Which skill owns **requirements completeness** versus **sprint readiness**?
- Does refinement happen before ticket delegation or inside each worker?
  Compare both as design **options**, with trade-offs; do not choose for the team.
- What minimum structured input/output should the handoff guarantee?
  Include ticket identity, evidence, unresolved questions, confidence and
  explicit blocked/needs-clarification/ready semantics **only if agreed**.
- Could identical questions be repeated, contradictory readiness judgments
  be returned, or unauthorized Jira modifications be attempted?
- Which platform-independent contract should survive a Claude→other-host
  migration, and which delegation mechanisms need a runtime adapter?

## Review acceptance criteria

- The **At a Glance** report covers every quality dimension even if its
  verdict is NOT APPLICABLE or UNVERIFIED.
- Each skill has separate file-backed evidence, source version and
  current-state Mermaid workflow; proposals never masquerade as existing
  behavior.
- Compliance reflects the actual published Agent Skills specification,
  not a universal claim about particular host plugin manifests.
- Existing safeguards precede risks. A written check or promise of
  read-only behavior does not count as an observed success.
- Cross-platform parity is not claimed without runtime evidence.
- Cases are **NOT RUN** and the team receives an explicit list of questions,
  owners/decisions to confirm, and a smallest next validation step.
