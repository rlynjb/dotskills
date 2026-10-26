# DotSkills

**DotSkills** is a canonical, version-controlled library of reusable, harness-agnostic agent skills. Each `skills/<name>/` package has an Agent Skills-compatible `SKILL.md` with optional on-demand `references/`.

It is a **skills library**, not an AI harness, MCP server, or duplicate Buffr implementation. Codex, Claude Code, ChatGPT Work, and other compatible hosts provide tool access and execution. [Buffr](https://github.com/rlynjb/buffr) remains the authoritative source for decision-support workflow code, contracts, state, and effects.

## Table of contents

- [Why DotSkills is different](#why-dotskills-is-different)
  - [How it relates to other skill-creation and evaluation tools](#how-it-relates-to-other-skill-creation-and-evaluation-tools)
- [Skill catalog](#skill-catalog)
- [Quick start](#quick-start)
- [Refine Skill](#refine-skill)
- [Structure](#structure)
- [Current source inventory](#current-source-inventory)
- [Next phases](#next-phases)

## Why DotSkills is different

**DotSkills is a canonical, portable skill library—not a replacement for a skill creator, eval runner, agent harness, or MCP server.** Its **`refine-skill`** methodology provides an optional, conference-informed, human-gated workflow for learning, evaluating, and refining skills. These operating rules apply to that methodology skill, **not automatically to every DotSkills package**.

| Design choice | Where it applies |
| --- | --- |
| **Conference-informed methodology, with source attribution** | Methodology skills synthesize selected AGNTCon/MCPCon 2026 session learnings about context, correctness, skill lifecycle, observability, and trust. When `refine-skill` makes recommendations, it labels their basis as **methodology source** (exact talk title when verified), **target-skill source**, **eval/repository evidence**, and/or **model recommendation**. Conference inspiration is not a claim that a speaker endorsed a particular rule or edit. |
| **Human approval gates in `refine-skill`** | When invoking `refine-skill`, the human approves consequential stage transitions and changes. The workflow presents evidence, one recommendation, viable alternatives, and space for the human's own solution. Feedback is **not** approval. Per-gate is the default; explicitly bounded batched or delegated modes can reduce interruptions without silently authorizing protected changes or final release decisions. |
| **Learning while doing in `refine-skill`** | Guided learning is that skill's default: explain the current concept, the case-specific evidence, and why a recommendation follows. **Deep dive** adds theory and trade-offs; **Fast** minimizes teaching. Learning notes and evaluator answer keys stay outside the target agent's eval input. |
| **Diagnosis before edits; evidence-based specialist routing in `refine-skill`** | A failed eval does not automatically imply a bad prompt. First distinguish case, grader, context, harness, model, trace, trust, or target-skill problems. Route only when evidence warrants it to [context engineering](skills/context-engineering/SKILL.md), [correctness and verification](skills/correctness-and-verification/SKILL.md), [skill lifecycle and release](skills/skill-lifecycle-and-release/SKILL.md), [observability and feedback](skills/agent-observability-and-feedback/SKILL.md), or [trust and governance](skills/agent-trust-and-governance/SKILL.md). |
| **Evidence-first evaluation in `refine-skill`** | Define observable behavior, neutral cases, separately held evaluator expectations, and an unchanged baseline; retain outputs and available tool traces. Grade **Pass / Fail / Unknown / Invalid / Error / Incomplete** as warranted, then compare revisions and check regressions rather than assuming a fluent result is correct. |
| **Portable canonical ownership** | Version-control skill packages, a [catalog](catalog.json), [source-locked upstream references](docs/sources.md), and [harness adapters](adapters/README.md) without equating instructions to an executable engine. DotSkills owns packaged skill guidance; [Buffr](https://github.com/rlynjb/buffr) owns its decision-support runtime. |
| **Separate quality and safety layers** | [Repository integrity checks](docs/skill-repository-integrity-and-runtime-safety.md) validate structure and local source-lock consistency; behavioral evals test actual behavior; sensitive permissions and actions require enforcement by the consuming harness/runtime. None of these layers alone certifies a skill as safe or correct. |

Use [Refine Skill](skills/refine-skill/SKILL.md) when you want this optional methodology workflow; it has a [step-by-step guide](docs/refine-skill.md) and [eval cases](evals/README.md). Other DotSkills skills remain independent.

### How it relates to other skill-creation and evaluation tools

| Tool | What it primarily contributes | How DotSkills / Refine Skill complements it |
| --- | --- | --- |
| [Anthropic Skill Creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Skill authoring, tests, feedback, performance benchmarks, and trigger optimization. | An optional, conference-informed `refine-skill` workflow with explicit approval cadence, guided learning, source labels, and diagnosis-first specialist routing. These are **emphases and local rules**, not claims that Skill Creator lacks human review. |
| [OpenAI Plugin Eval](https://github.com/openai/plugins/tree/main/plugins/plugin-eval) | Local Codex skill/plugin analysis, measurement plans, reports, and comparison workflows. | A canonical skill library; `refine-skill` provides the human-gated refinement process, context/trust/lifecycle methodologies, and decisions about when eval evidence justifies a change. |
| [Google Cloud EvalBench](https://github.com/GoogleCloudPlatform/evalbench) and [Promptfoo](https://www.promptfoo.dev/docs/guides/test-agent-skills/) | Execution and scoring of agent/skill evaluations, including supported cross-harness comparisons. | Requirements, evaluator boundaries, human decisions, provenance, and reusable skill packages; these runners are potential integrations, **not** currently wired into DotSkills. |

**Current boundary:** DotSkills has methodology skills (including the human-gated operating contract in `refine-skill`), static repository validation, templates, and a starter **manual** evaluation package. It **does not yet** provide an automated LLM eval pipeline, universal cross-harness guarantees, a deployed MCP gateway, or runtime-enforced approvals. Adapters, automated evals, and MCP integration are development directions, not shipped capabilities. See [architecture](docs/architecture.md) and [evaluation roadmap](evals/README.md).

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
| [code-review-ddia](skills/code-review-ddia/SKILL.md) | engineering | Standalone DDIA review with an evidence-calibrated rubric. |
| [investigate-existing-feature](skills/investigate-existing-feature/SKILL.md) | engineering | Feature provenance and dependencies investigation. |
| [investigate-new-feature](skills/investigate-new-feature/SKILL.md) | engineering | Pre-design feature discovery and requirements. |
| [refine-feature-requirements](skills/refine-feature-requirements/SKILL.md) | engineering | Ticket refinement and Superpowers handoff. |
| [system-learning-repo](skills/system-learning-repo/SKILL.md) | learning | Learn an unfamiliar repository architecture and data lifecycle. |
| [system-learning-implementation](skills/system-learning-implementation/SKILL.md) | learning | Learn a specific code implementation, its mechanisms, and trade-offs. |
| [buffr-decision-support](skills/buffr-decision-support/SKILL.md) | decision-support | Buffr M0–M7 module reference and execution guidance; engine remains external. |

See [`catalog.json`](catalog.json) for machine-readable discovery metadata and [`source-lock.json`](source-lock.json) for upstream origin paths and pinned blob identities.

## Quick start

1. Choose a skill above and read its `SKILL.md`.
2. Install or package **the whole skill directory**, including `references/`, for your chosen harness. For OpenAI harnesses, see the [OpenAI adapter](adapters/openai/README.md); other harness guidance lives under [adapters](adapters/README.md).
3. Load additional reference documents on demand. A skill is not automatically executable merely because it exists in a Git repository.
4. Check the library before edits:

```bash
python3 scripts/validate_skill_repository_integrity.py
```

Static CI verifies frontmatter, catalog consistency, referenced files, and immutable imported-source hashes; it is **not** an LLM evaluation pipeline.

## Refine Skill

Use the optional [Refine Skill](docs/refine-skill.md) methodology to learn how to improve a target skill through relevant conference-derived principles, human approval, representative eval cases, evidence-based grading, targeted specialist routing, and regression checks. It can also bootstrap rough source material when needed.

1. Define the skill's purpose, required context, and observable success criteria.
2. Create cases with agent inputs and separate evaluator expectations.
3. Run the skill in fresh sessions and preserve outputs and available tool evidence.
4. Grade the results and investigate failures, unknowns, and invalid runs.
5. Improve the responsible part of the system, then rerun existing and independent cases.

The guide includes a cycle diagram, a practical run checklist, a reusable case outline, and a worked DDIA example. The workflow applies across skills; the existing [manual eval package](evals/README.md) is a starting point for practicing it.

## Structure

```text
dotskills/
├── skills/                    # Fourteen skill packages (some hidden by default)
│   ├── refine-skill/
│   ├── context-engineering/
│   ├── correctness-and-verification/
│   ├── skill-lifecycle-and-release/
│   ├── agent-observability-and-feedback/
│   ├── agent-trust-and-governance/
│   ├── code-review/
│   ├── code-review-ddia/
│   ├── investigate-existing-feature/
│   ├── investigate-new-feature/
│   ├── refine-feature-requirements/
│   ├── system-learning-repo/
│   ├── system-learning-implementation/
│   └── buffr-decision-support/
│       └── references/        # module-map.md, runtime/, versioned/
├── catalog.json
├── source-lock.json
├── docs/                      # design, authoring, skill evaluation, sources, security
├── adapters/                  # harness-specific packaging/install adapters
│   └── openai/                # Codex repo install + portable OpenAI plugin build
├── evals/                     # manual skill-evaluation cases and roadmap
├── scripts/                   # dependency-free local validation
└── .github/workflows/         # CI structural/source-integrity checks
```

## Current source inventory

- **Dotfiles:** 10 Markdown documents from [dotfiles/reference](https://github.com/rlynjb/dotfiles/tree/master/reference), including five individual code-review lenses, investigation, requirements, and learning. The combined code-review prompt is no longer included. The PNG diagram remains in dotfiles; it is not a reusable prompt.
- **Buffr:** 10 versioned design/prompt documents and 8 runtime prompt snapshots covering shared policy M0 and stages M1–M7. They are **references only**; actual Buffr module execution is not installed here.

Every imported Markdown file is copied byte-for-byte and tracked against its upstream Git blob SHA. Original cross-reference links inside copied documents may point to neighboring source files that reside in another DotSkills package; use [source provenance](docs/sources.md) to locate them.


## Next phases

The first [manual code-review eval](evals/code-review/context-validation/README.md)
provides two cases. Each case holds its inputs, expected behavior, grading guidance,
and recorded attempts. Start with one case, run the reviewer, grade its response,
and save the result in that case’s `results/` folder.

Future work may include additional harness adapters, broader per-skill evals, automated regression runs, a release pipeline, compatibility testing, and optional MCP skill discovery/gateway integration.

Read [architecture](docs/architecture.md), [source policy](docs/sources.md), [authoring](docs/authoring.md), [skill repository integrity and runtime safety](docs/skill-repository-integrity-and-runtime-safety.md), and [contributing](CONTRIBUTING.md).
