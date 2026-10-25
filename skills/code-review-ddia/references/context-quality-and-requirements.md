# Code Review DDIA — Context Quality and Requirements

This guide defines the evidence needed to perform the standalone Master DDIA
code review without depending on the other prompts in the original prompt
library.

## 1. Establish the task

- Identify the review target, requested outcome, scope, and exclusions.
- Record the relevant branch, commit, pull request, revision, environment, or
  working state when available.
- Identify intended behavior, requirements, contracts, and acceptance criteria
  that materially affect correctness.
- Minimum starting context is an identifiable change or implementation path that
  can be inspected. If the target itself cannot be established, ask a focused
  question before making findings.

## 2. Gather relevant evidence

Start with the change, then expand only when needed to verify a concrete review
question. Relevant evidence can include:

- The diff or changed implementation.
- Callers, callees, and existing guards around the affected path.
- Data entities, schemas, migrations, queries, indexes, and storage configuration.
- Transaction boundaries and concurrency controls.
- Events, queues, caches, projections, retry behavior, and idempotency mechanisms.
- API, event, and persistence contracts.
- Tests that exercise the changed guarantees.
- Deployment, replication, partitioning, recovery, monitoring, or workload
  evidence when a finding depends on those conditions.
- Query plans, timings, benchmarks, or production metrics when available.

Do not retrieve unrelated repository material merely to make the review broader.

## 3. Load guidance progressively

- Read [Master DDIA code-review rubric](master-ddia-code-review.md) for every use
  of this skill.
- Treat all 15 dimensions as review questions. Mark a dimension not applicable or
  unsupported by available evidence rather than inventing a concern.
- The focused prompts from the original DDIA prompt library are not prerequisites
  and do not need to be loaded for this skill to function.

## 4. Check evidence and claims

Before declaring a finding:

- Cite actual code, configuration, schema, tests, contracts, or observed results.
- Check relevant surrounding behavior for guards or invariants that may already
  address the concern.
- Use these claim classes:
  - Confirmed defect: a supported requirement is contradicted or a failure can be
    demonstrated with the relevant conditions established.
  - Plausible risk: code supports a realistic failure scenario, but likelihood,
    reachability, or production impact still needs verification.
  - Verification gap: evidence needed for a conclusion is unavailable or a check
    was not performed. This is not automatically a defect.
  - Optional improvement: a justified design or performance alternative with a
    stated trade-off.
- Calibrate severity separately:
  - Blocking only for an evidenced release-stopping correctness, security,
    data-loss, or agreed-contract issue.
  - Important for consequential supported concerns.
  - Optional for nonurgent improvements.
- Distinguish tests and benchmarks actually executed from tests merely read or
  recommended.

## 5. Handle missing, stale, or conflicting context

- Missing intended behavior limits claims about product correctness; use explicit
  contracts, tests, or existing behavior when they are authoritative.
- Missing production load or metrics limits scale and performance conclusions;
  describe the triggering workload instead of asserting measured slowness.
- Missing infrastructure details limits claims about durability, consistency,
  replication, failover, and partitioning.
- Missing tests can be a verification gap; it is not proof that the implementation
  is wrong.
- Recheck stale summaries against current source when they affect a finding.
- Compare conflicting sources by authority, scope, and revision, and report
  unresolved conflicts rather than choosing silently.
- Continue supported parts of the review even when one dimension cannot be
  verified.

## 6. Stop when sufficiently grounded

The review is sufficiently grounded when:

- The target and review boundary are explicit.
- Each relevant Master DDIA dimension has been considered or marked not applicable.
- Every actionable finding has inspected evidence, conditions, consequence,
  calibrated claim type, and severity.
- Shared root causes are deduplicated.
- Checks actually run are distinguished from checks only suggested.
- Material unknowns and verification gaps are explicit.
- The review does not claim safety for uninspected code or environments.
