# REAZN

**Communication style:** Senior-engineer reasoning for a junior-developer audience. See the reusable [mentoring communication guideline](../../docs/senior-engineer-mentoring-communication.md); the `SKILL.md` links to this one guideline and retains only REAZN-specific output requirements. The shared file must be accessible when the skill runs. Explanations stay within the existing four-step SDI format and do **not** enable `learn: on` or add teaching sections.

**Input-agnostic, evidence-first engineering reasoning using the four-step System Design Interview (SDI) framework.**

REAZN examines an existing system, assesses a requested change, or explores a new design. It produces **one read-only assessment**—not implementation tasks, source edits, or automatic approvals. A Jira ticket or code repository is **not required**.

## Quick start

```text
Use reazn on this [source or target].
Goal: [what you want to understand or assess]
```

Add optional settings when you need a particular intent, scope, source version, comparison, or learning references.

## What can I give REAZN?

REAZN is **input-agnostic**: it uses the same four SDI steps regardless of the input format, adapting the evidence it inspects to the subject.

- **Code and systems:** a repository, feature, service, module, implementation, or code diff.
- **Requests and specifications:** a Jira/other tracker ticket, user story, acceptance criteria, feature brief, requirements, or design document.
- **Agent skills:** a `SKILL.md`, linked references, or an existing Audit Skill report.
- **Business and operational workflows:** process descriptions, roles, handoffs, policies, and proposed improvements.
- **Other accessible sources:** pasted text, structured data, PDFs, screenshots/images, or supported links.
- **New ideas:** a proposed system or workflow with no existing implementation.

**Give it a specific goal and a bounded target.** REAZN can work from partial evidence but will mark inaccessible, absent, or unverified sources explicitly. An Audit Skill report is **secondary evidence**, not proof of execution or approval.

## Invocation settings

All settings are **optional prompt-level selectors**, not guaranteed typed API arguments.

| Setting | Values / examples | Use |
| --- | --- | --- |
| `intent` | `auto` (default), `understand-existing`, `assess-change`, `design-new` | Choose whether to understand current behavior, compare a requested change, or design something new. |
| `scope` | `auto` (default), `system`, `subsystem` | Set the investigation breadth. `system` covers relevant affected boundaries, not every repository file. |
| `target` | `skills/reazn`, `Reporting API`, `approval workflow` | Identify the system, feature, skill, module, or process to inspect. |
| `revision` | Git commit/branch/tag or document version | Identify the source version to inspect; REAZN checks what it actually accessed. |
| `compare` | `main...feature-branch`, PR diff, document versions | Compare available before/after evidence without assuming an approval or a wider scope. |
| `learn` | `off` (default), `on` | Add selective `*Further reading:` and `*Study focus:` book/chapter pointers to relevant findings. |

For more repeatable runs, keep the **goal, intent, scope, target, source versions, audit report, and learning setting** the same. Exact wording can still vary.

## Example invocations

**Understand an existing implementation**

```text
Use reazn on the reporting module.
Goal: Understand what is implemented, its contracts, and unknowns.
intent: understand-existing
scope: subsystem
target: src/services/reporting
revision: <verified-commit>
```

**Assess a feature request**

```text
Use reazn on this Jira ticket and the relevant repository.
Goal: Compare the requested CSV export with existing behavior.
intent: assess-change
scope: subsystem
target: reporting
compare: main...feature-branch
```

**Assess an agent skill using an audit**

```text
Use reazn on this SKILL.md and the attached Audit Skill report.
Goal: Understand documented behavior, evidence gaps, and risks.
intent: understand-existing
learn: on
```

**Design a new workflow**

```text
Use reazn on this proposed approval workflow.
Goal: Define expected outcomes, boundaries, contracts, and trade-offs.
intent: design-new
scope: system
```

The paths and Git refs above are illustrative; REAZN must verify the actual sources.

## What does REAZN output?

One evidence-backed report with a consistent structure:

1. **Input Snapshot** — four groups: **Assessment objective**, **Purpose & core capabilities**, **Investigation scope**, and **Evidence & recommendation**. Includes resolved intent, examined baseline, and evidence limits.
2. **Step 1 — Requirements & scope** — source-supported functional requirements (FRs), non-functional requirements (NFRs), and questions **when applicable**.
3. **Step 2 — Verify patterns & recommend high-level design** — existing responsibilities, evidence, reuse fit, conditional recommendations, and current/proposed flow diagrams **when relevant**.
4. **Step 3 — Deep dive & data flow** — four relevant areas: mechanisms & boundaries; data-flow traces; contract considerations; and **Output Assessment** (what the subject produces, expected vs. observed behavior, evidence and verification status). Only contracts and output assessments use fixed multi-field blocks; an optional free-form **Additional findings** section captures material observations that fit neither.
5. **Step 4 — Trade-offs, risks & readiness** — material alternatives, risks, mitigation, verification needs, proposed decision records, optional implementation watchpoints, and free-form **Additional findings** when warranted.
6. **Open decisions / questions** — remaining owner-specific gaps, or a statement that none were identified.

