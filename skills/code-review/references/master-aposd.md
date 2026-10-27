# APOSD master review lens

Extracted from [the imported source](code-review-aposd.md), section 0.
Use this master prompt as the complete technical checklist for this lens.
The shared tutorial and draft-comment format in SKILL.md controls presentation.
These are book-inspired review instructions, not verbatim book text.

Review this change using principles from A Philosophy of Software Design.

Do not focus only on style or formatting.

Evaluate:

1. What behavior the change introduces or modifies.
2. Whether the implementation matches the intended behavior.
3. Which modules and interfaces are affected.
4. Where the new complexity is located.
5. Whether modules hide meaningful complexity from callers.
6. Whether any interface became more complicated.
7. Whether implementation details leak across module boundaries.
8. Whether design knowledge is duplicated.
9. Whether responsibilities and state ownership are clear.
10. Whether the change introduces temporal coupling or required call ordering.
11. Whether the change increases change amplification.
12. Whether names and control flow make the code obvious.
13. Whether errors are handled at the correct abstraction level.
14. Whether the tests verify behavior and important invariants.
15. Whether a smaller or more localized design would be clearer.

Separate findings into:

- Correctness issues
- Design and complexity issues
- Maintainability risks
- Testing gaps
- Optional improvements

For every finding:

- Cite the file and symbol
- Explain the concrete consequence
- Give a realistic scenario where it matters
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Do not recommend abstraction merely to reduce line count.
Do not reward additional layers unless they hide meaningful complexity.

Evidence calibration: check the relevant surrounding code, tests,
contracts, and configuration before declaring a defect. Distinguish
confirmed defects, plausible code-backed risks, verification gaps,
and optional improvements; attach preconditions to uncertain claims.
Severity must follow supported impact; do not label speculative future
scale, unmeasured latency, or unknown deployment behavior as a blocker.
Report the reviewed scope and which tests or checks were actually run.
If no actionable issues are supported, report zero findings with limits
rather than implying the entire repository is defect-free.
