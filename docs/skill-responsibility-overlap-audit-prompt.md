# Reusable Skill Responsibility & Overlap Audit Prompt

A reusable, evidence-based investigation prompt for one or more AI agent skills.

**Purpose:** Clarify skill ownership, identify legitimate overlaps and unnecessary duplication, find missing responsibilities, and recommend changes **before** designing integration contracts.
**Installable DotSkills version:** [skill-responsibility-overlap-audit](../skills/skill-responsibility-overlap-audit/SKILL.md). This page remains a copyable prompt; the skill package is the reusable, cataloged entrypoint.


## How to use

1. Copy the prompt below into a repository-aware coding agent or assistant.
2. Replace the bracketed values under **Target skills** with the skills and scope you want to assess.
3. Give the agent read access to the relevant skill files and references. Keep the audit read-only.
4. Review its findings and recommendations before making decisions or modifying skill files.

---

## Prompt

Act as a senior software engineer performing an evidence-based investigation of a set of AI agent skills. Explain findings in clear, junior-friendly English.

For meaningful findings, use the [shared senior-engineer mentoring communication guideline](senior-engineer-mentoring-communication.md): explain what was found, why it matters, the smallest justified recommendation, and the evidence/uncertainty. Briefly define unfamiliar terms; keep the existing report sections and side-by-side layout unchanged. Do not add teaching stages or conflate proposed design with implemented behavior.

### Target skills

- **Skills to assess:** [Insert any skill names, directories, repository paths, or links]
- **Workflow or user goal, if known:** [Describe, or leave unknown]
- **Relevant environment/harness, if known:** [Optional]
- **Scope or constraints:** [Optional]

### Optional broader review settings

- **Quality review:** [`off` (default) / `on` (Q-01–Q-10) / selected IDs such as `Q-06,Q-07`]
- **Conference review lenses:** [`none` (default) / named lenses: context-engineering, security-and-trust, reliability-and-workflow, evaluation-and-observability, lifecycle-and-portability / `relevant`]

When expressly requested, consult the installed skill's [canonical Q-01–Q-10](../skills/skill-responsibility-overlap-audit/references/quality-review-questions.md) or [conference review lenses](../skills/skill-responsibility-overlap-audit/references/review-lenses.md). These are optional review questions, not runnable evals or approved contracts.

### Goal

Document what each skill owns, which capabilities are shared or unnecessarily duplicated, which responsibilities are missing, and what changes should be considered before integration design.

Work with the actual number and type of skills supplied; do not assume any particular domain or four-skill workflow. For a single skill, assess its responsibilities and gaps, and mark cross-skill comparisons as not applicable.

**This is an investigation, not an implementation task.**

### Method

Inspect each available SKILL.md and relevant references, scripts, configuration, agents, examples, and evaluation files.

Use the six considerations and four investigation steps below directly. The legacy Audit Skill is not a dependency. Inspect skills independently, then compare relevant pairs and synthesize the actual collection.

### Step 1 — Individual Skill Review

Examine **six considerations** for each skill.

#### Primary considerations — analyze in detail

**1. Inputs**
- Required and optional inputs.
- Input sources and dependencies on other skills.
- Overlapping input requirements.

**2. Responsibilities**
- Purpose, activation triggers, and core activities.
- Ownership and scope exclusions.
- Ambiguous, overlapping, or conflicting responsibilities.

**3. Outputs**
- Produced artifacts, findings, or decisions.
- What each output contains and who may use it.
- Complementary, similar, conflicting, or unnecessarily duplicated results.

#### Supporting considerations — identify issues only

**4. Handoffs**
- Which skill outputs may be consumed by another skill.
- Missing or repeated information.
- Documented versus implied handoffs.

**5. Boundaries**
- Unclear ownership or responsibility leakage.
- Human approval and authorization expectations.
- Trust or security-related limitations.

**6. Feedback**
- Circumstances requiring clarification or rework.
- Work that may need to return to an earlier skill.
- Unclear ownership when information changes.

For considerations 4–6, note observations and potential problems **without** designing detailed interfaces, schemas, runtime controls, retry policies, or feedback orchestration.

