# Profile Agent Workflow

**A read-only skill for measuring whether agent workflows perform necessary work efficiently.**

The focus is not to make an agent use fewer tokens at any cost. It is to understand **what was dispatched**, **why**, **what it cost**, **what evidence is missing**, and **what can safely be tested next**.

## Where it fits

```text
Approved workflow architecture and routing contracts
                         │
                         ▼
                Actual execution trace
                         │
                         ▼
               Profile Agent Workflow
                  │           │
                  ▼           ▼
          Dispatch checks   Resource accounting
                  └─────┬─────┘
                        ▼
             Evidence-backed candidate
                        │
                        ▼
       Evaluate Skill (approved paired evals)
                        │
                        ▼
       Team decides whether to change routing
```

This is **not a router, a live observability backend, a model provider, or an evaluation runner**. It does not mutate orchestration or run target agents. [Evaluate Skill](../evaluate-skill/README.md) is responsible for execution and grading. The existing [Agent Observability and Feedback](../agent-observability-and-feedback/SKILL.md) covers broader diagnostics; this skill specializes in **dispatch correctness and resource efficiency**.

## Before you start

Bring what you have:

1. A workflow description and the relevant approved per-skill routing rules (required, forbidden, or optional for each case).
2. Actual trace events, including **SKIP decisions** as well as observed starts, tool calls, and provider-reported token/cost usage.
3. Any available case outcome/quality evidence (for example, a separate Evaluate Skill report).
4. Optional team-approved budgets and a comparable baseline.

If you only have the contracts and no trace, ask for a **telemetry readiness review**; the skill should tell you what to record, not invent results. If you only have a trace, it can calculate observed usage but cannot label calls unnecessary without approved rules.

## First run — illustrative offline sample

The optional analyzer is standard-library Python; it reads supplied files and prints JSON to stdout. It makes **no LLM calls**, **no network calls**, **no agent dispatches**, and **no file writes**.

From the repository root:

```bash
python3 skills/profile-agent-workflow/scripts/profile_trace.py \
  --trace skills/profile-agent-workflow/examples/trace.json \
  --policy skills/profile-agent-workflow/examples/routing-policy.json
```

The deliberately fictional sample has two units: T-014 (refinement should be skipped) and T-015 (refinement is required). The analyzer should find the rule-compliant dispatches, separate execution from grader usage, and mark two repeated `jira.read` calls as **REVIEW_ONLY**, not confirmed waste. All the budgets are arbitrary teaching values, **not recommended production thresholds**.

### What the analyzer returns

- `dispatch_checks`: per-unit routing rule, decision events, observed starts, and PASS / FAIL / UNKNOWN / NOT APPLICABLE.
- `uncontracted_invocations`: observed starts not covered by an approved routing rule; these are **UNKNOWN**, not automatically unnecessary.
- `repeat_tool_call_candidates`: repeated hashed tool requests that warrant investigation, not automatic cost defects.
- `usage`: observed execution and grader tokens/costs separately. Cached input tokens are already included within input tokens.
- `budget_checks`: measured use against **supplied** limits, with UNKNOWN when below-limit evidence is incomplete.
- `coverage_warning` and `unknowns`: provenance and measurement limits that should not be hidden.

**Exit status:** 0 means the analyzer produced a valid report, including reports containing FAIL. Exit status 2 means input validation failed; an input error is not a clean performance report.

## Suggested invocation

```text
Use profile-agent-workflow to inspect this workflow's approved routing
contracts and these redacted traces. Identify only evidence-backed dispatch
violations, count tool/model/sub-agent use, separate grader and execution
cost, and identify optimization candidates. Mark missing data Unknown.
Do not run the workflow or change any files. Suggest one evaluation
case I can run with Evaluate Skill to verify the most promising change.
```

## Integrating tools later

The skill deliberately has **no built-in data connector**. Codex events, Promptfoo results, OpenTelemetry spans, or an approved Bifrost gateway can supply input when their actual fields and coverage semantics have been verified and normalized. Their configurations and APIs change; do not assume they emit the sample JSON directly.

A trusted instrumentation layer—not the reporting skill—should attribute a dispatch to its ticket/workflow ID and record a reason for dispatch or skip. The analyzer cannot distinguish a missing event from a skipped action without reliable coverage. Do not send restricted workplace traces or secrets into unapproved services.

## Evaluation and limitations

The local [trace contract](references/trace-contract.md) describes the input semantics. The [assessment rubric](references/assessment-rubric.md) defines PASS / FAIL / UNKNOWN and optimization guardrails. Proposed behavioral cases live in `evals/evals.json`; **their existence does not mean live agent evaluations were run**.

For deterministic analyzer regression checks, run:

```bash
python3 -m unittest discover -s skills/profile-agent-workflow/tests -v
```

The offline analyzer only validates and counts records in a normalized report. It **does not verify trace authenticity, enforce cost limits, evaluate answer quality, certify safety, discover policies automatically, or prove that any real company workflow has been optimized**. Those require independently trusted instrumentation, approved eval execution and human review.
