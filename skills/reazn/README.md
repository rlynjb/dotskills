# REAZN

**REAZN is a noninteractive, read-only, evidence-first skill using the same four SDI reasoning steps across input types.**

Give this skill an identifiable problem or proposed change: a Jira/other tracker item, pasted feature brief, acceptance criteria, architecture document, source code, agent-skill definition, Audit Skill findings, workflow description, PDF, screenshot, or another source the active host can actually inspect. It produces **one** concise assessment, not an interview or a new methodology. A Jira integration or codebase is not required for non-software problems.

It complements [Refine Requirements](../refine-requirements/README.md), which provides longer collaborative design exploration and explicit decision approvals.

## How it works — one SDI framework

1. **Step 1 — Understand the problem and scope:** Clarify the objective, actors, expected behavior/outcomes, constraints, functional requirements (FRs) and nonfunctional requirements (NFRs) where applicable, acceptance and unresolved assumptions.
2. **Step 2 — Verify existing patterns and recommend high-level design:** Inspect relevant code, agent skill, documented process or other current-state evidence. Explain what exists, who owns it, whether to FOLLOW/ADAPT or justify NEW REQUIRED, and compare the current/proposed flow when meaningful.
3. **Step 3 — Deep dive into mechanisms and contracts:** Focus on interfaces, guarantees, responsibilities, permissions, process handoffs, data flow, error behavior or other domain-relevant mechanics. **Do not invent APIs, databases or services** for nontechnical inputs.
4. **Step 4 — Trade-offs, risks and readiness:** Explain meaningful alternatives, evidence gaps, verification needs, minimal change footprint and proposed engineering decisions (D-IDs) without claiming approval.

The **Input/Ticket Snapshot** groups purpose and numbered, evidence-labeled core capabilities into four clearly titled subsections. These explain what the subject already does (or proposes to do), **not** the requirements for the requested change. The report uses **vertical, individually labeled findings** with source evidence. It keeps FR/NFR/D IDs when meaningful, boxed ASCII diagrams for relevant multi-component Step 2 flows, and `---` separators **only between distinct Step 2 pattern/design entries**. No Markdown tables in skill output.

## Strict item spacing and structure

- **One item = one block:** A bold `FR-xx`, `NFR-xx`, `Area:`, `Contract:`, `Risk:`, `D-xx`, or `Q-xx` heading is followed immediately by its consecutive Markdown `**Label:** value` fields (label bold, value regular). **No blank line between heading and fields or between fields within an item.**
- **Between items:** Exactly **one blank line**. Only Step 2 may separate full existing-pattern or design-option items with a standalone `---` and one blank line on either side. No dividers for FRs, NFRs, risks, contracts, decisions, or open questions.
- **Bold field labels:** In Markdown, use `**Requirement:** value`, `**Status:** value`, `**Source:** value` and the same pattern for every field in the Snapshot and four SDI steps. Bold only the label and colon; leave the value and citation/link in regular weight. In plain text use `Label: value` without Markdown markers.
- **Visible line breaks:** In Markdown, end the heading and nonfinal field lines with **two trailing spaces** so each label remains on its own line. No bullet prefixes, label indentation, padded blank paragraphs or Markdown tables.
- **Optional study fields:** With `learn: on`, the bold literal-asterisk labels `**\*Further reading:**` and `**\*Study focus:**` follow the same finding's evidence/reasoning **without any blank line**. All factual labels stay unprefixed.

**Illustrative NFR blocks (not real project findings):**

```markdown
**NFR-02 — Provenance and uncertainty**  
**Quality:** Distinguish facts, observations, and assumptions.  
**Status:** DOCUMENTED  
**Source:** [verified reference]

**NFR-03 — Portable packaging**  
**Quality:** Support independent skill installation.  
**Status:** NOT VERIFIED  
**Source:** [inspected packaging evidence]
```


## Grouped Input Snapshot — CLI-first presentation

