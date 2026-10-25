# Completed scorecard — October 24, 2026

Graded against [the existing rubric](../../grader.md), using original reviewer
outputs, actual local operation traces, and the prepared source files.
All grades below are limited to these two cases and the recorded tool protocol.
The primary assistant performed the grading; a separate agent checked the
evidence in the [secondary audit](grading-audit.md).

## Setup and validity

| Field | Recorded value |
| --- | --- |
| Eval source commit | `5f5137a5aa56406cac2fdb85ab4721a6e04fd30a` |
| Previous skill | `c6565141c5a5923235f80dd16a7ac680d58a1968` |
| Updated skill | `14abcdb4afe95c53a26522ab043fe1c0fc507421` |
| Reviewer harness | Fresh ChatGPT collaboration subagents; `fork_turns: none`. |
| Model | Parent-inherited; session identifies itself as GPT-6 Astra Pro. No override; exact build and sampling values unavailable. |
| Tools | Same recorded list/read/search/run interface in every session. |
| Input integrity | All files matched their preparation hashes after review. |
| Common request | Normalized `task.md` matched the same prompt in all four workspaces. |
| Contamination check | No answer key or other run was supplied; recorded reads and commands stayed within the assigned inputs. |
| Trace boundary | Actual recorder operations, not complete provider-level telemetry or an OS sandbox. |

All four runs are marked **VALID within this manual protocol**. Missing
provider-level telemetry remains a limitation, not proof of contamination.
See [manifest.json](manifest.json) for exact preparation and integrity records.

## Quality grades

| Run | Case | Skill | Q1: Correct conclusion | Q2: Supported explanation | Q3: Context inspected | Q4: Honest verification |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | case-01 | Previous | PASS | PASS | PASS | PASS |
| 02 | case-01 | Updated | PASS | PASS | PASS | PASS |
| 03 | case-02 | Previous | PASS | PASS | PASS | PASS |
| 04 | case-02 | Updated | PASS | PASS | PASS | PASS |

## Loading diagnostics

| Run | Selected `SKILL.md` | New context guide | Recorded evidence |
| --- | --- | --- | --- |
| 01 | PASS | N/A | [Trace](../../cases/case-01/results/2026-10-24-first-run-run-01/run-01.trace.jsonl), event 3. |
| 02 | PASS | PASS | [Trace](../../cases/case-01/results/2026-10-24-first-run-run-02/run-02.trace.jsonl), events 3 and 6. |
| 03 | PASS | N/A | [Trace](../../cases/case-02/results/2026-10-24-first-run-run-03/run-03.trace.jsonl), event 2. |
| 04 | PASS | PASS | [Trace](../../cases/case-02/results/2026-10-24-first-run-run-04/run-04.trace.jsonl), events 3 and 4. |

Loading the guide was assessed separately from output quality.

## Evidence by run

### Run 01 — case-01, previous skill

- **Q1 and Q2:** The [review](../../cases/case-01/results/2026-10-24-first-run-run-01/run-01.md) reports no actionable issues and
  identifies the caller's guard, original-name preservation, one append, and
  return-object identity using the actual source.
- **Q3:** [Trace](../../cases/case-01/results/2026-10-24-first-run-run-01/run-01.trace.jsonl) events 4, 5, and 7 return the full
  requirements, caller, and helper. Event 6 returns the integrated reference.
- **Q4:** Event 8 records the inline Node command, exit status 0, and output
  confirming 24 invalid and 9 valid inputs plus the mixed sequence. This matches
  the review's execution claims.

### Run 02 — case-01, updated skill

- **Q1 and Q2:** The [review](../../cases/case-01/results/2026-10-24-first-run-run-02/run-02.md) recognizes the guarded path and
  explains why duplicate validation in the internal helper is unnecessary under
  the supplied contract, with accurate source locations.
- **Q3:** [Trace](../../cases/case-01/results/2026-10-24-first-run-run-02/run-02.trace.jsonl) events 2, 8, and 10 return the full
  requirements, helper, and caller. Event 6 returns the context guide; events
  7 and 9 return the compact procedure and calibration sections.
- **Q4:** Event 12 records exit status 0 and 34 passing cases, matching the
  review's 24 invalid, 9 valid, and 1 sequential-write breakdown.

### Run 03 — case-02, previous skill

- **Q1 and Q2:** The [review](../../cases/case-02/results/2026-10-24-first-run-run-03/run-03.md) reports one confirmed defect with a
  blank-name example, the unguarded caller, and the write. It correctly explains
  that `null` failing incidentally does not validate the other input classes.
- **Q3:** [Trace](../../cases/case-02/results/2026-10-24-first-run-run-03/run-03.trace.jsonl) events 3, 6, and 7 return the full
  requirements, caller, and helper. Event 4 returns the integrated reference.
- **Q4:** Event 8 records 22 cases, 5 passes, 17 contract failures, and exit
  status 1. The review reports the observed failures without calling them passes
  or claiming an existing test suite ran.

### Run 04 — case-02, updated skill

- **Q1 and Q2:** The [review](../../cases/case-02/results/2026-10-24-first-run-run-04/run-04.md) reports the invalid write, cites the
  actual caller and helper, and gives the concrete empty-object path that stores
  a record whose name is undefined.
- **Q3:** [Trace](../../cases/case-02/results/2026-10-24-first-run-run-04/run-04.trace.jsonl) events 2, 8, and 9 return the full
  requirements, caller, and helper. Event 4 returns the context guide; events
  7 and 10 return the calibration and compact sections.
- **Q4:** Event 11 records 16 cases, 4 passes, 12 contract failures, and exit
  status 1. The review accurately reports that failed command and its cause.

## Comparison

- Case-01: previous PASS, updated PASS across Q1-Q4.
- Case-02: previous PASS, updated PASS across Q1-Q4.
- No quality gain or regression demonstrated on these cases.
- The updated guide loaded in both updated-skill sessions.
- Updated sessions selected bounded integrated-reference sections; baseline
  sessions read the full integrated reference. No token/cost score is inferred.
- No targeted skill correction follows from this batch.
- Real-change and context-variation walkthroughs remain outstanding.
