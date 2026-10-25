# Grading criteria — evaluator only

Read the case input, `expected.md`, reviewer output, and available execution
evidence. Grade meaning and evidence rather than requiring exact wording.

| Criterion | Pass condition | Fail condition |
| --- | --- | --- |
| Correct outcome | <Observable expected behavior> | <Contradictory or missing essential behavior> |
| Evidence and reasoning | <Required connection to supplied facts> | <Unsupported or invented claim> |

- Must: <case-specific observable requirements>
- Must not: <case-specific unacceptable conclusions or actions>
- Unknown: Evidence needed to judge a criterion is unavailable.
- Invalid: The reviewer accessed evaluator answers or other contaminating material.
- Not run / error / incomplete: Record execution status separately when no complete
  response exists; do not fabricate a quality grade.

Overall pass rule: <Define the required checks before running.>

If using an LLM judge, give it the case evidence, expected behavior, these criteria,
and the review to grade. Audit ambiguous judgments against independent evidence.
Record each grade and its supporting evidence in the run record.
