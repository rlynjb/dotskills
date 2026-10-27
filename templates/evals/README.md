# Agent Skills-aligned evaluation template

This template is an **optional** starter for a target skill.
Copy `evals.json` into `skills/<target>/evals/evals.json`,
set `skill_name` equal to the target skill's folder, replace both
prompts with realistic use cases, and explain success in
`expected_output`. Start with 2–3 cases, including an edge case.
Include `files` only when needed; those paths are skill-root-relative
and must point to real fixture files (typically in `evals/files/`).

After the first paired runs, add specific `assertions` to each
case; version any changed grading definitions and apply them to
both baseline arms. The guide's JSON fields are an **evaluation
convention**, not required for a valid Agent Skill.

```bash
python3 scripts/validate_evals.py skills/<target>/evals/evals.json
```

This checks schema and fixture paths, **not agent quality**.
Evaluate through [Refine Skill](../../docs/refine-skill.md).
Keep `evals.json` (expected outputs and assertions) and generated
`grading.json` / `benchmark.json` outside the evaluated agent's
readable environment. DotSkills runtime installers omit local
`evals/` directories by default.
