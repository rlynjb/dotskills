# DDIA master review lens

Extracted from [the imported source](code-review-ddia.md), section 0.
Use this master prompt as the complete technical checklist for this lens.
The shared tutorial and draft-comment format in SKILL.md controls presentation.
These are book-inspired review instructions, not verbatim book text.

Review this change using principles from Designing Data-Intensive Applications.

Do not focus only on style or the happy path.

Evaluate:

1. What user or system behavior the change introduces or modifies.
2. Whether the implementation matches the intended behavior.
3. Which data entities, schemas, stores, and data flows are affected.
4. Which store is authoritative for each important value.
5. Whether the read and write access patterns match the storage and indexes;
   where relevant, compare normalized joins with denormalized/derived reads,
   including performance evidence, update cost, and freshness trade-offs.
6. Whether transaction boundaries preserve all important invariants.
7. Whether concurrent operations can produce anomalies.
8. What consistency and ordering guarantees the feature provides.
9. Whether retries, duplicate requests, or redelivery are safe.
10. Whether events, queues, caches, and derived views remain consistent enough.
11. Whether schema and encoding changes are backward and forward compatible.
12. Whether replication, partitioning, or failover assumptions are safe.
13. Whether partial failures and ambiguous outcomes are recoverable.
14. Whether the design remains safe and operable at 10× or 100× scale.
15. Whether tests verify the important guarantees and failure cases.

Separate findings into:

- Correctness and invariant issues
- Data-model and consistency issues
- Reliability and operability risks
- Testing gaps
- Optional improvements

For every finding:

- Cite the file, symbol, query, schema, migration, or configuration
- Explain the concrete consequence
- Give a realistic event sequence, concurrency scenario, or workload
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Clearly separate guarantees proven by code or configuration from assumptions.

Do not recommend distributed infrastructure merely because it could scale
further in theory.

Evidence calibration: check the relevant surrounding code, tests,
contracts, and configuration before declaring a defect. Distinguish
confirmed defects, plausible code-backed risks, verification gaps,
and optional improvements; attach preconditions to uncertain claims.
Severity must follow supported impact; do not label speculative future
scale, unmeasured latency, or unknown deployment behavior as a blocker.
Report the reviewed scope and which tests or checks were actually run.
If no actionable issues are supported, report zero findings with limits
rather than implying the entire repository is defect-free.
