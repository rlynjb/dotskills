# Buffr module map (reference snapshot)

This skill does **not** contain Buffr's workflow engine. Buffr's live implementation, contracts, and work-engine state live in [rlynjb/buffr](https://github.com/rlynjb/buffr), especially `src/workflow/`, `src/agents/`, and `src/contracts/modules.ts`.

| ID | Role | Runtime prompt snapshot | Versioned module reference |
| --- | --- | --- | --- |
| M0 | Shared policy, not a workflow stage | [policy](runtime/m0-policy.md) | [core v3](versioned/etsy-core-agent-prompt-v3.md) |
| M1 | Product context and observation | [context](runtime/m1-context.md) | [context v2](versioned/product-context-observation-module-v2.md) |
| M2 | Metrics, qualification, and post-experiment measures | [metrics](runtime/m2-metrics.md) | [metrics v3](versioned/metrics-qualification-module-v3.md) |
| M3 | Conditional bounded read-only domain research | [research](runtime/m3-research.md) | [research v2](versioned/domain-research-module-v2.md) |
| M4 | Classification and diagnosis | [diagnosis](runtime/m4-diagnosis.md) | [diagnosis v3](versioned/classification-diagnosis-module-v3.md) |
| M5 | Hypothesis and conceptual experiment design | [hypothesis](runtime/m5-hypothesis.md) | [hypothesis v3](versioned/hypothesis-experiment-design-module-v3.md) |
| M6 | Test definition and measurement plan | [test definition](runtime/m6-test-definition.md) | [test v3](versioned/test-definition-module-v3.md) |
| M7 | Outcome evaluation and learning | [evaluation](runtime/m7-evaluation.md) | [evaluation v3](versioned/evaluation-learning-module-v3.md) |

The [versioned module contract manifest](versioned/etsy-prompt-module-contract-revision-manifest.md) and [revision pass summary](versioned/etsy-module-revision-pass-summary.md) give design history, not executable contracts.

## Critical boundaries

- M0 is a prepended shared policy, **not** an independent engine stage.
- M3 is a conditional side route; a requester can resume once research is done.
- M2 owns metric qualification; M6 consumes its baseline, and M7 consumes post-experiment qualified outcomes.
- The deterministic engine owns routing, constraints, wait/resume, trace, validation, and persistence.
- Historical/versioned prompts and runtime snapshots can differ. Recheck the running Buffr revision before reporting current behavior.
- A prompt is not an authorized tool call. Without real Buffr integration, no workflow has run.
