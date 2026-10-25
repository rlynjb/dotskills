# DotSkills

**DotSkills** is a canonical, version-controlled library of reusable, harness-agnostic agent skills. Each `skills/<name>/` package has an Agent Skills-compatible `SKILL.md` with optional on-demand `references/`.

It is a **skills library**, not an AI harness, MCP server, or duplicate Buffr implementation. Codex, Claude Code, ChatGPT Work, and other compatible hosts provide tool access and execution. [Buffr](https://github.com/rlynjb/buffr) remains the authoritative source for decision-support workflow code, contracts, state, and effects.

## Skill catalog

| Skill | Category | Purpose |
| --- | --- | --- |
| [code-review](skills/code-review/SKILL.md) | engineering | Engineering code review through individual book lenses. |
| [investigate-existing-feature](skills/investigate-existing-feature/SKILL.md) | engineering | Feature provenance and dependencies investigation. |
| [investigate-new-feature](skills/investigate-new-feature/SKILL.md) | engineering | Pre-design feature discovery and requirements. |
| [refine-feature-requirements](skills/refine-feature-requirements/SKILL.md) | engineering | Ticket refinement and Superpowers handoff. |
| [system-learning-repo](skills/system-learning-repo/SKILL.md) | learning | Learn an unfamiliar repository architecture and data lifecycle. |
| [system-learning-implementation](skills/system-learning-implementation/SKILL.md) | learning | Learn a specific code implementation, its mechanisms, and trade-offs. |
| [buffr-decision-support](skills/buffr-decision-support/SKILL.md) | decision-support | Buffr M0–M7 module reference and execution guidance; engine remains external. |

See [`catalog.json`](catalog.json) for machine-readable discovery metadata and [`source-lock.json`](source-lock.json) for upstream origin paths and pinned blob identities.

## Quick start

1. Choose a skill above and read its `SKILL.md`.
2. Install or copy **the whole skill directory**, including `references/`, into a location supported by your chosen harness. See [harness adapters](adapters/README.md).
3. Load additional reference documents on demand. A skill is not automatically executable merely because it exists in a Git repository.
4. Check the library before edits:

```bash
python3 scripts/validate_skills.py
```

Static CI verifies frontmatter, catalog consistency, referenced files, and immutable imported-source hashes; it is **not** an LLM evaluation pipeline.

## Eval-Driven Skill Development

Use [Eval-Driven Skill Development](docs/eval-driven-skill-development.md) to build and improve any DotSkills skill through clear expectations, representative eval cases, evidence-based grading, and regression checks.

1. Define the skill's purpose, required context, and observable success criteria.
2. Create cases with agent inputs and separate evaluator expectations.
3. Run the skill in fresh sessions and preserve outputs and available tool evidence.
4. Grade the results and investigate failures, unknowns, and invalid runs.
5. Improve the responsible part of the system, then rerun existing and independent cases.

The guide includes a cycle diagram, a practical run checklist, a reusable case outline, and a worked DDIA example. The workflow applies across skills; the existing [manual eval package](evals/README.md) is a starting point for practicing it.

## Structure

```text
dotskills/
├── skills/                    # Seven installable Agent Skills packages
│   ├── code-review/
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
├── adapters/                  # harness distribution guidance, not an installer yet
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

Future work may include tested harness installers, prompt-to-skill migration review, broader per-skill evals, automated regression runs, a release pipeline, and optional MCP skill discovery/gateway integration.

Read [architecture](docs/architecture.md), [source policy](docs/sources.md), [authoring](docs/authoring.md), [skill validation and runtime safety](docs/skill-validation-and-runtime-safety.md), and [contributing](CONTRIBUTING.md).
