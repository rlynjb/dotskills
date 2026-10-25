---
name: skill-lifecycle-and-release
description: "Manage an agent skill as versioned software: compare current and proposed versions, run regression and portability evals, review changes, and make evidence-based release or rollback decisions. Use for skill changes, model or harness upgrades, CI/CD planning, regressions, or release readiness."
---

# Skill Lifecycle and Release

## Objective

Make skill changes reviewable, comparable, reversible, and continuously tested across
the environments they claim to support.

## Human-gated specialist use

This skill normally operates as a specialist under `eval-driven-skill-development`.
Return evidence, diagnosis, teaching, recommendations, alternatives, and unresolved
questions to the entry-point methodology; do not independently edit the target skill,
run a gated comparison, or accept regression/release decisions.

When this specialist is invoked directly for skill improvement, use the same default
interaction contract:
- explain the relevant methodology concept in guided-learning mode;
- make one clear recommendation and explain why;
- offer materially different alternatives when useful;
- allow the human to contribute their own solution, opinion, constraint, or concern;
- treat feedback as feedback, not approval;
- obtain explicit approval before any consequential action such as changing the target
  skill, executing a gated run, or accepting a final decision.

If the entry-point methodology already owns the current human gate, do not create a
duplicate approval loop; return the specialist result to that gate.

## Required context

Provide:
- Current and proposed skill versions.
- Relevant eval suite and known failure modes.
- Supported models, harnesses, tools, and permission assumptions.
- Change rationale and intended behavior.
- Previous release or baseline results when available.

## Procedure

1. Version the skill change and state the behavior it intends to improve.
2. Run paired evals under comparable conditions: current versus proposed skill.
3. Check known defects, false positives, side effects, and preservation of protected state.
4. Re-run previously passing cases before accepting the change.
5. Test supported harnesses or models when portability is claimed.
6. Treat model, harness, tool-schema, or permission changes as regression triggers even
   when the skill text did not change.
7. Add boundary or adversarial cases for newly discovered failure modes.
8. Record release evidence, remaining limits, and rollback path.
9. Release only when evidence supports the intended improvement without unacceptable regression.
10. Keep historical results for future comparison.

## Output

Return:
- Version/change under review.
- Eval coverage run.
- Before/after results.
- Regressions and portability differences.
- Release decision: ready, blocked, limited, or rollback recommended.
- Required follow-up coverage.

## Decision rules

- Treat skills like software: version, evaluate, review, release.
- Do not declare portability without testing the claimed environments.
- Do not select only favorable runs.
- Keep infrastructure failures separate from quality scores.
- Structural validation is necessary but is not behavioral certification.

## Session-derived principles

This skill synthesizes AGNTCon/MCPCon material on agent regression testing, EvalBench,
and shipping agent skills safely: compare current and proposed skills on the same tasks,
run suites after skill and model changes, test across supported agents or harnesses,
use known clean state for mutating evals, and retain a rollback path.
