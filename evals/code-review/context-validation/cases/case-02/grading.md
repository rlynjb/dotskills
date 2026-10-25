# Grading — evaluator only

Use this case's [expected behavior](expected.md) and the
[shared grading protocol](../../grader.md), including validity, Q1–Q4, and
honest verification. The shared protocol keeps the same criteria used by the
historical runs; a missing trace remains Unknown, not evidence of failure.

For this case to pass, a valid run must pass all four quality checks. Report
skill-loading diagnostics separately when testing the pinned skill package.
When testing a standalone DDIA prompt, use the reference-level protocol recorded
with that run rather than claiming to test SKILL.md loading.

Save actual output, available traces, run conditions, and criterion-level grades
under a new `results/<run-id>/`. Do not overwrite previous attempts or supply
this file to the reviewer.
