# DFRDE — Initial Engineering Review: Refine Requirements — Light

## Review summary

- **Scope:** Public Refine Requirements — Light skill only.
  - No workplace Jira ticket reviewed
  - No private application code reviewed
  - No runtime execution reviewed
- **Reviewed on:** November 8, 2026
- **Current status:**
  - **Stage 1 — Discover:** Review required
  - **Stage 2 — Design:** Proposed
  - **Stage 3 — Contract:** Not approved
  - **Stages 4–6:** Not started
- **Next step:** Confirm the problem, success criteria, and review owner.

> Links point to the inspected source revision. Documented behavior is not a tested result. Keep workplace evidence outside this public repository.

## Table of contents

- [Audit Skill — At a Glance](#audit-skill--at-a-glance)
- [1. Discover](#1-discover--what-problem-and-existing-reality-are-we-working-with)
- [2. Design](#2-design--what-approach-best-fits-the-requirements)
- [3. Contract](#3-contract--what-must-participants-and-components-guarantee)
- [Prioritized team discussion](#prioritized-team-discussion--ask-only-what-the-source-cannot-settle)
- [Decision log](#decision-log-no-decisions-approved)
- [Next checkpoint and status](#next-checkpoint-and-status)

## Audit Skill — At a Glance

**Purpose and trigger (DOCUMENTED):** A one-pass, noninteractive, read-only assessment of assigned Jira feature work, using four SDI steps and *verified* relevant existing application code. It is intended to provide an actionable technical overview before implementation, not to implement or approve a design. **[source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L3-L76).**

**Inputs:** Assigned Jira issue/feature request, its requirements/acceptance criteria, applicable company conventions, and authorized access to relevant application code (if available). Optional DDIA 2e/FODE lenses when the data path warrants them. **[source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L47).**

**Process:** Scope requirements → locate and verify candidates → recommend `FOLLOW`/`ADAPT`/`NEW REQUIRED` or an explicitly uncertain outcome → targeted full-stack/data-path analysis → risks, readiness and unresolved questions. **[source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L24-L55).** No declared subagent orchestration or autonomous scheduling was found in this skill definition; do not infer anything about hosts' separate agent capabilities.

**Output:** Ticket Snapshot, four SDI-labeled sections and owner-specific open questions. Readiness values are `READY FOR REVIEW`, `CONDITIONAL`, `BLOCKED`. **[source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L49-L69).**

**Side effects:** The text prohibits source edits, Jira posts, migrations, deployment, Superpowers invocation and agent launch. It is **prompt-level guidance, not proof that a consuming host technically enforces restrictions**. **[source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L71-L76).**

**Source scope and limits:** Inspected the public Light `SKILL.md`, README, the sibling's boundary, DotSkills adapter documentation, the audit/DFRDE guidance, repository tree and configured CI workflow. The Light package itself has only `SKILL.md` and `README.md`; no skill-local `evals/evals.json`, test script, runtime trace or approved internal Jira/code fixture was available in this review. The repo has general CI configuration, but that does **not** demonstrate behavior of this skill.

### Documented workflow (not an execution trace)

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

Diagram based on [the skill instructions](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L76); no execution was observed.

### Ten-dimension review dashboard

**What this is:** A project-specific engineering review rubric that combines software engineering, AI reliability, security and trust, and lifecycle concerns. It reflects ideas found in established practices (such as NIST AI RMF, OWASP guidance, and the Agent Skills specification), but **this exact ten-dimension dashboard is not an official industry standard, a compliance assessment, or a certification**.

**How to read it:** Each row shows (1) what the reviewed files describe, (2) what has not yet been checked, and (3) the source or next evidence needed. **A written instruction is not proof that the skill follows it when run.** No runtime execution was observed for this initial review.

**Status guide:**

- **Documented (not tested):** The inspected files describe the behavior or rule. Earlier reviews called this `PASS (static)`: *static* means reading code/docs without running the skill.
- **Needs verification:** A claim or protection has not been checked in the actual tools or operating setup. This is **unknown**, not a failure.
- **Partial gap:** Some situations are documented, but others are not addressed in the inspected instructions. It is not necessarily a runtime defect.
- **Evidence gap:** The inspected sources did not contain skill-specific test runs, results, or traces proving behavior. Missing evidence is not proof the behavior fails.

**Jargon translated:** *Runtime* = the skill actually running in a host such as Claude Code or Codex. *Environment* = the real Jira/code access, connected tools, settings, and permissions. *Parser compatibility* = whether another program can reliably read the skill's output. *Enforcement* = a technical permission/control that prevents an action, rather than merely telling the agent not to do it. *Behavioral evidence* = test results or execution traces showing what actually happened.

| Area | Finding in plain English | What this means / supporting source |
| --- | --- | --- |
| **Q-01 Purpose & boundaries** | **Documented (not tested)** | The skill describes its job and what it must not do. [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L8-L76) |
| **Q-02 Activation & discovery** | **Documented; activation not tested** | The skill has a name and example invocation. No test showed whether a host selects it for appropriate requests. [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L1-L87) |
| **Q-03 Inputs & dependencies** | **Documented; real access not checked** | The instructions name required ticket, code and standards inputs. Actual Jira/repository access and permissions were not examined. [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L38) |
| **Q-04 Workflow & decisions** | **Documented (not tested)** | The four SDI steps and reuse decisions are explained. No run showed whether the agent follows them correctly. [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L22-L55) |
| **Q-05 Contracts & outputs** | **Documented; machine-reading not tested** | The expected sections and readiness labels are specified. It has not been shown that a downstream program could reliably parse the output; no enforced output schema was inspected. [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L49-L69) |
| **Q-06 Context & trust** | **Documented; actual behavior not tested** | The instructions distinguish confirmed source facts from proposals and uncertainty. No test checked whether the skill consistently respects that distinction. [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L76) |
| **Q-07 Permissions & effects** | **Needs verification: real restrictions** | The skill says **read-only**, but the host's tool permissions were not inspected to see whether writes are technically prevented. [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L71-L76) |
| **Q-08 Failure & stopping** | **Partial gap: some failures not described** | Missing tickets/code and no-match cases are addressed, but tool failures, timeouts and stale information lack explicit recovery guidance. [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L17-L73) |
| **Q-09 Evals & observability** | **Evidence gap: no skill-specific test results found** | No Light-specific evaluation fixture, execution trace or graded run was found in the inspected package. General repository CI does not prove Light behaves correctly. |
| **Q-10 Lifecycle & portability** | **Needs verification: cross-platform behavior** | Git versioning and adapter instructions exist, but there are no observed runs demonstrating equivalent behavior on Claude Code and Codex. |

**Interpretation:** This is a quick view of the **current evidence**, not an overall pass/fail grade or a claim that the skill is production-ready. Q-08 is a documentation gap, not a proven runtime defect; Q-07, Q-09 and Q-10 call for additional evidence before stronger claims.

### Agent Skills specification — structural checks only

| Requirement | Finding | Evidence |
| --- | --- | --- |
| Skill folder with `SKILL.md` | PASS (static) | `skills/refine-requirements-light/SKILL.md` exists |
| YAML frontmatter, `name`, non-empty `description` | PASS (static) | [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L1-L4), directory and name match |
| Lowercase hyphenated name, limits | PASS (static) | `refine-requirements-light`; valid visible form |
| Markdown body | PASS (static) | [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L6-L87) |
| `references/`, `scripts/`, `assets/` | NOT APPLICABLE | Optional per spec; absence is not a format defect |
| Native `skills-ref validate` | **NOT RUN** | No CLI validator executed in this review |

Skill-format compliance does not prove evaluation, security, or cross-runtime reliability.

### Cross-platform compatibility — explicit evidence limits

| Capability | Claude Code | Codex / OpenAI harness | Evidence / what to verify |
| --- | --- | --- | --- |
| Skill packaging | **NOT VERIFIED** at runtime | **NOT VERIFIED** at runtime | DotSkills provides [Claude](../../adapters/claude/README.md) and [OpenAI](../../adapters/openai/README.md) adapter *instructions*, but Light installation wasn't executed |
| Discovery/activation | NOT VERIFIED | NOT VERIFIED | Confirm selection on Jira-ticket prompts and rejection of unrelated requests |
| Local application-code access and context | NOT VERIFIED | NOT VERIFIED | Confirm repo access, conventions/instruction hierarchy and reference loading |
| Tool names, ticket access, credentials | NOT VERIFIED | NOT VERIFIED | Jira integration and effective user/tool permissions are host-specific |
| Delegation and concurrency | NOT APPLICABLE in skill's documented workflow | NOT APPLICABLE in skill's documented workflow | No subagent delegation is prescribed by Light, [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L12-L76) |
| Side-effect enforcement | NOT VERIFIED | NOT VERIFIED | Prompt-level read-only is not a permission mechanism |
| Output/readiness contract | NOT VERIFIED behaviorally | NOT VERIFIED behaviorally | Compare sample outputs and missing-context behavior |
| Versioned regression evidence | NOT VERIFIED | NOT VERIFIED | No comparative skill eval runs inspected |

### Existing protections before possible improvements

The skill calls for verified reuse, clear uncertainty labels, conditional recommendations, no edits, and owner-specific questions ([source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L76)). These safeguards are written instructions, not verified enforcement.

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

**No tests were run or graded.** This review does not certify safety.

---

## 1. Discover — What problem and existing reality are we working with?

**SDI:** Step 1 — understand requirements and scope. The problem statement below is proposed, not confirmed.

### Draft problem statement — PROPOSED, HUMAN CONFIRMATION REQUIRED

> Developers need a concise, trustworthy assessment of Jira work grounded in existing code, without an interview or premature implementation. This review checks whether Light meets that need and what evidence would justify any change.

This is inferred from the skill's purpose, **not confirmed by the team**. Review any integration with another workflow separately.

### Stage 1 prefilled questions

| ID | Question | Draft answer / unknown | Evidence state and source | Question status / next action |
| --- | --- | --- | --- | --- |
| **S1-Q01** | Who needs help, and what outcome? | The skill targets faster, code-grounded ticket review. Actual users and workplace impact are not confirmed. | DOCUMENTED purpose, [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L8-L12); business outcome inferred | **NEEDS CONFIRMATION** — identify users and success measures |
| **S1-Q02** | What exists, and what was inspected? | Light contains a SKILL.md and README and describes a one-pass four-step SDI review. No internal app or runtime was inspected. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L22-L76), [README](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/README.md#L9-L16); reviewed source linked | **ANSWERED BY EVIDENCE** — documented package; runtime not verified |
| **S1-Q03** | Who invokes and reviews it? | A developer or coding agent supplies a Jira ticket. The assessment is noninteractive; human decisions remain outside the skill. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L3-L87) | **NEEDS CONFIRMATION** — confirm roles and host |
| **S1-Q04** | What goes in and comes out? | Inputs: ticket, acceptance criteria, company standards, relevant code if accessible. Output: ticket snapshot, four SDI sections, open questions. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L69) | **ANSWERED BY EVIDENCE** — intended format; access not verified |
| **S1-Q05** | Which decisions and statuses exist? | Reuse is classified as FOLLOW, ADAPT, NEW REQUIRED, scoped no-fit, or NOT VERIFIED. Readiness is READY FOR REVIEW, CONDITIONAL, or BLOCKED. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L19-L75) | **ANSWERED BY EVIDENCE** — written rules; confirm owner |
| **S1-Q06** | What safeguards and tests exist? | Strong written verification and uncertainty safeguards. No Light-specific executed evals/traces supplied; repo has a [configured CI workflow](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/.github/workflows/validate.yml). | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L76); [CI workflow configuration](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/.github/workflows/validate.yml) inspected | **NOT VERIFIED** — run approved synthetic evals |
| **S1-Q07** | What are the trust and permission limits? | The skill is written as read-only and follows Agent Skills structure. Host-enforced permissions and portability are untested. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L76); [Agent Skills specification](https://agentskills.io/specification) / [Claude adapter](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/adapters/claude/README.md) and [OpenAI adapter](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/adapters/openai/README.md) | **NOT VERIFIED** — inspect host permissions |
| **S1-Q08** | What requirements and success measures are agreed? | The skill explains how to extract FR/NFRs. No approved quality targets, SLOs, or team scope were found. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L24-L55); business thresholds UNVERIFIED | **NEEDS CONFIRMATION** — agree on acceptance criteria |
| **S1-Q09** | Could the current skill be enough? | Possibly. Test its current behavior before adding workflow steps or schemas. | INFERRED from documented small-change rule [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L19-L54) | **OPEN DECISION** — compare in Stage 2 |
| **S1-Q10** | What evidence is missing? | A safe ticket/code fixture, access expectations, host permissions, baseline results, owner, and supported runtimes. | NOT VERIFIED beyond public source; **F-01–F-06** | **NOT VERIFIED** — assign evidence owners |

### Known requirements, constraints and non-goals

**Documented behavior:** one read-only pass; verify code before suggesting reuse; report requirements, relevant data flow, risks, readiness, and open questions ([source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L76)).

**Proposed success criteria (not approved):** no invented code evidence or unauthorized effects; all five output sections; honest conditional/blocked states; useful owner-specific questions; consistent meaning across supported runtimes. Numeric thresholds and reviewers remain open.

**Not in scope:** Sprint Assessment integration, application redesign, Jira actions, private-code inspection, Light edits, or executed behavioral tests.

### Deliverables and review gate

| Output | Current status | Next evidence |
| --- | --- | --- |
| Skill inventory / documented current-state flow | **DRAFT — SOURCE-BACKED** | [SKILL.md](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md) and [README](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/README.md) |
| User problem and measurable success | **PROPOSED — REVIEW REQUIRED** | Confirm with user/skill consumer |
| Functional/nonfunctional review criteria | **DRAFT — REVIEW REQUIRED** | Approve useful quality criteria |
| Effective runtime, tools, ownership | **NOT VERIFIED** | Approved host configuration/owner |
| Stage 1 approval | **HUMAN REVIEW REQUIRED — Discover** | Record reviewer and decision in internal working record |

---

## 2. Design — What approach best fits the requirements?

**SDI:** Steps 2–4 — compare approaches, components, and trade-offs. The design options assume the team wants to validate Light before changing it; none is approved.

### Stage 2 prefilled questions

| ID | Question | Evidence-backed response / proposed options | Source / evidence | Question status / next action |
| --- | --- | --- | --- | --- |
| **S2-Q01** | What options could solve this? | A: test Light as written. B: make targeted fixes if tests find gaps. C: add a structured handoff only for a confirmed consumer. | INFERRED options from [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L69) | **OPEN DECISION** — choose after confirming the problem |
| **S2-Q02** | What existing behavior should stay? | Four SDI steps; code-first evidence; reuse labels; scoped inspection; five output sections; optional DDIA/FODE and company standards. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L69) | **ANSWERED BY EVIDENCE** — host behavior unverified |
| **S2-Q03** | Who owns orchestration and decisions? | Light describes one report, without subagent dispatch. No downstream automation is established. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L12-L76); future options PROPOSED | **OPEN DECISION** — verify any consumer |
| **S2-Q04** | What trade-offs matter? | A makes few changes but may keep defects; B may add prompt complexity; C adds consumer coupling and versioning. Runtime cost is unknown. | INFERRED; no measurements, **F-01–F-06** | **NEEDS CONFIRMATION** — use measured risks |
| **S2-Q05** | Has anyone approved a design? | No approval was found in the inspected source. | NOT VERIFIED; [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L71-L76) (no auto-approval) | **OPEN DECISION** — human review required |

