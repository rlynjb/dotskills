# Fundamentals of Data Engineering Code-Review Prompt Library

Quick-reference for reviewing a change with an AI coding agent, using *Fundamentals of Data Engineering* to judge whether the change improves the data engineering lifecycle, serves real downstream needs, respects the undercurrents, and avoids tool-first architecture.

A normal review asks:

```text
Does this code work?
Are there bugs?
Are there tests?
```

A Fundamentals of Data Engineering review also asks:

```text
Where does this change sit in the data engineering lifecycle?
Who consumes the data, and what do they need from it?
What source, storage, ingestion, transformation, and serving contracts changed?
Which undercurrents are affected: security, data management, DataOps,
architecture, orchestration, and software engineering?
Is this technology choice justified by workload, team maturity, cost, and reversibility?
```

Fundamentals of Data Engineering should **complement, not replace** reviews for ordinary correctness, security, accessibility, maintainability, performance, and product behavior.

---

## Evidence and severity calibration (applies to every review prompt)

**Use this rule for master, compact, and focused prompts.** Each copyable
prompt below also includes a concise reminder, so standalone prompts still
calibrate claims. The goal is accuracy, not a long list of possible problems.

- **Ground findings in inspected evidence:** cite actual code, relevant call
  paths, tests, contracts, config, or results. Check existing guards,
  validations, and surrounding behavior before claiming something is missing.
- **Label the claim, not just its severity:**
  - **Confirmed defect:** a contradiction of a supported requirement or a
    reproducible error/failure, with the relevant conditions established.
  - **Plausible risk:** a code-supported failure scenario whose likelihood,
    reachability, or real-world impact still needs verification; state the
    preconditions and uncertainty.
  - **Verification gap:** needed evidence is inaccessible or checks were not
    performed; this is not automatically a bug.
  - **Optional improvement:** a design/performance alternative with a
    justified trade-off, not a defect by default.
- **Calibrate severity separately:** use **blocking** only for an evidenced
  release-stopping correctness, security, data-loss, or agreed-contract issue;
  **important** for consequential supported concerns; **optional** for
  nonurgent improvements. Unknown impact is not automatically high severity.
- **Do not overclaim:** a hypothetical failure is not an observed incident;
  a theoretical complexity concern is not measured slowness; absent tests
  are not proof the code is wrong; code inspection is not proof of production
  behavior, load, cost, or deployment configuration.
- **Report the review boundary:** say whether this is a diff, feature path,
  representative sample, or broader repository inspection. List meaningful
  gaps in files, environments, tests, or tools. Never claim the entire repo
  is safe or free of issues when only part was inspected.
- **State verification honestly:** distinguish tests/benchmarks actually run
  and their outcomes from tests merely read or recommended. Don't invent
  outputs, metrics, exploitability, root causes, or stakeholder intent.
- **Prefer precision over volume:** deduplicate shared root causes and permit
  **zero actionable findings**. If none are supported, say "No actionable
  issues found in the inspected scope," with limitations, not "bug-free."

## Index

