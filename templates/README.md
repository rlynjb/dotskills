# Reusable templates

Copy [skill/](skill/SKILL.md) to `skills/<skill-name>/` to create a new DotSkills
package. This is an authoring template, not an installed or cataloged skill.

| Template | Use it for |
| --- | --- |
| [skill/](skill/SKILL.md) | A new skill with its entry point and supporting references. |
| [case/](case/README.md) | A new eval case with inputs, expected behavior, grading, and results. |

Keep reusable starting templates here. Put completed skills under `skills/`
and actual eval cases under `evals/`.

## Create a skill

1. Define one useful task and realistic requests that should trigger the skill.
2. Copy `templates/skill/` into `skills/<skill-name>/`.
3. Set the frontmatter `name` to match the folder using lowercase letters,
   digits, and hyphens. Replace every TODO, including the description's triggers.
4. Fill in the required context, workflow, output, and tool boundaries.
   Customize `references/context-quality-and-requirements.md` to define needed
   inputs, evidence checks, missing-context handling, and completion conditions.
5. Replace `references/guide.md` with useful supporting material, or remove it
   and its link. Keep the entry point short and say when to read each reference.
6. Add `scripts/` only for necessary executable helpers and `assets/` only for
   files used in the output. Do not create unused folders.
7. Register the completed skill in `catalog.json`. For imported references,
   follow the [source policy](../docs/sources.md) and record their provenance.
8. Run `python3 scripts/validate_skills.py` from the repository root.
9. Copy the [eval case template](case/README.md), define an
   expected outcome and grading checks, then run and grade one case. Save the
   result in that case's `results/<run-id>/` folder.

Repository validation checks structure and source integrity; it does not prove
that the skill behaves correctly. Start with one case and add cases as needed.

See [authoring guidance](../docs/authoring.md) and the
[development workflow](../docs/eval-driven-skill-development.md).
