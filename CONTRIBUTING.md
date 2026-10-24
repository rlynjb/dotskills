# Contributing to DotSkills

DotSkills is a skill-package library. Keep instructions **portable**, short, and testable.

1. Create `skills/<kebab-case-name>/SKILL.md` with valid `name` and `description` frontmatter.
2. Write specific triggers and a task-focused workflow; put longer knowledge and templates under local `references/`.
3. Keep packages self-contained where possible. State tool and permission requirements rather than assuming access.
4. Register new skills in `catalog.json`. Imported references also require a pinned record in `source-lock.json` with their original blob hash.
5. Run `python3 scripts/validate_skills.py` and review the diff, sources, and scripts before publication.
6. Build evaluation fixtures for correctness, prompt injection, and regression before claiming a skill is validated across harnesses.
7. Do not copy Buffr's executable engine into skills. Integration must call the authorized Buffr runtime.

Documentation and CI checks are not substitutes for actual agent tests or a security review.
