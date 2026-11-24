# Implementation Alignment Review — Stage 3 (Optional)

**Purpose:** After Stage 4, compare modified skill source with the **specific human-approved** Stage 3 integration contract (`IC-xx`) and decision (`D-xx`). This optional, **read-only** mode stays inside `skill-integration-contracts`. It is not a script, implementation, general code review, runtime test or substitute for Stage 5.

**Invocation:** `implementation_alignment_review: on`. **Default: off**; otherwise use the existing four-step Stage 3 design process and seven-section design report. The alignment mode uses the separate report below and never changes target files.

## Inputs and approval baseline

- **Approved baseline:** actual exact IC-xx terms, linked D-xx decisions, explicit human approval of those exact terms, and design version/revision if available. Approval of D-01 does not authorize separate D-02; a previous `CLEAR` score, Stage 2 recommendation, or proposed text is not approval.
- **Implemented source:** actual updated target `SKILL.md` and affected references/config/executable code where relevant, links and inspected revision or base/head diff if available. A current source snapshot can prove current documentary alignment, but **without a diff it cannot prove which changes were newly introduced**.
- **Read-only access:** Inspect only authorized source and supplied evidence. Do not change files, invoke target skills, run tests, publish, approve, or grant permissions.
- **Missing approved design:** Report `APPROVED BASELINE NOT VERIFIED`, identify what exact approved text or decision is unavailable, and do **not** mark anything ALIGNED to an approved contract. A limited clearly labeled comparison to PROPOSED text may be useful, never authoritative.
- **Evidence distinctions:** `APPROVED DESIGN`, `CURRENT DOCUMENTED SOURCE`, `INSPECTED CODE/CONFIG`, `SUPPLIED OBSERVED RESULT`, `NOT VERIFIED`. Documentary instructions about permissions or automatic dispatch are not proof of actual host/runtime enforcement.

## Read-only comparison procedure

### Step 1 — Resolve the approved IC/D version

Identify exact approved clauses and D-xx decisions, owner and any available design revision. Exclude rejected, deferred, unapproved, changed or superseded decisions. Check the design applies to the inspected connections; don't invent an approval date or baseline.

### Step 2 — Inspect changed or current source

Read affected current skill instructions, references and relevant executable tools/config only when accessible. Inspect base/head diff when available and cite actual source file/line/section. Note missing revisions and out-of-scope host enforcement. Check independent invocation, optional context, source provenance, failure/feedback and human decision boundaries where approved.

### Step 3 — Assess material guarantees

Compare **each material approved guarantee**, not each generic lens or every optional field. Use four source-level verdicts:

- **ALIGNED:** Inspected current source/code/config adequately reflects the approved guarantee at the stated evidence level. Does **not** imply runtime PASS, permission enforcement, newly introduced behavior or approved deployment.
- **PARTIALLY ALIGNED:** Some approved expectations are reflected but a material part is missing or ambiguous.
- **MISMATCH:** Direct inspected source contradicts an approved guarantee, including a formerly optional handoff made mandatory or a changed approval owner.
- **NOT VERIFIED:** Missing/inaccessible evidence or insufficient approval/version information prevents a reliable source-level comparison. **Absent runtime traces alone do not turn source-ALIGNED documentation into a mismatch or defect.**

Link each verdict to the **specific approved IC-xx wording** and the **actual inspected source evidence**; where relevant distinguish `ALIGNED — DOCUMENTED` from host/tool enforcement still `NOT VERIFIED AT RUNTIME`. One IC can have different outcomes for different guarantees. No new findings-ID family.

### Step 4 — Route gaps to the appropriate stage

