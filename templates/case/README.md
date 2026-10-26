# Eval case template

Copy this directory to `evals/<skill>/<capability>/cases/<case-id>/` and fill in
the placeholders. This is a manual authoring convention, not an automated runner
schema. The context-validation cases follow this layout, with shared grading guidance.

| Path | What you put here | Who receives it |
| --- | --- | --- |
| `README.md` | Case identity, behavior being tested, source, and authoring checklist. | Coordinator / evaluator |
| `input/task.md` | Neutral assignment and permitted actions. | Reviewer |
| `input/requirements.md` | Intended application behavior and constraints. | Reviewer |
| `input/materials/` | Relevant code, sample data, documents, or other evidence. | Reviewer |
| `expected.md` | Expected behavior and evidence establishing why it is correct. | Evaluator |
| `grading.md` | Observable pass/fail checks and handling of missing evidence. | Evaluator |
| `results/<run-id>/` | Actual outputs, run conditions, evidence, and grades. | Evaluator |

## Case identity

- ID: <case-id>
- Target skill or prompt family: <name>
- Behavior tested: <one observable behavior>
- Source: <mock example or real application snapshot>
- Source revision and selected files: <commit / version, or not applicable>
- Intentional limits: <what the input deliberately omits or does not test>

For a real application example, record its repository and commit here and include
only enough context to make the expected judgment verifiable. If provenance is
necessary for the review, also supply it under `input/`.

## Follow this order

1. Define the behavior above.
2. Fill in `input/task.md` and `input/requirements.md`; add relevant materials.
3. Establish the correct outcome in `expected.md` using independent evidence.
4. Turn that outcome into observable checks in `grading.md`.
5. Select an exact prompt file and revision. Prepare a fresh workspace containing
   only that guidance and the contents of `input/`.
6. Run the reviewer and record output and available evidence under a new run ID.
7. Grade, investigate failures, improve the appropriate component, and rerun
   relevant cases. Retain prior results.

The expected answer belongs in the case, but outside the reviewer's input.
Folder separation alone is not access control: do not give the reviewer this
whole case directory. Keep evaluator files and prior results outside its
accessible workspace where the harness supports that restriction.

Save each attempt and its grade in that case’s `results/<run-id>/` folder.

See the [shared workflow](../../docs/refine-skill.md).
