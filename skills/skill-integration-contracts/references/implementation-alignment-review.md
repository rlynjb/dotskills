# Implementation Alignment Review — Stage 3 (Optional)

**Purpose:** After Stage 4, assess modified skill source against the strongest available design evidence. Use specific human-approved IC/D terms when verified, compare against an independent proposal when approval is unavailable, or assess documented integration behavior directly when neither exists. This optional **read-only** mode stays inside `skill-integration-contracts`. It is not implementation, general code review, a runtime test or a substitute for Stage 5.

**Invocation:** `implementation_alignment_review: on`. **Default: off**; otherwise use the existing four-step Stage 3 design process and seven-section design report. Alignment review always uses the five-section report below; it never changes target files. No new flag, retained chat session or approval record is required to start a useful review.

## Inputs and adaptive review basis

- **Target source:** Actual current `SKILL.md`, referenced handoff files, relevant config/executable code, accessible branch/revision and working-tree or base/head diff if available. Read only authorized sources. A snapshot supports current documentary findings, not claims about when a change was introduced.
- **Optional independent design:** Exact approved IC/D wording, version and explicit human approval; or a separately identifiable proposal (file, supplied text or accessible prior design) with sufficiently specific terms to compare. Use existing IDs only when grounded. A Stage 2 recommendation supports provisional comparison only if it specifies an independent design expectation. A source-derived summary is not independent design evidence.
- **Approval limits:** Implementation, commit history, diff, prior CLEAR result, or a claim that a design was implemented cannot establish exact human approval. Approval of D-01 does not approve D-02. If approval or exact approved wording cannot be established, report `APPROVED BASELINE NOT VERIFIED` and state what is missing.
- **Evidence distinctions:** APPROVED DESIGN, INDEPENDENT PROPOSAL, CURRENT DOCUMENTED SOURCE, INSPECTED CODE/CONFIG, SUPPLIED OBSERVED RESULT, INFERRED, NOT VERIFIED. Documentary permissions and dispatch instructions are not proof of runtime enforcement.

### Three adaptive review modes — automatic selection

| Mode | Required evidence | Permitted source-level verdicts |
| --- | --- | --- |
| **1 — APPROVED DESIGN ALIGNMENT** | Exact independent terms plus verified explicit human approval of that version and scope | ALIGNED / PARTIALLY ALIGNED / MISMATCH / NOT VERIFIED |
| **2 — PROVISIONAL DESIGN ALIGNMENT** | Independent sufficiently specific proposed terms, approval missing/unverified | CONSISTENT WITH PROPOSAL / PARTIALLY CONSISTENT / MISMATCH (against proposal) / NOT VERIFIED |
| **3 — SOURCE-BASED INTEGRATION ASSESSMENT** | Current source and relevant changes without an independent sufficiently specific design baseline | DOCUMENTED / INCONSISTENT / GAP IDENTIFIED / NOT VERIFIED |

Select the strongest supported mode for each assessed scope. For mixed scopes, group rows by basis and label the corresponding verdicts and validation candidates. Never extend approval to another term. Without an independent design, do not fabricate IC/D wording or call a source's agreement with itself alignment. **Missing approval limits claims, not the five-section output.** Complete Sections 1–5 using the strongest available evidence. If target source is unavailable, disclose that limit rather than inventing observations/tests.

## Read-only review procedure

### Step 1 — Resolve the strongest available design basis

Inspect supplied or accessible relevant design/approval records; identify actual version, scope and owner when known. Select Mode 1 if exact approved terms are verified; otherwise report APPROVED BASELINE NOT VERIFIED and select Mode 2 for independent specific proposed terms or Mode 3 without them. Distinguish rejected/deferred terms from proposals under consideration; do not revive superseded designs or fabricate signoff. A fresh session with source and diffs alone is valid Mode 3 input. Do not require prior chat recovery before assessing accessible source.

### Step 2 — Inspect changed or current source

Read affected current skill instructions, directional handoff references and relevant executable tools/config. Inspect base/head or working-tree diff when available and cite actual file/line/section and revision. Note unknown host enforcement. Check material independent invocation, optional/required context, ownership, source provenance, failure/feedback and human decision boundaries. Use the six contract dimensions only where helpful; do not force a checklist or coordinator.

