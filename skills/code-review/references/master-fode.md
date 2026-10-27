# FODE master review lens

Extracted from [the imported source](code-review-fode.md), section 0.
Use this master prompt as the complete technical checklist for this lens.
The shared tutorial and draft-comment format in SKILL.md controls presentation.
These are book-inspired review instructions, not verbatim book text.

Review this change using principles from Fundamentals of Data Engineering.

Do not focus only on code style or whether the happy path runs.

Evaluate:

1. What user, analyst, ML, operational, or platform behavior the change modifies.
2. Which data engineering lifecycle stages are affected: generation, storage,
   ingestion, transformation, serving.
3. Which source systems, source contracts, and upstream owners are involved.
4. What data is stored, where it is stored, how it is formatted, and how long it
   is retained.
5. How ingestion handles schema drift, late data, duplicates, retries, replay,
   and source throttling.
6. Whether transformations preserve business meaning, lineage, freshness,
   quality, and incremental correctness.
7. Whether served outputs match consumer needs, SLAs, access patterns, and
   definitions.
8. Whether data quality checks, metadata, ownership, lineage, and governance are
   sufficient for the importance of the dataset.
9. Whether security and privacy are handled across the lifecycle rather than as
   a final serving-layer concern.
10. Whether orchestration expresses true dependencies, recovery behavior,
   schedules, retries, and backfill semantics.
11. Whether DataOps practices support safe promotion, reproducible runs,
   environment isolation, rollback, monitoring, and incident response.
12. Whether architecture choices are loosely coupled, scalable, failure-aware,
   reversible, and proportionate to the team's maturity.
13. Whether technology choices solve a real lifecycle problem instead of adding
   tool-centered complexity.
14. Whether cost, capacity, observability, and on-call burden are visible and
   acceptable.
15. Whether tests prove the important source contracts, transformations,
   quality checks, recovery paths, and consumer-facing behavior.

Separate findings into:

- Lifecycle and consumer-fit issues
- Data quality, governance, and security issues
- Reliability and operability risks
- Technology-choice and cost issues
- Testing gaps and optional improvements

For every finding:

- Cite the file, dataset, model, DAG, job, query, schema, configuration, or tool
- Explain the concrete consequence
- Give a realistic source, pipeline, consumer, workload, or incident scenario
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Clearly separate what the implementation proves from what it assumes about
sources, schemas, schedules, quality, consumers, costs, and operations.

Do not reward fashionable data architecture unless it improves a concrete
lifecycle stage or undercurrent.

Evidence calibration: check the relevant surrounding code, tests,
contracts, and configuration before declaring a defect. Distinguish
confirmed defects, plausible code-backed risks, verification gaps,
and optional improvements; attach preconditions to uncertain claims.
Severity must follow supported impact; do not label speculative future
scale, unmeasured latency, or unknown deployment behavior as a blocker.
Report the reviewed scope and which tests or checks were actually run.
If no actionable issues are supported, report zero findings with limits
rather than implying the entire repository is defect-free.
