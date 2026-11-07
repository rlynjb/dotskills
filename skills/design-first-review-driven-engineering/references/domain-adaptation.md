# Domain adaptation — choose only relevant lenses

This methodology is **domain-agnostic**, not domain-blind. Use only the row(s) relevant to the actual request; verify organizational and official standards before declaring compliance. These prompts are examples, **not a taxonomy of independent skills or unconditional release rules**.

| Domain | Discovery/design emphasis | Contract and evaluation emphasis | Common operational risks |
| --- | --- | --- | --- |
| **Agent skill** | Skill purpose, discoverability, existing instruction/reference conventions and composition | Agent Skills `SKILL.md` format (when applicable), activation/stop conditions, input/output/permission boundaries, behavioral evals and host parity | Prompt-level restrictions mistaken for enforcement; tool names or delegation semantics differing by harness |
| **MCP/API tool or integration** | User intent, existing API/service behavior, authentication and data provenance | Tool descriptions, schemas, authorization, error codes, idempotency, contract/integration/misuse tests | Excessive privileges, schema drift, prompt injection via tool results, uncontrolled retries or writes |
| **Agent or multi-agent application** | Required autonomy, simpler workflow alternatives, role separation and orchestration | Decision authority, tool restrictions, handoff schemas, state, observable task success, trajectory/safety evals | Delegation laundering, untrusted context, silent failures, unverifiable worker execution |
| **Agent harness/runtime** | Execution model, context lifecycle, supported providers, isolation boundaries | Scheduling, tool adapters, state/receipt semantics, budgets, recovery, permission enforcement, deterministic routing, replay and fault tests | Credential leakage, broken isolation, nonrepeatability, tool/environment divergence |
| **Web/mobile/backend application** | User journey, existing code patterns, architecture, data model, UX/accessibility | API/data contracts, acceptance criteria, unit/integration/E2E, accessibility, performance and security tests | Regression, inconsistent state, migrations, operational and accessibility gaps |
| **Infrastructure or distributed system** | Topology, dependencies, capacity, existing change controls, SLOs | Configuration interfaces, rollout/rollback, observability, recovery objectives, load and fault-injection evidence | Outages, privilege escalation, downtime, data loss and cascading failure |
| **Data/ML pipeline** | Source ownership, quality/retention, training/inference boundaries | Data lineage, schema/feature contracts, quality/drift checks, reproducibility and model/metric evaluation | Leakage, biased or stale inputs, schema changes and irreproducible results |

## Portable engineering questions

- **Discover:** What already exists? What do we know from actual sources? What is still only assumed? Is a new component necessary?
- **Design:** What are the realistic options? What does the simplest adequate solution look like? What is the blast radius?
- **Contract:** Which party owns each decision? What is guaranteed? Which authority or permissions are enforced by real controls?
- **Implement:** Which exact state, files or services will change? Who authorizes that change?
- **Evaluate:** What would falsify the design? How will a reviewer verify the observable outcome, including failures?
- **Release:** Who approves, operates, monitors and rolls back the change?

## Optional specialist routing

For **agent-skill targets only**, suggest `audit-skill` for source-based skill review and `evaluate-skill` for governed skill behavioral evaluation. Do not invoke either just because this file mentions it. For non-skill domains use verified available tests, organization-approved systems or a reviewed manual evaluation plan. Framework-specific action support, safety and authority differ; cross-platform portability requires evidence rather than naming multiple runtimes.

The methodology is a *synthesis of engineering practices*, not a universal industry certification, specification or formal AAIF workflow standard.