The first screen of a REAZN report is an **orientation summary** with four `###` subsections, in this exact order: **Assessment objective**, **Purpose & core capabilities**, **Investigation scope**, **Evidence & recommendation**. They group the Snapshot only, **not** the four SDI steps.

- **Assessment objective:** Input source/type and the requested goal.
- **Purpose & core capabilities:** The subject's purpose and **2–5** relevant capabilities when evidenced. Number them `01 —`, `02 —` and give each compact `What:`, `Status:`, and `Source:` fields. Distinguish `OBSERVED`, `DOCUMENTED`, `PROPOSED` and `NOT VERIFIED`; a new feature is not an existing capability.
- **Investigation scope:** Requested/resolved scope, basis, target, revision, comparison, included/excluded areas.
- **Evidence & recommendation:** Relevant dependencies and evidence limits, with a short recommendation **at the bottom**.

Use bold Markdown labels (`**Label:** value`) and **one blank line between groups and complete capability items**, **no blank lines inside an item's fields**, and Markdown hard breaks (two trailing spaces) so labels remain distinct in iTerm2/Codex. Do **not** use tables or horizontal rules in the Snapshot. Use short clickable `file:line` source labels when the destination is verified; otherwise state `NOT VERIFIED` without inventing a link. Detailed FR/NFR/Area/Contract/Risk/D/Q items keep their existing compact formatting in Steps 1–4.

**CLI preview (illustrative content, not verified project findings):**

```markdown
## Input Snapshot — Reporting service

### Assessment objective

**Input:** Feature brief + inspected repository  
**Goal:** Assess proposed CSV export

### Purpose & core capabilities

**Purpose:** Generate authorized reports  
**Status:** DOCUMENTED  
**Source:** [verified specification reference]

**Core capabilities:** 2 relevant behaviors

**01 — View reports**  
**What:** Display report results.  
**Status:** OBSERVED  
**Source:** [verified file:line]

**02 — Filter reports**  
**What:** Filter report results.  
**Status:** OBSERVED  
**Source:** [verified file:line]

### Investigation scope

**Requested scope:** subsystem  
**Resolved scope:** subsystem  
**Basis:** Explicit request  
**Target:** Reporting  
**Revision:** NOT VERIFIED  
**Comparison:** NOT PROVIDED  
**Included:** Reporting UI and relevant API contracts  
**Excluded:** Unrelated subsystems

### Evidence & recommendation

**Dependencies:** Reporting API  
**Evidence limits:** Runtime tests NOT RUN  
**Recommendation:** CONDITIONAL — verify export contracts before proposing changes.
```

## Scope resolution — optional invocation selectors

Set **`scope`** to define the breadth of the SDI assessment and optionally supply **`target`**, **`revision`**, and **`compare`** to make its evidence boundaries explicit. These are **prompt-level settings**, not guaranteed typed API parameters or additional SDI steps.

- **`scope: auto | system | subsystem`** — Default `auto`: infer the **smallest coherent boundary** from the objective and accessible evidence. `system`: examine major **affected** subsystems and cross-system contracts for a system-wide problem, without exhaustively mapping the repository. `subsystem`: focus on a named feature, service, skill, component or process step and necessary neighbors.
- **`target`** — Optional repository, system, feature, module, component, agent skill or workflow to investigate. The presence of a repository root never automatically implies `scope: system`.
- **`revision`** — Optional branch, commit, tag or document version to inspect. The skill verifies the actual version rather than assuming that `main` or a named branch exists.
- **`compare`** — Optional base/head comparison, such as `main...feature-branch`, PR diff or document versions. A comparison scopes **change evidence**, not the system boundary or approval of the change.

**Resolution rules:** Explicit `scope` wins. With `auto`, choose and **disclose** the narrowest supported boundary; read across it only to inspect relevant contracts and dependencies. When a target, revision or comparison is unavailable, label it **NOT VERIFIED** and provide a conditional four-step assessment. The Input/Ticket Snapshot records **requested vs. resolved scope, target, actual revision, comparison, included/excluded areas and cross-boundary dependencies**.

