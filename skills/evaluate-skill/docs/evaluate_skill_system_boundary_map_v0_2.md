# Evaluate Skill — System Boundary Map v0.2

> **Historical:** The active canonical map is the
> [Docker-Only System Boundary Map v0.4](./evaluate_skill_system_boundary_map_v0_4.md).

**Status:** Offline control/evidence foundation implemented; live execution paths unverified and Blocked — Not Run.
**Scope:** Provider-native evaluation first; Docker only when independently verified native isolation is insufficient.

```mermaid
flowchart TD
  subgraph CONTROL["Trusted control plane"]
    A["Evaluate Skill<br/>Stages 0–11 + human checkpoints"]
    B["Coordinator<br/>Versioned case + capability needs"]
    C{"Policy assessment<br/>Native restrictions verified?"}
    D{"Docker fallback<br/>Verified and supported?"}
    X["BLOCKED — NOT RUN"]
    AP["Approved immutable run plan<br/>Provider + backend + scope"]
    E["Existing eval integration<br/>Promptfoo + Claude/Codex SDK adapter"]
  end

  subgraph EXEC["Restricted execution plane · choose ONE path"]
    N["NATIVE PATH<br/>Verified provider sandbox<br/>Fresh disposable fixture"]
    K["DOCKER PATH<br/>Verified restricted container<br/>Fresh disposable fixture"]
    M["Controlled mock MCP/API tools<br/>Only approved routes"]
  end

  subgraph EVID["Trusted evidence + grading plane"]
    H["Independent host evidence<br/>Tool visibility, policy checks, state/cleanup"]
    G["Deterministic assertions + LLM/agent rubrics<br/>Safety checked independently"]
    R["Versioned results<br/>Human review + regression decision"]
  end

  A --> B --> C
  C -->|"Yes"| AP
  C -->|"No"| D
  D -->|"Yes"| AP
  D -->|"No"| X
  AP --> E
  E -->|"Approved native route"| N
  E -->|"Approved Docker route"| K
  N -.->|"Only if case needs mocks"| M
  K -.->|"Only if case needs mocks"| M
  N --> H
  K --> H
  M --> H
  E --> H
  H --> G --> R --> A
```

**Reading the map:** Evaluate Skill and the coordinator define and approve an immutable plan. The existing Claude/Codex evaluation integration executes through **one approved isolation path**, either a verified native sandbox or a verified Docker fallback. Only explicitly approved mock tools are available. Independent host evidence and grading inform the human review. The v0.2 repository implements the offline contracts, policy, probes, evidence audit, bounded/mock authorization interfaces and Stage 3/9 checkpoint gate; those interfaces do not interpose on tools by themselves, and the repository does not implement a verified live native host or Docker backend. When neither route can enforce the required restrictions, the run is **blocked**.

For detailed requirements, security invariants, and component contracts, see [Execution Architecture v0.2](./evaluate_skill_execution_architecture_v0_2.md).
