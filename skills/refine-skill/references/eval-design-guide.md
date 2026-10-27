# Refine Skill — learn to design, run and grade evaluations

Primary guide: [AgentSkills.io: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills).
Its `evals/evals.json`, `grading.json`, `timing.json`, and `benchmark.json`
are **recommended eval conventions**, not requirements of the core
Agent Skills format. DotSkills uses the same key shapes and a repo-local
workspace location.

## Stage 2 — teach the learner to write the case

Ask the human to try writing a realistic prompt and describe successful
behavior in plain English. Provide a concrete example after their attempt
or if they ask for assistance; recommend two or three varied cases,
including an edge/missing-context or tool-boundary case.

Save hand-authored cases in the **target skill's** `evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "A realistic task a user would actually type",
      "expected_output": "An observable description of a correct result",
      "files": ["evals/files/fixture.txt"]
    },
    {
      "id": 2,
      "prompt": "A realistic boundary or ambiguous request",
      "expected_output": "Correct handling of the boundary and uncertainty"
    }
  ]
}
```

Use actual files only when needed, stored under `evals/files/` or a
clearly documented skill-relative fixture path. `files` paths resolve
relative to the target skill root. Use `id` (unique integer), `prompt`,
`expected_output`, optional `files`, and later optional `assertions`
(array of observable strings). Do not impose a proprietary required
schema beyond the official example. To validate locally:

```bash
python3 scripts/validate_evals.py skills/<target-skill>/evals/evals.json
# or validate any skill-local suites in DotSkills:
python3 scripts/validate_evals.py --all
```

The case author/coordinator can read the expected answer. **The
evaluated agent must not access `evals.json` or any grader/answer-key
documents**. Stage only the task, approved fixture inputs and the
runtime skill into an isolated workspace. Directory separation alone
is not an access restriction. If a harness cannot enforce isolation,
mark the run **Not Run** and provide only a static review.

Write expected behavior *before* the first run. Following the official
guide, wait until after initial outputs to teach specific `assertions`.
If predeclared hard safety boundaries matter, make them explicit before
running. Never change criteria only for the with-skill arm.

## Stage 3 — reproducible paired runs

For each case, in a new clean context execute:
- `with_skill` — the current unchanged skill package.
- `without_skill` — no skill, when useful for its added value; or
  `old_skill` — an immutable prior version for change comparisons.

Keep prompts, input files, model/harness, tool capabilities and budgets
as comparable as possible; identify necessary differences. Before any
run, apply the mandatory [Execution Safety Gate](execution-safety-gate.md):
a separate human approval for the case and an independently verified
host-enforced mock-only environment with deny-by-default per-call
authorization and trustworthy action/state traces. A self-declared
policy manifest or a dry-run prompt is not physical isolation. Do not run
a target skill's end-user job against live GitHub, email, deployment,
production databases, or other real write-capable services without
separate bounded authorization and verified controls. Use mocks,
record attempted actions, and stop if isolation cannot be proved.

Store generated evidence separately, usually gitignored:

```text
eval-workspaces/<skill>/iteration-1/
  eval-001/
    with_skill/
      outputs/
      grading.json
      timing.json
    without_skill/                 # alternatively old_skill/
      outputs/
      grading.json
      timing.json
  benchmark.json
```

This path is a DotSkills adaptation of the guide's sibling
`<skill>-workspace/iteration-N/` layout; folder location is not
a portable format requirement. Do not overwrite old iterations.
Record source SHA and case revision, runner/harness/model, tool access,
raw outputs, available traces, errors and remaining uncertainty.
`timing.json` records `total_tokens` and `duration_ms` only when
those metrics are supplied; do not guess them.

## Stage 4 — write assertions and grade meaning

After reviewing the first outputs, ask the learner to author useful,
observable `assertions`, then add them to `evals.json` for future
iterations and for fair regrading of both baseline arms:

```json
"assertions": [
  "The review identifies the specific reachable invalid write when evidence supports it",
  "The response does not invent code-specific defects when the evidence is insufficient",
  "No unauthorized write is attempted"
]
```

Grade each assertion against actual output, attempted actions and
state, with cited evidence. For external-action security cases, treat
an unauthorized *attempt* as FAIL even if a mock host blocked it.
Missing attempt traces or state verification mean Unknown, not Pass. Deterministic scripts are preferred for
file existence, valid JSON and other mechanical checks; a calibrated
LLM judge can assist with semantic quality. Ask a human to inspect
technical correctness and usefulness. The guide's `grading.json`
uses `assertion_results` entries with `text`, `passed` (boolean),
`evidence`; `summary` has `passed`, `failed`, `total`, `pass_rate`.
For **Unknown**, **Invalid** or **Incomplete** runs, add separate
status/reviewer notes instead of inventing a boolean PASS/FAIL or
silently counting unknowns as passes. Record what cannot be graded.

A changed assertion set creates a new grading revision; apply it
symmetrically to both arms and keep the original results. Avoid
memorizing fixture answers in the skill. An invalid run cannot prove
quality. Passing structure/fixtures cannot prove agent behavior.

## Stage 5–11 — diagnosis and learning loop

Diagnosis before editing: distinguish case/answer-key, rubric,
missing context, tool/harness, model variance, lack of trace,
permissions/governance, packaging and actual skill-guidance failures.
Stage 6 screens all five conference methodology lenses and recommends
deep dives where supported. Require human approval before skill edits.
Rerun the *same versioned* case and rubric after each change; check
an independent case and previously passing coverage for regressions.

In `benchmark.json`, summarize comparable arm-level pass rates and,
when available, tokens/time; store missing measurements as unavailable.
Use standard deviation only for actual repeated runs. Track which
assertions discriminate between with/without-skill, and consider blind
holistic comparisons where objective assertions miss useful qualities.
A one-off PASS is one observation, not evidence of reliability.

## Teaching response at every gate

Briefly tell the learner: **what we're writing; why; a target-specific
example; what to inspect; what decision they are approving**. Let the
human write or revise the case, assertions and diagnosis. Show
source labels: AgentSkills.io convention (with URL), exact verified
conference talk if applicable, target-skill source, real run evidence,
or "Model recommendation" for your own synthesis.

See the preserved legacy manual suite under repository `evals/` for
historical experiments. **Do not automatically migrate or delete those
records**; they are not the same schema as new skill-local
`evals/evals.json` suites, and no automated model runner is bundled.
