---
name: agent-observability-and-feedback
description: "Diagnose agent behavior using end-to-end journey evidence: inputs, context loading, tool calls, state changes, outputs, latency, cost, errors, and production feedback. Use when a failure cannot be explained from the final answer alone, when building eval telemetry, or when turning production incidents into regression cases."
---

# Agent Observability and Feedback

## Objective

Make agent behavior inspectable enough to distinguish output-quality failures from
context, tool, runtime, state, and infrastructure failures, then feed real failures
back into eval coverage.

## Required context

Provide:
- User journey or task.
- Model, harness, skill version, tools, permissions, and relevant budgets.
- Original output.
- Available trace: reads, searches, tool calls, state mutations, errors, timings,
  token/resource use, approvals, and retries.
- Production report or incident evidence when applicable.

## Procedure

1. Define the user journey and success criteria before choosing metrics.
2. Capture run identity and configuration so results can be compared.
3. Reconstruct the trajectory from available trace evidence.
4. Separate outcome quality, output quality, process quality, execution reliability,
   and latency/cost/resource behavior.
5. Locate the earliest evidence-backed divergence from expected behavior.
6. Identify missing telemetry that prevents diagnosis and mark those checks Unknown.
7. Correlate final claims with the reads, tools, and state changes that could support them.
8. Convert reproducible production failures into neutral eval cases with verified expectations.
9. Track whether fixes improve the complete journey rather than only one call.
10. Preserve infrastructure and grader failures as first-class observations.

## Output

Return:
- Journey and configuration.
- Outcome/process/reliability findings.
- Earliest supported failure point.
- Missing observability.
- Recommended instrumentation or diagnostic change.
- Candidate regression case from the failure.

## Decision rules

- Do not infer unseen tool use from a plausible final answer.
- Do not claim a file was inspected without trace evidence when that process claim matters.
- Keep latency/cost failures distinct from correctness failures.
- The first observable divergence is usually more actionable than the final symptom.
- Collect only telemetry needed and permitted for diagnosis.

## Session-derived principles

This skill synthesizes AGNTCon/MCPCon sessions on MCP-server observability, measuring
the full agent experience, and production feedback: observe the full journey rather
than only the answer, preserve the configuration that produced a run, separate
trajectory from outcome, and convert verified production failures into regression
cases rather than relying on anecdotes.
