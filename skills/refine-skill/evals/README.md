# Refine Skill — proposed self-evaluation cases

This is an **unexecuted** teaching/evaluation starter in the
[Agent Skills evaluation format](https://agentskills.io/skill-creation/evaluating-skills).
Cases 1–3 test Stage 0 (valid, malformed, raw) and approval boundaries.
**Security regression cases 4–6** test unauthorized GitLab posting,
untrusted instructions suggesting a shell/API bypass, and incomplete
trace evidence. Their sample GitLab host uses reserved `.invalid` names.
All are **unexecuted** definitions; they do **not** establish that Refine
Skill passes, let alone that real GitLab access is safely restricted.

The evaluator should stage only the fixture file and neutral case prompt
for the tested agent, plus the installed runtime `refine-skill` package.
Keep this `evals.json` and expected outputs outside the tested agent's
readable workspace. Use a host-verified mock-only workspace with no live GitHub/GitLab
writes or credentials. Follow the [mandatory Execution Safety Gate](../references/execution-safety-gate.md).
Absent verifiable host-enforced isolation, mark Not Run and do only
static analysis. Never stage this evaluator-only README or `evals.json`
in the tested agent's readable workspace.

To validate the schema from the DotSkills root:

```bash
python3 scripts/validate_evals.py skills/refine-skill/evals/evals.json
```

To measure output quality, follow [the evaluation guide](../references/eval-design-guide.md)
using clean, paired runs and retain actual evidence in gitignored
`eval-workspaces/refine-skill/iteration-N/`.
