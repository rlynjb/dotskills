# DotSkills

**DotSkills** is a harness-agnostic library of reusable agent skills for any compatible agent harness.

## Skill catalog

Skills are grouped by use.

### Skill development and assessment

| Skill | Purpose |
| --- | --- |
| [refine-skill](skills/refine-skill/SKILL.md) | Evaluate and improve agent skills through guided tests, evidence-based diagnosis, and approved changes. |
| [audit-skill](skills/audit-skill/SKILL.md) | Explore, audit, or compare skills to understand their workflows, identify gaps, and spot overlaps without making changes. |

### Everyday workflows

| Skill | Purpose |
| --- | --- |
| [code-review](skills/code-review/SKILL.md) | Review code through a software-engineering book lens, explaining evidence-backed findings, trade-offs, and suggested review comments. |
| [refine-requirements](skills/refine-requirements/SKILL.md) | Refine feature requirements against existing code, identify functional and nonfunctional gaps, and prepare stakeholder questions and design handoffs. |
| [learn-repo](skills/learn-repo/SKILL.md) | Learn an unfamiliar codebase through a selectable question menu, code-backed deep dives, and recent-change analysis. |
| [learn-implementation](skills/learn-implementation/SKILL.md) | Learn an implementation through an evidence-backed question and design-decision menu, then Alex Xu's four-step guided deep dives into code, trade-offs, and failure modes. |

### Decision support

| Skill | Purpose |
| --- | --- |
| [buffr-decision-support](skills/buffr-decision-support/SKILL.md) | Explore Buffr's M0–M7 decision-support workflow and use its modules when an authorized runtime is available. |

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
