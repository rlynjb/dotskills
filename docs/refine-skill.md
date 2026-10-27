# Refine Skill — practical guide (Agent Skills-aligned)

**Source of truth:** [`skills/refine-skill/SKILL.md`](../skills/refine-skill/SKILL.md).
The runtime instructions and 12 stages are split into focused
[references](../skills/refine-skill/references/workflow.md) so the
entry point stays small and progressively loaded.

Refine Skill is **not a full skill creator or automated model runner**.
Its purpose is to coach you through writing good evaluations,
diagnosing observed failures, applying five conference methodology
lenses, and making evidence-backed improvements through human gates.
It accepts raw prompts as well as existing skills.

## How a session starts

```text
Run Refine Skill on <target prompt or skill>.
Use Guided learning and pause at human gates.
Teach me to write the cases and assertions myself.
```

### Stage 0: basic Agent Skills format gate

Every run checks for a package-root `SKILL.md` with valid YAML
`name` / `description` and a Markdown body. A valid package skips
reformatting. Raw/invalid prompts get a *minimal* conversion proposal
plus a human approval gate, not a rewrite of task behavior.

Official contracts: [Quickstart](https://agentskills.io/skill-creation/quickstart)
and [Specification](https://agentskills.io/specification).
`references/`, `scripts/`, `assets/` and `evals/` are optional.
The DotSkills source path `skills/<name>/` does not conflict with
harness-specific discovery locations.

### Stages 1–11: learn eval design and improve output quality

| Stage | What you do | Learner output |
| --- | --- | --- |
| 1 | Choose one behavior to measure | Observable success criterion |
| 2 | Write 2–3 realistic cases | `<target>/evals/evals.json` with prompts and expected outputs |
| 3 | Run clean paired comparisons | With-skill vs without-skill or old-skill outputs |
| 4 | Study outputs, write assertions, grade | Evidence-backed `grading.json` and human feedback |
| 5 | Ask what actually failed | Diagnosis, including bad case/grader/context/harness |
| 6 | Screen all five methodology lenses | Evidence-backed specialist/no-specialist recommendation |
| 7 | Propose the smallest general fix | Human-reviewed change proposal |
| 8 | Apply approved change | Targeted diff and version |
| 9 | Rerun unchanged cases | New iteration with comparable conditions |
| 10 | Check regressions and independent cases | Before/after evidence, `benchmark.json` if measured |
| 11 | Accept, revise, revert or continue | Human decision and learning notes |

Stages preserve the original 0–11 numbering. Training can proceed one
case at a time; 2–3 is a starting recommendation, not a rigid gate.

The [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills)
recommends `evals/evals.json` in the target skill with `skill_name`
and `evals` (case `id`, `prompt`, `expected_output`, optional `files`,
later `assertions`). Generated evidence belongs in separate per-iteration
workspaces. DotSkills uses gitignored `eval-workspaces/<skill>/iteration-N/`;
the official guide illustrates a sibling `<skill>-workspace/`.
These are evaluation **conventions**, not core skill-format requirements.

The authoring template is [`templates/evals/`](../templates/evals/README.md).
Run `python3 scripts/validate_evals.py --all` to check registered
skill-local suites; this validates **structure only**, not LLM quality.

## Teaching: one example, one case, one decision

For the DDIA code-review lens, suppose an agent claims a partial-write
defect even though a transaction rollback is proven by the supplied
caller and storage contract. A case should provide a *neutral review
request* and only the relevant code/contract; evaluator-only
`expected_output` requires recognizing the protection. After a clean
run, inspect the conclusion and trace, write assertions that distinguish
true defects from false positives, and keep the case fixed while
evaluating a general change.

The learner writes the prompt/expected behavior first; the coach
explains and critiques, but does not invent that the test passed.
Correctly identifying a defect while attempting an unauthorized post
still fails the action-boundary check. Missing trace evidence remains
Unknown, not automatically Pass.

## Five methodology lenses (conference-informed)

| Specialist | Use it to ask |
| --- | --- |
| [Context Engineering](../skills/context-engineering/SKILL.md) | Did missing, stale, excessive or injected context distort the run? |
| [Correctness & Verification](../skills/correctness-and-verification/SKILL.md) | Was the conclusion supported by requirements and evidence? |
| [Observability & Feedback](../skills/agent-observability-and-feedback/SKILL.md) | Did tool/action traces reveal a different trajectory from the answer? |
| [Trust & Governance](../skills/agent-trust-and-governance/SKILL.md) | Did an input or tool request cross authorization boundaries? |
| [Skill Lifecycle & Release](../skills/skill-lifecycle-and-release/SKILL.md) | Does the improvement survive regressions, other harnesses and version changes? |

Scan **all five** every cycle and recommend a specialist deep dive
when evidence justifies it or the learner requests the full-lens
teaching experience. Specialist handoffs remain human-approved; a
failed eval need not mean the target `SKILL.md` is wrong. See
[conference source mappings](../skills/README.md); the mapping is
not a verified transcript for every talk.

## Migration and safety boundaries

The previous manually authored cases under
[`evals/code-review/context-validation/`](../evals/code-review/context-validation/README.md)
and their recorded attempts are **preserved**. They use an older case
template, and this update does not silently move, remove or regrade
them. The newly added `refine-skill/evals/evals.json` contains
**proposed test cases only**, not executed outcomes.

The evaluator must stage agent-facing inputs separately and keep
answer keys and earlier runs inaccessible; simply putting them in
another folder is insufficient. The Claude/OpenAI adapter copy/build
paths should exclude skill-local `evals/`; linking a canonical folder
that includes evals must not be treated as isolated. Harness
permissions, not prompt prose, enforce write restrictions.

**No new automatic model-evaluation runner** is installed by this
workflow. Tests, grades, timings and benchmarks are recorded only
after actual authorized runs; never invent them.