### Step 3 — Assess material guarantees according to the selected basis

**Mode 1 — Approved Design Alignment:** Compare each material approved guarantee with inspected evidence.

- **ALIGNED:** Source/code/config adequately reflects the approved term at the stated evidence level.
- **PARTIALLY ALIGNED:** Some approved expectations are reflected but a material part is missing or ambiguous.
- **MISMATCH:** Inspected source directly contradicts an approved term.
- **NOT VERIFIED:** Missing or insufficient evidence prevents a reliable comparison.

**Mode 2 — Provisional Design Alignment:** Compare actual independent proposed terms to source.

- **CONSISTENT WITH PROPOSAL:** Source adequately reflects the proposed term.
- **PARTIALLY CONSISTENT:** Some proposed expectations are reflected but a material part is missing or ambiguous.
- **MISMATCH (against proposal):** Source contradicts the proposal; not a violation of an approved agreement.
- **NOT VERIFIED:** Insufficient evidence to compare.

**Mode 3 — Source-Based Integration Assessment:** Compare producer/consumer instructions, handoff references and relevant diffs for mutual consistency and documented guarantees. Report observations and meaningful candidate guarantees, not invented approved clauses.

- **DOCUMENTED:** Current inspected source explicitly describes behavior; not approval, correctness or enforcement.
- **INCONSISTENT:** Actual inspected instructions/code conflict across a material boundary; cite both sides and explain the consequence.
- **GAP IDENTIFIED:** A concretely justified integration expectation is absent or ambiguous (e.g., required handoff field has no receiving-side behavior, or consequential revision has no stated owner). Ground the expectation and consequence in evidence, not a generic checklist.
- **NOT VERIFIED:** Source/evidence or runtime capability is missing, inaccessible or inconclusive. Missing runtime traces alone are not a source defect.

In every mode cite actual evidence, distinguish documentary instructions from inspected enforcement or supplied observed results, and avoid invented IC/D/F IDs. No source verdict demonstrates runtime PASS, change history, merge/deploy approval or actual tool authority.

### Step 4 — Route gaps and future validation

- **Approved mismatch:** Propose smallest Stage 4 correction to the existing approved agreement; rerun against the same design version and new source. If design itself needs revision, return to Stage 3 for explicit new approval before Stage 4.
- **Provisional mismatch:** Clarify whether proposal or implementation needs revision. Propose the smallest change and obtain the appropriate human decision before changing intended scope/authority. Do not imply an approved contract was violated.
- **Source inconsistency/gap:** Propose targeted clarification/correction of actual conflicting or incomplete instructions. Route unresolved ownership/design choices to Stage 3; a clear source correction may be proposed for Stage 4. No edits or approval in this review.
- **Missing independent baseline/approval:** Recover an existing record or separately review and approve a design if authoritative alignment is desired. This is not a prerequisite for source assessment, candidate preparation or separately authorized tests of documented/proposed behavior. Do not declare approved alignment complete.
- **Future Stage 5:** Prepare proportionate cases for approved, proposed or documented expectations with material behavioral uncertainty. Separately authorized controlled tests may evaluate the scoped expectation without verified approval; they cannot establish approved-contract compliance or acceptance. Resolve material contradictions, permissions and safety prerequisites before executing affected tests; unaffected cases may be scoped separately.

## Alignment-mode report (separate from seven-section design report)

**All five headings and substantive sections are mandatory in every mode.** Use mode-specific content rather than stopping when approval is missing. If evidence is unavailable, explain what is NOT VERIFIED and why.

### 1. Review Scope & Approved Baseline

- **Mode:** IMPLEMENTATION ALIGNMENT REVIEW — READ ONLY; [selected mode(s) and scope].
- **Scope:** [Actual skill connections/standalone boundary; real IC/D/F references only if supplied/found.]
- **Review basis / approval status:** [Exact approved terms/version and approval in Mode 1; independent proposal and APPROVED BASELINE NOT VERIFIED in Mode 2; current source/diff only and APPROVED BASELINE NOT VERIFIED in Mode 3. State missing evidence.]
- **Implementation reviewed:** [Actual paths, revisions/working-tree changes and limits.]
- **What this review establishes:** [Approved alignment vs provisional consistency vs source observations; actual behavior remains unverified unless supplied evidence establishes it.]

