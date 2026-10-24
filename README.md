# DotSkills

**DotSkills** is a canonical, version-controlled library of reusable, harness-agnostic agent skills. Each `skills/<name>/` package has an Agent Skills-compatible `SKILL.md` with optional on-demand `references/`.

It is a **skills library**, not an AI harness, MCP server, or duplicate Buffr implementation. Codex, Claude Code, ChatGPT Work, and other compatible hosts provide tool access and execution. [Buffr](https://github.com/rlynjb/buffr) remains the authoritative source for decision-support workflow code, contracts, state, and effects.

## Skill catalog

| Skill | Category | Purpose |
| --- | --- | --- |
| [code-review](skills/code-review/SKILL.md) | engineering | Integrated engineering code review with five specialized book lenses. |
| [investigate-existing-feature](skills/investigate-existing-feature/SKILL.md) | engineering | Feature provenance and dependencies investigation. |
| [investigate-new-feature](skills/investigate-new-feature/SKILL.md) | engineering | Pre-design feature discovery and requirements. |
| [refine-feature-requirements](skills/refine-feature-requirements/SKILL.md) | engineering | Ticket refinement and Superpowers handoff. |
| [system-learning-repo](skills/system-learning-repo/SKILL.md) | learning | Learn an unfamiliar repository architecture and data lifecycle. |
| [system-learning-implementation](skills/system-learning-implementation/SKILL.md) | learning | Learn a specific code implementation, its mechanisms, and trade-offs. |
| [rehearse-ga-call](skills/rehearse-ga-call/SKILL.md) | career | Golden Analytics recruiter screen rehearsal. |
| [rehearse-google-call](skills/rehearse-google-call/SKILL.md) | career | Google recruiter call rehearsal. |
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

## Structure

```text
dotskills/
├── skills/                    # Nine installable Agent Skills packages
│   ├── code-review/
│   ├── investigate-existing-feature/
│   ├── investigate-new-feature/
│   ├── refine-feature-requirements/
│   ├── system-learning-repo/
│   ├── system-learning-implementation/
│   ├── rehearse-ga-call/
│   ├── rehearse-google-call/
│   └── buffr-decision-support/
│       └── references/        # module-map.md, runtime/, versioned/
├── catalog.json
├── source-lock.json
├── docs/                      # design, authoring, source ownership, security
├── adapters/                  # harness distribution guidance, not an installer yet
├── evals/                     # future skill-evaluation design
├── scripts/                   # dependency-free local validation
└── .github/workflows/         # CI structural/source-integrity checks
```

## Initial source inventory

- **Dotfiles:** all 13 Markdown documents from [dotfiles/reference](https://github.com/rlynjb/dotfiles/tree/master/reference), including five code-review lenses, investigation, requirements, learning, and recruiter call materials. The PNG diagram remains in dotfiles; it is not a reusable prompt.
- **Buffr:** 10 versioned design/prompt documents and 8 runtime prompt snapshots covering shared policy M0 and stages M1–M7. They are **references only**; actual Buffr module execution is not installed here.

Every imported Markdown file is copied byte-for-byte and tracked against its upstream Git blob SHA. Original cross-reference links inside copied documents may point to neighboring source files that reside in another DotSkills package; use [source provenance](docs/sources.md) to locate them.

**Privacy:** Some recruiter-script examples contain personal career history. Review these public files before installing them in shared contexts.

## Next phases

Future work may include tested harness installers, prompt-to-skill migration review, per-skill evals and regression fixtures, a release pipeline, and optional MCP skill discovery/gateway integration. These are not yet implemented.

Read [architecture](docs/architecture.md), [source policy](docs/sources.md), [authoring](docs/authoring.md), [security](docs/security.md), and [contributing](CONTRIBUTING.md).
