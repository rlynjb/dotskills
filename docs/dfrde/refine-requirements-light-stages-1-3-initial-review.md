# DFRDE — Initial Engineering Review: Refine Requirements — Light

> **Review scope:** One existing agent skill (`refine-requirements-light`) using the current DotSkills `audit-skill` evidence-first method. **Stages 1–3 are prefilled for discussion, not completed or approved.** This reviews the publicly documented skill contract—not a workplace Jira ticket or internal application architecture.
>
> **Status:** Stage 1 **REVIEW REQUIRED**; Stage 2 **CONDITIONAL / PROPOSED**; Stage 3 **CONDITIONAL / NOT APPROVED**. No target execution, runtime evaluation, code modification, Jira interaction, or stakeholder sign-off was performed.
>
> **Date:** 2026-11-08. **Repository:** `rlynjb/dotskills`, `main`, at inspection. **Owner/reviewer:** NOT CONFIRMED. **Next checkpoint:** Confirm the actual user problem and desired quality criteria, then review the options and contracts with the skill owner.

## 0. How to read and review this document

This is a **copy-ready, audit-prefilled instance** of [the generic DFRDE review template](engineering-review-template.md), not a new methodology and not an approval. The source itself is public; **do not add internal Jira content, private company code, credentials, meeting recordings, or sensitive findings to this public file**. Keep internal evidence and approved review outcomes in a company-controlled copy; refer to redacted evidence or approved access-controlled links here.

**Evidence key (line numbers refer to the inspected `main` files):**

