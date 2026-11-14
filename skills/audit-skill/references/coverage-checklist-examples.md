# Audit Skill — Q-01–Q-10 explained with REAZN examples

**Optional learning reference, not a completed audit.** These examples explain the ten canonical questions in [Audit Skill's SKILL.md](../SKILL.md), using [REAZN](../../reazn/SKILL.md) as an illustrative target. Actual checkbox status **must be decided from the inspected source, revision, and evidence**. This guide is not a second questionnaire or a source of requirements.

A **checked / PRESENT** item means the applicable criterion is sufficiently evidenced within the audit scope—not that all runtime behavior was tested or a human approved it. Use **unchecked / PARTIAL, MISSING, or NOT VERIFIED** as appropriate; use **N/A** only when the whole criterion genuinely does not apply. Documentation may establish documented instructions, but it cannot establish tool permissions, runtime reliability, or host parity by itself.

## Q-01 — Purpose & boundaries

**What it checks:** Does the skill explain its purpose, intended use, exclusions and forbidden actions?

**REAZN example:** Its instructions describe one read-only four-step SDI assessment. They prohibit changing code, creating tickets, and auto-approving decisions.

**How to assess:** **PRESENT** when those boundaries are actually documented. This confirms a stated contract, **not** that an external host technically prevents writes.

## Q-02 — Activation & discovery

**What it checks:** Can users and supported harnesses determine when and how to activate the skill, including when not to activate it?

**REAZN example:** Its frontmatter, invocation examples, and selectors such as `intent: understand-existing`, `scope: subsystem`, and `target: reporting` tell a user how to invoke it.

**How to assess:** **PRESENT** for documented activation/discovery instructions in the inspected package; **do not infer** that every host actually discovers or invokes it correctly without testing.

## Q-03 — Structure, inputs & dependencies

**What it checks:** Are entry points, inputs, required/optional references, tools and unavailable-source handling clear?

**REAZN example:** It accepts tickets, code, design documents or an Audit Skill report. `learn: on` optionally loads `references/learning-chapters.md` if packaged and available.

**How to assess:** **PRESENT** for defined structure/dependencies and fallback rules. Verify the referenced files actually exist; a named external tool is not proof it is installed.

## Q-04 — Workflow & orchestration

**What it checks:** Are stages, decisions, applicable delegation and human gates defined?

**REAZN example:** It specifies one pass through four SDI steps (requirements/scope, existing patterns, contracts, risks/readiness) without mandatory interactive approvals.

**How to assess:** **PRESENT** for a sufficiently defined workflow. No agent delegation may be **not applicable to that sub-concern**, but the overall workflow still needs assessment; static instructions are not execution evidence.

## Q-05 — Contracts & outputs

**What it checks:** Are inputs, output fields, validation, invariants, responsibility and failure handoffs defined?

**REAZN example:** A Step 4 risk uses a fixed block:

```markdown
**Risk: Contract regression**  
_Impact:_ Interface changes could break consumers.  
_Mitigation:_ Verify compatibility before approval.  
_Linked decision:_ D-01
```

**How to assess:** **PRESENT** for an evidenced output contract and applicable failure-handling rules. Do not equate exact label instructions with verified runtime adherence.

## Q-06 — Context & trust

**What it checks:** Are provenance, source authority, freshness, contradictions and untrusted input handling addressed?

**REAZN example:** If the primary ticket requires **CSV** export but an audit summary says **PDF**, REAZN must preserve the ticket's expected behavior, identify the disagreement and avoid silently promoting the audit summary to product authority.

**How to assess:** **PRESENT** if those evidence/authority rules are documented; actual correctness on conflicting inputs still needs a run.

## Q-07 — Permissions & effects

**What it checks:** Are permitted side effects and authorization boundaries **enforced** at the relevant host/tool/server layers?

**REAZN example:** Its `SKILL.md` says read-only, but a Codex/Claude host might have access to write-capable tools unless those capabilities are separately restricted.

**How to assess:** Typically **PARTIAL** when only written restrictions are evidenced. Stronger evidence includes verified tool policies, sandbox/permission configuration, or actual traces demonstrating enforced boundaries—not simply the sentence “read-only.”

## Q-08 — Failure & stop behavior

**What it checks:** Does the skill describe missing sources, ambiguous requests, errors, partial results, escalation and relevant stop conditions?

**REAZN example:** If a named revision cannot be accessed, it should say `REVISION NOT VERIFIED`, preserve the scope limitation and issue a conditional assessment instead of inventing files or executed tests.

**How to assess:** **PRESENT** for documented, applicable fallback and stopping rules. This is a statement about instructions until behavior is observed.

## Q-09 — Evals & observability

**What it checks:** Are evaluation cases, grading evidence, real runs/traces and regression results accurately distinguished?

**REAZN example:** Its evaluation suite defines seven cases and a five-run consistency protocol. Defining cases and passing structural CI checks **does not mean those seven behavioral cases or five repeated runs were executed**.

**How to assess:** **PARTIAL** if evaluation definitions exist but there are no completed behavioral traces/results. To substantiate reliability, run the cases under separately authorized conditions, retain outputs and grade observed results against expectations.

## Q-10 — Lifecycle & portability

**What it checks:** Are maintainers, versions, review/rollback procedures, dependencies and claimed harness compatibility supported by evidence?

**REAZN example:** The repository has Codex/OpenAI and Claude Code adapter documentation and CI checks, but that alone does not establish owner policy, rollback practice or equivalent behavior across those hosts.

**How to assess:** **PARTIAL** when packaging/static validation is evidenced but release ownership, rollback and cross-host runtime parity are not. A stronger result needs defined ownership/release procedures and actual compatibility runs.

## Reading the checklist

The ten questions are **an audit of evidence**, not a numerical quality score. For any target, preserve the short Q-01–Q-10 at-a-glance lines and the normal six-field individual findings (`Question`, `Check`, `Finding`, `Evidence`, `Status`, `Recommendation`). Use this guide **only when someone asks for an explanation or examples**; do not append these ten worked examples to every standard audit.

The examples above are illustrative teaching material—not fresh inspection results, automatic statuses for later revisions, approvals, or evaluated proof of REAZN behavior.
