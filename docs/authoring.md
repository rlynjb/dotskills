# Authoring portable skills

DotSkills follows the [Agent Skills specification](https://agentskills.io/specification), which defines a directory with a required `SKILL.md` entrypoint and optional supporting files.

```text
skills/example-skill/
├── SKILL.md
├── references/    # on-demand information
├── scripts/       # reviewed scripts only when required
└── assets/        # optional templates and other resources
```

Minimal example:

```markdown
---
name: example-skill
description: Explain the task and specifically when to use the skill.
---

# Example skill

1. Determine the user's objective and boundaries.
2. Inspect authorized context.
3. Select only necessary references and permitted tools.
4. Report evidence, uncertainties, and results.
```

Guidance:

- Use lowercase letters, digits, and hyphens; keep `name` aligned with the directory.
- Include a useful **when-to-trigger** description and non-goals to prevent wrong activation.
- Favor progressive disclosure: keep `SKILL.md` concise and place detailed guides in `references/`.
- Prefer relative links internal to the package. Do not require other skills to be installed.
- Do not claim external tools or integration are connected; check tool availability at runtime.
- Use the source-lock process for byte-for-byte imported references; add adapted content separately rather than silently changing source snapshots.

`scripts/validate_skills.py` checks the repository's supported flat frontmatter convention, catalog, local reference paths, and source hashes. A future pipeline can use the upstream `skills-ref` validator and behavioral evals for broader spec coverage.
