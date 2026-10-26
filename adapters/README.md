# Harness adapters

`skills/` is the canonical, harness-agnostic DotSkills source. Adapters translate that
source into installation/package layouts expected by particular agent harnesses.

Adapters must not become a second source of skill instructions. They should select,
copy/link, package, validate, or publish canonical skill directories.

## Available adapters

### OpenAI

See [`openai/README.md`](openai/README.md).

The OpenAI adapter currently supports:

- installing selected skills into a Codex-compatible repo-local
  `.agents/skills/<skill-name>/` layout;
- building a portable OpenAI plugin with root `plugin.json` + `skills/` for supported
  ChatGPT/Codex plugin workflows.

The default selector is the `methodology` category, which packages
`refine-skill` and its five specialist methodology skills.

## Distribution rule

Each directory under `../skills/` remains an independently distributable package.
Install the **entire directory**, preserving `SKILL.md`, `references/`, scripts, templates,
and other skill-local assets.

Do not assume that putting skills in Git, exposing an MCP server, or building a package
makes them automatically discoverable in every client. Discovery rules, permissions,
plugin availability, and publication requirements are harness-specific and may change.

## Planned adapters/capabilities

- Claude-specific installation/package adapter
- tested compatibility matrix with version constraints
- versioned distribution manifests and rollback support
- release-time plugin validation and public-directory packaging
- optional MCP skill discovery/export when appropriate
