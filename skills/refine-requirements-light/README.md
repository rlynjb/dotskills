# Refine Requirements Light

**A noninteractive, read-only, evidence-first assessment using the same four SDI reasoning steps across input types.**

Give this skill an identifiable problem or proposed change: a Jira/other tracker item, pasted feature brief, acceptance criteria, architecture document, source code, agent-skill definition, Audit Skill findings, workflow description, PDF, screenshot, or another source the active host can actually inspect. It produces **one** concise assessment, not an interview or a new methodology. A Jira integration or codebase is not required for non-software problems.

It complements [Refine Requirements](../refine-requirements/README.md), which provides longer collaborative design exploration and explicit decision approvals.

## How it works — one SDI framework

1. **Step 1 — Understand the problem and scope:** Clarify the objective, actors, expected behavior/outcomes, constraints, functional requirements (FRs) and nonfunctional requirements (NFRs) where applicable, acceptance and unresolved assumptions.
2. **Step 2 — Verify existing patterns and recommend high-level design:** Inspect relevant code, agent skill, documented process or other current-state evidence. Explain what exists, who owns it, whether to FOLLOW/ADAPT or justify NEW REQUIRED, and compare the current/proposed flow when meaningful.
3. **Step 3 — Deep dive into mechanisms and contracts:** Focus on interfaces, guarantees, responsibilities, permissions, process handoffs, data flow, error behavior or other domain-relevant mechanics. **Do not invent APIs, databases or services** for nontechnical inputs.
4. **Step 4 — Trade-offs, risks and readiness:** Explain meaningful alternatives, evidence gaps, verification needs, minimal change footprint and proposed engineering decisions (D-IDs) without claiming approval.

The report uses **vertical, individually labeled findings** with source evidence. It keeps FR/NFR/D IDs when meaningful, boxed ASCII diagrams for relevant multi-component Step 2 flows, and `---` separators **only between distinct Step 2 pattern/design entries**. No Markdown tables in skill output.

### Verify before recommending

Existing software, an agent skill or a business workflow may contain reusable behavior, but it must be inspected rather than assumed. Use **FOLLOW** for verified fit, **ADAPT** for verified partial fit, and **NEW REQUIRED** when evidence justifies a new approach. A bounded search may yield **NO SUITABLE PATTERN FOUND IN INSPECTED SCOPE**; incomplete access is **NOT VERIFIED**; no known current baseline is **CURRENT STATE NOT PROVIDED**. None of these means an absent component has been proven impossible.

**Domain-aware analysis:** For a codebase, inspect code, contracts, tests and conventions. For agent skills, inspect instructions, references, dependencies and relevant audit findings (which are not proof of runtime execution). For business workflows, inspect participants, decisions, handoffs and documents. Mark irrelevant software checks **NOT APPLICABLE** with a reason.

## Optional book references — `learn`

This is an **optional invocation setting**, not an extra SDI step:

- **`learn: off` (default):** The assessment stays focused on evidence and engineering decisions. No learning references or empty reading placeholders appear.
- **`learn: on`:** For each **material finding with a strong topic match**, the skill adds **`*Further reading:`** (book, edition, chapter number/title) and **`*Study focus:`** (the concept worth exploring) **under that finding**. These labels carry a **literal leading asterisk** (escape it as `\*` in Markdown output), unlike factual fields such as `Evidence:` and `Verdict:`. References supplement the usual output and do not change source evidence, factual claims or approval status.

**Example of a learning reference (illustrative, not verified project evidence):**

```text
Area: Module ownership
What exists today: [description grounded in inspected code]
Evidence: [actual file/symbol]
Verdict: FOLLOW
Why: [source-backed explanation]
*Further reading: A Philosophy of Software Design, 2nd ed. — Chapter 5, Information Hiding (and Leakage).
*Study focus: How interface boundaries reduce coupling.
```

Chapter suggestions come **only from these six books**: Alex Xu's *System Design Interview — An Insider's Guide* (Volumes 1 and 2; Volume 2 with Sahn Lam), *Designing Data-Intensive Applications* (2nd ed.), *Fundamentals of Data Engineering*, *Algorithmic Thinking* (2nd ed.), *A Philosophy of Software Design* (2nd ed.), and **Micheal Lanham's *AI Agents in Action*, Second Edition (Manning, 2026)**. The [optional chapter guide](references/learning-chapters.md) lists edition-checked chapter pointers. Only include a genuinely relevant, verified chapter; don't force every book, repeat the same reference needlessly, or turn the report into a tutorial. Actual evidence lives in **`Source:` / `Evidence:`**, not in a book citation.

## Invocation examples

**Normal assessment (no learning references):**

```text
Run refine-requirements-light on this ticket or feature brief.
Verify applicable existing patterns and give one concise four-step SDI
assessment with evidence, contracts, trade-offs and open decisions.
No interview, implementation or source edits.
```

**Assessment with study references:**

```text
Run refine-requirements-light on this [feature / agent skill / workflow].
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
