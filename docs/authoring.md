# Authoring portable skills

Use this checklist to create and package a skill. The [templates folder](../templates/README.md)
contains the reusable starting files and examples; [Eval-Driven Skill Development](eval-driven-skill-development.md)
covers testing and improving the skill's behavior.

## Create a skill

1. **Choose one task.** Define its useful outcome, scope, realistic trigger
   requests, and closely related tasks it should not handle.
2. **Copy the [skill template](../templates/skill/SKILL.md).** Copy the entire
   `templates/skill/` folder to `skills/<skill-name>/`.
3. **Customize the entry point.** In `SKILL.md`, match the frontmatter `name`
   to the folder using lowercase letters, digits, and hyphens. Write a specific
   trigger description, concise workflow, output format, and tool boundaries.
4. **Define the context requirements.** Customize
   [context quality and requirements](../templates/skill/references/context-quality-and-requirements.md)
   for required inputs, evidence checks, missing or conflicting information,
   and completion conditions.
5. **Add only necessary supporting guidance.** Adapt the
   [task-guide template and worked example](../templates/skill/references/skill-name.md).
   Rename it for its subject, update its link in `SKILL.md`, and state when to
   read it. Remove unused examples, authoring notes, placeholders, and files.
6. **Keep the package portable.** Use relative links within the package.
   Add `scripts/` only for reviewed executable helpers and `assets/` only for
   needed output resources. State required tools and permissions, and check
   availability at runtime rather than assuming an integration is connected.
7. **Register and review it.** Add the skill to `catalog.json`. Follow the
   [source policy](sources.md) for imported references and source-lock records;
   preserve locked snapshots and put adaptations in separate files. Apply
   [skill validation and runtime safety guidance](skill-validation-and-runtime-safety.md)
   before executing external content.
8. **Validate the package.** From the repository root, run
   `python3 scripts/validate_skills.py`. Resolve reported structural, catalog,
   reference-path, and local source-lock consistency errors. Passing does not
   establish safe or correct behavior.
9. **Create and run its first eval case.** Start with the
   [case template](../templates/case/README.md), then follow the
   [eval development workflow](eval-driven-skill-development.md) to establish
   expectations, run the agent, grade evidence, and retain results.

Keep detailed instructions in references and evaluator-only material under
`evals/`. The package-root `SKILL.md` remains the entry point.

See [contributing](../CONTRIBUTING.md) for repository requirements.
