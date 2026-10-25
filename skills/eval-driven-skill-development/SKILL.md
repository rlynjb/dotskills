---
name: eval-driven-skill-development
description: "Develop or improve any agent skill using representative eval cases, preserved run evidence, diagnosis before editing, targeted changes, and regression checks. Use when creating a new skill, improving an existing skill, investigating a failed eval, or deciding which methodology should diagnose a skill failure. Do not use it as the task skill that performs the end-user job itself."
---

# Eval-Driven Skill Development

## Objective

Improve a target skill through evidence from actual eval runs instead of adding
instructions speculatively. The target skill may be code review, investigation,
refinement, learning, prompting, or any other reusable skill.

## Required context

Establish:
- The target skill and exact version.
- One observable capability or failure to evaluate.
- The eval case and evaluator-only expected behavior.
- Model, harness, tools, permissions, and relevant limits.
- Original output plus available read/search/tool/command evidence.

Keep answer keys and grading criteria out of the evaluated agent's input.

## Procedure

1. Define and verify one observable expected behavior.
2. Run the unchanged target skill on a neutral case in a fresh task context.
3. Preserve the output, trace, configuration, errors, and limitations.
4. Grade the result without forcing certainty: Pass, Fail, Unknown, Invalid, Error,
   or Incomplete are valid outcomes.
5. Diagnose before editing. Determine whether the cause is the case, rubric, missing
   context, harness/tooling, model variability, or target-skill guidance.
6. Route a confirmed target-skill weakness to the relevant methodology:
   - missing, stale, conflicting, distracting, or excessive context → `context-engineering`
   - unsupported claims, broken invariants, or weak verification → `correctness-and-verification`
   - versioning, regressions, portability, CI, or release → `skill-lifecycle-and-release`
   - unclear trajectory, insufficient telemetry, or production feedback → `agent-observability-and-feedback`
   - authority, provenance, permissions, approvals, or unsafe actions → `agent-trust-and-governance`
7. Make the smallest general change supported by the diagnosis. Do not encode the
   case's specific answer into the target skill.
8. Re-run the same case under comparable conditions.
9. Run relevant previously passing cases and an independent case when practical.
10. Keep useful cases as regression coverage and record unresolved limits.

## Failure handoff

When invoking a specialist methodology, pass:

```text
Target skill and version:
Capability under test:
Case and expected behavior:
Observed behavior:
Relevant output/trace evidence:
Known setup limitations:
Current failure hypothesis:
Question for the specialist methodology:
```

The specialist diagnoses the failure; it does not automatically edit the target skill.

## Output

Return:
- Target skill and capability.
- Case and run status.
- Evidence-backed diagnosis.
- Specialist methodology used, if any.
- Targeted change proposed or made.
- Before/after result and regression status.
- Remaining uncertainty and next independent case.

## Decision rules

- A failed eval is evidence to investigate, not an automatic prompt rewrite.
- A plausible final answer does not prove a file or tool was used.
- Preserve unsuccessful attempts and infrastructure failures.
- Hold the case and rubric fixed when comparing skill versions.
- Treat model or harness changes as possible regression triggers.

## Session-derived principles

This operational method synthesizes the AGNTCon/MCPCon sessions on real agent
evaluations, agent regression testing, EvalBench, and shipping agent skills safely:
evaluate realistic user journeys, start mutating evals from known state, keep
comparisons reproducible, treat skills like versioned software, and re-run coverage
when the skill, model, harness, or tools change.
