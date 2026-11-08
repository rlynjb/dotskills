# DFRDE Stage 1 — Discover: evidence-first prefill contract

This is the **output contract** for a read-only `audit-skill` review when producing a DFRDE Stage 1 draft. It supplements the existing Audit Skill quality and standards review; it is **not** a separate mode, an integration runner, a behavioral evaluator, or permission to edit an engineering record.

**Canonical human-facing template:** `docs/dfrde/engineering-review-template.md`, section **1. Discover** (when that file is accessible). If the template is unavailable to the host, still produce an equivalent inline Stage 1 draft; do not invent file access.

## Why do this?

Use source inspection to answer technical questions **before** a team meeting. Humans should spend the meeting confirming intended behavior, owning decisions, resolving uncertainty, and defining success—not repeatedly reading facts already documented in the repository.

The audit can establish **what available source evidence says**. It cannot decide why the organization wants a change, whether a business problem is accepted, or whether a proposed architecture is approved.

## How to generate the handoff

1. Audit each available target independently first. Capture `SKILL.md`, relevant supporting files, tool/agent manifests, revision, existing tests and other inspected evidence. When 2+ targets exist, add a grounded overlap/ownership analysis.
2. Use evidence to prefill the generic Stage 1 questions below. For existing skills, give **as-is** answers first; do not inject unapproved to-be design as current behavior.
3. For each answer, include **source path:line and version**, evidence type (**DOCUMENTED INSTRUCTIONS**, **IMPLEMENTED CHECK**, **OBSERVED RESULT**, **INFERRED**, or **NOT VERIFIED**) and a *separate* question-action status:
   - **ANSWERED BY EVIDENCE:** directly supported by a cited inspected source. Written instructions establish *documented intent* only, not runtime behavior. Retain an explicit runtime limitation where relevant.
   - **NEEDS CONFIRMATION:** sources suggest intent, users, owners, desired outcome or standards, but a human must confirm. Do not mark a business goal or success threshold agreed solely from the code.
   - **OPEN DECISION:** multiple reasonable approaches or responsibility assignments require an accountable human decision. Carry forward to Stage 2, not a model-selected conclusion.
   - **NOT VERIFIED:** insufficient/missing/inaccessible evidence or no approved runtime test. State which source or authorized check would resolve it.
4. Create a compact **draft problem statement**, clearly labeled **PROPOSED — HUMAN CONFIRMATION REQUIRED**. Never equate the requested integration with the actual user/business problem.
5. Prefill known constraints, FR/NFRs, non-goals, source versions, risks, as-is diagram references, existing checks and proposed success measures **where supported**. Unknown does not mean absent.
6. Extract **only remaining questions for collaborators**; distinguish quick confirmation (yes/no/correction), ownership decisions (carry to Design), and evidence checks (assigned, possibly blocking). Avoid asking again about cited static facts unless source drift or intent requires validation.
7. Return a **Stage 1 deliverables/status** summary (draft vs pending) and a clear **HUMAN REVIEW REQUIRED** gate. No gate is approved because the audit produced a draft.

## Stage 1 question map — mandatory coverage

Use the same stable IDs as the canonical template. Every question receives an answer or a transparent gap.

| ID | Question to prefill from available evidence | Audit dimensions useful for evidence | Human boundary |
| --- | --- | --- | --- |
| **S1-Q01** | What actual problem affects which users and what outcome would help? | Q-01, project scope, prior approved requirement | Problem statement is a **proposal** unless confirmed |
| **S1-Q02** | What exists today and which sources/revisions were inspected? | Inventory, Q-03, Q-04, current-state Mermaid flow | No fabricated as-is runtime evidence |
| **S1-Q03** | Who uses/invokes the current skill(s), and who participates? | Q-01/Q-02, agent definitions | Actual roles and intent may need confirmation |
| **S1-Q04** | What inputs, outputs, tool/data dependencies and external integrations exist? | Q-03/Q-05/Q-06 | Distinguish available declared vs effective runtime |
| **S1-Q05** | Which decisions, contracts, handoffs and ownership boundaries exist or overlap? | Q-04/Q-05, relationship analysis (if multiple) | Candidate responsibility divisions are PROPOSED |
| **S1-Q06** | What safeguards, tests, CI, observed results and failure paths exist? | Q-07/Q-08/Q-09, evidence map | Tests not run are NOT RUN; unknown runtime is NOT VERIFIED |
| **S1-Q07** | What trust, permissions, privacy, standards and runtime constraints apply? | Q-06/Q-07/Q-10, spec and portability matrices | Written policy ≠ technical enforcement; standards adoption is a team choice |
| **S1-Q08** | What FR/NFR, non-goals and success metrics are agreed? | Source-backed requirements, Q-01/Q-09 | Proposed success criteria require stakeholder approval |
| **S1-Q09** | Could simpler existing mechanisms solve the problem? | Existing patterns, supported options | Log candidate choices as OPEN DECISION for Design |
| **S1-Q10** | What high-impact unknowns need more evidence, from whom? | Unverified claims, risk findings, gaps | Assign source/test request; don't claim tests were run |

When only one skill is accessible, S1-Q05 addresses its own interfaces and marks inter-skill relationships NOT APPLICABLE. If a second skill is named but inaccessible, mark it NOT ASSESSED and do not fabricate overlap. When greenfield work has no existing skill source, recommend starting general DFRDE Discovery instead of inventing an Audit Skill result.

## Minimal first-response handoff shape

After **Audit Skill — At a Glance** (profiles, workflow/evidence, standards and quality, cross-runtime, findings, proposed NOT RUN cases), include:

```markdown
## DFRDE Stage 1 — Discover (audit-prefilled draft)
**Target(s) and inspected versions:** ...
**Proposed problem statement — needs human confirmation:** ...
**What we know from sources:** ...
**What remains unknown or inferred:** ...
**Existing architecture:** Mermaid as-is diagrams above; runtime observations explicitly limited.

| Question | Prefilled answer / unknown | Evidence (path:line + type) | Status | Ask / next action |
| --- | --- | --- | --- | --- |
| S1-Q01 ... S1-Q10 | ... | ... | ... | ... |

**Known FR/NFR, non-goals, trust and environmental constraints:** ...
**Success criteria:** proposed unless previously approved.
**Top questions for teammate:** confirmations and unresolved choices only.
**Evidence backlog:** missing runtime proof, owner and safe verification method.
**Stage 1 deliverables:** draft inventory, questions and problem; approval pending.
**Stage 1 gate:** HUMAN REVIEW REQUIRED. Stop before Design/implementation.
```

Keep cells short on the first pass; offer a deep dive by `S1-Qxx`, `F-xx` or domain. The handoff is **copy-ready text**, not automatically saved into a public repository, workplace document, or canonical record.

## Safety and failure handling

- Audit Skill remains **read-only**. Do not run target skills, external integrations, shell tools, agent workers or behavioral evals merely to complete a missing Stage 1 answer.
- Lack of source access or test execution is **NOT VERIFIED**, not a reason to invent facts, pretend a tool enforced authorization, or mark a question answered.
- Reports are drafts for human review; direct organizational decisions, approved architecture/contracts, implementation, and evaluation belong to subsequent DFRDE stages.
- Keep company-private material in approved storage. Use redacted content and access-controlled evidence references where necessary.