### 2. Contract Alignment Coverage

Always assess available material behavior in a compact source-backed Markdown table. Use the appropriate schema, grouping mixed scopes by basis. Avoid fake IDs, empty tables and placeholder clauses.

**Mode 1: Approved Design Alignment**

| Approved clause | Current source evidence | Source-level verdict |
| --- | --- | --- |
| [Actual approved IC/version/term] | [Exact inspected file/section] | [ALIGNED / PARTIALLY ALIGNED / MISMATCH / NOT VERIFIED — reason] |

**Mode 2: Provisional Design Alignment**

| Proposed clause / independent design reference | Current source evidence | Provisional verdict |
| --- | --- | --- |
| [Actual independent proposed term; approval unverified] | [Exact inspected file/section] | [CONSISTENT WITH PROPOSAL / PARTIALLY CONSISTENT / MISMATCH (against proposal) / NOT VERIFIED — reason] |

**Mode 3: Source-Based Integration Assessment**

| Contract dimension / documented behavior | Source evidence and consistency assessment | Status |
| --- | --- | --- |
| [Material behavior, e.g. optional handoff or ownership; no fabricated IC] | [Specific producer/consumer links; actual agreement, conflict, justified gap or evidence limit] | [DOCUMENTED / INCONSISTENT / GAP IDENTIFIED / NOT VERIFIED — reason] |

In Mode 3 assess both sides of a connection when accessible; explain the boundary and implications instead of only restating implementation text. Keep documented expectations separate from inferred candidate requirements. Use applicable dimensions and cite evidence. No purported approved-clause rows without verified approval. If no source is inspectable, explain the access limitation and needed evidence here.

### 3. Material Gaps & Evidence Limits

Use concise **vertical notes** for material partial alignment, contradictions, gaps and consequential unknowns, including missing independent baseline/approval.

- **Expectation / basis:** [Actual approved term, independent proposal or documented behavior and evidence-based issue.]
- **Inspected source and evidence level:** [Actual file/revision or inaccessible area.]
- **Assessment / impact:** [Mode-specific verdict; meaningful consequence.]
- **Smallest next correction or evidence needed:** [Proposed Stage 4 correction, Stage 3 clarification, missing evidence or separate validation; no edits.]
- **Design decision impact:** [Existing approved decision unchanged, or proposal/unresolved decision requiring human review; no invented D-xx.]

Zero material gaps is valid. In Mode 2/3, if supported, report no material proposal contradictions or source inconsistencies in inspected scope, not "no deviations from approved design." Distinguish absent approval, source gaps and unverified runtime behavior; never inflate unknowns into defects.

### 4. Next Stage & Iteration Handoff

- **Overall outcome:** [Mode(s), supported conclusions and remaining limits.]
- **Stage 3 design / baseline:** [Verified approved terms unchanged, or recover independent design/approval if needed for authoritative alignment; real unresolved decisions.]
- **Stage 4 implementation:** [Smallest proposed correction for actual mismatch/inconsistency, or none indicated by assessed evidence; no unsupported approval/completion claim.]
- **Next stage:** [Separate Stage 5 candidates for actual basis; prerequisites for execution; unapproved expectations cannot establish approved-contract compliance. Do not block candidate preparation because approval is missing.]
- **Rerun / future baseline:** [Retain approved version if available; otherwise retain independent proposal reference or inspected revision and optionally obtain independent approval in a separate task.]
- **Boundary:** Review never grants permission to merge, deploy, publish, change source or invoke runtime controls.

### 5. Stage 5 Candidates — NOT EXECUTED

**Required output format:** Render this section in full in every alignment-mode report. Use the three visible blocks below in order: **What we are doing here**, **How to proceed with Stage 5** (four numbered steps), and **Validation candidate cards**. Do not collapse this section into a table or key-only list, even on a concise rerun or when previous reports used such a table. Instructions in this reference specify the content of the generated report, not optional background for the reviewing agent. If no candidate is justified, retain both explanatory blocks and state the reason instead of inventing a card.

