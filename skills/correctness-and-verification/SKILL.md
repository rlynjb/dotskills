---
name: correctness-and-verification
description: "Diagnose and improve whether another skill reaches correct, evidence-backed conclusions. Use when evals reveal unsupported claims, missed invariants, incorrect boundary reasoning, weak verification, or confusion between observed facts and intended behavior. Do not invent domain requirements that have not been supplied or established."
---

# Correctness and Verification

## Objective

Turn requirements and claims into verifiable propositions, test relevant invariants
and failure paths, and preserve uncertainty when evidence does not establish a conclusion.

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
