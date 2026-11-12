# DotSkills

**DotSkills** is a harness-agnostic library of reusable agent skills for any compatible agent harness.

## Skill catalog

Skills are grouped by use.

### Skill development and assessment

**Skill:** [evaluate-skill](skills/evaluate-skill/SKILL.md)  
**Purpose:** Evaluate and improve agent skills through guided tests, evidence-based diagnosis, and approved changes.  
**What you'll learn:** LLM evals, test cases, assertions, grading, and regression analysis.
**Skill:** [audit-skill](skills/audit-skill/SKILL.md)  
**Purpose:** Review one or more skills automatically with at-a-glance profiles, standards and quality checks, Mermaid workflows, cross-platform compatibility, risks, and handoffs; read-only.  
**What you'll learn:** Skill contracts, Agent Skills compliance, evidence quality, trust, portability, responsibility boundaries, and proposed eval cases.

### Everyday workflows

**Skill:** [refine-documentation](skills/refine-documentation/SKILL.md)  
**Purpose:** Clean up existing documents with a minimal editorial pass: remove repetition and jargon without adding facts or losing decisions.  
**What you'll learn:** Clear editing, information preservation, and concise technical writing.
**Skill:** [code-review](skills/code-review/SKILL.md)  
**Purpose:** Review code through a software-engineering book lens, explaining evidence-backed findings, trade-offs, and suggested review comments.  
**What you'll learn:** Software design (APOSD), algorithms, DDIA, data engineering, and SDI.
**Skill:** [refine-requirements-light](skills/refine-requirements-light/SKILL.md)  
**Purpose:** Review assigned tickets against verified application code, reuse existing patterns where appropriate, and deliver a noninteractive four-step SDI engineering assessment.  
**What you'll learn:** Applied SDI for ticket analysis: scope, verified patterns, high-level design, relevant request/data flows, and technical risks.
**Skill:** [learn-repo](skills/learn-repo/SKILL.md)  
**Purpose:** Learn an unfamiliar codebase through a selectable question menu, code-backed deep dives, and recent-change analysis.  
**What you'll learn:** SDI (Alex Xu's four steps) for whole-system architecture: scope, components, data flows, bottlenecks, and trade-offs.
**Skill:** [study-mcpa](skills/study-mcpa/SKILL.md)  
**Purpose:** Study for Linux Foundation MCPA with a selectable topic menu, guided practice, mock questions, and optional hands-on DotSkills MCP Server labs.  
**What you'll learn:** MCP fundamentals, protocol security, integrations, and hands-on server concepts.
**Skill:** [track-working-groups](skills/track-working-groups/SKILL.md)  
**Purpose:** Track public working-group updates, manage group metadata and private checkpoints, and prepare source-backed meeting briefings.  
**What you'll learn:** Technical governance, working-group processes, and source-backed research.
**Skill:** [learn-implementation](skills/learn-implementation/SKILL.md)  
**Purpose:** Learn how existing code works through a skimmable four-step SDI overview, boxed ASCII implementation flow, code-backed trade-offs, relevant book chapters, and optional Guided/Practice deep dives.  
**What you'll learn:** Retrospective SDI reasoning for existing features: behavior, component ownership, code/data flows, design decisions, performance and maintainability trade-offs, and selective reading from five engineering books.
**Skill:** [review-implementation](skills/review-implementation/SKILL.md)  
**Purpose:** Guided post-implementation self-review: Inspect → Understand → Challenge → Verify, then report evidence-backed reliability and readiness gaps before a merge request.  
**What you'll learn:** Understanding AI-generated changes, SDI reasoning, failure-mode analysis, hands-on verification, and engineering ownership.

### Decision support

**Skill:** [buffr-decision-support](skills/buffr-decision-support/SKILL.md)  
**Purpose:** Explore Buffr's M0–M7 decision-support workflow and use its modules when an authorized runtime is available.  
**What you'll learn:** Modular agent workflows, evidence-based decisions, experiments, and evaluation.

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