**What we are doing here:** Explain the selected review basis: approved source alignment, consistency with an independent proposal, or current documented integration behavior. Stage 5 — Validation & Iteration exercises skills to determine whether the corresponding observable expectations hold. Source assessment does not establish runtime correctness, tool enforcement or workflow readiness. If approval is unverified, label candidates as provisional or source-based; future tests cannot establish approved-contract compliance. Prepare a separate validation task, not execution.

**What a V-xx candidate means:** `V-xx` is a report-local validation scenario identifier, not an industry-defined test type. Give every candidate a descriptive title that explains the behavior under review, rather than displaying a bare key. The Given–When–Then pattern is an established way to structure behavioral scenarios: Given = initial state and test setup, When = the action performed, Then = the observable assertions that should hold. Expected evidence is what the future evaluator will inspect to determine whether those assertions passed; it is not evidence already collected.

#### How to proceed with Stage 5

Render all four numbered steps below as user-facing instructions, concisely adapted to the actual review basis, scope and Section 4 routing:

1. **Confirm the validation scope and prerequisites.** Identify the inspected revision and actual basis: approved IC/D version, independent proposal or documented behavior. Resolve relevant safety, permissions and blocking inconsistencies; scope unaffected cases separately. Missing approval blocks validation as approved-contract compliance, not candidate preparation or separately authorized controlled tests of documented/proposed expectations. No review grants execution or production-write permission.
2. **Check coverage and choose the smallest useful level.** Map material expectations under the actual basis to verified evidence and candidate scenarios. Start with standalone behavior where applicable, then the scoped integration, then representative end-to-end paths only when broader scope is separately authorized and relevant. Include meaningful success, missing/conflicting input, optional handoff, ownership/approval, and feedback or recovery cases where the contract calls for them. Do not require every category or a full workflow run to validate one connection. Identify material coverage gaps instead of asserting completeness.
3. **Turn candidates into executable evaluations.** In a separate Stage 5 task, use the actual review basis, target revision and these cards to select representative controlled/synthetic fixtures, authorized execution environments, explicit assertions and evidence collection. Use Evaluate Skill where its runner and fixtures support the scoped evaluation; otherwise define an appropriate controlled manual or integration test. Use Profile Agent Workflow separately when available traces, latency, context usage or cost help diagnose execution. Profiling alone is not a correctness evaluation. This alignment skill does not invoke either tool or generate claims of completed tests.
4. **Execute, assess, and iterate (future Stage 5 work only).** Compare collected artifacts and available traces with each assertion; record PASS, FAIL, INCONCLUSIVE/NOT VERIFIED, or NOT EXECUTED as warranted. If an approved guarantee is violated, route the smallest Stage 4 correction and re-evaluate. For provisional or documented expectations, assess whether behavior, instructions or intended design need clarification; obtain human decisions when design/authority must change. If an approved guarantee needs revision, return to Stage 3 for new explicit approval before implementation. Missing or insufficient evidence calls for additional authorized verification rather than an invented pass or automatic redesign.

#### Validation candidate cards

Use concise **vertical Markdown cards**, separated by whitespace; no table (including a compact three-column table), key-only list, or prose-only summary. Render each of the seven fields below with its exact readable label; Given and When remain separate. Each card must stand on its own and answer what is being tested, how it would be tested, what must pass, and how the result would be demonstrated. Include the following fields in order:

**V-01 — [Descriptive scenario title]**

