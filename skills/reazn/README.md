# REAZN

**REAZN is a noninteractive, read-only, evidence-first skill using the same four SDI reasoning steps across input types.**

Give this skill a bounded existing-system understanding goal, identifiable problem, or proposed change: a Jira/other tracker item, pasted feature brief, acceptance criteria, architecture document, source code, agent-skill definition, Audit Skill findings, workflow description, PDF, screenshot, or another source the active host can actually inspect. It produces **one** concise assessment, not an interview or a new methodology. A Jira integration or codebase is not required for non-software problems.

It complements [Refine Requirements](../refine-requirements/README.md), which provides longer collaborative design exploration and explicit decision approvals.

## Assessment intent and semantic consistency

Choose an optional prompt-level `intent: auto | understand-existing | assess-change | design-new` (default `auto`). **Understand-existing** describes current capabilities and known requirements **without inventing a change**; **assess-change** compares expected behavior with inspected actual evidence and gaps; **design-new** uses proposed requirements when there is no implemented baseline. All three retain the same four SDI steps.

REAZN classifies source claims **before** generating FR/NFR IDs: **DOCUMENTED REQUIREMENT** (source expectations, with real approval state), **OBSERVED IMPLEMENTATION** (static inspected code vs genuine runtime traces kept distinct), **PROPOSED CHANGE** (a user-requested future change or unapproved suggestion), and **UNVERIFIED GAP / CONFLICT** (source missing, inaccessible or contradictory). The codebase's current behavior is not automatically product intent. Audit Skill suggestions are **secondary evidence**, not approved requirements or tasks; inspect the original cited source where accessible. When requirements are unavailable, observed capabilities remain described in the Input Snapshot and Step 2 rather than being fabricated as FR/NFRs.

For comparable runs, fix the **intent, goal, target, scope, Git/document revisions, audit report version, compare selector and `learn` setting**. The Input Snapshot now reports `Intent:`, `Input baseline:`, `Audit handoff:` and `Learn:`. Preserve source identifiers when available, and assign new FR/NFR IDs by authoritative source order rather than subjective importance. A source claim should keep its evidence category and provenance across runs; exact wording and defensible recommendations can still vary.

**Repeatability evaluation:** [REAZN eval cases](evals/evals.json) and the [five-run comparison protocol](evals/README.md) provide synthetic frozen inputs, expected source classifications and a manual cross-run consistency check. These definitions are **not evidence of executed behavioral tests**.

## How it works — one SDI framework

1. **Step 1 — Understand the problem and scope:** Clarify the objective, actors, expected behavior/outcomes, constraints, functional requirements (FRs) and nonfunctional requirements (NFRs) where applicable, acceptance and unresolved assumptions.
2. **Step 2 — Verify existing patterns and recommend high-level design:** Inspect relevant code, agent skill, documented process or other current-state evidence. Explain what exists, who owns it, whether to FOLLOW/ADAPT or justify NEW REQUIRED, and compare the current/proposed flow when meaningful.
3. **Step 3 — Deep dive into mechanisms and contracts:** Focus on interfaces, guarantees, responsibilities, permissions, process handoffs, data flow, error behavior or other domain-relevant mechanics. **Do not invent APIs, databases or services** for nontechnical inputs.
4. **Step 4 — Trade-offs, risks and readiness:** Explain meaningful alternatives, evidence gaps, verification needs, minimal change footprint and proposed engineering decisions (D-IDs) without claiming approval.

The **Input/Ticket Snapshot** groups purpose and numbered, evidence-labeled core capabilities into four clearly titled subsections. These explain what the subject already does (or proposes to do), **not** the requirements for the requested change. The report uses **vertical, individually labeled findings** with source evidence. It keeps FR/NFR/D IDs when meaningful, boxed ASCII diagrams for relevant multi-component Step 2 flows, and `---` separators **only between distinct Step 2 pattern/design entries**. No Markdown tables in skill output.

## Strict item spacing and structure

