# AT master review lens

Extracted from [the imported source](code-review-at.md), section 0.
Use this master prompt as the complete technical checklist for this lens.
The shared tutorial and draft-comment format in SKILL.md controls presentation.
These are book-inspired review instructions, not verbatim book text.

Review this change using principles from Algorithmic Thinking.

First understand the problem before criticizing the implementation.

Evaluate:

1. What problem is being solved.
2. What the expected inputs and outputs are.
3. What assumptions are made about the input.
4. What constraints affect the solution.
5. What the simplest correct solution would look like.
6. What algorithmic approach the implementation uses.
7. Why that algorithm should produce the correct result.
8. What data structures are used and why.
9. Whether those data structures fit the operations performed.
10. What invariants must remain true during execution.
11. What boundary cases or unusual inputs could break the implementation.
12. What the time complexity is.
13. What the space complexity is.
14. Where repeated or unnecessary work occurs.
15. Whether tests verify the important input classes and invariants.

Separate findings into:

- Problem-understanding issues
- Correctness issues
- Algorithm and data-structure issues
- Complexity issues
- Testing gaps
- Optional improvements

For every finding:

- Cite the file and symbol
- Explain the concrete consequence
- Give a specific input or execution that demonstrates the issue
- Explain expected versus actual behavior
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Clearly separate:

- Behavior proven by the implementation
- Assumptions
- Complexity analysis
- Potential optimizations

Prefer the simplest solution that satisfies the actual constraints.

Do not optimize merely because a theoretically faster algorithm exists.

Evidence calibration: check the relevant surrounding code, tests,
contracts, and configuration before declaring a defect. Distinguish
confirmed defects, plausible code-backed risks, verification gaps,
and optional improvements; attach preconditions to uncertain claims.
Severity must follow supported impact; do not label speculative future
scale, unmeasured latency, or unknown deployment behavior as a blocker.
Report the reviewed scope and which tests or checks were actually run.
If no actionable issues are supported, report zero findings with limits
rather than implying the entire repository is defect-free.
