# Run records — evaluator only

Create a new `<run-id>/` directory for each attempt. Start with status **Not run**;
record actual results only after execution. Keep prior attempts, including failures.

For each run save:

- `run.md`: case revision, exact selected prompt file and revision, model, harness,
  settings, tools, permissions, date, commands, and completed/error status.
- `response.md`: the actual reviewer response, without editorial rewriting.
- `grading.md`: criterion-level Pass / Fail / Unknown, evidence, validity status,
  overall outcome, limitations, and diagnosis or next action.
- Available traces or command evidence, when captured. Mark unavailable evidence
  unknown rather than inferring that a tool was used.

When comparing runs, identify the changed factor and keep other conditions
comparable. A single passing attempt does not establish deterministic behavior.