| #  | Prompt                                                                        | What it does                                                       | Reach for it when                                      |
| -- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------ |
| ★  | [**Compact daily**](#compact-daily-code-review-prompt)                        | 12-point pass in one shot, blocking vs optional                    | Default for data pipeline, analytics, or platform diffs |
| 0  | [**Master**](#0-master-fundamentals-of-data-engineering-code-review-prompt)   | Full 15-point review -> 5 finding buckets                          | Bigger or higher-risk data engineering changes         |
| 1  | [**Understand the change**](#1-understand-the-change-first)                   | Reconstructs lifecycle position and data flow before critique      | First -- don't review what you don't understand        |
| 2  | [**Lifecycle fit**](#2-review-data-engineering-lifecycle-fit)                 | Generation, storage, ingestion, transformation, serving            | Any data-affecting diff                                |
| 3  | [**Source systems**](#3-review-source-systems-and-generation)                 | Source contracts, ownership, extraction constraints                | New or changed upstream source                         |
| 4  | [**Storage**](#4-review-storage-layout-and-access)                            | File/table design, formats, partitioning, retention                | Storage layer changed                                  |
| 5  | [**Ingestion**](#5-review-ingestion-contracts-and-reliability)                | Batch/stream loading, schema drift, replay, dedupe                 | Connectors, syncs, events, CDC, APIs                   |
| 6  | [**Transformation**](#6-review-transformation-and-modeling)                   | Business logic, modeling, lineage, incremental builds              | SQL/dbt/Spark/ELT/ETL changed                          |
| 7  | [**Serving**](#7-review-serving-data-consumers)                               | Analytics, ML, APIs, reverse ETL, consumer SLAs                    | Outputs or consumer-facing datasets changed            |
| 8  | [**Data quality and management**](#8-review-data-quality-and-data-management) | Quality checks, metadata, ownership, catalog, lineage              | Dataset reliability or governance matters              |
| 9  | [**Security and privacy**](#9-review-security-privacy-and-governance)         | Least privilege, sensitive data, access, retention                 | PII, secrets, access, exports, multi-tenant data        |
| 10 | [**Orchestration**](#10-review-orchestration-and-dependencies)                | DAG shape, dependencies, backfills, retries, schedules             | Workflows or schedulers changed                        |
| 11 | [**DataOps**](#11-review-dataops-and-release-safety)                          | CI/CD, environments, deployment, rollback, monitoring              | Platform/process/test changes                          |
| 12 | [**Architecture**](#12-review-data-architecture-and-coupling)                 | Loose coupling, reversibility, scalability, failure planning       | New components or boundaries                           |
| 13 | [**Technology and cost**](#13-review-technology-choice-and-cost)              | Tool fit, maturity, build vs buy, FinOps                           | New vendor, service, framework, or expensive path       |
| 14 | [**Operations**](#14-review-operability-observability-and-scale)              | SLAs, alerts, incidents, load, capacity, on-call surface           | Production reliability or scale risk                   |
| 15 | [**Tests as lifecycle evidence**](#15-review-tests-as-lifecycle-evidence)     | Tests for contracts, quality, replay, serving behavior             | Reviewing test changes                                 |
| A  | [**AI-generated change**](#a-reviewing-an-ai-generated-change)                | Skeptical pass for tool-first and fake-production assumptions      | Diff came from an agent                                |
| B  | [**Single pipeline or dataset**](#b-review-a-single-pipeline-job-or-dataset)  | Zoomed review of one data product                                  | Investigating one job, model, table, or feed           |
| C  | [**New data tool or platform**](#c-review-a-new-data-tool-or-platform)        | Whether new infrastructure earns its lifecycle role                 | New warehouse, lake, orchestrator, catalog, tool        |
| D  | [**Migration or backfill**](#d-review-a-migration-or-backfill)                | Online rollout, historical repair, verification, rollback          | Schema/data migration or historical rebuild            |
| E  | [**Review comments**](#e-producing-useful-review-comments)                    | Concrete, scenario-based, severity-tagged output                   | Turning findings into PR comments                      |

Reference (not prompts): [Review workflow](#recommended-review-workflow) · [Manual-review questions](#questions-to-remember-during-manual-review) · [The four reviews](#the-overall-model)

---

## Compact daily code-review prompt

**What it does:** Runs the lifecycle review as a single 12-point pass and separates blocking problems from optional improvements.

```text
Review this diff using principles from Fundamentals of Data Engineering.

Focus on:

1. Behavioral correctness and violated data contracts
2. Data engineering lifecycle position: generation, storage, ingestion,
   transformation, serving
3. Upstream source assumptions and ownership
4. Storage layout, formats, retention, and access patterns
5. Ingestion reliability, schema drift, replay, and deduplication
6. Transformation correctness, lineage, and incremental behavior
7. Serving fit for analytics, ML, APIs, reverse ETL, or operational consumers
8. Data quality, metadata, ownership, and governance
9. Security, privacy, access control, and sensitive-data handling
10. Orchestration, dependencies, backfills, and operational recovery
11. Technology choice, cost, team maturity, and reversibility
12. Test quality and observability

For every finding, provide:

- Evidence
- Concrete consequence
- Severity
- A realistic source, pipeline, consumer, workload, or failure scenario
- Smallest recommended improvement

Separate blocking issues from optional design improvements.

Do not recommend a new data tool, platform, queue, warehouse, orchestrator,
catalog, or framework unless the workload and lifecycle need justify it.

Calibrate every claim: distinguish CONFIRMED DEFECT, PLAUSIBLE RISK,
VERIFICATION GAP, and OPTIONAL IMPROVEMENT. Provide the evidence and
conditions for each; severity must match demonstrated impact, not a
hypothetical worst case. State what was inspected or actually tested,
and what was not. Zero findings is a valid result.
```

---

## 0. Master Fundamentals of Data Engineering code-review prompt

**What it does:** The full 15-point pass producing five finding buckets. Each finding must be tied to a concrete lifecycle stage, consumer need, operational scenario, or undercurrent.

```text
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
```

---

## 1. Understand the change first

**What it does:** Forces the agent to reconstruct the actual data engineering behavior before criticizing it.

```text
Explain this change before reviewing it.

Identify:

- The user, analyst, ML, operational, or platform behavior being changed
- The data engineering lifecycle stages affected
- Source systems and upstream owners
- Data entities, datasets, tables, files, events, or features involved
- Storage locations and formats
- Ingestion mechanism
- Transformation logic
- Served outputs and consumers
- Schedules, DAGs, dependencies, and triggering behavior
- Quality checks, metadata, lineage, and ownership
- Security, privacy, and access-control assumptions
- Existing behavior being replaced
- Important data contracts and invariants
- Freshness, latency, retention, and cost expectations
- Assumptions made by the implementation

Separate what is directly confirmed by the diff from what you inferred.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 2. Review data engineering lifecycle fit

**What it does:** Checks whether the change makes sense in the end-to-end lifecycle rather than only inside one job or tool.

```text
Review this change through the data engineering lifecycle:

- Generation
- Storage
- Ingestion
- Transformation
- Serving

For each stage affected, identify:

- What changed
- Who owns it
- What contract exists
- What can fail
- What can be late, missing, duplicated, stale, or malformed
- What downstream stage depends on it
- What consumer-facing behavior depends on it

Look for:

- A stage optimized locally while breaking a later stage
- Transformations that compensate for unclear source contracts
- Storage choices that do not match ingestion or serving access patterns
- Serving outputs with unclear consumers or definitions
- Lifecycle stages hidden inside one script with no explicit boundary
- Missing feedback path from consumers back to producers
- Ambiguous ownership between source teams, platform teams, and data consumers

Explain whether the change improves the whole lifecycle or merely moves work,
risk, or ambiguity from one stage to another.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 3. Review source systems and generation

**What it does:** Reviews the upstream origin of data, source constraints, and producer contracts.

```text
Review every source system, event producer, API, database, file drop, or manual
process introduced or changed by this patch.

For each source, identify:

- Owner
- Business process represented
- Extraction mechanism
- Expected volume and cadence
- Schema and contract
- Identifier strategy
- Timestamp semantics
- Update and delete behavior
- Late-arriving or corrected data behavior
- Rate limits or operational constraints
- Security and access requirements
- Known data quality problems

Look for:

- Treating a source system as if the data team controls it when it does not
- Missing producer contract
- Unclear meaning of timestamps, IDs, statuses, or deletes
- Polling without source limits or change detection
- Manual extracts becoming hidden production dependencies
- API pagination or rate-limit assumptions
- Source schema drift with no detection
- No owner to contact when upstream data changes
- Security credentials broader than needed

For every concern, explain the downstream lifecycle effect.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 4. Review storage layout and access

**What it does:** Checks whether storage choices match data shape, lifecycle stage, cost, retention, and access patterns.

```text
Review the storage layer introduced or changed by this patch.

Identify:

- Data stored
- Logical model
- Physical location
- File, table, document, or event format
- Partitioning, clustering, indexing, or sorting
- Compression and serialization
- Retention and deletion policy
- Backup or recovery expectations
- Read and write access patterns
- Dataset size now and expected growth
- Cost drivers
- Ownership and access permissions

Look for:

- Storage optimized for ingestion but painful for serving
- Storage optimized for one query while harming common workloads
- Unbounded raw data retention without policy
- No raw/intermediate/curated separation where lifecycle stages need it
- Ambiguous table or bucket ownership
- File sizes that create too many small files or oversized partitions
- Partitions chosen from convenience rather than query patterns
- Formats that block schema evolution or efficient reads
- Data duplicated without a freshness, ownership, or cleanup strategy
- Sensitive data copied into less controlled stores

Explain whether the storage design makes the data durable, usable, governable,
and cost-aware for its lifecycle role.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 5. Review ingestion contracts and reliability

**What it does:** Reviews movement from source systems into the data platform, including drift, late data, replay, and duplicate handling.

```text
Review the ingestion path introduced or changed by this patch.

Identify:

- Source
- Ingestion mode: batch, streaming, CDC, file drop, API pull, push, manual load
- Trigger or schedule
- Expected volume, latency, and freshness
- Schema contract
- Deduplication key
- Checkpoint or offset
- Retry behavior
- Replay behavior
- Backfill behavior
- Handling of late, missing, corrected, or deleted data
- Quarantine or dead-letter path
- Monitoring and alerting

Look for:

- Assuming one delivery when duplicates are possible
- No stable checkpoint or high-water mark
- No way to replay from the source of truth
- Offset pagination over a changing source
- Late data silently dropped
- Deletes ignored
- Schema drift breaking jobs without diagnosis
- Retry loops that multiply source load
- Partial ingestion with no reconciliation
- Errors logged but not surfaced to owners
- Source credentials or secrets embedded in pipeline code

For each issue, describe the exact source or ingestion event sequence that causes
incorrect or incomplete downstream data.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 6. Review transformation and modeling

**What it does:** Checks whether transformations preserve meaning, quality, lineage, and incremental correctness.

```text
Review every transformation, model, query, feature build, enrichment, or business
rule changed by this patch.

Identify:

- Input datasets
- Output datasets
- Grain
- Keys
- Business definitions
- Filters
- Joins
- Aggregations
- Incremental logic
- Late-arriving data handling
- Null and invalid value handling
- Lineage
- Ownership
- Quality checks
- Downstream consumers

Look for:

- Grain changes hidden in a query
- Many-to-many joins that multiply rows
- Filters that redefine a business metric without review
- Business logic duplicated across models
- Incremental models that miss updates or deletes
- Late-arriving facts excluded permanently
- Time zones or timestamp windows handled inconsistently
- Nulls converted into meaningful values without justification
- Derived fields without lineage or definition
- Transformations coupled to one consumer's current dashboard layout
- No review path for business definition changes

For every issue, provide a concrete input dataset or event sequence and the
incorrect output it produces.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 7. Review serving data consumers

**What it does:** Checks whether outputs actually serve their intended consumers: analytics, ML, reverse ETL, APIs, operations, or external users.

```text
Review the data products, tables, marts, features, extracts, APIs, dashboards,
or reverse ETL outputs introduced or changed by this patch.

For each served output, identify:

- Consumer
- Use case
- Required freshness
- Required correctness
- Access pattern
- Availability expectation
- Definition owner
- Access permissions
- Retention expectation
- Change notification path
- Failure or delay behavior

Look for:

- Dataset built without a named consumer or use case
- Consumer-facing schema changed without compatibility handling
- Freshness promise not supported by the pipeline
- ML feature leakage or training/serving mismatch
- Dashboard metric definition changed silently
- Reverse ETL writing back to source systems without lineage
- Operational API backed by analytical data with unsuitable latency
- Extracts or shares that bypass governance
- No communication path for breaking changes

Explain whether the served data is fit for its consumer, not merely present in a
warehouse or lake.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 8. Review data quality and data management

**What it does:** Reviews quality checks, ownership, metadata, cataloging, lineage, retention, and governance.

```text
Review this change for data quality and data management.

Identify:

- Dataset owners
- Critical data elements
- Quality expectations
- Validation rules
- Metadata
- Lineage
- Catalog or documentation updates
- Retention and deletion rules
- Classification of sensitive data
- Stewardship or approval workflow
- Incident response path for bad data

Look for:

- Important data with no owner
- Quality checks that only prove the job ran
- Missing uniqueness, freshness, completeness, validity, or referential checks
- Silent quarantines that consumers never see
- Metadata updated separately from code
- Lineage broken by out-of-band scripts
- Dataset names that hide business meaning
- Retention policy unspecified
- Deletion requests incompatible with downstream copies
- Governance handled only after serving

For each concern, explain which consumer, process, or compliance obligation is
at risk.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 9. Review security, privacy, and governance

**What it does:** Applies least privilege and sensitive-data thinking across the whole lifecycle, not only at the endpoint.

```text
Review this data engineering change for security, privacy, and governance.

Identify:

- Sensitive fields
- Data classification
- Source permissions
- Pipeline credentials
- Storage permissions
- Transformation access
- Serving access
- Cross-environment movement
- Encryption expectations
- Retention and deletion expectations
- Audit and access logs
- External sharing or vendor access

Look for:

- Admin or broad read/write access where narrower access would work
- Secrets committed, logged, or passed through job parameters
- PII copied into raw, debug, test, or derived stores unnecessarily
- Data masking applied only in the serving layer
- Tenant or customer boundaries enforced by convention only
- Training, analytics, or QA environments receiving production-sensitive data
- Logs containing raw records or credentials
- External exports without approval, expiration, or recipient tracking
- Retention conflicts between raw, transformed, and served layers

Explain the specific exposure path and the smallest change that closes it.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 10. Review orchestration and dependencies

**What it does:** Reviews DAG shape, schedules, dependencies, retries, backfills, and operational recovery.

```text
Review the orchestration behavior introduced or changed by this patch.

Identify:

- DAGs, jobs, tasks, sensors, or triggers
- Upstream dependencies
- Downstream dependencies
- Schedule or event trigger
- Task ordering
- Retry policy
- Timeout policy
- Backfill behavior
- Concurrency limits
- Resource requirements
- Failure notification
- Manual intervention path

Look for:

- Time-based ordering used where data dependency is needed
- Hidden dependency on another job's side effect
- Retries that are unsafe or amplify upstream load
- No timeout on long-running tasks
- Backfills that overwhelm systems or overwrite good data
- No way to resume from a failed step
- Task success reported despite partial outputs
- Cycles or fan-out/fan-in complexity without observability
- Environment-specific schedules not represented in code
- Manual steps that are not documented or monitored

For every concern, describe the failed run, delayed source, or backfill scenario.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 11. Review DataOps and release safety

**What it does:** Checks whether the change can be developed, tested, deployed, observed, rolled back, and operated safely.

```text
Review this change for DataOps maturity.

Identify:

- Development workflow
- CI checks
- Test data strategy
- Environment separation
- Deployment process
- Configuration management
- Rollback or roll-forward path
- Monitoring and alerting
- Incident response
- Ownership and runbook updates

Look for:

- Production-only validation
- No isolated environment for pipeline changes
- Tests using unrealistic clean data
- Configuration copied manually between environments
- Migrations deployed separately from code without order control
- No canary, sample, or shadow validation for high-risk output changes
- Rollback impossible because data was destructively transformed
- Alerts tied to infrastructure health but not data freshness or quality
- Runbooks missing the commands or owners needed during an incident
- Changes that increase on-call burden without making it visible

Classify each gap as blocking, important, or optional based on dataset criticality.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 12. Review data architecture and coupling

**What it does:** Tests whether architectural choices are loosely coupled, scalable, failure-aware, reversible, secure, and proportionate.

```text
Review the data architecture affected by this change.

Identify:

- Components added or changed
- Boundaries
- Contracts
- Data ownership
- Coupling between source, storage, transformation, and serving
- Scalability assumptions
- Failure assumptions
- Reversibility of decisions
- Security posture
- Operational ownership

Look for:

- Tight coupling between producer schemas and consumer models
- One pipeline becoming the hidden integration point for many domains
- Direct warehouse dependencies where a stable contract is needed
- New architecture pattern copied from industry fashion rather than need
- Irreversible vendor or format choice without exit plan
- Single tenant assumptions in a future multi-tenant path
- Failure modes that cascade across lifecycle stages
- Security or governance bolted on after architecture decisions
- Components that no team clearly owns

Explain whether the architecture improves lifecycle clarity or creates a tool-
centered system that will be hard to operate and change.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 13. Review technology choice and cost

**What it does:** Checks whether new tools, services, and expensive patterns are justified by requirements, team maturity, reversibility, and cost.

```text
Review the technology choices in this change.

For each new or materially changed tool, service, framework, vendor, or platform
feature, identify:

- Problem it solves
- Lifecycle stage it supports
- Requirements that require it
- Alternatives considered
- Operational ownership
- Team skill requirement
- Integration complexity
- Failure modes
- Vendor lock-in or exit path
- Pricing model
- Cost driver
- Expected utilization
- Reversibility

Look for:

- Tool chosen before requirements are clear
- New infrastructure for a problem the existing platform can handle
- Streaming used where batch satisfies freshness needs
- Distributed processing used for small data
- Warehouse compute hidden behind frequent small jobs
- Premium vendor feature used without lifecycle benefit
- Cost estimates absent from high-volume paths
- Operational burden assigned to no one
- Technology that solves ingestion while complicating transformation or serving
- Claims of scalability without workload estimates

Classify the choice as:

- Necessary now
- Reasonable and reversible
- Premature but low-risk
- Operationally under-specified
- Cost risk
- Unnecessary complexity

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 14. Review operability, observability, and scale

**What it does:** Reviews whether the system can be monitored, debugged, recovered, scaled, and supported in production.

```text
Review this change for operability, observability, and scale.

Identify:

- Expected data volume
- Expected run frequency
- Expected latency or freshness
- Expected consumer concurrency
- Resource usage
- Scaling limits
- SLOs or SLAs
- Metrics
- Logs
- Traces or run metadata
- Alerts
- Dashboards
- Runbooks
- Ownership

Look for:

- No visibility into freshness, completeness, quality, or lag
- Metrics that show task success but not data correctness
- Logs that do not identify dataset, partition, source, or run ID
- Alerts with no owner or remediation path
- Work proportional to full history on every run
- Unbounded fan-out to source APIs or consumers
- No capacity limit, throttling, or overload policy
- Cost growth hidden behind data growth
- Backfills competing with production workloads
- No way to answer "what changed, when, and why?"

For every concern, give:

- Triggering workload or incident
- Expected symptom
- Consumer-visible consequence
- Metric or log that would reveal it
- Smallest mitigation

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 15. Review tests as lifecycle evidence

**What it does:** Determines whether tests prove lifecycle behavior rather than only exercising a happy-path function.

```text
Review the tests changed or added by this patch.

Determine whether they verify:

- Source contracts
- Schema drift behavior
- Ingestion retries and replay
- Duplicate, late, corrected, and deleted data
- Storage layout assumptions
- Transformation business rules
- Grain and join behavior
- Incremental processing
- Data quality checks
- Metadata and lineage expectations
- Security and access constraints
- Orchestration dependencies
- Backfill and resume behavior
- Serving schemas and consumer behavior
- Observability and alert behavior

Look for tests that:

- Use only clean, tiny, idealized data
- Mock away the source, warehouse, filesystem, or orchestrator behavior being
  relied on
- Verify SQL compiled but not output correctness
- Check row counts but not business meaning
- Ignore duplicate, late, or corrected records
- Do not test old and new schemas together
- Never rerun the same partition or job
- Depend on current time without control
- Pass despite stale or partial outputs
- Treat local execution as proof of production scheduling behavior

Separate:

- Missing unit coverage
- Missing data-contract coverage
- Missing integration coverage
- Missing backfill/replay coverage
- Missing security/governance coverage
- Optional load or cost testing

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## A. Reviewing an AI-generated change

**What it does:** Applies extra skepticism to common AI mistakes in data engineering code.

```text
Review this AI-generated change skeptically using Fundamentals of Data
Engineering principles.

Look specifically for:

- Tool-first architecture without a named lifecycle problem
- New pipeline code with no consumer or data product definition
- Source systems treated as stable, clean, and fully controlled
- Schema drift ignored
- Late, duplicate, corrected, or deleted records ignored
- Transformations that invent business definitions
- Tests that use perfect synthetic data only
- Missing freshness, quality, and lineage checks
- Admin credentials or broad permissions
- Secrets in code, logs, configs, or notebook output
- Costly full-refresh logic where incremental processing is needed
- Streaming, queues, warehouses, or orchestration added without workload need
- Backfill or replay paths that cannot run in production
- Monitoring that checks only process success
- Documentation that describes the tool but not ownership, contracts, or consumers

For each finding, require a concrete source, pipeline, consumer, failure, cost, or
governance scenario.

Prefer the simplest lifecycle design that satisfies real source constraints,
consumer needs, security requirements, and operational maturity.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## B. Review a single pipeline, job, or dataset

**What it does:** Zooms in on one data product and reconstructs its full lifecycle behavior.

```text
Review [pipeline, job, model, table, feature set, extract, or dataset] using
Fundamentals of Data Engineering principles.

Identify:

- Consumer and use case
- Source systems
- Input data
- Output data
- Lifecycle stages involved
- Storage location and format
- Grain and keys
- Ingestion mode
- Transformation logic
- Serving path
- Schedule or trigger
- Quality checks
- Security permissions
- Lineage and metadata
- Failure behavior
- Backfill and replay behavior
- Expected volume, latency, freshness, and cost

Then answer:

1. Is the dataset useful for a named consumer?
2. Are source contracts explicit enough?
3. Does ingestion handle drift, duplicates, lateness, and replay?
4. Does transformation preserve business meaning and grain?
5. Does serving match the consumer's access pattern and freshness need?
6. Are quality, lineage, ownership, and documentation sufficient?
7. Are permissions and retention appropriate?
8. Can the pipeline be debugged, backfilled, and operated?
9. What becomes expensive or fragile as data grows?
10. Which lifecycle assumptions are proven and which are only assumed?

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## C. Review a new data tool or platform

**What it does:** Tests whether adding data infrastructure solves a real lifecycle problem and whether its operational cost is understood.

```text
Review the new data warehouse, lake, lakehouse, orchestrator, catalog, quality
tool, ingestion framework, transformation framework, reverse ETL tool, feature
store, streaming system, or platform component introduced by this change.

Identify:

- Concrete lifecycle problem it solves
- Stages affected
- Consumers affected
- Data stored or moved
- Current limitation
- Expected workload
- Team that owns it
- Required skills
- Security and governance model
- Integration points
- Failure modes
- Rollout plan
- Migration plan
- Cost model
- Exit or rollback path

Then ask:

- Why cannot the existing platform handle this requirement?
- Which lifecycle stage improves?
- Which undercurrents become stronger or weaker?
- Does it reduce coupling or create a new central dependency?
- Is ownership clear?
- Can teams operate it during incidents?
- How are data quality, metadata, lineage, and access handled?
- How are old and new systems run together during rollout?
- What cost grows with data volume, job count, or users?
- What happens if the vendor, service, or component is unavailable?
- At what workload or organizational maturity is this component justified?

Classify it as:

- Necessary now
- Reasonable and reversible
- Premature but low-risk
- Operationally under-specified
- Security or governance risk
- Cost risk
- Unnecessary complexity

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## D. Review a migration or backfill

**What it does:** Reviews rollout, historical repair, mixed-version compatibility, resumability, verification, and rollback.

```text
Review this schema migration, data migration, platform migration, historical
backfill, or dataset rebuild.

Identify:

- Old representation
- New representation
- Source of truth
- Affected lifecycle stages
- Existing readers and writers
- Consumer compatibility requirements
- Deployment order
- Data volume
- Batch or partition strategy
- Runtime impact
- Resume checkpoint
- Idempotency
- Validation method
- Quality checks
- Security implications
- Rollback or roll-forward plan
- Cleanup step

Check whether the process supports:

- Old and new consumers running together
- Repeated execution
- Partial completion
- Process restart
- Concurrent source updates
- Late-arriving data
- Throttling
- Progress monitoring
- Error quarantine
- Reconciliation
- Post-migration validation
- Cost controls

Look for:

- Destructive changes before consumers are migrated
- Backfill and live ingestion racing
- One giant transaction or job
- Offset-based historical paging over changing data
- Rows skipped or processed twice
- No deterministic checkpoint
- No count, checksum, sample, or business-metric validation
- No comparison between old and new outputs
- Permissions becoming broader during migration and never tightened
- Cleanup before confidence is established
- Rollback that cannot restore transformed data or consumer contracts

For every risk, describe the exact deployment, interruption, or consumer-impact
scenario.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## E. Producing useful review comments

**What it does:** Converts findings into actionable comments grounded in lifecycle stages, undercurrents, and realistic scenarios.

```text
Turn the review findings into actionable pull-request comments.

For each comment, include:

- Severity: blocking, important, or optional
- File, dataset, job, DAG, model, query, schema, configuration, or tool
- Concrete lifecycle or undercurrent problem
- Why it matters
- Realistic source, pipeline, consumer, failure, security, cost, or scale scenario
- Smallest recommended improvement

Do not write vague comments such as:

- "This is not production ready."
- "Use a data quality framework."
- "Add orchestration."
- "This needs governance."
- "Use streaming."
- "Use a catalog."
- "This will not scale."
- "This needs better DataOps."

Instead explain:

- Which lifecycle stage is underspecified
- Which source assumption can break
- Which consumer contract changes
- Which data quality rule is missing
- Which access path exposes sensitive data
- Which orchestration failure leaves partial output
- Which cost grows with data volume or job count
- Which operational signal would reveal the problem
- How the proposed change improves the lifecycle
- What trade-off it introduces

Avoid speculative architecture advice not supported by expected data volume,
freshness, consumer value, governance requirements, or team maturity.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## Recommended review workflow

### Pass 1 -- Understand behavior and lifecycle position

Run:

```text
1. Understand the change first
2. Review data engineering lifecycle fit
```

Goal:

```text
Understand what changed, which lifecycle stages are affected, and who consumes
the result.
```

### Pass 2 -- Review lifecycle stages

Run the relevant prompts:

```text
3. Review source systems and generation
4. Review storage layout and access
5. Review ingestion contracts and reliability
6. Review transformation and modeling
7. Review serving data consumers
```

Goal:

```text
Understand whether data remains useful and trustworthy as it moves from source
to consumer.
```

### Pass 3 -- Review undercurrents

Run:

```text
8. Review data quality and data management
9. Review security, privacy, and governance
10. Review orchestration and dependencies
11. Review DataOps and release safety
```

Goal:

```text
Determine whether cross-cutting responsibilities are built into the lifecycle
instead of patched on afterward.
```

### Pass 4 -- Review architecture, cost, and production behavior

Run:

```text
12. Review data architecture and coupling
13. Review technology choice and cost
14. Review operability, observability, and scale
```

Goal:

```text
Judge whether the design is proportionate, reversible, operable, scalable, and
cost-aware.
```

### Pass 5 -- Review evidence

Run:

```text
15. Review tests as lifecycle evidence
```

Goal:

```text
Determine whether tests, checks, and observability prove the important data
contracts and failure behavior.
```

### Pass 6 -- Produce comments

Run:

```text
E. Producing useful review comments
```

Goal:

```text
Turn the highest-value findings into concrete, proportionate PR feedback.
```

---

## Questions to remember during manual review

```text
Who consumes this data?

What decision, product behavior, model, dashboard, or process depends on it?

Which lifecycle stages changed?

What source system generated the data, and who owns that source?

What source contract exists?

What can be late, duplicated, corrected, deleted, missing, or malformed?

Where is the data stored, in what format, and for how long?

Does the storage layout match ingestion and serving access patterns?

What business definition or grain does the transformation establish?

Can the transformation be replayed or backfilled?

What quality checks prove the output is fit for use?

What metadata, lineage, and ownership will help debug future problems?

Who can access the data at each lifecycle stage?

Does sensitive data move into a less controlled environment?

What dependencies, schedules, retries, and failure paths does orchestration encode?

Can this change be deployed, rolled back, monitored, and operated?

What does it cost as data volume, consumers, or jobs grow?

Why is this tool or platform component necessary now?

Which assumption is proven by code, tests, checks, or configuration?

Which assumption is only hoped for?
```

---

## The overall model

A complete Fundamentals of Data Engineering code review contains four different reviews:

```text
Behavior review
    Does the change do what the product, analyst, ML, or operational consumer expects?

Lifecycle review
    Does data move from generation to serving with explicit contracts and ownership?

Undercurrent review
    Are security, data management, DataOps, architecture, orchestration, and software
    engineering handled across the lifecycle?

Operational review
    Can the system be deployed, observed, recovered, scaled, governed, and paid for?
```

The book's strongest review value is the second, third, and fourth reviews. It should not replace the first.

---

## Lifecycle-evidence rule

Never accept:

```text
This is production ready because the pipeline runs successfully.
```

Require:

```text
The source contract is explicit.

The ingestion checkpoint supports retry and replay.

The transformation has tests for grain, joins, nulls, and business definitions.

The served dataset has a named consumer, freshness expectation, quality checks,
ownership, lineage, access controls, and alerts.

The backfill and rollback paths have been tested on realistic data.
```

Likewise:

```text
Pipeline success != data quality

Warehouse table != data product

Dashboard exists != consumer contract

Raw data != recoverability

Streaming != real-time business value

Orchestration != operational readiness

Catalog entry != ownership

Lineage graph != correctness

Admin access != enablement

Full refresh != simplicity at scale

Vendor platform != data architecture

Tool adoption != DataOps maturity
```

---

## Final code-review principle

The goal is not to ask:

```text
Does this use the modern data stack correctly?
```

The better sequence is:

```text
Who needs this data?
What lifecycle stage changed?
What source contract is being relied on?
How is the data stored, transformed, and served?
What can go wrong during drift, lateness, replay, backfill, or failure?
Which undercurrents are affected?
How is quality, lineage, security, ownership, and cost handled?
Can the team operate this in production?
Which assumptions are proven?
Which technology choices are justified by actual requirements?
```

Technology names are secondary. The real review is about lifecycle fitness, consumer value, data trust, operational maturity, security, and cost-aware architecture.
