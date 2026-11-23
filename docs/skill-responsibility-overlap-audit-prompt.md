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