- **One item = one block:** A bold `FR-xx`, `NFR-xx`, `Area:`, `Contract:`, `Risk:`, `D-xx`, or `Q-xx` heading is followed immediately by its consecutive Markdown `_Label:_ value` fields (label italic, value regular). **No blank line between heading and fields or between fields within an item.**
- **Between items:** Exactly **one blank line**. Only Step 2 may separate full existing-pattern or design-option items with a standalone `---` and one blank line on either side. No dividers for FRs, NFRs, risks, contracts, decisions, or open questions.
- **Italic field labels:** In Markdown, use `_Requirement:_ value`, `_Status:_ value`, `_Source:_ value` and the same pattern for every field in the Snapshot and four SDI steps. Italicize only the label and colon; leave the value and citation/link in regular weight. In plain text use `Label: value` without Markdown markers.
- **Visible line breaks:** In Markdown, end the heading and nonfinal field lines with **two trailing spaces** so each label remains on its own line. No bullet prefixes, label indentation, padded blank paragraphs or Markdown tables.
- **Optional study fields:** With `learn: on`, the italic literal-asterisk labels `_\*Further reading:_` and `_\*Study focus:_` follow the same finding's evidence/reasoning **without any blank line**. All factual labels stay unprefixed.

**Illustrative NFR blocks (not real project findings):**

```markdown
**NFR-02 — Provenance and uncertainty**  
_Quality:_ Distinguish facts, observations, and assumptions.  
_Status:_ DOCUMENTED  
_Source:_ [verified reference]

**NFR-03 — Portable packaging**  
_Quality:_ Support independent skill installation.  
_Status:_ NOT VERIFIED  
_Source:_ [inspected packaging evidence]
```


## Stable finding labels across the four SDI steps

**The structure stays consistent; the findings depend on the evidence.** [SKILL.md](SKILL.md) now defines required labels **and their order** for each item type. It does not require a fixed count of FRs, risks, contracts or trade-offs.

- **Step 1:** FR = Requirement → Status → Source (optional Acceptance, Open question); only sourced DOCUMENTED/PROPOSED requirements are FR/NFRs—not observations or unapproved audit suggestions. NFR = Quality → Status → Source (optional Linked FR, Verification, Open question).
- **Step 2:** Area = Where it lives → What exists today → Purpose → Fit to objective → Verdict → Why → Source; preserve current/proposed ASCII diagrams.
- **Step 3:** Contract = Current → Owner → Guarantee → Unknown → Linked requirements → Linked decision (optional Source). Data-flow reporting remains domain-sensitive.
- **Step 4:** Trade-off = Benefit → Cost → Preferred approach → Linked decision; Risk = Impact → Mitigation → Linked decision; Change footprint = Affected areas → Cross-boundary impact; Readiness = Status → Reason → Verification; D-ID = Decision → Why/evidence → Alternative → Contract impact → Linked requirements → Status → Revisit if.

Step 4 orders the groups as **trade-offs → risks → change footprint (when relevant) → readiness → proposed decision records**. Readiness always appears; other types appear only when meaningful. Use `NOT VERIFIED` or `NOT APPLICABLE` with a reason for unsupported values instead of inventing them. Keep bold headings, *italic labels*, regular values, compact fields and optional `learn: on` reading lines at the end of each applicable item.

**Illustrative Step 4 format (not project findings):**

```markdown
## Step 4 — Trade-offs, risks & readiness

**Trade-off: Reuse versus new component**  
_Benefit:_ Reuses an existing interface.  
_Cost:_ Existing limits may constrain changes.  
_Preferred approach:_ ADAPT — conditional on verification.  
_Linked decision:_ D-01

**Risk: Contract regression**  
_Impact:_ Interface changes could break callers.  
_Mitigation:_ Verify compatibility before approval.  
_Linked decision:_ D-01

**Readiness**  
_Status:_ CONDITIONAL  
_Reason:_ Compatibility evidence is missing.  
_Verification:_ Inspect callers and run approved checks.
```

## Grouped Input Snapshot — CLI-first presentation

The first screen of a REAZN report is an **orientation summary** with four `###` subsections, in this exact order: **Assessment objective**, **Purpose & core capabilities**, **Investigation scope**, **Evidence & recommendation**. They group the Snapshot only, **not** the four SDI steps.

- **Assessment objective:** Input source/type and the requested goal.
- **Purpose & core capabilities:** The subject's purpose and **2–5** relevant capabilities when evidenced. Number them `01 —`, `02 —` and give each compact `What:`, `Status:`, and `Source:` fields. Distinguish `OBSERVED`, `DOCUMENTED`, `PROPOSED` and `NOT VERIFIED`; a new feature is not an existing capability.
- **Investigation scope:** Requested/resolved scope, basis, target, revision, comparison, included/excluded areas.
- **Evidence & recommendation:** Relevant dependencies and evidence limits, with a short recommendation **at the bottom**.

