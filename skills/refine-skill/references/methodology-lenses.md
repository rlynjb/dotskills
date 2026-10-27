# Refine Skill — conference methodology lenses

## Stage 6: scan every lens; route only when justified

Every refinement cycle gives the learner a quick explanation of all
five lenses; record for each **relevant**, **not evidenced** or
**currently not applicable**, anchored to an actual case/trace.
For problems or deeper teaching requests, recommend a specialist,
explain alternatives and wait at the human gate before invoking it.
A failed assertion is **not automatically** a skill prompt defect.

| Lens / specialist skill | Inspect for | Why it matters |
| --- | --- | --- |
| `context-engineering` | Missing, stale, conflicting, excessive or injected information; whether the agent stopped retrieving too soon | The model can only reason well from trustworthy, sufficient context |
| `correctness-and-verification` | Broken invariants, unsupported claims, lack of deterministic checks | A plausible answer is not a proven result |
| `agent-observability-and-feedback` | Tool traces, attempted effects, user feedback, missing timing/cost signals | Output alone can hide an incorrect or unsafe trajectory |
| `agent-trust-and-governance` | Input authority, provenance, permissions, approvals, unsafe side effects | Retrieved instructions are data, not permission |
| `skill-lifecycle-and-release` | Skill revisions, regressions, cross-harness behavior, portability, release decisions | Local gains must survive other cases and environments |

If the evidence fits none, record "no specialist needed" rather than
running all specialists. **Full-lens learning mode** is a supported
human-selected educational option, but its conclusions still need
evidence; do not invent a failure just to demonstrate a lens.

## Conference provenance

The following are *source-session mappings recorded in DotSkills*,
not independent verification of the original talks. Before attributing
a specific principle to a particular talk, read the available source
notes/reference. A talk title alone is not evidence for a proposed
case, diagnosis or change: label that synthesis "Model recommendation".

| Skill | Role | Source session / resource |
| --- | --- | --- |
| `refine-skill` | Optional refinement entry point. Human-gated learning and evidence-based evaluations guide diagnosis, approved improvements, and specialist routing. | Agntcon02 — **Stop Vibe Testing**; Agntcon04 — **Beyond Pass/Fail**; Agntcon05 — **Building Production-Ready Agents with a Regression Test Suite**; Agntcon24 — **Building an Agentic Eval Pipeline with EvalBench**. |
| `context-engineering` | Context selection, progressive retrieval, provenance, freshness, conflict handling, and stopping conditions. | Agntcon27 — **How Contexts Fail (and How to Fix Them)**; Agntcon06 — **Trustworthy Context Is Untrusted by Default**. |
| `correctness-and-verification` | Requirements, invariants, evidence, deterministic checks, and uncertainty. | Agntcon07 — **Cut the Noise: Building a Code Reviewer You Can Trust**; correctness / universal-properties material; Agntcon25 — **Shipping Agent Skills Safely** for verification and guardrail practices. |
| `skill-lifecycle-and-release` | Versioning, paired evals, regression coverage, portability checks, and release decisions. | Agntcon25 — **Shipping Agent Skills Safely**; Agntcon28 — **Declarative Agent Architecture**. |
| `agent-observability-and-feedback` | Agent-journey traces, outcome/process signals, diagnostics, and production-feedback loops. | Agntcon03 — **What Your MCP Server Does When Nobody's Looking**; Agntcon04 — **Beyond Pass/Fail** / full-agent-experience measurement; Agntcon10 — **What Production Knows**. |
| `agent-trust-and-governance` | Authority, provenance, permissions, approvals, guardrails, and risk controls. | **Governing Agents When You Can't Trust the Model**; Agntcon26 — **Durability, Guardrails, and Attestation**; Agntcon06 — **Trustworthy Context Is Untrusted by Default**. |

## Failure handoff

When invoking a specialist methodology, pass:

```text
Target skill and version:
Target maturity / package state:
Capability under test:
Case and expected behavior:
Observed behavior:
Relevant output/trace evidence:
Known setup limitations:
Current failure hypothesis:
Methodology coverage scan:
Human constraints or feedback relevant to diagnosis:
Question for the specialist methodology:
```

The specialist diagnoses the failure; it does not automatically edit the target skill.

## Session-derived principles

This operational method synthesizes the AGNTCon/MCPCon sessions on real agent
evaluations, agent regression testing, EvalBench, shipping agent skills safely, context
engineering, verification, observability, and trust: evaluate realistic user journeys,
start mutating evals from known state, keep comparisons reproducible, treat skills like
versioned software, preserve human judgment at consequential methodology boundaries,
learn from concrete failures, normalize rough capabilities before measuring them when
needed, and re-run coverage when the skill, model, harness, tools, or package structure
change.
