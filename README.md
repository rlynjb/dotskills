# DotSkills

**DotSkills** is a harness-agnostic library of reusable agent skills for any compatible agent harness.

## Skill catalog

Skills are grouped by use.

### Skill development and assessment

| Skill | Purpose | What you'll learn |
| --- | --- | --- |
| [evaluate-skill](skills/evaluate-skill/SKILL.md) | Evaluate and improve agent skills through guided tests, evidence-based diagnosis, and approved changes.  LLM evals, test cases, assertions, grading, and regression analysis. |
| [audit-skill](skills/audit-skill/SKILL.md) | Explore, audit, or compare skills to understand their workflows, identify gaps, and spot overlaps without making changes.  Skill auditing, evidence quality, gaps, and responsibility boundaries. |
| [integrate-skills](skills/integrate-skills/SKILL.md) **(draft)** | Learn how to collaboratively design, connect, evaluate, and release multi-skill workflows; walkthrough only, no automated changes.  Multi-skill collaboration, composition, handoffs, and release planning. |

### Everyday workflows

| Skill | Purpose | What you'll learn |
| --- | --- | --- |
| [code-review](skills/code-review/SKILL.md) | Review code through a software-engineering book lens, explaining evidence-backed findings, trade-offs, and suggested review comments.  Software design (APOSD), algorithms, DDIA, data engineering, and SDI. |
| [refine-requirements](skills/refine-requirements/SKILL.md) | Refine feature requirements against existing code, identify functional and nonfunctional gaps, and prepare stakeholder questions and design handoffs.  Requirements engineering: FRs/NFRs, scope, edge cases, and trade-offs. |
| [learn-repo](skills/learn-repo/SKILL.md) | Learn an unfamiliar codebase through a selectable question menu, code-backed deep dives, and recent-change analysis.  System design (SDI), architecture, code/data flows, and trade-offs. |
| [study-mcpa](skills/study-mcpa/SKILL.md) | Study for Linux Foundation MCPA with a selectable topic menu, guided practice, mock questions, and optional hands-on DotSkills MCP Server labs.  MCP fundamentals, protocol security, integrations, and hands-on server concepts. |
| [track-working-groups](skills/track-working-groups/SKILL.md) | Track public working-group updates, manage group metadata and private checkpoints, and prepare source-backed meeting briefings.  Technical governance, working-group processes, and source-backed research. |
| [learn-implementation](skills/learn-implementation/SKILL.md) | Learn an implementation through an evidence-backed question and design-decision menu, then Alex Xu's four-step guided deep dives into code, trade-offs, and failure modes.  SDI applied to existing code: design decisions, execution flows, and trade-offs. |

### Decision support

| Skill | Purpose | What you'll learn |
| --- | --- | --- |
| [buffr-decision-support](skills/buffr-decision-support/SKILL.md) | Explore Buffr's M0–M7 decision-support workflow and use its modules when an authorized runtime is available.  Modular agent workflows, evidence-based decisions, experiments, and evaluation. |

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
