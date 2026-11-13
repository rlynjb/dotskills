# DotSkills

**DotSkills** is a harness-agnostic library of reusable agent skills for any compatible agent harness.

## Skill catalog

Skills are grouped by use.

### Workflows

- **Skill:** [reazn](skills/reazn/SKILL.md)  
  **Purpose:** Reason through an identifiable problem or proposed change using one evidence-backed, four-step SDI assessment. Verify current behavior, examine design and contract boundaries, and explain trade-offs across software, agent skills, and workflows. Read-only and one-pass; optional `learn: on` adds selective book chapters.  
  **Core capabilities:** Input-agnostic analysis; configurable system/subsystem scope; evidence-first investigation; FR/NFR and design-decision traceability; architecture, contracts, and risk assessment; optional learning references.  
  **What you'll learn:** Problem framing, separating evidence from assumptions, system design reasoning, interfaces and invariants, and explaining engineering decisions.

- **Skill:** [slice](skills/slice/SKILL.md)  
  **Purpose:** Turn feature requirements or a REAZN assessment into the smallest set of independently testable, vertically sliced delivery outcomes. Draft tracker-agnostic stories with keyed acceptance criteria, optional subtasks or a parent, and explicit dependencies and unresolved decisions—without publishing tickets.  
  **Core capabilities:** Outcome-based story decomposition; `ST-xx` / `AC-xx` criteria linked to `FR/NFR/D` evidence; scope and dependency tracking; proportional subtasks and parents; provisional readiness checks.  
  **What you'll learn:** Vertical versus horizontal slicing, translating technical design into deliverable work, writing testable acceptance criteria, and maintaining traceability through delivery planning.

- **Skill:** [review-implementation](skills/review-implementation/SKILL.md)  
  **Purpose:** Use **after [reazn](skills/reazn/SKILL.md) and after implementation**, before a merge request. Inspect → Understand → Challenge → Verify the actual changes against requirements, contracts, and risks. A prior REAZN report helps but is not required.  
  **What you'll learn:** Taking ownership of AI-generated or human-written changes, checking design/contract alignment, investigating failure modes, verifying tests, and assessing readiness for human review.

---

### Study

- **Skill:** [refine-documentation](skills/refine-documentation/SKILL.md)  
  **Purpose:** Clean up existing documents with a minimal editorial pass: remove repetition and jargon without adding facts or losing decisions.  
  **What you'll learn:** Clear editing, information preservation, and concise technical writing.

- **Skill:** [study-mcpa](skills/study-mcpa/SKILL.md)  
  **Purpose:** Study for Linux Foundation MCPA with a selectable topic menu, guided practice, mock questions, and optional hands-on DotSkills MCP Server labs.  
  **What you'll learn:** MCP fundamentals, protocol security, integrations, and hands-on server concepts.

- **Skill:** [track-working-groups](skills/track-working-groups/SKILL.md)  
  **Purpose:** Track public working-group updates, manage group metadata and private checkpoints, and prepare source-backed meeting briefings.  
  **What you'll learn:** Technical governance, working-group processes, and source-backed research.

---

### Skill development and assessment

- **Skill:** [evaluate-skill](skills/evaluate-skill/SKILL.md)  
  **Purpose:** Evaluate and improve agent skills through guided tests, evidence-based diagnosis, and approved changes.  
  **What you'll learn:** LLM evals, test cases, assertions, grading, and regression analysis.

- **Skill:** [audit-skill](skills/audit-skill/SKILL.md)  
  **Purpose:** Review one or more skills automatically with at-a-glance profiles, standards and quality checks, Mermaid workflows, cross-platform compatibility, risks, and handoffs; read-only.  
  **What you'll learn:** Skill contracts, Agent Skills compliance, evidence quality, trust, portability, responsibility boundaries, and proposed eval cases.

---

### Decision support

- **Skill:** [buffr-decision-support](skills/buffr-decision-support/SKILL.md)  
  **Purpose:** Explore Buffr's M0–M7 decision-support workflow and use its modules when an authorized runtime is available.  
  **What you'll learn:** Modular agent workflows, evidence-based decisions, experiments, and evaluation.

See [`catalog.json`](catalog.json) for machine-readable categories and exposure settings, and [`source-lock.json`](source-lock.json) for upstream provenance.

---

## Quick start

1. Choose a skill above and read its `SKILL.md`.
2. Install or package the **runtime skill files**, including `SKILL.md` and `references/` but excluding evaluator-only `evals/` and generated workspaces, for your chosen harness. For OpenAI harnesses, see the [OpenAI adapter](adapters/openai/README.md); for the Claude Code CLI, see the [Claude Code adapter](adapters/claude/README.md). Other harness guidance lives under [adapters](adapters/README.md).
3. Load additional reference documents on demand. A skill is not automatically executable merely because it exists in a Git repository.
4. Check the library before edits:

```bash
python3 scripts/validate_skill_repository_integrity.py
```

Static CI checks package/source integrity, skill-local eval JSON structure, and adapter behavior; it is **not** an LLM evaluation pipeline.
