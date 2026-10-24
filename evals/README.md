# Evaluation roadmap

The library currently has **static checks only**, not a running evaluation harness.

Future behavioral evals should cover:
- correct versus incorrect skill triggering
- requirements discovery without unauthorized implementation
- evidence-backed code-review calibration and zero-finding cases
- source-citation fidelity, errors, and unknowns
- prompt-injection resistance and tool-permission boundaries
- cross-harness behavior and regression
- Buffr integration tests against the **real** engine with controlled normalized evidence

Prefer deterministic assertions for format and hard boundaries. For subjective quality, use reproducible scenarios, documented judge rubrics, repeated runs, and separate calibration data. Avoid claiming a score until tests actually run.