### Design option comparison — all PROPOSED

| Option | Description | Benefit | Trade-off / evidence prerequisite |
| --- | --- | --- | --- |
| **A. Validate existing behavior first** | Leave Light unchanged; use approved synthetic tasks and review actual outputs | Least disruption; yields a defensible baseline before edits | Needs safe harness/tool isolation and representative fixtures; may reveal problems requiring B |
| **B. Minimal contract/instruction hardening** | If tests reveal gaps, clarify requirements preflight, source evidence fields, response stop/blocked semantics, and review criteria while preserving one-pass format | Potentially more consistent assessments without redesign | Risk of over-specification and larger prompt; must be justified and regression-tested |
| **C. Explicit downstream interface** | If a real consumer exists, define a separately reviewed structured handoff or adapter | Could enable integration with another workflow | Consumer, schema, ownership, migration and permissions **not established**; do not introduce speculatively |

**Working recommendation (not approved):** Start with A. Consider B or C only if testing or a confirmed consumer justifies more complexity.

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

The current path is documented; the test path is only proposed.

### Deliverables and review gate

| Output | Current status |
| --- | --- |
| As-is component/flow and source-backed assumptions | DOCUMENTED / runtime NOT VERIFIED |
| Options and trade-offs | PROPOSED |
| Chosen architecture, owner and rationale | **OPEN DECISION** |
| Stage 2 approval | **HUMAN REVIEW REQUIRED — Design** |