Use italic Markdown labels (`_Label:_ value`) and **one blank line between groups and complete capability items**, **no blank lines inside an item's fields**, and Markdown hard breaks (two trailing spaces) so labels remain distinct in iTerm2/Codex. Do **not** use tables or horizontal rules in the Snapshot. Use short clickable `file:line` source labels when the destination is verified; otherwise state `NOT VERIFIED` without inventing a link. Detailed FR/NFR/Area/Contract/Risk/D/Q items keep their existing compact formatting in Steps 1–4.

**CLI preview (illustrative content, not verified project findings):**

```markdown
## Input Snapshot — Reporting service

### Assessment objective

_Input:_ Feature brief + inspected repository  
_Intent:_ assess-change (explicit)  
_Goal:_ Assess proposed CSV export

### Purpose & core capabilities

_Purpose:_ Generate authorized reports  
_Status:_ DOCUMENTED  
_Source:_ [verified specification reference]

_Core capabilities:_ 2 relevant behaviors

**01 — View reports**  
_What:_ Display report results.  
_Status:_ OBSERVED  
_Source:_ [verified file:line]

**02 — Filter reports**  
_What:_ Filter report results.  
_Status:_ OBSERVED  
_Source:_ [verified file:line]

### Investigation scope

_Requested scope:_ subsystem  
_Resolved scope:_ subsystem  
_Basis:_ Explicit request  
_Target:_ Reporting  
_Revision:_ NOT VERIFIED  
_Comparison:_ NOT PROVIDED  
_Input baseline:_ UNFROZEN — revision not confirmed  
_Audit handoff:_ NOT PROVIDED  
_Learn:_ off  
_Included:_ Reporting UI and relevant API contracts  
_Excluded:_ Unrelated subsystems

### Evidence & recommendation

_Dependencies:_ Reporting API  
_Evidence limits:_ Runtime tests NOT RUN  
_Recommendation:_ CONDITIONAL — verify export contracts before proposing changes.
```

## Scope resolution — optional invocation selectors

Set **`scope`** to define the breadth of the SDI assessment and optionally supply **`target`**, **`revision`**, and **`compare`** to make its evidence boundaries explicit. These are **prompt-level settings**, not guaranteed typed API parameters or additional SDI steps.

- **`scope: auto | system | subsystem`** — Default `auto`: infer the **smallest coherent boundary** from the objective and accessible evidence. `system`: examine major **affected** subsystems and cross-system contracts for a system-wide problem, without exhaustively mapping the repository. `subsystem`: focus on a named feature, service, skill, component or process step and necessary neighbors.
- **`target`** — Optional repository, system, feature, module, component, agent skill or workflow to investigate. The presence of a repository root never automatically implies `scope: system`.
- **`revision`** — Optional branch, commit, tag or document version to inspect. The skill verifies the actual version rather than assuming that `main` or a named branch exists.
- **`compare`** — Optional base/head comparison, such as `main...feature-branch`, PR diff or document versions. A comparison scopes **change evidence**, not the system boundary or approval of the change.

**Resolution rules:** Explicit `scope` wins. With `auto`, choose and **disclose** the narrowest supported boundary; read across it only to inspect relevant contracts and dependencies. When a target, revision or comparison is unavailable, label it **NOT VERIFIED** and provide a conditional four-step assessment. The Input/Ticket Snapshot records **requested vs. resolved scope, target, actual revision, comparison, included/excluded areas and cross-boundary dependencies**.

This doesn't turn REAZN into [Learn Repo](../learn-repo/SKILL.md) (whole-codebase onboarding), [Learn Implementation](../learn-implementation/SKILL.md) (understanding existing code), or [Review Implementation](../review-implementation/SKILL.md) (post-implementation verification). Even `scope: system` needs an **identifiable problem or proposed change**.

**Example — focused branch assessment:**

```text
Run reazn to assess a proposed Facility Map change.
scope: subsystem
target: Facility Map
revision: feature/facility-map
compare: main...feature/facility-map
learn: on

Verify that the references exist, inspect the scoped changes and
necessary shared contracts, and give one four-step SDI report.
```

The branch names are illustrative. For a system-wide problem, set `scope: system`; to let the skill infer scope, omit the field or use `scope: auto`.

### Verify before recommending

