# Evaluations

The library has static repository checks and a first manual behavioral eval
package. It does not yet have an automated model-evaluation harness.

## Start here

[Code review: context for input validation](code-review/context-validation/README.md)
contains two runnable fixtures, a shared review request, pinned before/after
skill versions, an evaluator answer key, and a blank four-run scorecard.

The [first recorded comparison](code-review/context-validation/results/2026-10-24-first-run/README.md)
includes four completed reviews, a graded scorecard, and operation traces.
Both versions satisfied the initial pair; no quality gain or regression was
demonstrated on those cases.

The [DDIA reference baseline](code-review/context-validation/results/2026-10-24-ddia-baseline/README.md)
uses the same cases with the unchanged DDIA prompt file supplied directly.
Both reviews passed the four quality checks. It is a starting point for work
on that individual lens, not a test of the skill wrapper or full DDIA coverage.

The fixture verifier checks that the example code behaves as expected.
Static checks and fixture checks are not skill-quality scores.

## Roadmap

Future behavioral evals should cover:
- correct versus incorrect skill triggering
- requirements discovery without unauthorized implementation
- evidence-backed code-review calibration and zero-finding cases
- source-citation fidelity, errors, and unknowns
- prompt-injection resistance and tool-permission boundaries
- cross-harness behavior and regression
- Buffr integration tests against the **real** engine with controlled normalized evidence

Prefer deterministic assertions for format and hard boundaries. For subjective quality, use reproducible scenarios, documented judge rubrics, repeated runs, and separate calibration data. Avoid claiming a score until tests actually run.
