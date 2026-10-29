# DotSkills skill families

DotSkills keeps every installable skill as a first-level package under `skills/<name>/`.
The conceptual hierarchy is expressed through `catalog.json` categories rather than
nested skill directories, so each skill remains independently discoverable and portable.

## Methodology skills

Use these to develop, diagnose, and improve other skills.

| Skill | Role | Source session / resource |
| --- | --- | --- |
| `refine-skill` | Optional refinement entry point. Human-gated learning and evidence-based evaluations guide diagnosis, approved improvements, and specialist routing. | Agntcon02 — **Stop Vibe Testing**; Agntcon04 — **Beyond Pass/Fail**; Agntcon05 — **Building Production-Ready Agents with a Regression Test Suite**; Agntcon24 — **Building an Agentic Eval Pipeline with EvalBench**. |
| `audit-skill` | Read-only **Explore / Audit / Compare** modes: learn one skill with a question menu and chosen deep dives; assess gaps or compare workflows without edits. | DotSkills-authored, adapted from the Sprint Assessment / Refine Requirements audit prompt; not attributed to a conference session. |
| `context-engineering` | Context selection, progressive retrieval, provenance, freshness, conflict handling, and stopping conditions. | Agntcon27 — **How Contexts Fail (and How to Fix Them)**; Agntcon06 — **Trustworthy Context Is Untrusted by Default**. |
| `correctness-and-verification` | Requirements, invariants, evidence, deterministic checks, and uncertainty. | Agntcon07 — **Cut the Noise: Building a Code Reviewer You Can Trust**; correctness / universal-properties material; Agntcon25 — **Shipping Agent Skills Safely** for verification and guardrail practices. |
| `skill-lifecycle-and-release` | Versioning, paired evals, regression coverage, portability checks, and release decisions. | Agntcon25 — **Shipping Agent Skills Safely**; Agntcon28 — **Declarative Agent Architecture**. |
| `agent-observability-and-feedback` | Agent-journey traces, outcome/process signals, diagnostics, and production-feedback loops. | Agntcon03 — **What Your MCP Server Does When Nobody's Looking**; Agntcon04 — **Beyond Pass/Fail** / full-agent-experience measurement; Agntcon10 — **What Production Knows**. |
| `agent-trust-and-governance` | Authority, provenance, permissions, approvals, guardrails, and risk controls. | **Governing Agents When You Can't Trust the Model**; Agntcon26 — **Durability, Guardrails, and Attestation**; Agntcon06 — **Trustworthy Context Is Untrusted by Default**. |

The source column records the primary conference sessions/resources that informed each
methodology skill. Most methodology skills are syntheses rather than one-to-one
transcriptions of a single session.

For an unfamiliar single skill, start with `audit-skill` in **Explore Mode** and choose a learning question. Use **Audit Mode** for evidence-backed gaps and **Compare Mode** for multiple skills. Use `refine-skill` when ready for authorized evaluation and improvement. Invoke a specialist methodology only when evidence or an explicit learning request justifies it; a failed eval does not automatically mean the target skill should be edited.

### Default interaction

`refine-skill` is human-gated by default. It should make a
recommendation, explain why, show materially different alternatives when useful, and
give the human an open path to contribute their own solution, constraints, concerns, or
opinion.

Human feedback is not implicit approval. If the human revises a proposal or contributes
an alternative, the methodology should respond to that input and present the gate again
before taking the gated action.

Guided learning is also the default. At meaningful gates, the methodology briefly
explains the concept currently in use, how it applies to the concrete case, what evidence
to notice, and why the recommendation follows. Learning content stays outside the
evaluated target skill's task context.

Typical harness invocation:

```text
Use refine-skill to improve <target-skill>.

Work in the default human-gated, guided-learning mode.
Walk me through the methodology one gate at a time.
Do not invoke a specialist, edit the target skill, run a gated comparison,
or accept regression coverage without my explicit approval.
At each gate, make a recommendation, show useful alternatives,
and let me contribute my own solution or feedback.
```

This entry point refines existing skills and can bootstrap a raw prompt or draft into
an evaluable package when needed. Other DotSkills skills do not inherit its operating
modes unless explicitly invoked. For a new skill, define the intended capability and eval behavior before drafting
the implementation.

## Task skills

Task skills perform the user's actual work, for example code review, investigation,
requirements refinement, learning, and decision support. They are targets that the
methodology skills can evaluate and improve; they are not children of the methodology
packages in the filesystem.
