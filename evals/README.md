# Evaluations — legacy cases and new convention

DotSkills retains the **original manually authored cases** under
`evals/<skill>/<capability>/cases/`, including their historical
results and preparation scripts. No migration, deletion or regrading
of these records is performed automatically.

The original [code-review context-validation suite](code-review/context-validation/README.md)
has two synthetic cases and recorded attempts. Its fixture verifier
checks example code, **not** agent output quality. The
[legacy case template](../templates/case/README.md) remains useful
for reproducing those experiments.

## New Agent Skills-aligned workflow

For *new* tests, the
[official evaluation guide](https://agentskills.io/skill-creation/evaluating-skills)
recommends `skills/<target>/evals/evals.json` with:

- `skill_name` identifying the target skill;
- `evals` array of cases with `id`, realistic `prompt`,
  `expected_output` and optional skill-relative `files`;
- optional `assertions` added after studying initial outputs.

Copy the [evals.json template](../templates/evals/README.md).
The [Refine Skill Stage 2–4 guide](../skills/refine-skill/references/eval-design-guide.md)
coaches case writing, safe with-/without-skill or old-skill runs,
grading with evidence, and human review. Generated `grading.json`,
`timing.json` and `benchmark.json` belong under gitignored
`eval-workspaces/<skill>/iteration-N/`. Their content must come from
**real runs**, not invented metrics.

```bash
python3 scripts/validate_evals.py --all
python3 scripts/validate_evals.py skills/refine-skill/evals/evals.json
```

Validation checks JSON fields and fixture paths only, not evaluation
quality or correct tool behavior. A full automated model runner is
not installed. Safely isolate the eval coordinator's expected outputs
from the evaluated agent; copying a whole source skill with
`evals/` into its runtime workspace would leak answer keys.
DotSkills copy/build adapters exclude those evaluator files.

## Coverage roadmap

Expand from a few realistic cases toward skill triggering,
missing/conflicting context, calibrated code review and zero-finding
cases, prompt-injection resistance, permissions, cross-harness
behavior, regression, and Buffr runtime integration. Maintain
independent holdout cases instead of overfitting to one fixture.