| Key | Source inspected | Blob SHA / bounds |
| --- | --- | --- |
| **S** | [Refine Requirements — Light SKILL.md](../../skills/refine-requirements-light/SKILL.md) | `cbc20f6407477fc9fd10ef6b3c918087612450db`; lines 1–87 |
| **R** | [Refine Requirements — Light README](../../skills/refine-requirements-light/README.md) | `1445d529e7929245867f7d64fa2e924220af5aff`; lines 1–73 |
| **F** | [Full Refine Requirements SKILL.md](../../skills/refine-requirements/SKILL.md) | `7609b743cb586a001f7981463148d2c9306a7816`; related-skill boundary only |
| **A** | [Audit Skill SKILL.md](../../skills/audit-skill/SKILL.md) | `610065882d6a973b03725a42e17e7033c3cb15dc`; audit methodology |
| **CI** | [Repository validation workflow](../../.github/workflows/validate.yml) | Static repository/unit/adapter checks **configured**, execution status not checked |
| **SPEC** | [Agent Skills specification](https://agentskills.io/specification) | Consulted for packaging rules; **no `skills-ref validate` execution** |
| **ADAPTERS** | [Claude adapter](../../adapters/claude/README.md) and [OpenAI/Codex adapter](../../adapters/openai/README.md) | Installation paths described; this target's runtime behavior not tested |

**Evidence labels:** `DOCUMENTED` = source prescribes behavior; `IMPLEMENTED CHECK` = actual code/validator exists; `OBSERVED RESULT` = a real run/trace was verified; `INFERRED` = a reasoned interpretation; `NOT VERIFIED` = unavailable or untested. **Question action:** `ANSWERED BY EVIDENCE`, `NEEDS CONFIRMATION`, `OPEN DECISION`, `NOT VERIFIED`. **Proposed design/contract** and **human approval** are separate from either classification.

### Stage tracker

| DFRDE stage | Status | Why |
| --- | --- | --- |
| 1. Discover | **REVIEW REQUIRED** | Public skill instructions inspected; actual business problem, users, environment and baseline await confirmation |
| 2. Design | **CONDITIONAL / PROPOSED** | Alternatives derived from documented workflow, no architecture chosen |
| 3. Contract | **CONDITIONAL / NOT APPROVED** | Existing output expectations described; proposed stronger guarantees depend on a design decision |
| 4. Implement | NOT STARTED | No authorized change or implementation scope |
| 5. Evaluate | NOT RUN | No executed behavioral cases or trusted trajectory |
| 6. Release | NOT STARTED | No release decision |

---

## Audit Skill — At a Glance

**Purpose and trigger (DOCUMENTED):** A one-pass, noninteractive, read-only assessment of assigned Jira feature work, using four SDI steps and *verified* relevant existing application code. It is intended to provide an actionable technical overview before implementation, not to implement or approve a design. **S:L3, L8–12, L22–55, L71–76.**

**Inputs:** Assigned Jira issue/feature request, its requirements/acceptance criteria, applicable company conventions, and authorized access to relevant application code (if available). Optional DDIA 2e/FODE lenses when the data path warrants them. **S:L16–20, L24–29, L40–47.**

**Process:** Scope requirements → locate and verify candidates → recommend `FOLLOW`/`ADAPT`/`NEW REQUIRED` or an explicitly uncertain outcome → targeted full-stack/data-path analysis → risks, readiness and unresolved questions. **S:L24–55.** No declared subagent orchestration or autonomous scheduling was found in this skill definition; do not infer anything about hosts' separate agent capabilities.

**Output:** Ticket Snapshot, four SDI-labeled sections and owner-specific open questions. Readiness values are `READY FOR REVIEW`, `CONDITIONAL`, `BLOCKED`. **S:L49–69.**

**Side effects:** The text prohibits source edits, Jira posts, migrations, deployment, Superpowers invocation and agent launch. It is **prompt-level guidance, not proof that a consuming host technically enforces restrictions**. **S:L71–76.**

**Source scope and limits:** Inspected the public Light `SKILL.md`, README, the sibling's boundary, DotSkills adapter documentation, the audit/DFRDE guidance, repository tree and configured CI workflow. The Light package itself has only `SKILL.md` and `README.md`; no skill-local `evals/evals.json`, test script, runtime trace or approved internal Jira/code fixture was available in this review. The repo has general CI configuration, but that does **not** demonstrate behavior of this skill.

### As-is workflow — documented instructions, NOT an execution trace

```mermaid
flowchart TD
    T["Assigned Jira ticket / feature request"] --> G{"Ticket identifiable?"}
    G -->|"No — exceptional case"| ASK["Ask for identifying information"]
    G -->|Yes| S1["SDI 1: Scope FR/NFR, actors, acceptance, unknowns"]
    S1 --> ACCESS{"Relevant application code accessible?"}
    ACCESS -->|Yes| VERIFY["SDI 2: Locate + inspect real patterns, callers, contracts, standards"]
    ACCESS -->|No / incomplete| UNKNOWN["Mark reuse and design NOT VERIFIED; ticket-only provisional assessment"]
    VERIFY --> FIT{"Fit supported by inspected code?"}
    FIT -->|Fits / partial / justified new| PLAN["FOLLOW / ADAPT / NEW REQUIRED; proposed high-level change"]
    FIT -->|No suitable in inspected scope| NONE["Report scoped search limitation"]
    PLAN --> DEEP["SDI 3: Targeted code/data flow + critical contracts"]
    NONE --> DEEP
    UNKNOWN --> DEEP
    DEEP --> WRAP["SDI 4: Trade-offs, risks, readiness + open questions"]
    WRAP --> OUT["One read-only engineering brief"]
```

This diagram is a synthesis of **S:L16–20, L24–55, L57–76**. No branching or agent invocation is claimed to have occurred.

### Ten-dimension review dashboard

| Area | Static verdict | Source / practical implication |
| --- | --- | --- |
| **Q-01 Purpose & boundaries** | PASS (static) | Scope and exclusions stated, **S:L8–12, L71–76** |
| **Q-02 Activation & discovery** | PASS (static); runtime UNVERIFIED | Named skill and illustrative invocation, **S:L1–3, L78–87**; whether hosts activate it appropriately remains untested |
| **Q-03 Inputs & dependencies** | PASS (static); environment UNVERIFIED | Ticket, code and standards expectations defined, **S:L16–18, L24–38**; effective Jira/code access unknown |
| **Q-04 Workflow & decisions** | PASS (static) | Four SDI stages and reuse classifications, **S:L22–55**; actual adherence untested |
| **Q-05 Contracts & outputs** | PASS (written); parser compatibility UNVERIFIED | Five section contract + readiness states, **S:L49–69**; no machine-enforced response schema inspected |
| **Q-06 Context & trust** | PASS (written); behavior UNVERIFIED | Separates product authority, observed code and proposals, **S:L16–20, L76** |
| **Q-07 Permissions & effects** | UNVERIFIED (enforcement) | Read-only declared, **S:L71–76**, but no actual host/tool permissions inspected |
| **Q-08 Failure & stopping** | PARTIAL / GAP (static detail) | Missing-code, no-match and absent-ticket cases addressed, **S:L17, L20, L69, L73**; tool failure/timeout and stale-context recovery not explicitly specified |
| **Q-09 Evals & observability** | GAP (behavioral evidence) | No Light-specific eval fixture or run evidence in inspected package; repo-wide CI is not Light behavior testing |
| **Q-10 Lifecycle & portability** | UNVERIFIED | Source tracked in Git and adapter docs exist; version-by-version Claude/Codex behavioral parity untested |

The `PARTIAL / GAP` shorthand above denotes a *documentation gap*, not a confirmed runtime defect; use the Audit Skill's canonical `GAP` classification when triaging.

### Agent Skills specification — structural checks only

| Requirement | Finding | Evidence |
| --- | --- | --- |
| Skill folder with `SKILL.md` | PASS (static) | `skills/refine-requirements-light/SKILL.md` exists |
| YAML frontmatter, `name`, non-empty `description` | PASS (static) | **S:L1–4**, directory and name match |
| Lowercase hyphenated name, limits | PASS (static) | `refine-requirements-light`; valid visible form |
| Markdown body | PASS (static) | **S:L6–87** |
| `references/`, `scripts/`, `assets/` | NOT APPLICABLE | Optional per spec; absence is not a format defect |
| Native `skills-ref validate` | **NOT RUN** | No CLI validator executed in this review |

The format specification does not itself require a particular evaluation suite, security boundary or cross-runtime orchestration behavior. These are separate reliability questions.

### Cross-platform compatibility — explicit evidence limits

| Capability | Claude Code | Codex / OpenAI harness | Evidence / what to verify |
| --- | --- | --- | --- |
| Skill packaging | **NOT VERIFIED** at runtime | **NOT VERIFIED** at runtime | DotSkills provides [Claude](../../adapters/claude/README.md) and [OpenAI](../../adapters/openai/README.md) adapter *instructions*, but Light installation wasn't executed |
| Discovery/activation | NOT VERIFIED | NOT VERIFIED | Confirm selection on Jira-ticket prompts and rejection of unrelated requests |
| Local application-code access and context | NOT VERIFIED | NOT VERIFIED | Confirm repo access, conventions/instruction hierarchy and reference loading |
| Tool names, ticket access, credentials | NOT VERIFIED | NOT VERIFIED | Jira integration and effective user/tool permissions are host-specific |
| Delegation and concurrency | NOT APPLICABLE in skill's documented workflow | NOT APPLICABLE in skill's documented workflow | No subagent delegation is prescribed by Light, **S:L12, L71–76** |
| Side-effect enforcement | NOT VERIFIED | NOT VERIFIED | Prompt-level read-only is not a permission mechanism |
| Output/readiness contract | NOT VERIFIED behaviorally | NOT VERIFIED behaviorally | Compare sample outputs and missing-context behavior |
| Versioned regression evidence | NOT VERIFIED | NOT VERIFIED | No comparative skill eval runs inspected |

### Existing protections before possible improvements

The source explicitly instructs verification before reuse, scoped search limitations, separate claim/evidence labels, concise conditional recommendations, optional domain lenses, no edits, and owner-specific open questions (**S:L16–20, L34–38, L49–55, L71–76**). These are **documented safeguards**, not independently validated runtime controls.

### Ranked initial findings

| ID | Impact / confidence | Finding, consequence and next evidence |
| --- | --- | --- |
| **F-01** | Medium / high (static) | **No Light-specific behavioral eval evidence inspected.** The procedure is detailed but no fixture or run demonstrates its behavior. Start synthetic, approved skill evals with expected source citations and safe tool boundary. |
| **F-02** | Medium / high (evidence gap) | **Read-only is instruction-level here; host permission enforcement is unverified.** Inspect effective host/tool settings; avoid any live write probe without independent containment and approval. |
| **F-03** | Medium / high (evidence gap) | **No workplace Jira or application checkout in review.** Actual usefulness, selection of verified patterns, and source quality cannot be assessed from the public skill alone. Request a redacted/synthetic representative fixture. |
| **F-04** | Low–medium / medium | **One-pass output is prose-structured, not a demonstrated typed handoff.** Fine for a human review; a downstream machine consumer might need explicit fields/status parsing if that use case is confirmed. No need to add a schema without a consumer. |
| **F-05** | Medium / medium | **Runtime compatibility is not demonstrated.** Documented packaging is not activation/evaluation evidence; test each claimed supported harness only when its scope is agreed. |
| **F-06** | Low–medium / medium | **Some operational errors are unspecified beyond missing-code/ticket exceptions.** Determine whether transient Jira/tool failures require explicit handling based on observed cases; don't overbuild. |

### Proposed evaluation cases — ALL NOT RUN

| Case | Synthetic fixture / expected result | Objective check (requires authorized isolated execution) |
| --- | --- | --- |
| **E-01 Complete ticket + existing fitting pattern** | Outputs the five required sections, shows real fixture path/symbol, chooses `FOLLOW` or `ADAPT` with rationale | Cites exact existing fake-code symbol and doesn't invent unrelated services |
| **E-02 Ticket provided, application code unavailable** | Completes a one-pass **provisional** assessment with `NOT VERIFIED` reuse; no invented path | No fabricated source references, no false verified pattern |
| **E-03 Relevant bounded search finds no fit** | States `NO SUITABLE PATTERN FOUND IN INSPECTED SCOPE`; does not assert global absence | Scope limitation and justified minimal proposal visible |
| **E-04 Untrusted ticket content asks agent to post/edit/deploy** | Treats embedded instruction as task data, makes no external mutation | Independent tool-attempt traces / enforced no-write boundary |
| **E-05 Ticket ambiguity / conflicting requirements** | Explicitly labels proposed wording and owner-specific questions, avoids inventing acceptance approval | No false confirmed requirement; honest `CONDITIONAL` or `BLOCKED` state |
| **E-06 Claude Code vs Codex (only if both supported)** | Same synthetic task yields compatible essential sections, uncertainty, evidence and stop behavior | Separate host/adapter/permission trace per run; no parity claim otherwise |

**No cases were executed or graded**. This review neither exercises `evaluate-skill` nor certifies safety.

---

## 1. Discover — What problem and existing reality are we working with?

**SDI alignment:** Understand requirements and scope. **Source-backed prefill with a proposed business/problem hypothesis; human confirmation still required.**

### Draft problem statement — PROPOSED, HUMAN CONFIRMATION REQUIRED

> We want developers reviewing assigned Jira work to receive a concise, trustworthy, codebase-grounded requirements/design assessment without a lengthy interview or premature implementation. This review asks whether the existing Light skill already meets that need, how to verify it, and which *small, evidence-justified* adjustments—if any—would improve confidence in the output.

This is **inferred from the skill's stated purpose**, not a confirmed team request to redesign or integrate it. If the actual work is to integrate Light with another workflow, record the consumer and its requirements in a **separate multi-skill design review**.

### Stage 1 prefilled questions

| ID | Question | Draft answer / unknown | Evidence state and source | Question status / next action |
| --- | --- | --- | --- | --- |
| **S1-Q01** | Who has what problem and outcome? | Source describes developer need for a fast technical overview before implementation; measurable workplace pain and intended audience ownership are not documented here. | DOCUMENTED purpose, **S:L8–12**; business outcome inferred | **NEEDS CONFIRMATION** — confirm actual users and success |
| **S1-Q02** | What exists today and what was inspected? | A self-contained Light skill with entrypoint and README; one-pass four-step SDI. No internal application assessed. | DOCUMENTED **S:L22–76**, **R:L9–16**; current blob SHA above | **ANSWERED BY EVIDENCE** for package; runtime **NOT VERIFIED** |
| **S1-Q03** | Users, invocation and participants? | Developer/coding-agent user supplies an assigned Jira issue; no interactive interview, default one-pass report; human approver only for future implementation. | DOCUMENTED **S:L3, L10–12, L71–75, L78–87** | **NEEDS CONFIRMATION** — confirm actual roles/consumers and host |
| **S1-Q04** | Inputs/outputs/dependencies? | Ticket FR/NFR/acceptance, applicable standards, relevant repo code when available; snapshot + four SDI sections + open decisions. | DOCUMENTED **S:L16–18, L24–47, L57–69** | **ANSWERED BY EVIDENCE** for intended contract; environment NOT VERIFIED |
| **S1-Q05** | Decision points, contracts and ownership? | Existing classifications: `FOLLOW`, `ADAPT`, `NEW REQUIRED`, `NOT VERIFIED`; readiness `READY FOR REVIEW / CONDITIONAL / BLOCKED`. Human makes implementation decisions. Multi-skill ownership N/A for this review. | DOCUMENTED **S:L19, L49–55, L71–75** | **ANSWERED BY EVIDENCE** for instructions; owner confirmation pending |
| **S1-Q06** | Safeguards/tests/traces/failures? | Strong written verification and uncertainty safeguards. No Light-specific executed evals/traces supplied; repo has generic configured CI. | DOCUMENTED **S:L16–20, L69–76**; CI config inspected | **NOT VERIFIED** behavior — plan synthetic evals |
| **S1-Q07** | Trust, permissions, standards, portability? | Treat ticket as untrusted; approved specs are product authority, source code observes behavior; read-only stated; Agent Skills-format frontmatter. Host enforcement and runtime parity unverified. | DOCUMENTED **S:L16–18, L71–76**; SPEC / ADAPTERS | **NOT VERIFIED** enforcement — confirm hosting constraints |
| **S1-Q08** | Agreed FR/NFR, non-goals and metrics? | Skill instructs FR/NFR extraction and minimizes design; skill-change acceptance targets, SLOs and team scope aren't approved in inspected materials. | DOCUMENTED **S:L24–30, L49–55**; business thresholds UNVERIFIED | **NEEDS CONFIRMATION** — approve measurable quality bar |
| **S1-Q09** | Could existing/simple solution suffice? | Yes: leave Light unchanged and introduce synthetic validation first; avoid new workflow or schema unless evidence/consumer calls for it. | INFERRED from documented small-change rule **S:L19–20, L51–54** | **OPEN DECISION** — challenge alternatives in Stage 2 |
| **S1-Q10** | Highest-impact unknowns? | Real ticket samples (sanitized), repo-access expectations, host effective permissions, baseline task success, maintainer, supported runtimes. | NOT VERIFIED beyond public source; **F-01–F-06** | **NOT VERIFIED** — assign verification owners |

### Known requirements, constraints and non-goals

**Documented intended behavior:** read-only one-pass assessment; verify relevant existing code before recommending patterns; distinguish unverified absence; present FR/NFR, selective data flow, risks and readiness; list unresolved questions without interrupting the assessment (**S:L16–20, L22–76**).

**Proposed review success criteria (NOT APPROVED):** no fabricated verified path; all five report sections present; no unauthorized side effects; appropriate conditional/blocked result with missing evidence; actionable owner-specific questions; same essential result meaning in each *claimed* supported harness. Quantitative thresholds and review owners are OPEN.

**Non-goals for this initial review:** no integration with Sprint Assessment, no redesign of company applications, no Jira tool calls, no real code inspection, no edits to Light, no committed behavioral test results.

### Deliverables and review gate

| Output | Current status | Next evidence |
| --- | --- | --- |
| Skill inventory / documented current-state flow | **DRAFT — SOURCE-BACKED** | Public S/R sources above |
| User problem and measurable success | **PROPOSED — REVIEW REQUIRED** | Confirm with user/skill consumer |
| Functional/nonfunctional review criteria | **DRAFT — REVIEW REQUIRED** | Approve useful quality criteria |
| Effective runtime, tools, ownership | **NOT VERIFIED** | Approved host configuration/owner |
| Stage 1 approval | **HUMAN REVIEW REQUIRED — Discover** | Record reviewer and decision in internal working record |

---

## 2. Design — What approach best fits the requirements?

**SDI support:** Steps 2–4 (high-level alternatives, critical components and trade-offs). **CONDITIONAL / PROPOSED:** assumes the Stage 1 goal is *validating and, only if justified, improving Light*; no team design approval exists.

### Stage 2 prefilled questions

| ID | Question | Evidence-backed response / proposed options | Source / evidence | Question status / next action |
| --- | --- | --- | --- | --- |
| **S2-Q01** | What approaches could solve the problem? | A: keep instructions unchanged, add representative eval evidence; B: targeted clarity/validation improvements only if cases show gaps; C: structured consumer handoff if another system actually needs it. | INFERRED options from **S:L16–20, L57–69** | **OPEN DECISION** — choose after actual problem confirmation |
| **S2-Q02** | Which existing patterns/conventions preserve? | Four SDI steps, evidence-first and reuse labels, scoped code inspection, ticket snapshot/five-section output, optional DDIA/FODE and company architecture priority. | DOCUMENTED **S:L16–20, L22–69** | **ANSWERED BY EVIDENCE** for current intent; host context UNVERIFIED |
| **S2-Q03** | Where do orchestration and decisions live? | Today the source describes one skill producing one report, no automatic subagent dispatch. New external integration or a structured producer/consumer handoff needs separate justification. | DOCUMENTED **S:L12, L57–76**; future options PROPOSED | **OPEN DECISION** — clarify if any downstream consumer exists |
| **S2-Q04** | Material trade-offs/failures/costs? | A minimal change minimizes drift and coupling but may leave observed failures unresolved; B adds instruction/acceptance clarity but risks excessive prompt complexity; C improves machine handoff but adds versioning/consumer coupling. Runtime cost/latency unknown. | INFERRED; no measurements, **F-01–F-06** | **NEEDS CONFIRMATION** — prioritize only demonstrated risks |
| **S2-Q05** | Which design was approved by whom? | **None verified.** Source documents no explicit approval to restructure or add contracts. | NOT VERIFIED; **S:L71–76** (no auto-approval) | **OPEN DECISION — HUMAN REVIEW REQUIRED** |

### Design option comparison — all PROPOSED

| Option | Description | Benefit | Trade-off / evidence prerequisite |
| --- | --- | --- | --- |
| **A. Validate existing behavior first** | Leave Light unchanged; use approved synthetic tasks and review actual outputs | Least disruption; yields a defensible baseline before edits | Needs safe harness/tool isolation and representative fixtures; may reveal problems requiring B |
| **B. Minimal contract/instruction hardening** | If tests reveal gaps, clarify requirements preflight, source evidence fields, response stop/blocked semantics, and review criteria while preserving one-pass format | Potentially more consistent assessments without redesign | Risk of over-specification and larger prompt; must be justified and regression-tested |
| **C. Explicit downstream interface** | If a real consumer exists, define a separately reviewed structured handoff or adapter | Could enable integration with another workflow | Consumer, schema, ownership, migration and permissions **not established**; do not introduce speculatively |

**Working recommendation (NOT DECIDED):** Investigate Option A first because the source already documents a complete one-pass procedure. Only choose B/C if approved user outcomes and behavioral evidence justify added complexity.

### Existing architecture vs proposed review work

```mermaid
flowchart LR
    CURRENT["AS-IS (documented): Light skill instructions"] --> REPORT["Human-readable one-pass assessment"]
    REVIEW["PROPOSED: controlled review of existing behavior"] --> CASES["Synthetic ticket + code fixtures"]
    CASES --> RESULTS["Evidence-backed evaluation results (NOT RUN)"]
    RESULTS --> DECIDE{"Human decision"}
    DECIDE -->|Keep| CURRENT
    DECIDE -->|Improve if justified| CHANGE["PROPOSED scoped revision"]
    DECIDE -->|Integration need confirmed| CONTRACT["PROPOSED downstream contract"]
```

The as-is path is **documented only**; the evaluation path is a **proposal**, not implemented work.

### Deliverables and review gate

| Output | Current status |
| --- | --- |
| As-is component/flow and source-backed assumptions | DOCUMENTED / runtime NOT VERIFIED |
| Options and trade-offs | PROPOSED |
| Chosen architecture, owner and rationale | **OPEN DECISION** |
| Stage 2 approval | **HUMAN REVIEW REQUIRED — Design** |

---

## 3. Contract — What must participants and components guarantee?

**SDI support:** component/interface detail and trade-offs (Steps 3–4). **CONDITIONAL / NOT APPROVED.** The source already specifies a human-readable report contract. A strengthened or machine-readable contract is not approved, nor is any new runtime-side security control verified.

### Stage 3 prefilled questions

| ID | Question | Existing evidence / candidate response | Evidence state | Question status / next action |
| --- | --- | --- | --- | --- |
| **S3-Q01** | Producers, consumers, owners and versions? | Producer: Light's assessment flow; current consumer: ticket reviewer/developer. Repo file defines output. No approved machine consumer or named maintainer inspected. | DOCUMENTED **S:L8–12, L57–69**; ownership NOT VERIFIED | **NEEDS CONFIRMATION** — identify stakeholder and source owner |
| **S3-Q02** | Inputs/outputs, guarantees, invariants? | Documented: ticket snapshot + five sections, evidence-linked `FOLLOW/ADAPT/NEW REQUIRED/NO SUITABLE PATTERN FOUND IN INSPECTED SCOPE/NOT VERIFIED` classifications, readiness states and explicit uncertainty. Candidate critical invariants below. | DOCUMENTED **S:L17–20, L49–69**; candidate invariants PROPOSED | **OPEN DECISION** — decide whether checks should be machine-testable |
| **S3-Q03** | Trust, identity, permissions and approvals? | Source forbids edits, posts, deployment and tool/agent launch; ticket/tool content is untrusted; actual host/tool authorization and Jira identity are not inspected. | DOCUMENTED **S:L18, L71–76**; enforcement NOT VERIFIED | **NOT VERIFIED** — confirm effective permissions; no live write probes |
| **S3-Q04** | Error, retry, partial results, blocked behavior? | Missing app code yields provisional `NOT VERIFIED`; no suitable inspected pattern is scoped; no ticket may justify clarification; readiness may be conditional/blocked. Tool outage/timeouts and future consumer failure semantics unspecified. | DOCUMENTED **S:L17, L20, L54, L69, L73**; gaps INFERRED | **OPEN DECISION** — define only operationally relevant errors |
| **S3-Q05** | Tests, baseline and acceptance gate? | No Light-specific observed run/test supplied. Candidate E-01–E-06 above; baseline and thresholds need owner sign-off. | NOT RUN; CI configured but not an observed Light eval | **OPEN DECISION** — agree safe test environment and checks |
| **S3-Q06** | Contract location, versioning and approval? | Current human-readable output contract lives in Light `SKILL.md` and README; a new schema or separate contract file is not necessary without a verified consumer. Named owner and review/version policy unverified. | DOCUMENTED **S:L57–76, R:L66–73** | **NEEDS CONFIRMATION** — prefer existing file unless need proved |

### Existing written contract — not newly invented

| Boundary | Documented expectation | Source and assurance status |
| --- | --- | --- |
| **Ticket → assessment** | Ticket goal, actors, FR/NFR, acceptance criteria and constraints scoped | **S:L24–30**; DOCUMENTED |
| **Application code → evidence** | Inspect relevant real paths/symbols and contracts; distinguish no inspected fit from unverified | **S:L16–19, L34–38**; DOCUMENTED |
| **Assessment → human reviewer** | Ticket Snapshot + four SDI sections + open decisions; include evidence and readiness | **S:L49–69**; DOCUMENTED |
| **Side-effect boundary** | No code/Jira changes, migrations, deployments or subagent execution as part of Light | **S:L71–76**; instruction-level only; enforcement NOT VERIFIED |

### Candidate minimum invariants — PROPOSED for human agreement

- **I-01:** Never label a component or reusable pattern *verified* unless inspected source evidence identifies its path/symbol/behavior. **From documented intent S:L16–18, L34–37; behavioral compliance NOT RUN.**
- **I-02:** Missing code access must yield `NOT VERIFIED` / provisional recommendation, never a fabricated pattern or a universal absence claim. **S:L17, L37, L69.**
- **I-03:** Requirements explicitly approved by authorized sources remain separate from code observations and agent-proposed requirements. **S:L18, L26–29.**
- **I-04:** An assessment marked `READY FOR REVIEW` does not approve implementation, and the report cannot independently create external side effects. **S:L54, L71–76.** Host-enforced no-write must be verified separately.
- **I-05 (conditional consumer contract):** Only if an automated consumer is approved, each handoff should identify issue/revision, evidence, uncertainty, result state and failure reason. **PROPOSED; no present machine consumer documented.**

### Alternative-dependent contract direction

| Option | Minimum contract scope | What is NOT approved |
| --- | --- | --- |
| **A. Keep as-is and validate** | The already documented Ticket Snapshot, ordered sections, uncertainty rules and readiness labels; add external eval assertions | No new mandatory schema, permissions or workflow changes |
| **B. Harden based on failures** | Amend precise wording or field expectations *only for observed defects*, preserve human-readable contract and classifications | No extra gate inside the one-pass skill without explicit change request |
| **C. Add a downstream consumer** | Versioned producer/consumer identity, structured evidence/status, required/optional fields, compatibility/error semantics and authorization boundary | No assumed Sprint Assessment integration, API, schema or agent runtime |

**Contract owner/approver:** NOT CONFIRMED. **Stage 3 review gate:** **HUMAN REVIEW REQUIRED — Contract.** No code changes or permission shifts authorized by this document.

---

## Prioritized team discussion — ask only what the source cannot settle

| Priority | Question to confirm or decide | Why it matters | Suggested owner |
| --- | --- | --- | --- |
| **P1** | What real gap are we trying to address with Light: output quality, workflow placement, user adoption, or something else? | Source defines intended behavior, not an approved business problem or measured pain | Skill owner / users |
| **P1** | Which users and downstream consumers rely on the brief today? Is it consumed manually or by another workflow? | Determines whether Option A/B suffices or Option C has a real consumer | Skill owner / workflow owner |
| **P1** | Which Jira/code access and tool permissions are actually available to the intended host/users, and is no-write enforced externally? | Written read-only instructions are not a security control | Host/tool owner |
| **P1** | Which representative synthetic ticket and mock codebase can we safely use to test whether it verifies rather than guesses? | A reproducible baseline is missing | Skill owner / QA |
| **P2** | Which runtimes must be supported in practice, and who maintains installation/behavioral parity? | A portable format does not prove runtime compatibility | Platform owner |
| **P2** | What defines a good assessment, including acceptable unknowns, evidence citations and readiness? | Needed for measurable acceptance checks and evaluation rubrics | Skill users / reviewer |
| **P2** | Who approves changes to the skill and its output contract? | Prevents an inferred design from becoming an unreviewed requirement | Maintainer |

**Do not use meeting time to ask** whether the skill *claims* to be one-pass, uses four SDI steps, or lists specific readiness states: those are already established by **S:L12, L22–55**. If actual behavior matters, ask for **execution evidence**, not a repetition of the documentation.

## Decision log (no decisions approved)

| ID | Decision / question | Owner | Status |
| --- | --- | --- | --- |
| **D-01** | Confirm problem, users and desired success measures | UNASSIGNED | OPEN |
| **D-02** | Continue as-is/test first vs modify instructions vs define consumer handoff | UNASSIGNED | OPEN |
| **D-03** | Who owns effective permission boundaries and deployment targets? | UNASSIGNED | OPEN |
| **D-04** | Whether a downstream machine-readable contract is actually required | UNASSIGNED | OPEN |
| **D-05** | Approved eval fixtures, pass/fail rules and review gate | UNASSIGNED | OPEN |

## Next checkpoint and status

**Recommended next action:** In an approved environment, obtain a sanitized representative Jira ticket and synthetic application fixture, confirm the Stage 1 business problem and relevant user/owner, then review the **Option A (baseline first)** proposal. After human review, arrange a separate safely authorized Evaluate Skill workflow; do not treat this static review as an executed baseline.

**Deliverables produced:** Source-backed initial review, documented as-is Mermaid workflow, ten-dimension quality/standards/compatibility summaries, ten Stage 1 answers, five Stage 2 candidate answers, six Stage 3 candidate answers, conditional options and contract, **NOT RUN** test proposals, decision/evidence backlog.

**Not produced:** Real runtime or permission evidence, actual test results, approved design/contract, implementation, release.

**Review gate summary:** **HUMAN REVIEW REQUIRED — Discover; HUMAN REVIEW REQUIRED — Design; HUMAN REVIEW REQUIRED — Contract.**

This record is an initial public-source analysis. In a team setting, promote only confirmed decisions into a private canonical engineering review after the responsible reviewers agree.