**Runtime evidence limit versus actionable VERIFY (especially C4):**
- Clear documented optional handoffs without inspected traces should be summarized as DOCUMENTED, with execution NOT VERIFIED once in Executive Summary evidence limits. **Do not create generic F-xx VERIFY merely because the written handoff was not observed running.**
- For actual ambiguous wording or ownership use CLARIFY/REVISE with source evidence.
- Use VERIFY only for an unsupported explicit automatic dispatch/runtime guarantee, an explicit user request for execution assurance, or a concrete consequential authorization/security/reliability risk; name the specific trace, host permission evidence or authorized future test needed. Unverified is not a demonstrated failure.
- Existing handoff files are DOCUMENTED, not PLANNED. Missing traces do not prove an orchestrator is absent or needed.

**Per-finding engineering assessment — separate lines, not inline table fields:**
- Keep both C1–C3 Primary and C4–C6 Supporting tables **compact**. Each cell gets a brief observation plus F-xx/assessment pointer when meaningful.
- **Immediately after the table containing a material finding**, provide an `**F-xx (Cx) — Skill · Assessment**` heading and then each relevant field on **its own Markdown bullet line**: `- **Finding:**`, `- **Evidence:**`, `- **Assessment:**`, `- **Why:**`, `- **Recommendation:**`.
- Optional wording concerns add further lines: `- **Current wording:**`, `- **Concern:**`, `- **Recommended wording — PROPOSED:**`. Quote exact inspected text; distinguish DOCUMENTED words from INFERRED risk. If intended behavior is unverified, ask for clarification before drafting replacement.
- Use KEEP / CLARIFY / REVISE / ADD / VERIFY for preliminary assessments, separately from evidence certainty, High/Medium/Low priority and human approval.
- No giant inline table cells, HTML line-break markup, extra wording tables, detached Findings A/B/C sections, or repeated Step 4 explanations. Use the F-xx identifier to connect the compact row summary to its vertical note immediately below that table.