---

## 3. Contract — What must participants and components guarantee?

**SDI:** Steps 3–4 — interfaces and trade-offs. Light has a written report format; no new schema, contract, or host security control is approved or verified.

### Stage 3 prefilled questions

| ID | Question | Existing evidence / candidate response | Evidence state | Question status / next action |
| --- | --- | --- | --- | --- |
| **S3-Q01** | Who produces, reads, and owns the report? | Light produces a report for a reviewer/developer. A machine consumer and named maintainer are not documented. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L8-L69); ownership NOT VERIFIED | **NEEDS CONFIRMATION** — identify owners |
| **S3-Q02** | What must the output guarantee? | The written format requires a ticket snapshot, four sections, reuse classifications, readiness, and clear uncertainty. Candidate invariants follow. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L17-L69); candidate invariants PROPOSED | **OPEN DECISION** — choose testable guarantees |
| **S3-Q03** | Who can act, and with which permissions? | The skill forbids edits, posts, deployments, and agent launches. Effective Jira/tool permissions were not inspected. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L18-L76); enforcement NOT VERIFIED | **NOT VERIFIED** — inspect enforced permissions; no live write tests |
| **S3-Q04** | What happens when evidence or tools are missing? | The skill permits provisional reports, scoped no-fit, and blocked states. Tool timeout and retry rules are unspecified. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L17-L73); gaps INFERRED | **OPEN DECISION** — define only relevant failures |
| **S3-Q05** | How will compliance be tested? | No Light-specific runs were reviewed. Proposed cases E-01–E-06 need a safe environment and approval. | NOT RUN; CI configured but not an observed Light eval | **OPEN DECISION** — approve fixtures and checks |
| **S3-Q06** | Where does the contract live? | The existing report contract is in Light's SKILL.md and README. No machine consumer or separate schema is confirmed. | DOCUMENTED [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L57-L76), [README](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/README.md#L66-L73) | **NEEDS CONFIRMATION** — keep existing location unless needed |

