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

### Target skills

- **Skills to assess:** [Insert any skill names, directories, repository paths, or links]
- **Workflow or user goal, if known:** [Describe, or leave unknown]
- **Relevant environment/harness, if known:** [Optional]
- **Scope or constraints:** [Optional]

### Goal

Document what each skill owns, which capabilities are shared or unnecessarily duplicated, which responsibilities are missing, and what changes should be considered before integration design.

Work with the actual number and type of skills supplied; do not assume any particular domain or four-skill workflow. For a single skill, assess its responsibilities and gaps, and mark cross-skill comparisons as not applicable.

**This is an investigation, not an implementation task.**

### Method

Inspect each available SKILL.md and relevant references, scripts, configuration, agents, examples, and evaluation files.

Apply the existing Audit Skill methodology when useful. If the audit methodology compares only one or two skills at a time, review skills individually, perform relevant pairwise comparisons, and synthesize a cross-skill assessment. Do not imply it natively supports a larger batch.

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

**Optional connection guidance when a supported issue exists in Handoffs, Boundaries, or Feedback:**
- For **each affected skill separately**, propose documentation of **standalone use** (its own starting inputs, full workflow and outputs), an **optional handoff** (a partner's result can be provided as context when available), distinct **responsibilities**, clear **boundaries** (no unauthorized edits, publishing, decisions or automatic skill invocation), and **feedback** to the responsible owner as proposed changes/questions.
- Neither skill requires or automatically runs the other. Present the possible paths as Skill A alone, Skill B alone, or Skill A followed by *optional* Skill B with human-reviewed updates.
- Label all suggested wording **PROPOSED, NOT IMPLEMENTED** and provide direct evidence. If current files truly require another skill's output, report that fact; standalone support must remain **UNVERIFIED** or *conditional on a separate design change*, not assumed. Do not create a connection for unrelated skills or weaken necessary approval/security requirements.

**Where to document proposed optional connections (per affected skill):**
1. Prefer a short section directly in each skill's own `SKILL.md`. Keep independent inputs, complete workflow/outputs, ownership, boundaries, optional use of partner output and feedback there even if a reference is added.
2. Suggest a separate **skill-local** `references/` file only if field mappings, conditional cases, worked examples or conflict handling make the explanation substantial. The corresponding `SKILL.md` should link to that **own optional** reference with a clear read condition. Do not introduce a mandatory shared file or automatic skill invocation.
3. Name a one-direction reference `<source>-to-<destination>-handoff.md` (for example `prd-to-refinement-handoff.md`); use `handoffs` for a file spanning multiple transitions. Reverse feedback may use `<destination>-to-<source>-handoff.md`. Derive names from the actual skills; example paths are illustrative.
4. Reuse an existing suitable file instead of duplicating it. In the report, give `Documentation location: SKILL.md only` **or** `SKILL.md + references/<direction>-handoff.md`, a short complexity-based rationale, and `Status: PROPOSED` for **each** affected skill. Do not create files, claim they exist, or draft formal contracts during the audit.

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

Prioritize suggestions as **High, Medium, or Low**.

For each recommendation, provide:

- **Finding/problem:** What needs attention.
- **Evidence:** File links and relevant lines or sections.
- **Proposed change:** Ownership clarification or documentation adjustment.
- **Expected benefit/trade-off:** Why the change may help and any downside.
- **Human confirmation required:** Yes/no, with the decision owner if known.
- **Optional connection wording, when relevant:** Proposed documentation for **each affected skill** under Standalone use, Optional handoff, Responsibilities, Boundaries, Feedback—preserving standalone inputs, outputs and workflow and requiring no automatic cross-skill invocation.
- **Documentation placement, per skill:** Recommend `SKILL.md` only by default, or `SKILL.md` plus a locally owned, directional `references/<source>-to-<destination>-handoff.md` if substantial details justify a reference. Explain the trade-off without creating the files.
- **Optional coordinator decision for combined-workflow issues:** Check whether an explicitly invoked routing/sequencing skill is worth investigating, after considering documentation and manual next-action prompts. State NOT NEEDED, OPTIONAL COORDINATOR RECOMMENDED, or DEFER/UNVERIFIED, with evidence, minimal responsibilities, alternative, trade-off, and human confirmation. Do not create or require it.

Keep recommendations separate from confirmed findings. Do not implement them.

### Expected Report Structure

1. **Executive Summary** — Main findings and overall assessment.
2. **Individual Skill Assessments** — All six considerations per skill, side by side for two or more skills, with detail focused on inputs, responsibilities, and outputs.
3. **Cross-Skill Responsibility & Overlap Findings** — Intentional overlaps, duplication, conflicts, and unclear ownership.
4. **Missing Responsibilities & Gaps** — Evidence-backed gaps and potential impacts.
5. **Prioritized Recommendations** — Actionable proposed changes, not implemented decisions.
6. **Open Questions for Human Review** — Issues requiring clarification or approval.
7. **Deferred Integration Considerations** — Handoff, boundary, and feedback items to examine during contract design.

### Adaptive Side-by-Side Report Layout

- **One skill:** Use the six considerations as vertical sections. Cross-skill comparisons are not applicable.
- **Two or three skills:** In report section 2, use concise **side-by-side comparison tables** with one column per skill and the same six consideration rows, preferably split into Primary (Inputs, Responsibilities, Outputs) and Supporting (Handoffs, Boundaries, Feedback).
- **Four or more skills:** Compare in smaller side-by-side groups of two or three skills, then include an overall synthesis covering **every** selected skill and all material relationships.
- **Cross-skill overlap:** Align the activity and each involved skill's role; include classification and workflow effect. Explicitly name affected skills for gaps.
- **Supporting considerations 4–6:** For each real issue, give **per-skill** findings in the side-by-side cells, then show compact *proposed optional connection documentation* blocks for each affected skill directly below: Standalone use, Optional handoff, Responsibilities, Boundaries, Feedback **and Documentation placement** (`SKILL.md` only versus `SKILL.md` plus a separate optional, directional reference, with reason). Do not imply target files were changed.
- **Section 5:** When a material combined-workflow coordination issue exists, include an **Optional coordinator assessment** with one of the three outcomes, grounded rationale, a simpler alternative, a human decision, and explicit preservation of standalone use.
- Keep tables scannable; place evidence links, interpretation, and recommendations as short vertical notes below. If Markdown tables are not supported, use equivalent aligned comparison blocks. Do not invent data to fill cells.

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
