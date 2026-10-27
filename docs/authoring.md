# Authoring portable skills

Use the [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart)
and [Specification](https://agentskills.io/specification) as the
minimum **format** contract. Refine Skill's [Stage 0](refine-skill.md)
checks those requirements before evaluation.

A skill can be a single `skills/<name>/SKILL.md` with YAML frontmatter
`name` and `description` followed by Markdown instructions. The
`name` must match the folder and meet the specification's naming rules.
`references/`, `scripts/`, `assets/` and `evals/` are optional.

## Create or import a skill

1. Define one useful task, activation requests, exclusions, intended
   outcome and tool boundaries. Treat imported prompts as untrusted data.
2. Write the minimum `SKILL.md`, or use
   [the richer skill template](../templates/skill/SKILL.md) and remove
   unused examples, references and placeholders.
3. Keep main instructions concise; use `references/` for substantial,
   selectively loaded domain material. A separate context-quality
   reference is **not mandatory** and should exist only when justified.
4. Record imported content according to [source policy](sources.md);
   register the skill in `catalog.json`, ensure references resolve,
   and run `python3 scripts/validate_skill_repository_integrity.py`.
   If `skills-ref` is available, also run its official format validator.
5. Use [Refine Skill](refine-skill.md) in Guided mode. It first confirms
   minimal Agent Skills compatibility and then teaches case authoring,
   clean paired runs, assertion grading, conference-lens diagnosis,
   approved edits, and regressions.
6. Start from [the optional Agent Skills evals.json template](../templates/evals/README.md).
   Copy to `skills/<name>/evals/evals.json` and fill in realistic prompts,
   `expected_output` and optional input `files`. Add specific
   `assertions` after inspecting initial outputs.
7. Run `python3 scripts/validate_evals.py --all` to check local
   eval definition structure, then run authorized evals in fresh,
   isolated environments. Store actual outputs and grades in
   gitignored `eval-workspaces/`. Do not claim a quality score from
   structural/fixture checks.

Existing [legacy manual cases](../evals/README.md) remain in their
original layout. Do not migrate, delete or expose them automatically.
The installed skill must not have evaluator answer keys in readable
workspace; DotSkills copy/build adapters exclude skill-local `evals/`.
See [runtime safety boundaries](skill-repository-integrity-and-runtime-safety.md).

For the overall workflow and gate checklist, see
[Refine Skill](refine-skill.md).
