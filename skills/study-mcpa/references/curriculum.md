# MCPA curriculum, source map, and learning menu

## Source of truth (reviewed 2026-10-30)

- [Linux Foundation MCPA exam / Domains & Competencies](https://training.linuxfoundation.org/certification/model-context-protocol-associate-mcpa/): the five domain weights below, competencies, online-proctored multiple-choice format and 90-minute duration.
- [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28): protocol-level reference currently named on the exam page.
- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture) and [MCP TypeScript SDK v2](https://ts.sdk.modelcontextprotocol.io/v2/): explanatory and implementation references. Prefer the specification for normative behavior.
- [2026-07-28 release notes](https://blog.modelcontextprotocol.io/posts/2026-07-28/): version changes, including stateless core, removed initialization handshake, `server/discover`, Multi Round-Trip Requests, updated authorization.
- [Skills Extension overview](https://modelcontextprotocol.io/extensions/skills/overview) and [TypeScript SDK skills](https://ts.sdk.modelcontextprotocol.io/v2/servers/skills): OPTIONAL project material, not a separate MCPA exam domain.

Check authoritative pages again if the exam revision changes. Don't extrapolate new exam items from extension news or older guides. Distinguish official objective, documented mechanism, lab choice, and hypothetical teaching example. The publicly stated exam format and durations are not a license to reproduce actual test content.

## Official domain map and selectable learning questions

Weights are official; IDs and questions are **our study organization**, not official exam item identifiers.

### F — MCP Fundamentals (16%)

- **F-01** — Why does MCP exist and what problems does it standardize?
- **F-02** — How do tools, resources, prompts, and JSON-RPC fit together?
- **F-03** — What does interoperability mean, and what does MCP not guarantee?

### A — Architecture & Components (14%)

- **A-01** — What are host, client, and server responsibilities and boundaries?
- **A-02** — What does a complete host → client → server request/response path look like?
- **A-03** — How do schemas, structured input/output and transports shape integration?

### I — Interactions & Execution (26%)

- **I-01** — What happens when a tool is discovered, selected, invoked, and returned?
- **I-02** — How do `tools/list`, `tools/call`, `resources/read`, and prompts differ?
- **I-03** — How should callers handle protocol errors, tool errors, invalid outputs, and retries?
- **I-04** — How do current discovery, caching, and Multi Round-Trip Requests work, and what changed from older versions?

### S — Security & Governance (24%)

- **S-01** — Where are the client/server/model/data trust boundaries?
- **S-02** — How do identity, permissions, user consent, authorization, and least privilege differ?
- **S-03** — What can go wrong with prompt injection, arbitrary tool execution, or token handling?
- **S-04** — How do logging, auditability, human approvals, and deny-by-default controls reduce risks?

### E — Use Cases & Ecosystem (20%)

- **E-01** — When choose MCP instead of an app-specific API integration?
- **E-02** — How do roles, adoption, portability, and ecosystem compatibility affect design?
- **E-03** — What does deploying and maintaining an MCP integration require?

Spend relatively more assessment/review time on I and S (50% combined), while retaining coverage for every domain.

## Five-week learning plan

| Week | Core focus | Daily study goals | Weekly checkpoint | Optional DotSkills lab |
| --- | --- | --- | --- | --- |
| 1 | F + A | Protocol purpose, roles, primitives, schemas, architecture diagrams | Explain a host/client/server flow without notes; 10–15 original questions | L-01 curated skills and architecture |
| 2 | I | Current request metadata, tools/resources/prompts, discovery, failure patterns, MRTR | Walk through success/error invocation; 15–20 questions | L-02 local read-only MCP server |
| 3 | S | Trust boundaries, authentication/authorization, consent, prompt injection, audit trails | Analyze 5 risk scenarios; 15–20 questions | L-03 local security tests |
| 4 | E + integration | Operational use cases, ecosystem portability, deployment design | Explain MCP versus ordinary APIs and client compatibility | L-04 optional Fly.io deployment |
| 5 | Mixed review | Correct weak concepts, teach-back, practice under self-managed time | 2 mixed-domain mock exams; record errors and explain mitigations | L-05 connect compatible MCP client |

Daily default: 5 min retrieval practice → 20 min targeted concept → 10 min questions → 5 min error log. Keep a lab as an **optional** separate 60–90-minute session. If there are gaps, extend the schedule instead of rushing to deploy.

## First dashboard response

Present:
1. **Snapshot:** exam/spec revision verified or verification unavailable, study progress known or not tracked.
2. **Domain weights** and compact week-by-week roadmap.
3. **Complete topic index** above, grouped F/A/I/S/E, plus `L-01`–`L-05` lab names.
4. **Mode choices:** Guided / Practice / Lab / Mock / Review.
5. **Recommended Day 1:** F-01 plus A-01, draw a simple architecture with no implementation; optionally take five questions.
6. **Single checkpoint:** ask what to choose. No worked answer or quiz begins until selection (unless explicitly asked to start).

## Domain source checks

- **F/A:** use normative core concepts/architecture/schema and structured examples, distinguishing hosts, client objects, server capabilities and extension capabilities.
- **I:** for 2026-07-28, do not teach the removed `initialize/initialized` exchange as the current core flow. Use the current request metadata and optional `server/discover`. Show protocol errors separately from tool-level errors; do not promise idempotency.
- **S:** distinguish authorization/consent from automatically safe behavior. Never assume an LLM prompt enforces permissions. Cite current MCP authorization and transport guidance.
- **E:** distinguish base MCP primitives from extensions, host integrations, SDK behavior and project deployment patterns. Client adoption must be verified for the relevant extension.

A topic may need a prerequisite refresher; surface it briefly but honor the learner's chosen ID.
