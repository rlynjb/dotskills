# Reusable templates

All Agent Skills need only a package-root `SKILL.md` with valid YAML
`name` / `description` followed by Markdown. Optional folders should
be added because a real need exists, not just to match a template.

| Template | Use it for |
| --- | --- |
| [skill/](skill/SKILL.md) | Rich authoring starter with optional guidance (remove unused files). |
| [evals/](evals/README.md) | **Recommended new convention:** copy `evals.json` into a target skill's `evals/` folder. |
| [case/](case/README.md) | **Legacy manual suite:** original detailed cases and grading files; preserved for existing tests. |

## Start a skill

1. Define the task and when the skill should activate.
2. Write `skills/<name>/SKILL.md` using the
   [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart),
   or start from [the richer authoring template](skill/SKILL.md)
   and delete unnecessary references and placeholders.
3. Register the skill in `catalog.json` and run
   `python3 scripts/validate_skill_repository_integrity.py`.
4. Run Refine Skill. Its Stage 0 performs the minimum format check and
   **does not rewrite a valid skill**. In Stage 2, practice writing
   `evals/evals.json` for the target skill using [evals/](evals/README.md).
5. Validate the JSON with `python3 scripts/validate_evals.py --all`,
   then run safe isolated paired model evals and record actual results
   through the [workflow](../docs/refine-skill.md).

Tests and answer keys are **evaluator-only**. Install runtime skill copies
without local `evals/` and do not expose generated run directories.
Static validation does not mean an evaluation has run or passed.
