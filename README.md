# DotSkills

**DotSkills** is a version-controlled library of reusable agent skills for compatible harnesses. Each `skills/<name>/` package contains an Agent Skills-compatible `SKILL.md` and optional references. This repository owns skill packaging, discovery metadata, and source provenance; Codex, Claude Code, ChatGPT Work, and other compatible hosts provide execution. [Buffr](https://github.com/rlynjb/buffr) remains the authority for its own decision-support runtime.

## Table of contents

- [Why DotSkills is different](#why-dotskills-is-different)
  - [How it relates to other skill-creation and evaluation tools](#how-it-relates-to-other-skill-creation-and-evaluation-tools)
- [Skill catalog](#skill-catalog)
- [Quick start](#quick-start)
- [Refine Skill](#refine-skill)
  - [Why a passing eval is not enough](#why-a-passing-eval-is-not-enough)

## Why DotSkills is different

DotSkills is **not another skill creator or evaluation engine**. It keeps the library portable and source-attributed, while its optional [`refine-skill`](skills/refine-skill/SKILL.md) methodology guides improvements to individual skills. The workflow's human gates and learning modes are specific to that skill, not requirements imposed on every DotSkills package.

| Scope | Distinctive approach |
| --- | --- |
| **DotSkills library** | Versioned [skill packages](skills/README.md), [discovery metadata](catalog.json), [source-locked references](docs/sources.md), and [harness adapters](adapters/README.md) keep instructions and their origins reviewable and reusable. Portability must still be tested in each target environment. |
| **Conference-informed methodology** | `refine-skill` and its [specialist methodologies](skills/README.md) draw on AGNTCon/MCPCon 2026 material about context, correctness, observability, lifecycle, and trust. Speaker claims, repository evidence, and model recommendations remain distinct. |
| **Human-guided learning** | `refine-skill` offers Guided, Deep dive, and Fast learning depths. Consequential actions require explicit approval; feedback alone is not approval. Teaching and evaluator-only answers stay outside evaluated skill runs. |
| **Diagnosis before changes** | `refine-skill` evaluates neutral cases and recorded outcomes, checks whether graders and context are trustworthy, and identifies the likely failure source before proposing a change or specialist handoff. |
| **Validation boundaries** | [Static checks](docs/skill-repository-integrity-and-runtime-safety.md) cover repository structure and source integrity, not model behavior. The consuming harness—not skill text—enforces permissions and approvals. |

### How it relates to other skill-creation and evaluation tools

| Tool | What it contributes | How it fits with DotSkills |
| --- | --- | --- |
| [Anthropic Skill Creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Skill authoring, tests, benchmarking, and trigger optimization. | A potential companion to `refine-skill`'s conference-informed, human-gated learning and diagnosis workflow; this is a difference in emphasis, not a claim that Skill Creator lacks review. |
| [OpenAI Plugin Eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval) | Skill/plugin analysis, measurements, and evaluation reports. | A possible testing aid while DotSkills retains the canonical packages and human review decisions. |
| [Google Cloud EvalBench](https://github.com/GoogleCloudPlatform/evalbench) and [Promptfoo](https://www.promptfoo.dev/docs/guides/test-agent-skills/) | Evaluation execution, scoring, and supported model/harness comparisons. | Potential future runners; DotSkills currently defines manual cases and workflow decisions, not a built-in automated eval service. |

**Current scope:** DotSkills includes structural CI checks, templates, methodology skills, and a starter [manual eval package](evals/README.md). Automated model evaluation, universal cross-harness compatibility, a deployed MCP gateway, and runtime-enforced approvals are **not** included. See [architecture](docs/architecture.md) and [evaluation roadmap](evals/README.md).

## Skill catalog

| Skill | Category | Purpose |
| --- | --- | --- |
| [refine-skill](skills/refine-skill/SKILL.md) | methodology | Optional evidence-driven, conference-informed, human-gated workflow to learn, evaluate, and refine skills. |
| [audit-skill](skills/audit-skill/SKILL.md) | methodology | Read-only **Explore / Audit / Compare**: learn one skill through a question menu and selected deep dives, assess gaps, or compare workflows. [Guide](skills/audit-skill/README.md). |
| [context-engineering](skills/context-engineering/SKILL.md) | methodology | Diagnose and improve context selection, expansion, provenance, freshness, and stopping. |
| [correctness-and-verification](skills/correctness-and-verification/SKILL.md) | methodology | Turn requirements into verifiable claims, invariants, checks, and evidence. |
| [skill-lifecycle-and-release](skills/skill-lifecycle-and-release/SKILL.md) | methodology | Version, regression-test, review, and release skill changes safely. |
| [agent-observability-and-feedback](skills/agent-observability-and-feedback/SKILL.md) | methodology | Inspect agent journeys and turn production feedback into actionable eval coverage. |
| [agent-trust-and-governance](skills/agent-trust-and-governance/SKILL.md) | methodology | Apply provenance, authority boundaries, approvals, risk controls, and verification. |
| [code-review](skills/code-review/SKILL.md) | engineering | Engineering code review through individual book lenses. |
| [investigate-existing-feature](skills/investigate-existing-feature/SKILL.md) | engineering | Feature provenance and dependencies investigation. |
| [investigate-new-feature](skills/investigate-new-feature/SKILL.md) | engineering | Pre-design feature discovery and requirements. |
| [refine-requirements](skills/refine-requirements/SKILL.md) | engineering | Codebase-first guided/practice interview for FRs, NFRs, edge cases, and system-design-ready Superpowers handoff. |
| [learn-repo](skills/learn-repo/SKILL.md) | learning | Whole-repo learning menu, recent technical changes, and selected deep dives using Alex Xu's four steps and relevant book lenses. |
| [learn-implementation](skills/learn-implementation/SKILL.md) | learning | Learn an implementation using the extracted master prompt and five book lenses. |
| [buffr-decision-support](skills/buffr-decision-support/SKILL.md) | decision-support | Buffr M0–M7 module reference and execution guidance; engine remains external. |

See [`catalog.json`](catalog.json) for machine-readable discovery metadata and [`source-lock.json`](source-lock.json) for upstream origin paths and pinned blob identities.

## Quick start

1. Choose a skill above and read its `SKILL.md`.
2. Install or package the **runtime skill files**, including `SKILL.md` and `references/` but excluding evaluator-only `evals/` and generated workspaces, for your chosen harness. For OpenAI harnesses, see the [OpenAI adapter](adapters/openai/README.md); for the Claude Code CLI, see the [Claude Code adapter](adapters/claude/README.md). Other harness guidance lives under [adapters](adapters/README.md).
3. Load additional reference documents on demand. A skill is not automatically executable merely because it exists in a Git repository.
4. Check the library before edits:

```bash
python3 scripts/validate_skill_repository_integrity.py
```

Static CI checks package/source integrity, skill-local eval JSON structure, and adapter behavior; it is **not** an LLM evaluation pipeline.

## Refine Skill

Use [`refine-skill`](skills/refine-skill/SKILL.md) to evaluate and improve a skill, or to minimally convert a raw prompt to the [Agent Skills format](https://agentskills.io/skill-creation/quickstart) when needed. The [practical guide](docs/refine-skill.md) documents the 12 stages, learning modes, and approval gates.

The process is to check the skill's format, write realistic [skill-local eval cases](templates/evals/README.md), compare with-skill versus baseline runs, inspect evidence and grading, diagnose the cause, then apply **approved** changes and check regressions. [Legacy manual cases](evals/README.md) are retained. DotSkills does **not** include an automated model-evaluation runner.

### Why a passing eval is not enough

A **false pass** occurs when evaluation reports success despite a missed requirement or a safety-boundary violation. A rubric can check the wrong behavior, a grader can be misled by untrusted content, or an answer can look acceptable even when the tool trace shows an unauthorized action.

Review both the **grading basis** and the **actual behavior** (available traces, attempted versus completed actions, resulting state, and final output). Diagnose whether the problem lies in the case, rubric, context, harness, trust boundary, or skill. When the rubric changes, regrade preserved evidence if sufficient or rerun before attributing improvement to a skill edit.

This process is **not** an automatic security detector or safety certification. Runtime controls remain essential; see [repository integrity and runtime safety](docs/skill-repository-integrity-and-runtime-safety.md). The [methodology guide](docs/refine-skill.md) covers the relevant conference-informed evaluation practices.
