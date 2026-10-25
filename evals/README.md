# Evaluations

The library has static repository checks and a first manual behavioral eval
package. It does not yet have an automated model-evaluation harness.

## Start here

Use [Eval-Driven Skill Development](../docs/eval-driven-skill-development.md) for the shared workflow across skills, including case design, run checklists, grading, failure diagnosis, and regression comparisons.

[Code review: context for input validation](code-review/context-validation/README.md)
contains two runnable cases with expected behavior, grading guidance, and recorded
attempts. Run and grade one case at a time; save each attempt under that case’s
`results/<run-id>/` directory.

The fixture verifier checks that the example code behaves as expected.
Static checks and fixture checks are not skill-quality scores.

## Create a case

Copy the [reusable case template](../templates/case/README.md) to
`evals/<skill>/<capability>/cases/<case-id>/`. It separates reviewer inputs and
requirements from expected behavior, grading criteria, and actual run results.
Use the same structure for mock examples and real application snapshots; vary the
materials inside `input/` as needed. The template is for manual authoring and keeps the migrated suite's preparation commands working.

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