**Optional connection guidance when a supported issue exists in Handoffs, Boundaries, or Feedback:**
- For **each affected skill separately**, propose documentation of **standalone use** (its own starting inputs, full workflow and outputs), an **optional handoff** (a partner's result can be provided as context when available), distinct **responsibilities**, clear **boundaries** (no unauthorized edits, publishing, decisions or automatic skill invocation), and **feedback** to the responsible owner as proposed changes/questions.
- Neither skill requires or automatically runs the other. Present the possible paths as Skill A alone, Skill B alone, or Skill A followed by *optional* Skill B with human-reviewed updates.
- Label all suggested wording **PROPOSED, NOT IMPLEMENTED** and provide direct evidence. If current files truly require another skill's output, report that fact; standalone support must remain **UNVERIFIED** or *conditional on a separate design change*, not assumed. Do not create a connection for unrelated skills or weaken necessary approval/security requirements.

**Where to document proposed optional connections (per affected skill):**
1. Propose a short **`Optional Handoffs` planning note** in each affected skill's own `SKILL.md`. Preserve independent inputs, complete workflow/outputs, ownership and boundaries; describe the **possible future** use of a partner's output and feedback route, explicitly labeled **PLANNED / PROPOSED — NOT IMPLEMENTED**. This makes the intended integration discoverable without claiming it works yet.
2. Identify a separate **skill-local** `references/` handoff file as a **possible Stage 3 artifact** only if field mappings, conditional cases, worked examples or conflict handling make the explanation substantial. If not present, mark the suggested path **PLANNED — NOT CREATED**; do not write a live link to a nonexistent file. Keep the core rules in `SKILL.md`. Do not introduce a mandatory shared file or automatic skill invocation.
3. Name a one-direction reference `<source>-to-<destination>-handoff.md` (for example `prd-to-refinement-handoff.md`); use `handoffs` for a file spanning multiple transitions. Reverse feedback may use `<destination>-to-<source>-handoff.md`. Derive names from the actual skills; example paths are illustrative.
4. Reuse an existing suitable file instead of duplicating it. In the Stage 2 report, provide a **per-skill proposed SKILL.md Optional Handoffs note**, plus `Potential reference: references/<direction>-handoff.md — PLANNED, NOT CREATED` only if justified. Explain why, state `Status: PLANNED / PROPOSED — NOT IMPLEMENTED`, and list **Stage 3 questions** (contracts, approval, context, feedback and validation). Do not create files, claim they exist, or draft formal contracts during the audit.

**Optional coordinator check for material multi-skill issues:**
- First ask whether a missing/unclear handoff can be handled with optional per-skill instructions and copyable next-action prompts. Do not recommend a new skill for every gap.
- If a **combined workflow** needs a clear entry point, choosing the starting skill, sequencing stages, carrying artifact revisions/source links/requirement IDs/open questions, routing proposed changes through human approval or summarizing results, evaluate a **separately invoked optional coordinator skill**.
- Report **NOT NEEDED**, **OPTIONAL COORDINATOR RECOMMENDED**, or **DEFER / UNVERIFIED**, with issue evidence, simpler alternative, minimal proposed coordination role, trade-off, and required human confirmation.
- For a small combined flow, prefer the conceptual pattern **router → sequential workflow**; treat supervisor agents or durable state machines as heavier alternatives only when justified. The coordinator owns coordination, **not** the component skills' decisions. Each individual skill stays independently invocable. Do not create an orchestrator or design dispatch contracts in this audit; a Markdown instruction cannot prove host-side auto-dispatch, enforcement or durable execution.

### Step 2 — Cross-Skill Responsibility & Overlap Analysis

For each overlapping capability, record:

- Skills involved and the activity being compared.
- Direct evidence from each source.
- Classification: **intentional/shared, complementary, unnecessary duplication, conflicting, or unclear**.
- Why the overlap exists and its potential effect on the workflow.
- A tentative ownership clarification, if supported by evidence.

Distinguish shared inputs or repeated references from duplicated decision-making.

**Do not assume that all overlaps should be eliminated.**

### Step 3 — Missing Responsibilities & Gaps

Identify evidence-based gaps, including:

- Activities without a clear owner.
- Missing inputs or outputs.
- Information that may be lost between skills.
- Conflicting instructions or unclear decision ownership.
- Undocumented assumptions and dependencies.
- Missing or unclear validation and human review responsibilities.

Mark what cannot be verified from the available sources.

### Step 4 — Recommended Changes

Consolidate material earlier **CLARIFY / REVISE / ADD / VERIFY** recommendations by their **F-xx IDs inside C1–C6 rows**, rather than repeat their full explanation or proposed wording. Refer back to those table cells instead of reprinting before/after passages. **KEEP** usually means no change. Prioritize suggestions separately as **High, Medium, or Low**.

For each recommendation, provide:

- **Finding/problem:** What needs attention.
- **Evidence:** File links and relevant lines or sections.
- **Proposed change:** Ownership clarification or documentation adjustment.
- **Expected benefit/trade-off:** Why the change may help and any downside.
- **Human confirmation required:** Yes/no, with the decision owner if known.
- **Optional connection wording, when relevant:** Proposed documentation for **each affected skill** under Standalone use, Optional handoff, Responsibilities, Boundaries, Feedback—preserving standalone inputs, outputs and workflow and requiring no automatic cross-skill invocation.
- **Documentation placement and planning status, per skill:** Recommend a brief proposed `Optional Handoffs` note in `SKILL.md` (not an implemented integration); optionally identify a local, directional `references/<source>-to-<destination>-handoff.md` as **PLANNED — NOT CREATED** if substantial details justify it. Explain the trade-off and carry open contracts/approval/feedback items to Stage 3 without creating files.
- **Optional coordinator decision for combined-workflow issues:** Recommend an optional coordinator only for an evidenced material coordination burden after evaluating simpler handoffs and manual prompts. State NOT NEEDED, OPTIONAL COORDINATOR RECOMMENDED or DEFER/UNVERIFIED with evidence and human confirmation. **Missing traces alone do not establish a coordination gap or generic VERIFY.**

Keep recommendations separate from confirmed findings. Do not implement them.

### Expected Report Structure

1. **Executive Summary** — Main findings and overall assessment.
2. **Individual Skill Assessments** — All six considerations per skill, side by side for two or more skills, with detail focused on inputs, responsibilities, and outputs.
3. **Cross-Skill Responsibility & Overlap Findings** — Intentional overlaps, duplication, conflicts, and unclear ownership.
4. **Missing Responsibilities & Gaps** — Evidence-backed gaps and potential impacts.
5. **Prioritized Recommendations** — Actionable proposed changes, not implemented decisions.
6. **Open Questions for Human Review** — Issues requiring clarification or approval.
7. **Deferred Items for Integration-Contract Design** — Stage 3 contract questions and optional Stage 5 validation candidates, marked PROPOSED / NOT EXECUTED.

### Adaptive Side-by-Side Report Layout

- **One skill:** use vertical C1–C6 assessment blocks without inventing a second skill.
- **Two or three skills:** exactly one compact **Primary** table (C1 Inputs, C2 Responsibilities, C3 Outputs as rows) and one compact **Supporting** table (C4 Handoffs, C5 Boundaries, C6 Feedback as rows), with `Consideration | Skill A | Skill B` in the same skill order.
- **Table cells:** only short observations, source links, and meaningful F-xx/assessment labels. The five finding fields and full wording proposals **must not** be written inline within cells.
- **Immediately after Primary and Supporting respectively**, present material F-xx notes with **one Markdown bullet per field**, including optional Current wording, Concern and Recommended wording — PROPOSED. Preserve direct evidence and distinctions between source facts, inferred effects, and proposed changes.
- **Four or more skills:** repeat comparable two- or three-skill tables with an overall synthesis. Do not omit skills or material relationships.
- **Preflight:** headings and skill columns match; C1–C6 are row labels; F-xx points to nearby separate-line notes; no HTML, transposed tables, multi-line cells, extra wording tables, or disconnected finding sections.
- **Optional integration:** keep C4 handoff, C5 decision authority and C6 feedback separate. Proposals are PLANNED / PROPOSED — NOT IMPLEMENTED; Stage 3 defines contracts. Coordinator suggestions remain conditional.
- **Step 4:** prioritize actionable recommendations by F-xx without repeating full reasoning.

### Optional Q/lens reviews and future-stage preparation

- **Core only (default):** The original six considerations and seven report headings; no Q checklist or automatic conference lenses.
- **Full/subset Q review requested:** Use `quality-review-questions.md`. Assess ten Qs in canonical order or only requested IDs. After the Supporting table and its F-xx notes, show `Quality review coverage (optional)` as brief vertical lines with statuses, evidence and F-xx/Cx references. Do not generate duplicate findings.
- **Lenses requested:** Use `review-lenses.md` to ask topic-specific questions mapped to existing considerations. A lens-only review does not trigger the ten-question coverage checklist.
- **Evidence safeguards:** Q-05 identifies current contract gaps, not finalized new contracts. Q-07 separates documented permissions from enforced permissions. Q-09 separates existing eval definitions from run evidence.
- **Section 7:** Record supported Stage 3 contract-design questions and up to three Stage 5 Given/When/Then verification candidates when materially justified or explicitly requested; label them PROPOSED / NOT EXECUTED. Do not add candidates merely for ordinary unavailable traces or claim READY TO TEST.

### Evidence & Quality Requirements

- Link to actual source file paths and precise lines or sections wherever possible.
- Distinguish **DOCUMENTED, OBSERVED, INFERRED, and UNVERIFIED** findings.
- Do not invent responsibilities, source evidence, or runtime behavior.
- A skill instruction describing an action is not proof that the action was executed.
- Preserve intentional overlap; avoid recommending consolidation without a demonstrated problem.
- Use plain English, **side-by-side tables for multi-skill comparison**, and vertical notes for detailed evidence and recommendations. Avoid dense tables.
- Be explicit when evidence is missing or inconclusive.
- Do not finalize ownership or architecture decisions without human review.

### Scope Limitations

Remain read-only. **Do not**:

- Edit skill instructions, files, or repository content.
- Execute untrusted scripts or access unauthorized systems.
- Write to Jira, production systems, or other external services.
- Define formal input/output contracts, preconditions, postconditions, or invariants.
- Specify dispatch algorithms, retry policies, or orchestration design.
- Implement recommendations or claim unapproved decisions are final.

**Final deliverable:** An evidence-based **Skill Responsibility & Overlap Audit** that provides the foundation for a separate **Skill Integration Contracts** assessment.
