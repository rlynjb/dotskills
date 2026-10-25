# First recorded comparison — October 24, 2026

**Result: both skill versions satisfied this two-case diagnostic.**
Each of the four reviews passed the four quality checks in the
[existing rubric](../../grader.md). The updated skill loaded its context guide
in both runs. This batch demonstrated no review-quality gain or regression on
these cases.

## Outcomes

| Case | Previous skill | Updated skill |
| --- | --- | --- |
| case-01: the caller validates | Correctly reported no actionable validation defect and explained the guard. | Correctly reported no actionable validation defect and explained the guard. |
| case-02: the guard is absent | Reported the reachable invalid write, with a concrete input and source evidence. | Reported the reachable invalid write, with a concrete input and source evidence. |

All four reviewers inspected the requirements, caller, and storage helper.
All four executed their own local Node.js checks and accurately described the
results. The fixture code and supplied skill files remained unchanged.

The defective fixture intentionally fails some application checks. Those
failures are evidence supporting the reviewers' findings; they are not failures
of the reviewers on this eval.

## What was compared

- Previous skill: `c6565141c5a5923235f80dd16a7ac680d58a1968`.
- Updated skill: `14abcdb4afe95c53a26522ab043fe1c0fc507421`.
- Eval source: `5f5137a5aa56406cac2fdb85ab4721a6e04fd30a`.
- Run date: October 24, 2026, America/Los_Angeles. Trace timestamps use UTC.
- Four fresh reviewer sessions, each created with `fork_turns: none`.
- Same inherited model and session setup; no model override. Exact model build,
  sampling parameters, and reasoning-effort value were not exposed.
- Same common task and local tool interface, with only workspace paths and
  selected skill contents changing within each matched case.
- Runtime: Node.js v24.22.1, Python 3.12.14, Git 2.51.1.

The before/after comparison includes the whole skill update: the new guide and
its connection through `SKILL.md`. It is not a guide-only or no-skill ablation.
The selected skill was supplied explicitly, so skill selection was not tested.

## Recorded evidence

Start with the [completed scorecard](scorecard.md).
Each trace is JSON Lines: event 1 is the first line, event 2 the second, and so on.
Events record the requested operation, returned source or command output,
exit status, timestamp, and source hashes for reads.

| Run | Case / skill | Original review output | Local operation trace | Verification observed |
| --- | --- | --- | --- | --- |
| 01 | case-01 / previous | [Review](../../cases/case-01/results/2026-10-24-first-run-run-01/run-01.md) | [Trace](../../cases/case-01/results/2026-10-24-first-run-run-01/run-01.trace.jsonl) | 24 invalid inputs, 9 valid inputs, and a mixed-call sequence passed. |
| 02 | case-01 / updated | [Review](../../cases/case-01/results/2026-10-24-first-run-run-02/run-02.md) | [Trace](../../cases/case-01/results/2026-10-24-first-run-run-02/run-02.trace.jsonl) | 34 checks passed: 24 invalid, 9 valid, and 1 sequential-write case. |
| 03 | case-02 / previous | [Review](../../cases/case-02/results/2026-10-24-first-run-run-03/run-03.md) | [Trace](../../cases/case-02/results/2026-10-24-first-run-run-03/run-03.trace.jsonl) | 5 application checks passed and 17 failed; exit status 1. |
| 04 | case-02 / updated | [Review](../../cases/case-02/results/2026-10-24-first-run-run-04/run-04.md) | [Trace](../../cases/case-02/results/2026-10-24-first-run-run-04/run-04.trace.jsonl) | 4 application checks passed and 12 failed; exit status 1. |

The reviewers independently chose their verification inputs. Different numbers
of application checks are not comparative skill-quality scores.

Additional records:

- [Manifest](manifest.json): pinned revisions, preparation metadata, input and
  output hashes, inherited model setup, agent identifiers, and recorded grades.
- [Recorder](recording/observe.py) and [launch template](recording/launch-template.txt):
  the identical local observation protocol used for every review.
- [Fixture verification](fixture-verification.txt): deterministic setup check
  captured before launching the model reviews.
- [Secondary evidence audit](grading-audit.md): a separate agent checked the
  grades, source hashes, recorded operations, and execution claims.

The original review outputs are preserved. Some contain absolute workspace links
from the session; their cited source corresponds to the versioned
[case-01](../../cases/case-01/input) or [case-02](../../cases/case-02/input) files.
Run 03's Markdown hard breaks were normalized to blank lines for whitespace
checks; its wording is unchanged and its exact original text is retained in
[run-03.raw.json](../../cases/case-02/results/2026-10-24-first-run-run-03/run-03.raw.json).

## A process difference worth retaining

Both previous-skill sessions read the full 634-line integrated review reference.
Both updated-skill sessions read the new context guide and then the
evidence-calibration and compact-review sections of the integrated reference.
Neither updated session missed the small caller or helper in these cases.

This is an observed change in reference selection. It is not a measured token,
latency, or cost saving, and it does not establish general efficiency.

## Boundaries of this result

These were separate input directories and fresh agent contexts, not operating
system sandboxes. Reviewers were instructed to use the recorded interface and
stay within their assigned inputs. The answer key, other cases, other skill
versions, and previous answers were not supplied to their contexts. The recorded
actions stayed within scope and the final input hashes matched preparation.

The traces cover local operations through the recorder. They are not a
provider-level audit of all model or platform activity. Grade validity and
inspection claims within that documented observation boundary.

The primary assistant authored the eval and graded these runs. The separate
audit had access to the preliminary grades. No human adjudication is claimed.

This is one run per skill/case combination under one host configuration. It does
not establish general reliability, statistical significance, behavior in other
harnesses, or whether the context update caused a general improvement.
The existing skill already contained evidence-calibration guidance.

## What follows

Keep this pair as a small regression check. No skill correction is justified by
this batch: both versions reached supported conclusions. The next Phase 1 work
is the real-code walkthrough and the missing, distracting, stale, or conflicting
context scenarios. Those scenarios were not part of these four runs.
