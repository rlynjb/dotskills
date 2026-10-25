# DDIA baseline scorecard

Graded against the fixed [protocol](grading-protocol.md), the existing case
expectations and Q1–Q4 in [grader.md](../../grader.md), and the actual source
reads and execution results.

## Grades

| Run | Case | Q1: Correct conclusion | Q2: Supported explanation | Q3: Context inspected | Q4: Honest verification |
| --- | --- | --- | --- | --- | --- |
| 01 | case-01, caller validates | PASS | PASS | PASS | PASS |
| 02 | case-02, guard absent | PASS | PASS | PASS | PASS |

These grades apply to two individual reviews, not to the whole DDIA book lens.

## Loading and setup

| Check | Run 01 | Run 02 |
| --- | --- | --- |
| Pinned DDIA reference accessed | PASS: trace events 2 and 7 | PASS: trace events 4 and 6 |
| Assigned fixture and task | PASS | PASS |
| Prepared inputs unchanged after review | PASS | PASS |
| Validity within the recorded protocol | PASS | PASS |
| SKILL.md/context-guide loading | N/A: not supplied | N/A: not supplied |
| Complete model-visible delivery of every reference line | UNKNOWN | UNKNOWN |
| Absolute isolation beyond recorded operations | UNKNOWN | UNKNOWN |

All source-read hashes match the expected inputs. The reference's Git blob
and SHA-256 match the manifest. Both tasks match the common template after
workspace substitution. Each trace contains eight recorded operations.

## Run 01: validation exists

- **Q1:** The [review](../../cases/case-01/results/2026-10-24-ddia-baseline-run-01/run-01.md) explicitly reports no actionable issue and
  explains why validation in the caller makes a second guard in the internal
  helper unnecessary under the supplied contract.
- **Q2:** It cites the guard in `create-user.cjs:4–11`, call at line 14, write in
  `save-user.cjs:2–4`, and the corresponding requirements. It correctly preserves
  the supplied name instead of imposing a trimming requirement.
- **Q3:** [Trace](../../cases/case-01/results/2026-10-24-ddia-baseline-run-01/run-01.trace.jsonl) events 3, 5, and 6 return the full
  requirements, helper, and caller.
- **Q4:** Event 8 records the actual Node command and output: 27 invalid inputs,
  10 valid inputs, empty/populated arrays, repeated-call checks, 232 assertions,
  and exit code 0. The response accurately describes those checks and their limits.

## Run 02: validation is missing

- **Q1:** The [review](../../cases/case-02/results/2026-10-24-ddia-baseline-run-02/run-02.md) reports the reachable invalid write as a
  confirmed contract violation.
- **Q2:** It cites the unguarded call in `create-user.cjs:3–4`, helper write in
  `save-user.cjs:1–4`, and requirements lines 6–11. Examples include missing,
  non-string, and blank names. It correctly notes that `null` throwing does not
  protect other invalid inputs.
- **Q3:** [Trace](../../cases/case-02/results/2026-10-24-ddia-baseline-run-02/run-02.trace.jsonl) events 2, 5, and 7 return the full
  requirements, helper, and caller.
- **Q4:** Event 8 records five passing valid cases and only one passing
  invalid-input contract check out of 19. Each of the other 18 failure records
  shows an append without an exception. The diagnostic process exits 0 after
  printing the failures; the review reports the application failures accurately.

The rubric does not require a particular severity label when the actual impact
is accurately stated. The run 02 blocking classification is tied to the explicit
input-validation contract, not a speculative production scenario.

## Instruction-selection observations

Run 01 requested DDIA lines 1–1471 and then 373–875. Run 02 requested lines
1–1471 and then 350–932. The recorded stdout contains those numbered source
ranges without truncation. Outer tool delivery and internal model selection
are not captured, so no claim of complete comprehension follows.

Neither review invents a database, distributed-system, durability, or retry
requirement. No efficiency or formatting-quality score is inferred from
the broad reads or the length of the answers.

## Independent check

The [independent audit](grading-audit.md) was performed without supplying the
primary grades. It agreed with Q1–Q4, reference loading, and recorded-boundary
validity for both runs.

The DDIA reference remained byte-identical. No no-guidance, revised-prompt,
or broader DDIA comparison was run.