### Existing written contract — not newly invented

| Boundary | Documented expectation | Source and assurance status |
| --- | --- | --- |
| **Ticket → assessment** | Ticket goal, actors, FR/NFR, acceptance criteria and constraints scoped | [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L24-L30); DOCUMENTED |
| **Application code → evidence** | Inspect relevant real paths/symbols and contracts; distinguish no inspected fit from unverified | [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L38); DOCUMENTED |
| **Assessment → human reviewer** | Ticket Snapshot + four SDI sections + open decisions; include evidence and readiness | [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L49-L69); DOCUMENTED |
| **Side-effect boundary** | No code/Jira changes, migrations, deployments or subagent execution as part of Light | [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L71-L76); instruction-level only; enforcement NOT VERIFIED |

### Candidate minimum invariants — PROPOSED for human agreement

- **I-01:** Never label a component or reusable pattern *verified* unless inspected source evidence identifies its path/symbol/behavior. **From documented intent [source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L16-L37); behavioral compliance NOT RUN.**
- **I-02:** Missing code access must yield `NOT VERIFIED` / provisional recommendation, never a fabricated pattern or a universal absence claim. **[source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L17-L69).**
- **I-03:** Requirements explicitly approved by authorized sources remain separate from code observations and agent-proposed requirements. **[source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L18-L29).**
- **I-04:** An assessment marked `READY FOR REVIEW` does not approve implementation, and the report cannot independently create external side effects. **[source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L54-L76).** Host-enforced no-write must be verified separately.
- **I-05 (conditional consumer contract):** Only if an automated consumer is approved, each handoff should identify issue/revision, evidence, uncertainty, result state and failure reason. **PROPOSED; no present machine consumer documented.**

