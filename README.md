# DotSkills

**DotSkills** is a harness-agnostic library of reusable agent skills for any compatible agent harness.

## Table of contents

- [Skill catalog](#skill-catalog)
- [Quick start](#quick-start)
- [Refine Skill](#refine-skill)
  - [Why a passing eval is not enough](#why-a-passing-eval-is-not-enough)

## Skill catalog

Skills are grouped by use. The Refine Skill specialists can also be invoked independently.

### Skill development and assessment

| Skill | Purpose |
| --- | --- |
| [refine-skill](skills/refine-skill/SKILL.md) | Optional evidence-driven, conference-informed, human-gated workflow to learn, evaluate, and refine skills. |
| [audit-skill](skills/audit-skill/SKILL.md) | Read-only **Explore / Audit / Compare**: learn one skill through a question menu and selected deep dives, assess gaps, or compare workflows. [Guide](skills/audit-skill/README.md). |

### Refine Skill supporting methodologies

| Skill | Purpose |
| --- | --- |
| [context-engineering](skills/context-engineering/SKILL.md) | Diagnose and improve context selection, expansion, provenance, freshness, and stopping. |
| [correctness-and-verification](skills/correctness-and-verification/SKILL.md) | Turn requirements into verifiable claims, invariants, checks, and evidence. |
| [skill-lifecycle-and-release](skills/skill-lifecycle-and-release/SKILL.md) | Version, regression-test, review, and release skill changes safely. |
| [agent-observability-and-feedback](skills/agent-observability-and-feedback/SKILL.md) | Inspect agent journeys and turn production feedback into actionable eval coverage. |
| [agent-trust-and-governance](skills/agent-trust-and-governance/SKILL.md) | Apply provenance, authority boundaries, approvals, risk controls, and verification. |

### Everyday workflows

| Skill | Purpose |
| --- | --- |
| [code-review](skills/code-review/SKILL.md) | Engineering code review through individual book lenses. |
| [refine-requirements](skills/refine-requirements/SKILL.md) | Codebase-first guided/practice interview for FRs, NFRs, edge cases, and system-design-ready Superpowers handoff. |
| [learn-repo](skills/learn-repo/SKILL.md) | Whole-repo learning menu, recent technical changes, and selected deep dives using Alex Xu's four steps and relevant book lenses. |
| [learn-implementation](skills/learn-implementation/SKILL.md) | Learn an implementation using the extracted master prompt and five book lenses. |

### Feature investigation

| Skill | Purpose |
| --- | --- |
| [investigate-existing-feature](skills/investigate-existing-feature/SKILL.md) | Feature provenance and dependencies investigation. |
| [investigate-new-feature](skills/investigate-new-feature/SKILL.md) | Pre-design feature discovery and requirements. |

### Decision support

| Skill | Purpose |
| --- | --- |
| [buffr-decision-support](skills/buffr-decision-support/SKILL.md) | Buffr M0–M7 module reference and execution guidance; engine remains external. |

See [`catalog.json`](catalog.json) for machine-readable categories and exposure settings, and [`source-lock.json`](source-lock.json) for upstream provenance.

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