## Step-by-step analysis lenses & fields

A **lens** describes what REAZN examines; a **record** has fixed field labels and order. REAZN uses only relevant lenses and records, rather than inventing findings to fill a template. Source-backed claims remain distinct from assumptions, proposals, and runtime verification.

### Step 1 — Requirements & scope

- **Lenses:** objective, actors, expected outcomes, functional/non-functional requirements, constraints, acceptance criteria, and unknowns.
- **FR (functional requirement):** `Requirement` → `Status` → `Source`; optional `Acceptance` → `Open question`.
- **NFR (non-functional requirement):** `Quality` → `Status` → `Source`; optional `Linked FR` → `Verification` → `Open question`.
- In an existing-system assessment, observed code behavior does **not** automatically become an FR/NFR.

### Step 2 — Verify patterns & high-level design

- **Lenses:** existing responsibilities and patterns, evidence and reuse fit, proposed design alternatives, and current/proposed flows when meaningful.
- **Area / existing pattern:** `Where it lives` → `What exists today` → `Purpose` → `Fit to objective` → `Verdict` → `Why` → `Source`.
- **Design recommendation (when relevant):** `Recommendation` → `Why` → `Alternative` → `Linked requirements` → `Status`; optional `Source`.
- **Flow diagrams:** evidence-labeled current and proposed component/handoff flows where applicable, **not** another fixed-field record.

### Step 3 — Deep dive & data flow

- **Mechanisms & boundaries (lens):** ownership, validation, authorization, errors, side effects, and guarantees. No mandatory multi-field record.
- **Data-flow deep dive (lens):** source/input → transformation or handoff → destination/consumer, including read/write paths where relevant. No mandatory multi-field record.
- **Contract (fixed record):** `Current` → `Owner` → `Guarantee` → `Unknown` → `Linked requirements` → `Linked decision`; optional `Source`.
- **Output Assessment (fixed record):** `Output` → `Expected behavior` → `Observed behavior` → `Evidence` → `Verification status`. This evaluates what the **assessed subject** produces, not the REAZN report. Documented instructions and static code do not prove runtime execution; uninspected outputs remain `NOT VERIFIED`.
- **Additional findings (optional, free-form):** After the standard Step 3 analysis, briefly explain any material evidence-backed discovery that does not fit those lenses or records. No fixed fields; omit if none.

### Step 4 — Trade-offs, risks & readiness

- **Lenses:** material alternatives, consequences, mitigations, change impact, verification, and human decisions.
- **Trade-off:** `Benefit` → `Cost` → `Preferred approach` → `Linked decision`.
- **Risk:** `Impact` → `Mitigation` → `Linked decision`.
- **Change footprint (if relevant):** `Affected areas` → `Cross-boundary impact`.
- **Readiness (always):** `Status` → `Reason` → `Verification`. For `understand-existing`, this means **evidence readiness**, not approval to implement.
- **Proposed decision record (when consequential):** `Decision` → `Why/evidence` → `Alternative` → `Contract impact` → `Linked requirements` → `Status` → `Revisit if`.
- **Implementation Watchpoint (`Watchpoint: <name>`, optional fixed record):** `Expected` → `Verify` → `Evidence` → `Status`. Include **after any proposed decision records**, only for material design assumptions, contract changes or ownership/dependency decisions that merit a later implementation check. `PENDING VERIFICATION` means no comparison was performed; `REVIEW REQUIRED` needs grounded discrepancy evidence; `VERIFIED` needs an actual comparison. A watchpoint is not a confirmed bug or implementation task.
- **Additional findings (optional, free-form):** After any watchpoints, briefly capture material evidence-backed observations not covered by other Step 4 records. No prescribed labels or extra fields; omit if none.

After Step 4, any **open question** uses `Question` → `Why it matters` → `Decision owner` → `Linked requirements`. Optional `learn: on` references appear after applicable record fields. See [`SKILL.md`](SKILL.md) for the authoritative rules and edge cases.

**FRs/NFRs are not automatically work to implement.** They represent sourced expectations. REAZN distinguishes documented requirements, inspected implementation, proposed changes, and unverified gaps. In an understanding-only assessment, no new FR/NFR or design change needs to be invented.

The standard records keep **bold item headings, italic field labels, stable field order, compact spacing, and source references**. Optional Additional findings use concise free-form prose instead of a new schema; irrelevant items are omitted rather than manufactured. With `learn: on`, relevant findings may include a book chapter and study focus from the [optional learning guide](references/learning-chapters.md).

## Boundaries and references

REAZN is **one-pass and read-only**. It does not run tests automatically, modify repositories, create tickets, or approve decisions. Use [SLICE](../slice/SKILL.md) when you want to convert justified requirements or assessed changes into delivery tickets.

The canonical behavior and formatting rules live in [`SKILL.md`](SKILL.md). For repeatability testing, see the [evaluation cases](evals/evals.json) and [five-run protocol](evals/README.md); **behavioral consistency has not been demonstrated by those definitions alone**.
