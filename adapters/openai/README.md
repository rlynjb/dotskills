# OpenAI adapter

This adapter keeps `skills/` as the canonical DotSkills source and prepares those
packages for OpenAI harnesses without rewriting their instructions.

It supports two paths:

1. **Codex repo-local install** — copy or symlink selected skills into
   `<target>/.agents/skills/`.
2. **Portable OpenAI plugin build** — package selected skills under a root
   `plugin.json` + `skills/` layout for supported ChatGPT/Codex plugin workflows.

No compilation step changes `SKILL.md`. The adapter selects, copies, and packages the
canonical directories in the layout the harness expects.

## Codex repo-local install

Install the methodology family into another repository:

```bash
python3 adapters/openai/install_codex.py --target ../my-project
```

The default selector is `category=methodology`, so the result is:

```text
../my-project/
└── .agents/
    └── skills/
        ├── refine-skill/
        ├── context-engineering/
        ├── correctness-and-verification/
        ├── skill-lifecycle-and-release/
        ├── agent-observability-and-feedback/
        └── agent-trust-and-governance/
```

Useful variants:

```bash
# Preview only
python3 adapters/openai/install_codex.py --target ../my-project --dry-run

# Install one skill
python3 adapters/openai/install_codex.py \
  --target ../my-project \
  --skill code-review

# Install a category
python3 adapters/openai/install_codex.py \
  --target ../my-project \
  --category engineering

# Install every catalog skill
python3 adapters/openai/install_codex.py --target ../my-project --all

# Replace an existing install
python3 adapters/openai/install_codex.py --target ../my-project --force

# Development mode: symlink back to canonical DotSkills packages
python3 adapters/openai/install_codex.py --target ../my-project --link
```

Copy mode is the default because it is portable. Link mode is useful when developing
DotSkills locally and you want changes to be visible immediately in the target repo.

## Build a portable OpenAI plugin

Build the methodology package:

```bash
python3 adapters/openai/build_plugin.py --zip
```

Default output:

```text
dist/openai/dotskills-methodology/
├── plugin.json
└── skills/
    ├── refine-skill/
    ├── context-engineering/
    ├── correctness-and-verification/
    ├── skill-lifecycle-and-release/
    ├── agent-observability-and-feedback/
    └── agent-trust-and-governance/
```

With `--zip`, the adapter also writes:

```text
dist/openai/dotskills-methodology.zip
```

Other selectors:

```bash
# One or more named skills
python3 adapters/openai/build_plugin.py \
  --skill refine-skill \
  --skill context-engineering

# Another category
python3 adapters/openai/build_plugin.py --category engineering

# Every skill
python3 adapters/openai/build_plugin.py --all --name dotskills-all
```

The generated package uses the portable Agent Plugins root-manifest layout. It does
not add MCP configuration because DotSkills is currently a skills library; tools and
permissions remain the responsibility of the host environment.

## Source-of-truth rule

Do not hand-edit generated copies as if they were canonical.

```text
skills/<name>/              canonical source
        ↓
adapters/openai/            selection + packaging
        ↓
.agents/skills/ or dist/    harness-facing copies
```

To change behavior, edit the canonical skill, run the normal DotSkills validation/evals,
then rebuild or reinstall through this adapter.

## Current scope

This adapter intentionally does not:

- publish to the public OpenAI plugin directory;
- create or register an MCP server;
- add credentials or secrets;
- invent harness permissions;
- bundle logos/screenshots required for public-directory submission;
- keep generated installs automatically synchronized after copy mode.

Those can be added as separate release/distribution capabilities without changing the
canonical skill packages.
