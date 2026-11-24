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

**What we are doing here:** The alignment review checks whether the implementation reflects the approved design in source. Stage 5 — Validation & Iteration checks whether the implemented skills actually behave according to the approved contracts when exercised. A source-level ALIGNED verdict does not establish behavioral correctness, tool-level enforcement or workflow readiness. This section prepares the handoff to that separate validation stage; it does not execute any evaluation.

**What a V-xx candidate means:** `V-xx` is a report-local validation scenario identifier, not an industry-defined test type. Give every candidate a descriptive title that explains the behavior under review, rather than displaying a bare key. The Given–When–Then pattern is an established way to structure behavioral scenarios: Given = initial state and test setup, When = the action performed, Then = the observable assertions that should hold. Expected evidence is what the future evaluator will inspect to determine whether those assertions passed; it is not evidence already collected.

#### How to proceed with Stage 5

Explain the next steps concisely, adapted to the actual approved scope and Section 4 routing:

1. **Confirm the validation scope and prerequisites.** Use the exact approved IC/D version and inspected implementation revision. Resolve any required Stage 4 corrections or missing approval baseline before claiming validation readiness for affected terms; unaffected approved terms may be scoped separately. Approval of a design is not authorization to execute tests or modify production artifacts.
2. **Check coverage and choose the smallest useful level.** Map material approved guarantees to existing verified evidence and candidate scenarios. Start with standalone behavior where applicable, then the approved skill-to-skill integration, then representative end-to-end workflow paths only when that broader scope is separately approved and relevant. Include meaningful success, missing/conflicting input, optional handoff, ownership/approval, and feedback or recovery cases where the contract calls for them. Do not require every category or a full workflow run to validate one connection. Identify material coverage gaps instead of asserting completeness.
3. **Turn candidates into executable evaluations.** In a separate Stage 5 task, use the approved baseline, actual target revision and these cards to select representative controlled/synthetic fixtures, authorized execution environments, explicit assertions and evidence collection. Use Evaluate Skill where its runner and fixtures support the scoped evaluation; otherwise define an appropriate controlled manual or integration test. Use Profile Agent Workflow separately when available traces, latency, context usage or cost help diagnose execution. Profiling alone is not a correctness evaluation. This alignment skill does not invoke either tool or generate claims of completed tests.
4. **Execute, assess, and iterate (future Stage 5 work only).** Compare collected artifacts and available traces with each assertion; record PASS, FAIL, INCONCLUSIVE/NOT VERIFIED, or NOT EXECUTED as warranted. If the source or runtime implementation violates the approved guarantee, route the smallest correction to Stage 4 and re-evaluate. If the approved guarantee itself needs revision, return to Stage 3 for a new explicitly approved design before implementing changes. Missing or insufficient evidence calls for additional authorized verification rather than an invented pass or automatic redesign.

#### Validation candidate cards

Use concise **vertical Markdown cards**, separated by whitespace; no wide table or key-only list. Each card must stand on its own and answer what is being tested, how it would be tested, what must pass, and how the result would be demonstrated. Include the following fields in order:

**V-01 — [Descriptive scenario title]**

- **Purpose / contract guarantee:** [Plain-English behavior to validate, why it matters, exact approved IC-xx clause/version and related D-xx or supplied F-xx (Cx) when material. Refer to actual entries only.]
- **Validation level:** [Standalone / Integration / End-to-end; choose the smallest justified level. Do not imply an entire workflow is in scope.]
- **Given — Test setup:** [Initial state, representative fixture/input, available or deliberately unavailable dependencies, relevant permissions/approval state and controlled environment. Identify setup or authorization still needed; no invented fixtures or actual execution.]
- **When — Execution:** [Specific future action: invoke the identified skill with that input, perform the approved handoff, or exercise an applicable feedback path under the test conditions. Keep it proportional and distinguish human choice from automatic dispatch.]
- **Then — Assertions:** [Specific observable conditions that must hold for the approved guarantee. Use separate short bullets for independent checks; distinguish artifact assertions from behavior or permission assertions. A negative assertion such as no unauthorized tool action requires suitable evidence, not just an agent's statement.]
- **Expected evidence:** [Concrete output artifact, source/requirement identifiers, decision/status record, controlled harness result, tool/action receipt or available trace needed to evaluate each assertion. State evidence limitations and missing instrumentation; do not assume a trace exists or treat lack of a trace as proof that an action did not happen.]
- **Status:** NOT EXECUTED. [State any prerequisite correction, approval or evidence access needed before the case can run.]

Reuse actual earlier V-xx candidates and their identifiers when their scope and meaning are unchanged. Refine their descriptions and assertions without silently changing the approved IC/D baseline. If splitting a candidate into meaningful subcases or adding a justified candidate, make the relationship explicit and use distinct identifiers; do not manufacture a fixed V-01–V-04 catalog or renumber unchanged candidates. Check that every reference resolves to the actual report/baseline or supplied earlier evidence. When no prior candidates exist, create only the necessary report-local IDs. If no additional Stage 5 candidate is justified, say `No additional Stage 5 candidate justified` with the reason. If the approved baseline is missing, explain the blocker; do not present provisional scenarios as validation of approved terms. Candidate design is not an executed test, PASS result, or permission to run.

**Illustrative candidate (synthetic, not a fixed V-01 definition or an actual result):**

**V-01 — Standalone execution without the partner skill**

- **Purpose / contract guarantee:** Verify that the receiving skill's standalone entry remains usable without mandatory upstream context, as specified by the example approved optional-handoff agreement. In an actual report, link the exact approved IC/D terms.
- **Validation level:** Standalone.
- **Given — Test setup:** In an authorized controlled environment, only the receiving skill is available; the partner skill is not installed or accessible. Supply sufficient normal starting information, without a PRD.
- **When — Execution:** Invoke the receiving skill directly with that input.
- **Then — Assertions:**
  - Produce the expected standalone artifact with its required content.
  - Do not make the absent optional PRD or partner installation a prerequisite.
  - Do not invoke the partner skill; verify this from controlled environment or tool execution evidence rather than self-report.
- **Expected evidence:** Actual generated standalone artifact, test environment/fixture record, and available invocation/dispatch evidence sufficient to assess the absence of a partner invocation. If the latter cannot be established, mark that assertion INCONCLUSIVE/NOT VERIFIED in the future run.
- **Status:** NOT EXECUTED.

If the actual approved contract protects both skills' standalone paths, repeat the test with the roles reversed or specify two distinct subcases within the candidate. Use a different scenario title and setup for a different guarantee. Do not copy this example as an actual finding or assume it is applicable to every skill pair.

## Interaction with existing optional design reviews

`quality_review`, `quality_questions`, `review_lenses`, `industry_framework_review` and `industry_frameworks` are **design-mode** options. If combined with `implementation_alignment_review: on`, perform the alignment-mode report **only**; state that other design review flags were not run and that a separate contract-design invocation can reassess/revise the approved design. Do not silently regenerate or overwrite approved IC/D wording.

## Example (synthetic only)

An approved IC-01 makes a PRD optional, and the inspected receiving `SKILL.md` documents optional context and independent invocation. That guarantee may be `ALIGNED — CURRENT DOCUMENTED SOURCE`, while any actual automatic dispatch or security enforcement remains `NOT VERIFIED AT RUNTIME` without host/run evidence. Do not turn the latter into an unnecessary implementation defect.
