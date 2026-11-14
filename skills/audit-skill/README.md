# Audit Skill

**`audit-skill` is one read-only, overview-first workflow for reviewing one or more agent skills.** It automatically adjusts its scope from independent single-skill analysis to multi-skill responsibility and handoff analysis. There is **no Explore/Audit/Compare mode selection**.

The first result is a complete, **one-pass** At a Glance checklist plus **Q-01–Q-10 individual findings**. Each checkbox indicates whether the criterion is sufficiently evidenced; each finding explains what exists, what's unverified and a recommendation when justified. The audit does not execute tools, change documents, select architectures or approve decisions. No user checkpoints between questions.

## Table of contents

1. [Why audit an agent skill?](#1-why-audit-an-agent-skill)
2. [What are we reviewing?](#2-what-are-we-reviewing)
3. [Example: Audit Skill reviews REAZN](#3-example-audit-skill-reviews-reazn)
4. [How the one-pass audit works](#4-how-the-one-pass-audit-works)
5. [Understand the ten questions and checklist](#5-understand-the-ten-questions-and-checklist)
   - [Q-01–Q-10 engineering criteria](#q-01q-10-engineering-criteria)
   - [Worked examples](#worked-examples)
6. [Read the report and its evidence](#6-read-the-report-and-its-evidence)
   - [Evidence and safety rules](#evidence-and-safety-rules)
7. [Run your first audit](#7-run-your-first-audit)
8. [Cross-platform compatibility](#8-cross-platform-compatibility)
9. [How Audit Skill fits with other DotSkills](#9-how-audit-skill-fits-with-other-dotskills)

Think of this as a senior engineer walking a junior developer through their first review of an AI agent skill. The goal is to understand **what the skill claims to do**, **what the inspected files actually support**, and **what still needs testing**. This README teaches the process; it does **not** add extra questions, new output fields, or execution permissions to the skill.

## 1. Why audit an agent skill?

Imagine a teammate gives you a pull request and says, "This feature is secure and production-ready." As an engineer, you don't just accept that sentence. You read the code, inspect the tests and configuration, ask where the boundaries are, and identify anything that hasn't been proved.

**Auditing an agent skill works the same way.** A `SKILL.md` file describes how an AI coding assistant *should* behave, but a description isn't the same as seeing the behavior happen.

For example, if a skill says "read-only," you can confirm that the restriction is **documented**. You cannot conclude that writes are **technically blocked** unless you inspect the relevant permission enforcement or a genuine authorized result.

- **Audit Skill asks:** Is the skill's design, scope, workflow, and evidence clear and credible?
- **Evaluate Skill asks:** When the skill actually runs in an approved test environment, does its behavior meet expectations?

**Remember:** Audit is an evidence-backed *review*, not an execution test, a quality score, or an automatic approval to release.

## 2. What are we reviewing?

Before reviewing anything, identify the **target skill**. This is the skill being examined, not necessarily the skill doing the examining.

| Part | Plain-English meaning | Example |
| --- | --- | --- |
| **Auditor** | The reviewer that looks for engineering evidence and gaps. | Audit Skill |
| **Target** | The agent skill under review. | REAZN |
| **Source evidence** | What the reviewer is allowed to inspect: files, references, configurations, tests, and accessible history. | REAZN's `SKILL.md`, README, linked references, and eval definitions |
| **Report** | The reviewer’s findings, with citations and clear limits on what is known. | At a Glance checklist and ten Q-01–Q-10 findings |

One target is enough. For **two or more accessible skills**, Audit Skill reviews each independently and then checks responsibility overlap, ownership conflicts, and handoffs. You don't need to select a special compare mode.

If a named target isn't accessible, say **NOT ASSESSED** rather than making up its implementation or comparing it as though it were inspected. Record the branch or commit whenever possible so the evidence can be checked later.

## 3. Example: Audit Skill reviews REAZN

Let's use your real skills to make the difference concrete. **Audit Skill is doing the review; REAZN is only the target. REAZN does not run.**

Imagine Audit Skill reads a frozen revision of REAZN and notices:

1. **Purpose (Q-01):** REAZN describes a read-only four-step SDI assessment. That supports a claim about its *documented purpose*.
2. **Contracts (Q-05):** REAZN defines named output fields and expected behavior. That supports a claim about its *written output contract*, not automatic compliance by a running model.
3. **Permissions (Q-07):** The file says it won't modify the repository. Without inspected host-level restrictions, Audit Skill must **not** turn that into a claim of enforced read-only permission.
4. **Evaluations (Q-09):** REAZN may include defined eval cases. Their existence does **not** prove the cases were run successfully.

Those are **teaching examples**, not new inspection results or preset checkbox statuses. The real audit must cite the exact revision and files it actually inspected.

A useful question to ask for every conclusion is: **"How do we know that?"** If the answer is only "the prompt says so," report it as documented, not observed.

## 4. How the one-pass audit works

```text
                 One or more target skills
                           |
             Read-only source inspection
                           |
              Audit Skill — At a Glance
                           |
                Q-01–Q-10 checklist
               checked / unchecked / N/A
                           |
             Ten source-backed findings
       Question / Check / Finding / Evidence
              Status / Recommendation
                           |
          Standards / as-is flow / portability
        + multi-skill comparison when relevant
                           |
              Gaps and verification limits
                           |
          Optional user-selected deep dive
```

1. **Find and inspect** each available skill, references, agents, manifests, tests and relevant history, with source revision and line evidence.
2. **Apply the same review criteria to every skill**, whether one or several were supplied.
3. **Add relationships automatically** only when there are two or more accessible skills. Otherwise mark inter-skill comparison NOT APPLICABLE.
4. **Report the At a Glance checklist, followed by all ten individual findings in a single response** with supported/unsupported checks, concrete evidence, and brief recommendations. No pauses or automatic evaluation-case generation.
5. **Wait for a requested deep dive.** Never silently change the skill or run a behavioral evaluation.

If a named target cannot be accessed, label it NOT ASSESSED and avoid constructing a fictitious comparison.

**Junior-developer takeaway:** You get the full initial review in one response. The four SDI reasoning steps are used **internally**; Audit Skill does not turn them into additional output stages, ask for ten separate approvals, or automatically run evals.

## 5. Understand the ten questions and checklist

The ten questions are engineering **review criteria**. They help you avoid focusing only on whether the prompt sounds well written.

A checkmark means that the applicable expectation has enough evidence at the **appropriate level**. It does **not** mean the skill is production-ready. If the evidence is incomplete or the behavior is not verified, the report must say so.

### Checkbox decisions and individual findings

Audit Skill uses the **four SDI reasoning steps internally across the whole inspection**: understand the skill's job and scope; verify its workflow; examine relevant contracts, context, trust and failures; then assess gaps, trade-offs and readiness. **It does not assign an SDI step to each Q, print extra SDI stages or pause for Q-by-Q approval.**

The Q-01–Q-10 checklist uses:

- `- [x]` **PRESENT** — the criterion's relevant expectations are backed by inspected evidence. This is **presence**, not approval or a live test pass.
- `- [ ]` **PARTIAL / MISSING / NOT VERIFIED** — important coverage is incomplete, absent in the inspected scope or impossible to establish from available sources.
- **N/A** **NOT APPLICABLE** — the whole criterion genuinely does not apply, with an explanation.

A checkmark requires the **appropriate evidence level**. A documented output format may establish its contract, but a prompt saying "read-only" is not proof of enforced host permissions; a defined eval is not a run result.

Every criterion then has the same **six fields**: `Question`, `Check`, `Finding`, `Evidence`, `Status`, `Recommendation`. For example:

```markdown
**Q-05 — Contracts & outputs**  
_Question:_ Are required inputs, outputs, validation, invariants, ownership and failed handoffs defined?  
_Check:_ ☐  
_Finding:_ The output is documented, but missing-input handling was not described in the inspected scope.  
_Evidence:_ DOCUMENTED INSTRUCTIONS — [verified source reference]; execution NOT VERIFIED.  
_Status:_ PARTIAL  
_Recommendation:_ Define the missing-input response and verify the behavior separately.
```

This is an **illustrative** finding, not an observed audit. If a criterion is fully evidenced or not applicable, its recommendation can say `None justified`. If you later supply additional context, it stays **USER-PROVIDED — NOT VERIFIED** until supporting evidence is inspected. The initial audit remains read-only and fully one-pass.

### Q-01–Q-10 engineering criteria

The [Agent Skills specification](https://agentskills.io/specification) is the standards baseline for `SKILL.md`, naming/frontmatter and supporting resources. Its actual requirements are distinct from the team-defined engineering quality expectations below.

| ID | Requirement | What a reviewer should find |
| --- | --- | --- |
| Q-01 | Purpose and boundaries | Intended job, who uses it, when it should not activate |
| Q-02 | Activation and discovery | Invocation, triggers, incorrect-trigger behavior |
| Q-03 | Structure, inputs and dependencies | Source files, context, tools/MCP, credentials and environment assumptions |
| Q-04 | Workflow and orchestration | Steps, decisions, dynamic vs named agents, delegation, approvals and result aggregation |
| Q-05 | Contracts and outputs | Explicit inputs, outputs, guarantees, invariants, ownership and failed handoffs |
| Q-06 | Context and trust | Provenance, freshness, conflicting or untrusted information and evidence |
| Q-07 | Permissions and side effects | Enforced authorization, least privilege, scoped writes and human approval |
| Q-08 | Failure and stop behavior | Unavailable tools, ambiguous inputs, partial batches, retries, stop conditions |
| Q-09 | Evals and observability | Existing tests, CI, scenarios, execution traces, expected and observed outcomes |
| Q-10 | Lifecycle and portability | Owners, versioning, review/rollback, compatible hosts, adapters and regressions |

For each criterion, answer its canonical question using actual source evidence. Follow the same compact **Question → Check → Finding → Evidence → Status → Recommendation** layout, without inventing missing content. The detailed questions are defined in [SKILL.md](SKILL.md). A written instruction does not prove runtime enforcement; an eval definition does not prove execution.

The separate **standards compliance matrix** distinguishes required specification elements, recommendations and experimental/host-specific behavior. It should not imply full standards conformance if the published specification was not consulted or a validator was not run.

### Worked examples

For a plain-English explanation and **one REAZN example for every checklist criterion**, see [Q-01–Q-10 explained with examples](references/coverage-checklist-examples.md). It illustrates what evidence supports a checked or partial item; it does **not** change the default compact checklist, the six-field individual findings, or evidence-based checkbox decisions.

## 6. Read the report and its evidence

Think of the report as a code review with a traceable explanation: **what was checked, what was found, what evidence supports it, and what should happen next.**

A useful audit does not simply list ten opinions. It makes each material conclusion verifiable against the actual source and clearly separates what is written, what is implemented, and what has been observed.

The report begins **Audit Skill — At a Glance** (not a mode guide or a long question menu):

| Output | What it communicates |
| --- | --- |
| **Target/source boundary** | Which skills and revisions were inspected; what was inaccessible; no tests or target skill execution |
| **Skill profile(s)** | Purpose, activation, inputs, dependencies, steps/decisions, agents and tools, outputs, permissions, failures and handoffs |
| **Q-01–Q-10 checklist** | Ten ordered checked/unchecked/N/A items summarizing whether each criterion is evidenced, plus a short basis |
| **Individual findings** | A consistent Question → Check → Finding → Evidence → Status → Recommendation block for each criterion |
| **Agent Skills specification matrix** | Required format vs recommended/optional structure; normative claims tied to the published specification |
| **Mermaid current-state diagram(s)** | One flowchart per target, including decisions, delegation, stop conditions and unverified edges |
| **Relationship analysis (2+ only)** | Shared/unique responsibility matrix, conflicts, duplicate decisions, and proposed handoff/compose/merge alternatives |
| **Cross-runtime matrix** | Explicit host-by-capability compatibility evidence and adapter needs |
| **Evidence and gaps** | Existing safeguards first; important source-backed findings, limitations and unanswered questions |

The main report remains concise. A selected `F-xx`, quality dimension (`Q-01`–`Q-10`), diagram, workflow stage, or contract receives an evidence-backed deep dive without switching modes. Never present a hypothetical path as a tested run.

### Mermaid example (illustrative only)

```mermaid
flowchart TD
    A["Skill receives task"] --> B{"Required evidence available?"}
    B -->|Yes| C["Documented evaluation steps"]
    B -->|No| D["Clarify or stop as unresolved"]
    C --> E["Evidence-backed result"]
    D --> E
```

A real diagram must come from the target files and label which edges are inferred or unverified. For two skills, keep **as-is** diagrams distinct from any **PROPOSED** integration diagram.

### Evidence and safety rules

- **DOCUMENTED INSTRUCTIONS** = written guidance; **IMPLEMENTED CHECK** = code/config check found; **OBSERVED RESULT** = actual authorized trace; **NOT VERIFIED** = not established.
- Cite relevant file paths and lines; distinguish a referenced file from an actually loaded file.
- Report existing safeguards **before** gaps. Missing evidence must not become a fabricated failure or a passing test.
- The audit is **read-only** and never executes target agents, scripts, evals, live Jira/Confluence actions or repo mutations. Approved read-only file/repository sources may be inspected.
- Prompt text cannot enforce permissions. Only host/tool/server controls can enforce read-only authority.
- Preserve approved workplace data boundaries; do not paste confidential sources into a public repository.

**Remember:** A checklist can establish design coverage from source files. It cannot, by itself, certify that an AI agent will always follow the instructions, that tools enforce permissions, or that a deployment is safe.

## 7. Run your first audit

You don't need to build a new harness or write an eval suite to begin a **static, read-only audit**. Start with one skill you can inspect and one clear instruction: **review the source; don't execute or change it**.

Here's a simple walkthrough:

1. **Choose the target.** Start with REAZN or another accessible agent skill. Identify the exact revision and relevant references.
2. **Ask for the standard audit.** Request the full At a Glance Q-01–Q-10 checklist and ten findings, with source links and verification limits.
3. **Read the evidence before the recommendations.** Confirm each material statement comes from an inspected file. Question unsupported "verified," "production-ready," or "secure" claims.
4. **Pick one finding to discuss.** Ask for a focused deep dive if needed. Any proposed edit or behavioral eval is a **separate decision**, not an automatic consequence of the audit.

The example prompts below follow the skill's existing invocation contract.

**One skill — no mode to select:**

```text
Use audit-skill on Sprint Assessment in this repository.
Start with Q-01–Q-10 checked/unchecked/N/A at a glance,
then give the six-field evidence-backed finding for each question.
Include Agent Skills compliance, as-is Mermaid flow, compatibility
and material gaps.
Cite file/line evidence. Do not execute the skill or edit anything.
```

**Two skills — comparison happens automatically:**

```text
Use audit-skill on Sprint Assessment and Refine Requirements.
Inspect each independently, then include the ownership/overlap matrix,
conflicting decisions, missing handoffs and PROPOSED integration choices.
Include standards, quality, runtime-compatibility and evidence checks.
Read-only; no execution or edits. Pause for my review.
```

**Focused follow-up:**

```text
Deep dive F-02. Show the exact source evidence, implementation status,
risk, trade-offs and the smallest useful validation step.
```

The optional [Sprint Assessment example](references/sprint-assessment-audit.md) demonstrates a two-skill audit. It is task-specific guidance, not another review process.

## 8. Cross-platform compatibility

An Agent Skills-compatible Markdown directory does **not** guarantee that a multi-agent workflow behaves the same in every harness. The review explicitly covers:

1. Skill packaging and installation.
2. Discovery, triggers and invocation.
3. Context loading and configuration inheritance.
4. Tools, shell names, MCP integrations and local paths.
5. Agent delegation, concurrency and worker result aggregation.
6. User identity, permission and approval enforcement.
7. Output schemas, error handling, timeouts and partial failures.
8. Eval evidence, adapter ownership and supported versions.

Use a runtime × capability matrix with **SUPPORTED (evidenced)**, **ADAPTER REQUIRED**, **NOT SUPPORTED (evidenced)** and **NOT VERIFIED**. When runtimes are unspecified, say so. Do not assume Claude Code and Codex have interchangeable tool names or delegation APIs.

## 9. How Audit Skill fits with other DotSkills

| Skill | Responsibility |
| --- | --- |
| **Audit Skill** (this skill) | Read-only review of one or more skills across Q-01–Q-10, Agent Skills conformance, trust, source evidence, workflows, failure behavior and portability; no execution, approval or edits |
| [Evaluate Skill](../evaluate-skill/SKILL.md) | Separately authorized behavioral evaluation, diagnosis, human-approved changes and regression review; runtime safety gates still apply |
| [Integrate Skills](../integrate-skills/SKILL.md) | Draft collaboration/architecture walkthrough for connecting independently reviewed skills; not an implementation runner |
| [Learn Repo](../learn-repo/SKILL.md) | Guided learning of an entire codebase rather than skill-specific audit |

**Recommended path:** Audit as-is → discuss contracts/decisions with humans → separately authorize evaluation or implementation when warranted.

**Status:** This revision defines a single review procedure, not a proven new agent runtime or eval engine. Static documentation checks alone do not establish behavioral reliability.

**The mental model to keep:** **Target → inspected evidence → Q-01–Q-10 findings → human decision.** If you later want to prove runtime behavior, hand off to a separately authorized evaluation. Don't treat a good-looking audit report as a passing test.