### Alternative-dependent contract direction

| Option | Minimum contract scope | What is NOT approved |
| --- | --- | --- |
| **A. Keep as-is and validate** | The already documented Ticket Snapshot, ordered sections, uncertainty rules and readiness labels; add external eval assertions | No new mandatory schema, permissions or workflow changes |
| **B. Harden based on failures** | Amend precise wording or field expectations *only for observed defects*, preserve human-readable contract and classifications | No extra gate inside the one-pass skill without explicit change request |
| **C. Add a downstream consumer** | Versioned producer/consumer identity, structured evidence/status, required/optional fields, compatibility/error semantics and authorization boundary | No assumed Sprint Assessment integration, API, schema or agent runtime |

**Contract owner:** not confirmed. **Gate:** HUMAN REVIEW REQUIRED — Contract. No changes or permission expansions are authorized.

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

The one-pass format, four SDI steps, and readiness labels are already documented ([source](https://github.com/rlynjb/dotskills/blob/11da8e5f64c033eaf4b2e87cdf5c770f662ada3c/skills/refine-requirements-light/SKILL.md#L12-L55)). Ask for run evidence if behavior is in doubt.

## Decision log (no decisions approved)

| ID | Decision / question | Owner | Status |
| --- | --- | --- | --- |
| **D-01** | Confirm problem, users and desired success measures | UNASSIGNED | OPEN |
| **D-02** | Continue as-is/test first vs modify instructions vs define consumer handoff | UNASSIGNED | OPEN |
| **D-03** | Who owns effective permission boundaries and deployment targets? | UNASSIGNED | OPEN |
| **D-04** | Whether a downstream machine-readable contract is actually required | UNASSIGNED | OPEN |
| **D-05** | Approved eval fixtures, pass/fail rules and review gate | UNASSIGNED | OPEN |

## Next checkpoint and status

**Next:** Confirm the problem and owner, choose a sanitized ticket and synthetic code fixture, then review Option A (test current behavior first). Run Evaluate Skill separately only when authorized.

**Produced:** Static audit, documented workflow, quality/standards/compatibility checks, 10 Discover answers, 5 Design answers, 6 Contract answers, proposed options/invariants/tests, and open decisions.

**Not produced:** Runtime or permission evidence, test results, approved design/contract, implementation, or release.

**Review gate summary:** **HUMAN REVIEW REQUIRED — Discover; HUMAN REVIEW REQUIRED — Design; HUMAN REVIEW REQUIRED — Contract.**

This public-source review is a draft. Record confirmed team decisions separately after approval.
