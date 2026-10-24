# DotSkills architecture

```text
Claude Code / Codex / ChatGPT Work / other supported harness
            |  install or discover compatible skills
            v
        DotSkills
    SKILL.md + references + catalog + source-lock
            |  optional future MCP integration
            v
    Your future MCP platform
            |
            +---- Buffr tools -> Buffr runtime (engine, contracts, state)
            +---- Other services and tools
```

## Ownership boundaries

- **DotSkills:** canonical packaged instructions, reference materials, provenance, static quality gates, and future skill evals.
- **Harness:** model interactions, local tool access, context, execution permissions, confirmations, and operating environment.
- **MCP platform (future):** discovery and standardized access to tools/resources and, where supported, skill metadata. No MCP server is implemented in this repository.
- **Buffr:** executable evidence-to-decision modules, validated contracts, deterministic workflow transitions, durable state, traces, and human approval gates. A skill may *call* Buffr using an authorized integration, but cannot replace its work engine.
- **Evals:** behavioral tests against real tools and models once configured; current CI only checks repository structure and exact reference imports.

A canonical source library does not guarantee that each harness auto-discovers skills or supports identical tools. Validate distribution and execution per environment.
