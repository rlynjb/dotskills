# Product-to-Sprint: Reference Engineering Workflow

## Purpose

This diagram describes how four Agent Arcade skills may support work from product framing through sprint selection. The six phases represent **responsibilities and handoffs**, not a mandatory step-by-step execution script. Teams may tailor the sequence to a ticket's scope and available evidence, while keeping ownership, decision records, and human authorization clear.

## Engineering workflow — six phases

```mermaid
flowchart TD
    subgraph P1["PHASE 1 — PRODUCT FRAMING"]
        A["SKILL: PRD Development<br/>Define goals, scope, and success measures<br/>Output: Product context / PRD"]
    end

    subgraph P2["PHASE 2 — REQUIREMENTS REFINEMENT"]
        B["SKILL: Refine Requirements<br/>Clarify requirements, evidence, and open questions<br/>Output: Requirements brief"]
    end

    subgraph P3["PHASE 3 — TECHNICAL READINESS"]
        C["ACTIVITY: Technical Design — as needed<br/>Explore approach, contracts, risks, and decisions<br/>Human owners confirm material decisions"]
    end

    subgraph P4["PHASE 4 — DELIVERY PLANNING"]
        D["SKILL: Jira Ticket Decomposition<br/>Organize stories, tasks, and acceptance criteria<br/>Output: Ticket drafts and open decisions"]
    end

    subgraph P5["PHASE 5 — GOVERNANCE & REVIEW"]
        E["HUMAN APPROVAL REQUIRED<br/>Review and authorize ticket publication"]
    end

    subgraph P6["PHASE 6 — SPRINT PLANNING"]
        F["SKILL: Sprint Assessment<br/>Assess estimates, dependencies, and readiness"]
        G["HUMAN DECISION: Sprint Selection<br/>Confirm priorities against team capacity"]
        F --> G
    end

    A -->|"Product context"| B
    B -->|"Broader technical context needed"| C
    B -->|"Requirements sufficiently defined"| D
    C -->|"Technical findings, where applicable"| D
    D -->|"Ticket drafts for review"| E
    E -->|"Authorized tickets"| F

    classDef skill fill:#dbeafe,stroke:#4478b5,color:#16385d
    classDef activity fill:#fef3c7,stroke:#b78b34,color:#594316
    classDef human fill:#dcfce7,stroke:#38865b,color:#154b30
    class A,B,D,F skill
    class C activity
    class E,G human
```

**Legend:** Blue = agent skill; yellow = collaborative activity; green = human approval or decision; solid arrows = common handoffs; the branch around Technical Design = requirements-only shortcut when appropriate.

## Common feedback paths — illustrative, not exhaustive

```mermaid
flowchart LR
    subgraph FROM["FINDING / SOURCE"]
        direction TB
        A["Phase 4: Delivery Planning<br/>Unresolved technical choice"]
        B["Phase 5: Governance & Review<br/>Ticket revisions required"]
        C["Phase 6: Sprint Planning<br/>Unclear requirements"]
        D["Phase 6: Sprint Planning<br/>Missing or changed contract"]
        E["Phase 6: Sprint Planning<br/>Oversized or poorly divided tickets"]
    end
    subgraph TO["REVISIT RESPONSIBLE PHASE"]
        direction TB
        P2["Phase 2<br/>Requirements Refinement"]
        P3["Phase 3<br/>Technical Readiness"]
        P4["Phase 4<br/>Delivery Planning"]
    end
    A -.-> P3
    B -.-> P4
    C -.-> P2
    D -.-> P3
    E -.-> P4
    classDef finding fill:#fef3c7,stroke:#b78b34,color:#594316
    classDef phase fill:#dbeafe,stroke:#4478b5,color:#16385d
    class A,B,C,D,E finding
    class P2,P3,P4 phase
```

**Legend:** Yellow = a finding that may require rework; blue = a phase that may own its resolution; dashed arrows = suggested feedback routes, not automatic dispatch rules.

## Why this is a reference workflow, not a rigid script

Different Jira tickets need different levels of refinement and technical design. Requiring every decision and feedback condition to be encoded in the diagram would create unnecessary coupling and imply that the team has agreed to exhaustive routing rules. Instead, the diagram establishes stable **responsibilities, expected handoffs, and human authorization boundaries**, leaving each phase free to adapt its methods, evidence gathering, and depth of analysis.

## Design decisions

- **Six phases, four skills.** Phases describe responsibilities; not every phase needs a standalone skill.
- **Technical Design is conditional.** Requirements can move directly to ticket decomposition when deeper design is not needed.
- **Feedback is normal.** Work can revisit the phase best placed to resolve a gap. The shown routes are examples, not a complete decision tree.
- **Human control stays explicit.** Ticket publication requires authorization, and sprint selection is a team decision. Material technical decisions are confirmed with their owners as appropriate.
- **Contracts remain important.** Each skill should identify its responsibility, the information it needs, and the findings or artifacts it provides. The detailed execution rules belong in the skill instructions and associated contracts, not in this high-level diagram.

**Implementation note:** This is a proposed reference presentation based on the existing Agent Arcade product-to-sprint diagram. It does not establish that every handoff or feedback route has already been implemented or evaluated in Codex. Changes to published tickets should pass through the applicable review and authorization process again.

## Short team presentation description

> This is a reference workflow, not a fixed execution script. We use six phases to clarify who owns each type of work, four existing agent skills to support the process, and explicit human checkpoints for publishing and sprint selection. Teams can skip unnecessary technical design and revisit earlier phases when new information appears. The goal is flexibility within clear responsibilities and boundaries.
