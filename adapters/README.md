# Harness adapters (planned)

This folder documents distribution boundaries; it does not yet ship installers.

Each directory under `../skills/` is intended to be an independently distributable package. Install **the entire directory**, preserving `SKILL.md` and its `references/`.

For Codex environments that support repo-local skills, a typical destination is `.agents/skills/<skill-name>/`. For Claude Code, install under the skills directory supported by your current installation. For ChatGPT Work, use its supported skill installation/upload mechanism if enabled. Always confirm current discovery rules and permissions for each harness.

Do **not** assume that putting skills in Git, or exposing an MCP server, makes them automatically discoverable in every client.

Potential future adapters:
- Codex/Claude/ChatGPT installation and update commands
- A tested compatibility matrix with version constraints and capabilities
- A versioned distribution manifest and rollback support
- A supported MCP skill discovery/export endpoint when appropriate
