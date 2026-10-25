# DDIA baseline grading protocol

This protocol was fixed before the reviewer sessions were launched.

Reuse the established expectations and Q1–Q4 quality checks from
../../grader.md for the same two validation fixtures. Grade each result
against its case independently using PASS, FAIL, or UNKNOWN and observed evidence.

This is a direct-reference baseline. The supplied review guidance is the
unchanged code-review-ddia.md at e1eda00b1d36b543e8a138b3726921b05ed3062c.
The previous before/after skill revisions and SKILL.md/context-guide loading
checks in the shared grader do not apply. Instead, record whether this exact
DDIA reference was loaded, with its actual returned sections and any truncation.
Loading is separate from quality.

Run validity requires the assigned fixture and DDIA reference, unchanged inputs,
fresh reviewer context, and no answer key, other case, other output, or evaluator
corrections supplied to the reviewer. Report any uncertainty in the recorder's
observation boundary. The recorder is not an operating-system sandbox.

Record instruction-selection behavior descriptively: sections actually loaded,
any execution errors, and whether the output invents out-of-scope database or
distributed-system requirements. Do not convert section count, output length,
or formatting into a new quality score after seeing the reviews.

These cases exercise validation and evidence calibration. They do not establish
DDIA coverage of transactions, isolation, replication, retries, or consistency.
No no-guidance or reformatted-DDIA comparison is part of this baseline.
