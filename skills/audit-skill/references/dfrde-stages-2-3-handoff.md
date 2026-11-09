# DFRDE Stages 2–3 — optional audit evidence handoff

This reference explains how Audit Skill findings can support **Design and Contract drafts** when the user requests a DFRDE prefill. It is **not** a second question bank. The [DFRDE Engineering Review Template](../../../docs/dfrde/engineering-review-template.md) alone defines the questions and IDs.

## When to use

- **Audit-only request:** Stop after the read-only skill audit. Do not produce Design/Contract question tables.
- **Explicit DFRDE review prefill:** Read the latest engineering review template. Answer **only its existing three Design and two Contract question rows** using source evidence, without adding new questions. If the template is inaccessible, report the limitation and do not invent its wording.

## Evidence for Stage 2 — Design

- Show the **as-is** workflow, interfaces, existing reusable patterns, and ownership boundaries supported by inspected sources.
- Where appropriate, distinguish the smallest adequate **keep-as-is/reuse** option from other **proposed** approaches and their trade-offs. Do not invent a redesign simply to fill a table.
- Identify relevant risks (security, permissions, failures, reliability, cost, maintainability, and portability) **only where applicable**. Measurements and actual behavior require evidence.
- Describe recommendations as **PROPOSED**, not chosen or team-approved. The Design gate remains **HUMAN REVIEW REQUIRED**, especially if the Discover problem is unconfirmed.

## Evidence for Stage 3 — Contract

- Record existing **documented** input/output expectations, producer/consumer responsibilities, invariants, trust/authorization limits, and failure behavior. A written restriction is **not** technical enforcement.
- Suggest **conditional** guarantees, interfaces, ownership, and high-level acceptance expectations only as warranted by the proposed Design option. Do not assume a separate schema, machine consumer, or specific runtime without evidence.
- Note existing tests/CI/traces if inspected and clearly state which claims remain **not verified**. Do not propose detailed evaluation cases or run tests in this audit.
- Keep Contract ownership and approval **OPEN** until the accountable human reviewer confirms them. The Contract gate remains **HUMAN REVIEW REQUIRED**.

## Output discipline

Use the **template's question wording, IDs, and row structure**. Provide a concise draft answer or unknown, a direct link to inspected source lines, the evidence limitation, and any pending human decision. Do not replicate the questionnaire in this reference file.

Label facts **DOCUMENTED / OBSERVED**, suggestions **PROPOSED**, and missing proof **NOT VERIFIED**, explaining those meanings in plain English. Do not treat a code comment as effective authorization, a documentation path as a runtime trace, or an agent recommendation as approval. Never create an evidence-key index, extra questionnaire, or implementation/evaluation plan by default.

Audit Skill is read-only. Any saved DFRDE record or later behavioral evaluation requires its own authorization and workflow.
