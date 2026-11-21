# Profiling rubric — evidence over guessed efficiency

## Dispatch classification

Evaluate each approved per-unit/skill rule independently.

- **PASS:** REQUIRED has at least one observed start; FORBIDDEN has no observed start *and* complete dispatch coverage, with no recorded contradictory dispatch decision.
- **FAIL:** FORBIDDEN has an observed start or a recorded DISPATCH decision; REQUIRED has a recorded SKIP with no start or has no start with complete dispatch coverage.
- **UNKNOWN:** no approved rule, incomplete coverage prevents testing absence, or contradictory/malformed evidence prevents reliable correlation.
- **NOT APPLICABLE:** OPTIONAL rule, which does not impose a binary requirement.

An agent that started despite a SKIP record merits an **inconsistent trace / decision** finding; investigate rather than issuing a misleading PASS. An observed forbidden start remains FAIL. If the trace producer cannot distinguish attempted, blocked and successful dispatch, explicitly state that limitation.

## Efficiency findings and resource math

1. **Measured:** count events and sum reported per-model usage, keeping input, output and cached input distinct. Cached input is a subset of input.
2. **Potential duplication:** count repeated normalized tool fingerprints within the same unit; classify as **REVIEW**, not waste. Freshness requirements, retries and different returned data can justify repeats.
3. **Missing evidence:** report unavailable usage/coverage as **UNKNOWN**. Below-budget on a partial trace cannot PASS. A measured partial total already above a limit may FAIL.
4. **Optimization hypothesis:** recommend only one bounded change whose effect can be tested: conditional dispatch, deterministic precheck, progressive disclosure, relevant-only retrieval, structured small tool output, response/prompt caching, appropriate model routing, or bounded retries.
5. **Verification:** pair baseline and candidate runs on comparable fixtures, model/harness/tool configuration and approved rubrics. Compare cost **per successful output** and regressions in quality, safety and ticket isolation. Report not comparable when outcomes or usage are unknown.

Never prescribe a smaller model as a proven win without measuring retries and rework. Never let a token budget override a required evidence/safety step. A runtime budget that is only *configured*, not actually enforced, is an enforcement gap rather than an observed protection.

## Findings priority

- **High:** an observed forbidden dispatch or budget overrun with complete attributable evidence; material security/quality risk.
- **Medium:** repeated costly calls backed by trace IDs with a plausible bounded alternative but unproven necessity.
- **Low:** small or uncertain cost opportunity, incomplete attribution, or instrumentation gap.

Evidence labels: **OBSERVED**, **DOCUMENTED RULE**, **INFERRED**, **NOT VERIFIED**. Cite exact rule/event IDs or original trace/source locations. Do not manufacture percentages, savings, pricing, or number of calls.