This doesn't turn REAZN into [Learn Repo](../learn-repo/SKILL.md) (whole-codebase onboarding), [Learn Implementation](../learn-implementation/SKILL.md) (understanding existing code), or [Review Implementation](../review-implementation/SKILL.md) (post-implementation verification). Even `scope: system` needs an **identifiable problem or proposed change**.

**Example — focused branch assessment:**

```text
Run reazn to assess a proposed Facility Map change.
scope: subsystem
target: Facility Map
revision: feature/facility-map
compare: main...feature/facility-map
learn: on

Verify that the references exist, inspect the scoped changes and
necessary shared contracts, and give one four-step SDI report.
```

The branch names are illustrative. For a system-wide problem, set `scope: system`; to let the skill infer scope, omit the field or use `scope: auto`.

### Verify before recommending

Existing software, an agent skill or a business workflow may contain reusable behavior, but it must be inspected rather than assumed. Use **FOLLOW** for verified fit, **ADAPT** for verified partial fit, and **NEW REQUIRED** when evidence justifies a new approach. A bounded search may yield **NO SUITABLE PATTERN FOUND IN INSPECTED SCOPE**; incomplete access is **NOT VERIFIED**; no known current baseline is **CURRENT STATE NOT PROVIDED**. None of these means an absent component has been proven impossible.

**Domain-aware analysis:** For a codebase, inspect code, contracts, tests and conventions. For agent skills, inspect instructions, references, dependencies and relevant audit findings (which are not proof of runtime execution). For business workflows, inspect participants, decisions, handoffs and documents. Mark irrelevant software checks **NOT APPLICABLE** with a reason.

## Optional book references — `learn`

This is an **optional invocation setting**, not an extra SDI step:

- **`learn: off` (default):** The assessment stays focused on evidence and engineering decisions. No learning references or empty reading placeholders appear.
- **`learn: on`:** For each **material finding with a strong topic match**, the skill adds **`*Further reading:`** (book, edition, chapter number/title) and **`*Study focus:`** (the concept worth exploring) **under that finding**. These labels carry a **literal leading asterisk** (use `**\*Further reading:**` and `**\*Study focus:**` in Markdown output), unlike factual fields such as `Evidence:` and `Verdict:`. References supplement the usual output and do not change source evidence, factual claims or approval status.

**Example of a learning reference (illustrative, not verified project evidence):**

```markdown
**Area: Module ownership**  
**What exists today:** [description grounded in inspected code]  
**Evidence:** [actual file/symbol]  
**Verdict:** FOLLOW  
**Why:** [source-backed explanation]  
**\*Further reading:** A Philosophy of Software Design, 2nd ed. — Chapter 5, Information Hiding (and Leakage).  
**\*Study focus:** How interface boundaries reduce coupling.
```

Chapter suggestions come **only from these six books**: Alex Xu's *System Design Interview — An Insider's Guide* (Volumes 1 and 2; Volume 2 with Sahn Lam), *Designing Data-Intensive Applications* (2nd ed.), *Fundamentals of Data Engineering*, *Algorithmic Thinking* (2nd ed.), *A Philosophy of Software Design* (2nd ed.), and **Micheal Lanham's *AI Agents in Action*, Second Edition (Manning, 2026)**. The [optional chapter guide](references/learning-chapters.md) lists edition-checked chapter pointers. Only include a genuinely relevant, verified chapter; don't force every book, repeat the same reference needlessly, or turn the report into a tutorial. Actual evidence lives in **`Source:` / `Evidence:`**, not in a book citation.

## Invocation examples

**Normal assessment (no learning references):**

```text
Run reazn on this ticket or feature brief.
Verify applicable existing patterns and give one concise four-step SDI
assessment with evidence, contracts, trade-offs and open decisions.
No interview, implementation or source edits.
```

**Assessment with study references:**

```text
Run reazn on this [feature / agent skill / workflow].
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
