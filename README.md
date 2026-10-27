# DotSkills

**DotSkills** is a version-controlled library of reusable agent skills for compatible harnesses. Each `skills/<name>/` package contains an Agent Skills-compatible `SKILL.md` and optional references. This repository owns skill packaging, discovery metadata, and source provenance; Codex, Claude Code, ChatGPT Work, and other compatible hosts provide execution. [Buffr](https://github.com/rlynjb/buffr) remains the authority for its own decision-support runtime.

## Table of contents

- [Why DotSkills is different](#why-dotskills-is-different)
  - [How it relates to other skill-creation and evaluation tools](#how-it-relates-to-other-skill-creation-and-evaluation-tools)
- [Skill catalog](#skill-catalog)
- [Quick start](#quick-start)
- [Refine Skill](#refine-skill)
  - [Why a passing eval is not enough](#why-a-passing-eval-is-not-enough)
- [Structure](#structure)
- [Current source inventory](#current-source-inventory)
- [Next phases](#next-phases)

## Why DotSkills is different

DotSkills is **not another skill creator or evaluation engine**. It keeps the library portable and source-attributed, while its optional [`refine-skill`](skills/refine-skill/SKILL.md) methodology guides improvements to individual skills. The workflow's human gates and learning modes are specific to that skill, not requirements imposed on every DotSkills package.

| Scope | Distinctive approach |
| --- | --- |
| **DotSkills library** | Versioned [skill packages](skills/README.md), [discovery metadata](catalog.json), [source-locked references](docs/sources.md), and [harness adapters](adapters/README.md) keep instructions and their origins reviewable and reusable. Portability must still be tested in each target environment. |
| **Conference-informed methodology** | `refine-skill` and its [specialist methodologies](skills/README.md) draw on selected AGNTCon/MCPCon 2026 sessions covering context, correctness, observability, lifecycle, and trust. Recommendations distinguish verified conference-talk titles, target-skill sources, eval/repository evidence, and model recommendations; they do not attribute model-made decisions to speakers. |
| **Human-gated collaboration** | In `refine-skill`, consequential steps require explicit approval. It presents evidence, a recommendation, alternatives, and room for the human's own ideas. Feedback is not approval; the default per-gate cadence can be changed only with bounded authorization. |
| **Learning while refining** | `refine-skill` offers **Guided** (default), **Deep dive**, and **Fast** learning depths. Teaching and evaluator-only answer keys are kept outside the skill execution being tested. |
| **Diagnosis before changes** | `refine-skill` uses neutral eval cases, preserved run evidence, uncertainty-aware grading, and regression comparisons. It distinguishes context, grader, harness, trust, and skill failures before recommending edits, and routes to specialists only when supported by evidence. |
| **Clear validation boundaries** | [Repository checks](docs/skill-repository-integrity-and-runtime-safety.md) validate package structure and local source-lock consistency; behavioral results require actual evals. The consuming harness or runtime—not skill text—must enforce permissions, approvals, and other consequential controls. |

### How it relates to other skill-creation and evaluation tools

| Tool | What it contributes | How it fits with DotSkills |
| --- | --- | --- |
| [Anthropic Skill Creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Skill authoring, tests, benchmarking, and trigger optimization. | A potential companion to `refine-skill`'s conference-informed, human-gated learning and diagnosis workflow; this is a difference in emphasis, not a claim that Skill Creator lacks review. |
| [OpenAI Plugin Eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval) | Skill/plugin analysis, measurements, and evaluation reports. | A possible testing aid while DotSkills retains the canonical packages and human review decisions. |
| [Google Cloud EvalBench](https://github.com/GoogleCloudPlatform/evalbench) and [Promptfoo](https://www.promptfoo.dev/docs/guides/test-agent-skills/) | Evaluation execution, scoring, and supported model/harness comparisons. | Potential future runners; DotSkills currently defines manual cases and workflow decisions, not a built-in automated eval service. |

**Current scope:** DotSkills includes structural CI checks, templates, methodology skills, and a starter [manual eval package](evals/README.md). Automated model evaluation, universal cross-harness compatibility, a deployed MCP gateway, and runtime-enforced approvals are **not** included. See [architecture](docs/architecture.md) and [evaluation roadmap](evals/README.md).

## Skill catalog

| Skill | Category | Purpose |
| --- | --- | --- |
| [refine-skill](skills/refine-skill/SKILL.md) | methodology | Optional evidence-driven, conference-informed, human-gated workflow to learn, evaluate, and refine skills. |
| [context-engineering](skills/context-engineering/SKILL.md) | methodology | Diagnose and improve context selection, expansion, provenance, freshness, and stopping. |
| [correctness-and-verification](skills/correctness-and-verification/SKILL.md) | methodology | Turn requirements into verifiable claims, invariants, checks, and evidence. |
| [skill-lifecycle-and-release](skills/skill-lifecycle-and-release/SKILL.md) | methodology | Version, regression-test, review, and release skill changes safely. |
| [agent-observability-and-feedback](skills/agent-observability-and-feedback/SKILL.md) | methodology | Inspect agent journeys and turn production feedback into actionable eval coverage. |
| [agent-trust-and-governance](skills/agent-trust-and-governance/SKILL.md) | methodology | Apply provenance, authority boundaries, approvals, risk controls, and verification. |
| [code-review](skills/code-review/SKILL.md) | engineering | Engineering code review through individual book lenses. |
| [investigate-existing-feature](skills/investigate-existing-feature/SKILL.md) | engineering | Feature provenance and dependencies investigation. |
| [investigate-new-feature](skills/investigate-new-feature/SKILL.md) | engineering | Pre-design feature discovery and requirements. |
| [refine-requirements](skills/refine-requirements/SKILL.md) | engineering | Codebase-first guided/practice interview for FRs, NFRs, edge cases, and system-design-ready Superpowers handoff. |
| [learn-repo](skills/learn-repo/SKILL.md) | learning | Learn a whole repository through the extracted master onboarding prompt. |
| [learn-implementation](skills/learn-implementation/SKILL.md) | learning | Learn an implementation using the extracted master prompt and five book lenses. |
| [buffr-decision-support](skills/buffr-decision-support/SKILL.md) | decision-support | Buffr M0–M7 module reference and execution guidance; engine remains external. |

See [`catalog.json`](catalog.json) for machine-readable discovery metadata and [`source-lock.json`](source-lock.json) for upstream origin paths and pinned blob identities.

## Quick start

1. Choose a skill above and read its `SKILL.md`.
2. Install or package the **runtime skill files**, including `SKILL.md` and `references/` but excluding evaluator-only `evals/` and generated workspaces, for your chosen harness. For OpenAI harnesses, see the [OpenAI adapter](adapters/openai/README.md); for the Claude Code CLI, see the [Claude Code adapter](adapters/claude/README.md). Other harness guidance lives under [adapters](adapters/README.md).
3. Load additional reference documents on demand. A skill is not automatically executable merely because it exists in a Git repository.
4. Check the library before edits:

```bash
python3 scripts/validate_skill_repository_integrity.py
```

Static CI checks package/source integrity, skill-local eval JSON structure, and adapter behavior; it is **not** an LLM evaluation pipeline.

## Refine Skill

Invoke [`refine-skill`](skills/refine-skill/SKILL.md) to evaluate/refine an existing skill or minimally reformat a raw prompt to the [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart) format (Stage 0, only when needed). The [workflow guide](docs/refine-skill.md) covers the human gates, learning modes, and practical run checklists. A typical iteration is:

1. Check the target `SKILL.md` format; valid packages skip all formatting.
2. Learn to write realistic cases and expected outputs in `<skill>/evals/evals.json`.
3. Run isolated with-skill vs without-/old-skill comparisons and inspect results.
4. Add verifiable assertions, grade evidence and screen all five conference methodology lenses.
5. With human approval, improve the responsible component and test regressions.

The [practical guide](docs/refine-skill.md) links the 12 stages, teaching references
and AgentSkills.io conventions. [Legacy manual eval cases](evals/README.md)
remain preserved; the new [skill-local eval template](templates/evals/README.md)
is optional. DotSkills still has **no automated model-evaluation runner**.

### Why a passing eval is not enough

Beyond its learning modes and human approval gates, `refine-skill` guides an
**evidence-based review of both the target skill and the evaluation itself**.
A **false pass** occurs when a run is graded as successful even though a relevant
requirement or safety boundary was violated. This can happen when the rubric
checks the wrong thing, the grader is mistaken or misled by untrusted content,
or an acceptable-looking answer hides unsupported claims or unsafe actions.

The workflow asks the reviewer to inspect:

- **The grading basis:** independently supported expectations, meaningful criteria,
  grader errors, and contamination from answer keys or injected instructions.
- **The actual behavior:** available tool-call traces, attempted versus completed
  actions, resulting state, and the final answer. Missing evidence remains unknown.
- **The responsible cause:** a case, rubric, context, harness, trust boundary, or
  skill problem. More than one can need correction. If the rubric changes, regrade
  preserved baseline evidence where sufficient, or rerun as needed, before claiming
  that a skill edit improved behavior.

**Methodology sources:** *Trustworthy Context Is Untrusted by Default* informs
the concern about poisoned context and fallible graders; *Building an Agentic
Eval Pipeline: Battle-Tested Lessons with EvalBench* informs trajectory, outcome,
and output evaluation and grader calibration. This description is our synthesis
of those lessons, not a claim that either talk prescribed this exact workflow.

These are review and diagnosis instructions, **not an automatic malicious-content
detector or safety certification**. Pre-use content review and restricted execution
remain complementary safeguards; the consuming harness/runtime must enforce
permissions and isolation. See [skill repository integrity and runtime safety](docs/skill-repository-integrity-and-runtime-safety.md)
for existing coverage and planned controls.

## Structure

```text
dotskills/
├── skills/                    # Thirteen skill packages (some hidden by default)
│   ├── refine-skill/
│   ├── context-engineering/
│   ├── correctness-and-verification/
│   ├── skill-lifecycle-and-release/
│   ├── agent-observability-and-feedback/
│   ├── agent-trust-and-governance/
│   ├── code-review/
│   ├── investigate-existing-feature/
│   ├── investigate-new-feature/
│   ├── refine-requirements/
│   ├── learn-repo/
│   ├── learn-implementation/
│   └── buffr-decision-support/
│       └── references/        # module-map.md, runtime/, versioned/
├── catalog.json
├── source-lock.json
├── docs/                      # design, authoring, skill evaluation, sources, security
├── adapters/                  # harness-specific packaging/install adapters
│   ├── openai/                # Codex repo install + portable OpenAI plugin build
│   └── claude/                # Claude Code project install + plugin build
├── evals/                     # preserved legacy manual eval cases
├── templates/evals/           # optional skill-local evals.json starter
├── scripts/                   # repository + eval JSON static validators
├── eval-workspaces/           # generated paired run evidence (gitignored)
└── .github/workflows/         # CI structural/schema checks and adapter tests
```

## Current source inventory

- **Dotfiles:** 8 Markdown documents from [dotfiles/reference](https://github.com/rlynjb/dotfiles/tree/master/reference), including five individual code-review lenses, investigation, and requirements. The combined code-review prompt is no longer included. The PNG diagram remains in dotfiles; it is not a reusable prompt.
- **Buffr:** 10 versioned design/prompt documents and 8 runtime prompt snapshots covering shared policy M0 and stages M1–M7. They are **references only**; actual Buffr module execution is not installed here.

Every imported Markdown file is copied byte-for-byte and tracked against its upstream Git blob SHA. Original cross-reference links inside copied documents may point to neighboring source files that reside in another DotSkills package; use [source provenance](docs/sources.md) to locate them.


## Next phases

The preserved [manual code-review eval](evals/code-review/context-validation/README.md)
has two cases and recorded attempts; it remains in its previous layout.
New skill-local evaluations follow the [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills) and the [template](templates/evals/README.md). The [Refine Skill self-eval suite](skills/refine-skill/evals/README.md) is drafted but **not executed**.

Future work may include additional harness adapters, broader per-skill evals, automated regression runs, a release pipeline, compatibility testing, and optional MCP skill discovery/gateway integration.

Read [architecture](docs/architecture.md), [source policy](docs/sources.md), [authoring](docs/authoring.md), [skill repository integrity and runtime safety](docs/skill-repository-integrity-and-runtime-safety.md), and [contributing](CONTRIBUTING.md).
