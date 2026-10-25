# Evaluations

The library has static repository checks and a first manual behavioral eval
package. It does not yet have an automated model-evaluation harness.

## Start here

[Code review: context for input validation](code-review/context-validation/README.md)
contains two runnable fixtures, a shared review request, pinned before/after
skill versions, an evaluator answer key, and a blank four-run scorecard.

The fixture verifier checks that the example code behaves as expected.
Model review results remain **not run** until the manual reviews are performed
and graded. Static checks and fixture checks are not skill-quality scores.

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