- **Implementation mismatch / missing approved wording:** Stage 4 makes the smallest correction to the existing approved agreement. Rerun this mode on the **same approved design version** and a new current-source revision. Do not silently rewrite IC-xx.
- **Approved design no longer suitable or a new trust/ownership decision required:** Separate Stage 3 design revision, new D-xx human review/approval, then Stage 4 changes. Preserve the old approved version for comparison.
- **Source appears aligned, execution unverified:** Stage 5 runs authorized evaluations/integration tests; this mode can propose V-xx candidates but cannot run or mark them PASS.
- **Approved baseline missing:** Return to design-baseline recovery or explicit human approval; do not declare alignment complete.

## Alignment-mode report (separate from seven-section design report)

### 1. Review Scope & Approved Baseline

- **Mode:** IMPLEMENTATION ALIGNMENT REVIEW — READ ONLY.
- **Scope:** [Approved connections, exact IC-xx/D-xx and relevant Stage 2 F-xx (Cx) only if actually present.]
- **Approved design evidence and revision:** [Source link, human approval scope, version or `APPROVED BASELINE NOT VERIFIED`.]
- **Implementation reviewed:** [Affected current file paths, accessible base/head or revision and evidence limits.]

### 2. Contract Alignment Coverage

One compact Markdown table with **a row per material approved guarantee**, grouping rows by existing IC-xx. Avoid one row per generic quality category or introducing an `A-xx` ID series.

| Approved clause | Current source evidence | Source-level verdict |
| --- | --- | --- |
| [IC-01 — optional context] | [Exact inspected file/section] | [ALIGNED / PARTIALLY ALIGNED / MISMATCH / NOT VERIFIED — brief reason] |
| [IC-01 — human approval] | [Actual source/host evidence or limitation] | [Verdict with DOCUMENTED vs ENFORCED distinction] |

If no **verified approved baseline** is available, **omit purported approved guarantee rows**; instead state the missing approval/version evidence and optionally show a *provisional comparison to proposed terms*, not ALIGNED.

### 3. Material Gaps & Evidence Limits

Use concise **vertical notes** only for material partial alignment, contradictions or consequential unknowns:

- **Approved term and source:** [Exact IC-xx/D-xx wording and version.]
- **Inspected source and evidence level:** [Actual current file/revision or inaccessible area.]
- **Assessment / impact:** [One of the four verdicts; meaningful effect on connection or standalone behavior.]
- **Smallest next correction or evidence needed:** [Stage 4 proposal only, or missing evidence; no edits performed.]
- **Design decision impact:** [Existing D-xx unchanged or needs separate Stage 3 redesign/human approval.]

Zero material deviations is valid; don't fabricate warnings to fill the section.

### 4. Next Stage & Iteration Handoff

- **Overall source-level outcome:** [What is aligned, partially aligned, mismatched, or not verified; include evidence scope.]
- **Routing:** [Stage 4 correction / Stage 3 redesign & approval / supply approved baseline / Stage 5 test.]
- **Same-baseline rerun:** [Which approved IC/D version and updated source revision to compare next.]
- **Boundary:** Source review never grants permission to merge, deploy, publish, or invoke runtime controls.

### 5. Stage 5 Candidates — NOT EXECUTED

Only list justified V-xx Given/When/Then checks for **actual** runtime dispatch, authorization, failure response, or evidence continuity that source inspection cannot establish. Never invent PASS. Otherwise say `No additional Stage 5 candidate justified`.

## Interaction with existing optional design reviews

`quality_review`, `quality_questions`, `review_lenses`, `industry_framework_review` and `industry_frameworks` are **design-mode** options. If combined with `implementation_alignment_review: on`, perform the alignment-mode report **only**; state that other design review flags were not run and that a separate contract-design invocation can reassess/revise the approved design. Do not silently regenerate or overwrite approved IC/D wording.

## Example (synthetic only)

An approved IC-01 makes a PRD optional, and the inspected receiving `SKILL.md` documents optional context and independent invocation. That guarantee may be `ALIGNED — CURRENT DOCUMENTED SOURCE`, while any actual automatic dispatch or security enforcement remains `NOT VERIFIED AT RUNTIME` without host/run evidence. Do not turn the latter into an unnecessary implementation defect.
