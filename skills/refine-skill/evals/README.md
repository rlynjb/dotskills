# Refine Skill — proposed self-evaluation cases

This is an **unexecuted** teaching/evaluation starter in the
[Agent Skills evaluation format](https://agentskills.io/skill-creation/evaluating-skills).
The cases test Stage 0 (valid, malformed, raw) and approval boundaries.
They do **not** establish that Refine Skill passes.

The evaluator should stage only the fixture file and neutral case prompt
for the tested agent, plus the installed runtime `refine-skill` package.
Keep this `evals.json` and expected outputs outside the tested agent's
readable workspace. Use a disposable workspace; no live GitHub writes.

To validate the schema from the DotSkills root:

```bash
python3 scripts/validate_evals.py skills/refine-skill/evals/evals.json
```

To measure output quality, follow [the evaluation guide](../references/eval-design-guide.md)
using clean, paired runs and retain actual evidence in gitignored
`eval-workspaces/refine-skill/iteration-N/`.