Existing software, an agent skill or a business workflow may contain reusable behavior, but it must be inspected rather than assumed. Use **FOLLOW** for verified fit, **ADAPT** for verified partial fit, and **NEW REQUIRED** when evidence justifies a new approach. A bounded search may yield **NO SUITABLE PATTERN FOUND IN INSPECTED SCOPE**; incomplete access is **NOT VERIFIED**; no known current baseline is **CURRENT STATE NOT PROVIDED**. None of these means an absent component has been proven impossible.

**Domain-aware analysis:** For a codebase, inspect code, contracts, tests and conventions. For agent skills, inspect instructions, references, dependencies and relevant audit findings (which are not proof of runtime execution). For business workflows, inspect participants, decisions, handoffs and documents. Mark irrelevant software checks **NOT APPLICABLE** with a reason.

## Optional book references — `learn`

This is an **optional invocation setting**, not an extra SDI step:

- **`learn: off` (default):** The assessment stays focused on evidence and engineering decisions. No learning references or empty reading placeholders appear.
- **`learn: on`:** For each **material finding with a strong topic match**, the skill adds **`*Further reading:`** (book, edition, chapter number/title) and **`*Study focus:`** (the concept worth exploring) **under that finding**. These labels carry a **literal leading asterisk** (use `_\*Further reading:_` and `_\*Study focus:_` in Markdown output), unlike factual fields such as `Evidence:` and `Verdict:`. References supplement the usual output and do not change source evidence, factual claims or approval status.

**Example of a learning reference (illustrative, not verified project evidence):**

```markdown
**Area: Module ownership**  
_What exists today:_ [description grounded in inspected code]  
_Evidence:_ [actual file/symbol]  
_Verdict:_ FOLLOW  
_Why:_ [source-backed explanation]  
_\*Further reading:_ A Philosophy of Software Design, 2nd ed. — Chapter 5, Information Hiding (and Leakage).  
_\*Study focus:_ How interface boundaries reduce coupling.
```

Chapter suggestions come **only from these six books**: Alex Xu's *System Design Interview — An Insider's Guide* (Volumes 1 and 2; Volume 2 with Sahn Lam), *Designing Data-Intensive Applications* (2nd ed.), *Fundamentals of Data Engineering*, *Algorithmic Thinking* (2nd ed.), *A Philosophy of Software Design* (2nd ed.), and **Micheal Lanham's *AI Agents in Action*, Second Edition (Manning, 2026)**. The [optional chapter guide](references/learning-chapters.md) lists edition-checked chapter pointers. Only include a genuinely relevant, verified chapter; don't force every book, repeat the same reference needlessly, or turn the report into a tutorial. Actual evidence lives in **`Source:` / `Evidence:`**, not in a book citation.

## Invocation examples

**Repeatable audit-assisted assessment (pin actual versions before invoking):**

```text
Use reazn on the specified skill package and attached Audit Skill report.
intent: assess-change
scope: subsystem
target: <skill path>
revision: <verified Git SHA or document version>
learn: off
Goal: Assess documented behavior and explicitly proposed improvements.
Use the SAME pinned audit report/version and source files for each comparison.
Classify requirements vs observed implementation vs audit suggestions;
do not infer approval or produce implementation tickets.
```



**Normal assessment (no learning references):**

```text
Run reazn on this ticket or feature brief.
Verify applicable existing patterns and give one concise four-step SDI
assessment with evidence, contracts, trade-offs and open decisions.
No interview, implementation or source edits.
```

**Assessment with study references:**

```text
Run reazn on this [feature / agent skill / workflow].
learn: on
Give the usual one-pass four-step SDI assessment.
For applicable findings, add a Further reading and Study focus line
with a verified book and chapter from the six supported books.
Keep chapter pointers separate from source evidence; no lessons or quiz.
```

## Boundaries

- **One pass, read-only:** No interactive gates, automatic implementation, ticket writes, deployments, evaluations or coding agents. Unknowns become explicit questions/limitations in the report.
- **No fabricated current state or approval:** Documentation is not proof of execution; proposed decisions are not signed off; an inaccessible source is not magically inspected.
- **Chapter accuracy:** When `learn: on`, omit an irrelevant or unverified chapter rather than guessing its edition or number. Default output never includes book fields.
- **Respect source permissions:** Do not copy confidential workplace material into public files or external systems.

The operational contract is [`SKILL.md`](SKILL.md); the interactive sibling's approval steps are **not inherited**.
