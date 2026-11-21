# Normalized trace contract (v1)

This is a **portable, optional interchange format** for the offline analyzer, not a claim that Codex, Promptfoo, Bifrost, OpenTelemetry, or any other provider emits these exact fields. Normalize from the **actual approved** provider records; preserve original identifiers in a protected system for cross-checking. No raw prompts, secret values, personal data or full tool arguments are needed.

## Required inputs

Two JSON documents. A trace describes one captured run. A policy describes **reviewed rules** applicable to that run. The analyzer does not discover or approve rules.

```json
{
  "schema_version": 1,
  "run_id": "example-run",
  "workflow_revision": "proposed-v1",
  "coverage": {
    "dispatch_complete": true,
    "tool_complete": true,
    "model_usage_complete": true
  },
  "events": [
    {
      "id": "e1",
      "type": "dispatch_decision",
      "unit_id": "T-014",
      "skill": "refine-requirements",
      "decision": "SKIP",
      "reason_code": "REQUIREMENTS_COMPLETE"
    },
    {
      "id": "e2",
      "type": "agent_start",
      "unit_id": "T-014",
      "skill": "sprint-assessment"
    },
    {
      "id": "e3",
      "type": "tool_call",
      "unit_id": "T-014",
      "tool": "jira.read",
      "fingerprint": "hash-of-normalized-safe-request"
    },
    {
      "id": "e4",
      "type": "model_call",
      "unit_id": "T-014",
      "purpose": "execution",
      "usage": {
        "input_tokens": 1000,
        "cached_input_tokens": 200,
        "output_tokens": 250,
        "cost_usd": 0.02
      }
    }
  ]
}
```

```json
{
  "schema_version": 1,
  "policy_id": "illustrative-routing-rules-v1",
  "workflow_revision": "proposed-v1",
  "rules": [
    {
      "id": "R-READY",
      "unit_id": "T-014",
      "skill": "refine-requirements",
      "expected": "FORBIDDEN",
      "reason": "Approved routing contract says refinement is not needed here"
    }
  ],
  "budgets": {
    "max_execution_cost_usd": 0.05,
    "max_execution_input_tokens": 5000,
    "max_agent_starts": 2,
    "max_tool_calls": 5
  }
}
```

`FORBIDDEN` means "do not dispatch" under the approved condition, not a permanent prohibition on using the skill. `REQUIRED` means the skill must start under that condition. `OPTIONAL` has no binary pass requirement. These are **per-unit rules**; a policy should contain at most one rule for the same unit and skill. Do not interpret the illustrative rule as a real workplace contract.

## Event types

- `dispatch_decision`: `unit_id`, `skill`, `decision` = `DISPATCH` or `SKIP`, and optional `reason_code`. A decision is *not* proof of an actual start.
- `agent_start`: `unit_id`, `skill`. Record every attempt to start, including retries; the trace producer should explain blocked attempts separately if tracked.
- `tool_call`: `unit_id`, `tool`, optional `fingerprint` (stable hash only for **semantically equivalent** safe requests). Two calls with equal fingerprints are **repeat candidates** and may be necessary. Repeated `agent_start` events for the same unit and skill are likewise review candidates, not proof of waste.
- `model_call`: `unit_id`, `purpose` = `execution` or `grader`, optional `usage` numbers. Input, cached-input and output token counts must be nonnegative integers; cost must be a nonnegative number. `cached_input_tokens` must not exceed `input_tokens` when both are known.

Additional fields may be retained by the producer, but the offline analyzer ignores them. Every event must have a unique string `id`. Every event needs a string `unit_id`. The analyzer preserves referenced event IDs in findings; it does not read request bodies.

## Coverage and evidence strength

Coverage flags must be **explicit**, not inferred from an empty event list:

- `dispatch_complete`: all relevant decisions and starts for this scoped run are represented.
- `tool_complete`: all relevant tool invocations are represented.
- `model_usage_complete`: all relevant model invocations and their reported usage are represented.

False/missing coverage means an absence is **UNKNOWN**, and below-budget metrics cannot be certified. Even a `true` flag is only a **claim from the supplied trace**. It is not cryptographic attestation, independent host observation, complete billing, or proof of security isolation. The profiler must say which source reported completeness.

For reliable cross-system comparisons, also retain (outside the normalized minimal format) provider/model/adapter versions, routing-policy approval identifier, effective permissions, sampling policy, source trace digest, ticket snapshot and grader configuration. A comparison is invalid if changed requirements, coverage, model prices, or harness behavior make the runs noncomparable.

## Budgets and accounting

All budgets are optional, nonnegative and user/team-supplied. The analyzer recognizes:

- `max_execution_cost_usd` (excludes grader)
- `max_total_cost_usd` (execution plus grader)
- `max_execution_input_tokens` (input includes cached tokens)
- `max_agent_starts`
- `max_model_calls`
- `max_tool_calls`

Measured usage is **observed and provider-reported**. Provider-billed costs may differ from estimates. Do not add cached-input tokens to input tokens again; do not treat a cache hit as a free model invocation. Partial usage can demonstrate an **already observed overrun** but cannot prove that a run stayed under budget.

## Known exclusions

- No automatic OpenTelemetry / Promptfoo / Codex / Bifrost adapter; mapping must be verified for each source.
- No built-in semantic classifier for whether routing rules themselves are correct.
- No independent attestation of tool side effects or emitted trace completeness.
- No automatic judgment that repeated tool calls, context loads, or sub-agents were wasteful.
- No evaluation of final output correctness; consume an approved eval result from Evaluate Skill when available.

These boundaries prevent a telemetry report from being mistaken for a safety or quality evaluation.
