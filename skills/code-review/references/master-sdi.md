# SDI master review lens

Extracted from [the imported source](code-review-sdi.md), section 0.
Use this master prompt as the complete technical checklist for this lens.
The shared tutorial and draft-comment format in SKILL.md controls presentation.
These are book-inspired review instructions, not verbatim book text.

Review this change using system-design principles.

Start with requirements and architecture before suggesting technologies.

Evaluate:

1. What user or system requirement the change serves.
2. Functional requirements.
3. Non-functional requirements such as latency, availability, throughput,
   durability, and consistency.
4. Major system components and their responsibilities.
5. Request flow through the system.
6. Data flow and state ownership.
7. API and service boundaries.
8. Database and storage choices.
9. Read and write access patterns.
10. Caching strategy.
11. Synchronous versus asynchronous processing.
12. Expected bottlenecks and scaling behavior.
13. Failure modes and recovery behavior.
14. Monitoring, metrics, logging, tracing, and operational readiness.
15. Whether the architecture can evolve without unnecessary rewrites.

Separate findings into:

- Requirement and architecture issues
- Boundary and ownership issues
- Scalability risks
- Reliability and operability risks
- Testing gaps
- Optional improvements

For every finding:

- Cite the relevant file, service, API, schema, configuration, or component
- Explain the concrete consequence
- Give a realistic workload, growth, or failure scenario
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Clearly separate:

- Requirements
- Confirmed implementation behavior
- Assumptions
- Current problems
- Future scalability concerns

Do not design for hypothetical billions of users unless the requirements justify
it.

Prefer the simplest architecture that satisfies current requirements while
leaving reasonable room for growth.

Evidence calibration: check the relevant surrounding code, tests,
contracts, and configuration before declaring a defect. Distinguish
confirmed defects, plausible code-backed risks, verification gaps,
and optional improvements; attach preconditions to uncertain claims.
Severity must follow supported impact; do not label speculative future
scale, unmeasured latency, or unknown deployment behavior as a blocker.
Report the reviewed scope and which tests or checks were actually run.
If no actionable issues are supported, report zero findings with limits
rather than implying the entire repository is defect-free.