- **Purpose / contract guarantee:** [Behavior to validate and why it matters. Explicitly label **Basis: APPROVED DESIGN**, **Basis: INDEPENDENT PROPOSAL — APPROVAL NOT VERIFIED**, or **Basis: CURRENT DOCUMENTED SOURCE — APPROVAL NOT VERIFIED**. Link actual approved IC/D version, independent proposal, or inspected source file/revision respectively; use real F-xx (Cx) only if supplied. In source-based mode distinguish documented behavior and any inferred candidate expectation; never invent IC/D IDs.]
- **Validation level:** [Standalone / Integration / End-to-end; choose the smallest justified level. Do not imply an entire workflow is in scope.]
- **Given — Test setup:** [Initial state, representative fixture/input, available or deliberately unavailable dependencies, relevant permissions/approval state and controlled environment. Identify setup or authorization still needed; no invented fixtures or actual execution.]
- **When — Execution:** [Specific future action: invoke the identified skill with that input, perform the scoped handoff, or exercise an applicable feedback path under the test conditions. Keep it proportional and distinguish human choice from automatic dispatch.]
- **Then — Assertions:** [Specific observable conditions that must hold for the specified approved/proposed/documented expectation. Use separate short bullets for independent checks; distinguish artifact assertions from behavior or permission assertions. A negative assertion such as no unauthorized tool action requires suitable evidence, not just an agent's statement.]
- **Expected evidence:** [Concrete output artifact, source/requirement identifiers, decision/status record, controlled harness result, tool/action receipt or available trace needed to evaluate each assertion. State evidence limitations and missing instrumentation; do not assume a trace exists or treat lack of a trace as proof that an action did not happen.]
- **Status:** NOT EXECUTED. [State any prerequisite correction, approval or evidence access needed before the case can run.]

Reuse actual earlier V-xx candidates and their identifiers when their scope and meaning are unchanged. Refine descriptions/assertions without silently changing their basis or any approved IC/D baseline. If a prior candidate's approval record is unavailable, retain its behavior/ID only when justified by accessible evidence and explicitly re-label its basis. If splitting a candidate into meaningful subcases or adding a justified candidate, make the relationship explicit and use distinct identifiers; do not manufacture a fixed V-01–V-04 catalog or renumber unchanged candidates. Check that every reference resolves to the actual report/baseline or supplied earlier evidence. When no prior candidates exist, create only the necessary report-local IDs. If no additional Stage 5 candidate is justified, say `No additional Stage 5 candidate justified` with the reason. If the approved baseline is missing, disclose that limitation and still draft materially justified candidates from independent proposals or documented behavior, including evidence-based gaps where an expectation can be defined without inventing authority. Never present these as validation of approved terms. Missing approval alone is not a reason to omit candidate cards. Candidate design is not an executed test, PASS result, or permission to run.

**Final output check (before delivering the report):** Verify that the actual rendered Section 5 includes the explanatory blocks and four next steps, every justified V-xx has its descriptive title and all seven named fields, and every candidate is NOT EXECUTED. If the answer still contains a candidate table or missing labels, rewrite Section 5 before returning it. Keep verified approved design unchanged and check each card's explicit basis and unverified approval where applicable. Confirm Sections 1–5 are all present even without an independent baseline.

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

If the actual review basis supports both skills' standalone paths, repeat with reversed roles or specify subcases. In source-based mode the same scenario can be grounded in an inspected standalone entry instruction instead of an approved IC; label Basis: CURRENT DOCUMENTED SOURCE — APPROVAL NOT VERIFIED, cite it and do not claim approval. Use a different scenario title and setup for a different guarantee. Do not copy this example as an actual finding or assume it is applicable to every skill pair.

## Interaction with existing optional design reviews

`quality_review`, `quality_questions`, `review_lenses`, `industry_framework_review` and `industry_frameworks` are **design-mode** options. If combined with `implementation_alignment_review: on`, perform the alignment-mode report **only**; state that other design review flags were not run and that a separate contract-design invocation can reassess/revise the approved design. Do not silently regenerate or overwrite approved IC/D wording.

## Example (synthetic only)

The inspected receiving `SKILL.md` documents optional PRD context and independent invocation. With an independently verified approved IC specifying this, the verdict may be ALIGNED — CURRENT DOCUMENTED SOURCE (Mode 1). With an independent proposal but no approval, it may be CONSISTENT WITH PROPOSAL (Mode 2). With source alone, it is DOCUMENTED (Mode 3); compare sender/receiver instructions for actual inconsistencies and prepare a source-based standalone candidate. In all modes actual automatic dispatch or security enforcement is NOT VERIFIED AT RUNTIME without suitable evidence. Missing approval is not a source defect, and a successful source-based test cannot retroactively approve the design.
