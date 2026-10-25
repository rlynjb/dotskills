---
name: correctness-and-verification
description: "Diagnose and improve whether another skill reaches correct, evidence-backed conclusions. Use when evals reveal unsupported claims, missed invariants, incorrect boundary reasoning, weak verification, or confusion between observed facts and intended behavior. Do not invent domain requirements that have not been supplied or established."
---

# Correctness and Verification

## Objective

Turn requirements and claims into verifiable propositions, test relevant invariants
and failure paths, and preserve uncertainty when evidence does not establish a conclusion.

## Required context

Provide:
- Target skill and capability under evaluation.
- Applicable requirements or expected behavior.
- Relevant source evidence, fixtures, contracts, or observations.
- Agent output and available execution/tool trace.
- Known missing evidence and environmental limits.

## Procedure

1. State the claim being evaluated in falsifiable form.
2. Identify the requirement, invariant, property, or contract the claim depends on.
3. Determine what evidence would confirm, refute, or leave the claim unresolved.
4. Prefer deterministic checks for directly observable facts.
5. Inspect relevant boundaries and failure paths, not only the happy path.
6. Distinguish observed behavior, intended behavior, inferred behavior, and unknown behavior.
7. Search for counterexamples that would invalidate the current conclusion.
8. Check that cited evidence supports the claimed scope and condition.
9. If evidence is insufficient, preserve Unknown rather than upgrading plausibility to fact.
10. Recommend a general verification rule and a regression case.

## Output

Return:
- Claim under test.
- Governing requirement or invariant.
- Supporting and contradicting evidence.
- Verification status: confirmed, refuted, or unresolved.
- General target-skill improvement.
- Regression check or case.

## Decision rules

- Confidence, citations, and fluent explanation are not proof.
- Reading a test is not the same as executing it.
- A passing test supports only what the test actually checks.
- Do not infer intended behavior from implementation alone.
- Prefer a precise unresolved conclusion to a fabricated binary answer.

## Session-derived principles

This skill synthesizes AGNTCon/MCPCon material on correctness and universal properties,
trustworthy code review, and eval judging. Translate vague goals into properties that
can be disproved, inspect the boundaries that could change the result, use deterministic
checks where possible, and require semantic graders to evaluate defined meaning rather
than surface plausibility.
