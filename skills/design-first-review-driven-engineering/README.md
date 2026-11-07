# Design-First, Review-Driven Engineering

An **engineering methodology skill** for developing, changing and integrating *anything technical*: agent skills, MCP tools, agents, harnesses, applications, services, data systems and infrastructure.

**Core idea:** Discover → Design → Contract → Implement → Evaluate → Release, with human review at meaningful decision points. It is an adaptable engineering synthesis, **not** a formal AAIF standard or an automatic CI/deployment engine.

## When to use it

Use this as an overview-first **coordinator** whenever a task needs design deliberation, explicit contracts, measurable behavior or release readiness. It can start with existing systems or greenfield work. It can guide a small reversible change quickly or spend more effort on costly, security-sensitive, production work.

| Stage | Output |
| --- | --- |
| 1. Discover | Problem, evidence, existing architecture or greenfield assumptions, constraints |
| 2. Design | Options, trade-offs, proposed design and human decision |
| 3. Contract | Ownership, inputs/outputs, invariants, permissions, failure cases and test plan |
| 4. Implement | Approved small change, change evidence and deviations |
| 5. Evaluate | Expected vs observed outcomes, safety, regression evidence and limits |
| 6. Release | Human go/no-go, rollout/rollback, monitoring and ownership |

A failure can loop back to discovery, design or contracts. Determine acceptance criteria **before implementation**; establish a safe baseline **before changing** an existing system whenever feasible.

## Invocation examples

**A new MCP tool:**
```text
Use design-first-review-driven-engineering to guide a new MCP tool.
Start with the engineering overview and Stage 1. Help me review
alternatives and the API/security contract before proposing code.
```

**An existing agent harness:**
```text
Use design-first-review-driven-engineering on this agent harness refactor.
Inspect existing behavior and architecture before designing. Include
execution boundaries, tool permissions, failure recovery and regression
evidence. Pause at design/implementation gates.
```

**Two related agent skills:**
```text
Use design-first-review-driven-engineering to guide an integration of
Sprint Assessment and Refine Requirements. Use the existing skill
auditing/evaluation capabilities only if available and separately
approved. Keep current-state evidence separate from proposed integration.
```

**A small application change:**
```text
Use design-first-review-driven-engineering on this small feature.
Keep the process lightweight, reuse existing patterns, define acceptance
checks and ask me before writing changes.
```

## Composition and authority

This skill **coordinates engineering decisions**, not the implementation details of every domain. When auditing an actual agent skill, it may recommend [Audit Skill](../audit-skill/SKILL.md). For separately authorized skill behavior tests, it may recommend [Evaluate Skill](../evaluate-skill/SKILL.md). Mentioning a skill or an agent is **not an execution or tool permission**. For non-skill domains it should select appropriate tools/tests rather than assuming a skill-specific evaluator works everywhere.

Default behavior is planning and authorized read-only inspection. Before writes, risky tests, external actions or releases, a **fresh explicit approval** for the scope is required. Host/tool enforcement, not these instructions, determines what actions are technically allowed.

## Files

- [`SKILL.md`](SKILL.md) — entrypoint, review sequence, decision criteria, safety boundaries.
- [`references/lifecycle.md`](references/lifecycle.md) — detailed six-stage method and human gates.
- [`references/domain-adaptation.md`](references/domain-adaptation.md) — optional per-domain considerations.
- [`references/engineering-record.md`](references/engineering-record.md) — optional lightweight decision/evidence template.
- [`evals/evals.json`](evals/evals.json) — proposed scenario-based tests for this skill itself (**NOT RUN**).

**Current status:** documented methodology with static evaluation cases; not a verified behavioral orchestration engine. Do not infer portability or runtime execution from successful packaging.
