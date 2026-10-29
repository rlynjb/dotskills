# Audit Skill

**`audit-skill` helps you understand, assess, or compare agent skills without modifying or executing them.** It now supports **Explore Mode** for getting acquainted with one unfamiliar skill, in addition to its existing evidence-backed Audit and Compare workflows.

The central idea: **understand first → choose an angle → investigate with evidence → decide whether evaluation or improvement is warranted.** A documented instruction is not proof that an agent follows it.

## Table of contents

- [Choose a mode](#choose-a-mode)
- [Explore Mode: learn one skill](#explore-mode-learn-one-skill)
- [First response and question menu](#first-response-and-question-menu)
- [Deep dives and methodology lenses](#deep-dives-and-methodology-lenses)
- [Audit and Compare modes](#audit-and-compare-modes)
- [Evidence and safety boundaries](#evidence-and-safety-boundaries)
- [How to invoke](#how-to-invoke)
- [Relationship to other DotSkills skills](#relationship-to-other-dotskills-skills)
- [Files and status](#files-and-status)

## Choose a mode

| Mode | Use when | Result |
| --- | --- | --- |
| **Explore** | "Help me understand this one skill" | Overview, Skill Contract, workflow/evidence orientation, **complete initial question menu**, learner-chosen deep dives |
| **Audit** | "Assess this skill and find missing validation" | Evidence-backed gaps/risks, existing controls, recommendations, three **proposed** test cases |
| **Compare** | "How do these two skills overlap?" | Both skill contracts, overlapping and distinct decisions, conflicting instructions, handoffs, and audit findings |

**Explore** is the default for a single skill when the user wants to learn or gives no assessment goal. Explicit audit/assessment requests still use **Audit**. Comparison requests use **Compare** only with a second accessible skill. These are **modes of the same skill**, not three separate skills.

```text
                     Existing skill(s)
                            |
                 Read-only source discovery
                            |
               Choose mode from user intent
           /                |                 \
     EXPLORE              AUDIT             COMPARE
    Learn one         Assess one        Examine 2+ skills
       |                  |                 |
  Skill overview      Evidence &         Contracts &
  + question menu     gap report         overlaps/risks
       |                  |                 |
  Choose Q / T / F     Choose finding     Choose finding
       |                  |                 |
  Guided deep dive    Review next step   Review next step
           \                |               /
           Human decides whether to request Refine Skill
```

## Explore Mode: learn one skill

Use Explore when you want to know *how a skill works* before deciding whether anything needs to be improved. This mode does **not** require finding a defect, producing a readiness score, or writing evals.

The process follows five steps:

1. **Inspect:** read the target `SKILL.md` and relevant references, scripts, templates, and tests progressively. Record what was accessible and the source revision.
2. **Orient:** summarize the **Skill Contract** — purpose, trigger, inputs, workflow, decisions, outputs, validation, and handoff.
3. **Map:** show the major stage/decision/handoff flow and a small **Evidence & Pattern Map** linking concepts to file/line evidence and verification status.
4. **Offer a menu:** provide the **material initial questions** for all applicable topics. Do not pre-answer them or hide them behind an arbitrary "top three".
5. **Let the learner choose:** pause for a topic, question, finding, workflow stage, or request for a recommended learning order. Then investigate only that selection.

### First response and question menu

Organize the menu under these nine perspectives. `T-xx` identifies a stable topic, while `Q-xx` identifies a stable question.

| Topic | Explore questions such as ... |
| --- | --- |
| **T-01 Purpose & boundaries** | Why does this skill exist? What triggers it and when should it stop? |
| **T-02 Structure & dependencies** | What are the entry point, references, scripts, templates, and dependencies? |
| **T-03 Inputs & context** | What information does the skill require? How is context selected and trusted? |
| **T-04 Workflow & decisions** | What happens at each stage? How are decisions made? |
| **T-05 Outputs & handoffs** | What does it produce? Where does that output go? |
| **T-06 Validation & reliability** | What checks exist? What is documented versus actually verified? |
| **T-07 Trust & tool boundaries** | What tools, permissions, and possible side effects matter? |
| **T-08 Observability & failures** | What evidence exists for failures, traces, feedback, and uncertainty? |
| **T-09 Lifecycle & trade-offs** | How is the skill versioned, maintained, tested, and made portable? |

The agent derives **concrete, target-specific questions** from inspected files, not from assumptions. The menu includes every material question identified on the initial pass, with concise source pointers. It marks uncertain questions `PROVISIONAL / NOT VERIFIED`, inapplicable topics `NOT APPLICABLE`, and noteworthy patterns or unknowns with optional `F-xx` IDs. **A finding is not automatically a defect.**

For example, an **illustrative menu only** for Sprint Assessment might read:

```text
Skill: Sprint Assessment | Mode: Explore
Snapshot: [source revision, inspected files, known limitations]
Skill Contract: [purpose / inputs / decisions / outputs / handoff]
Workflow: [documented stages and decision points]
Evidence Map: [claim -> file:line -> documented / implemented / observed / unverified]

T-01 Purpose & boundaries
  Q-01 When should Sprint Assessment be invoked? [source or NOT VERIFIED]
T-03 Inputs & context
  Q-02 Which requirements and stakeholder answers does it consume? [source or NOT VERIFIED]
T-04 Workflow & decisions
  Q-03 How does it determine sprint readiness? [source or NOT VERIFIED]
  Q-04 How does it reason about sizing or uncertainty? [source or NOT VERIFIED]
T-07 Trust & tool boundaries
  Q-05 Can it call tools or change external systems? [source or NOT VERIFIED]
T-09 Lifecycle & trade-offs
  Q-06 What evaluations or regression checks exist? [source or NOT VERIFIED]

F-01 [Optional observed pattern or unresolved question; not a proven defect]

Choose Q-xx, T-xx, F-xx, a stage, or a named concept.
```

This is **not an actual audit of Sprint Assessment**: the example questions are prompts for investigation, not verified facts. A real first pass covers every applicable topic, not just the illustrative subset above.

### Deep dives and methodology lenses

After you choose, Explore uses a **guided, one-topic-at-a-time** walkthrough:

**What/why → actual skill evidence → worked example or documented decision path → trade-offs and unknowns → takeaway/checkpoint.**

You can ask for **Fast** or **Deep Dive** depth. You may select any question out of order. The skill keeps question IDs stable, tracks `covered / pending / not applicable / not verified`, and doesn't repeat the full menu unless asked or new evidence materially changes it.

Your five DotSkills methodology skills provide relevant **angles**, not mandatory steps or automatic tool execution:

| Methodology lens | Explore where useful |
| --- | --- |
| [Context Engineering](../context-engineering/SKILL.md) | Inputs, context provenance, freshness, missing information (`T-03`) |
| [Correctness & Verification](../correctness-and-verification/SKILL.md) | Decision criteria, invariants, evidence, existing checks (`T-04`, `T-06`) |
| [Trust & Governance](../agent-trust-and-governance/SKILL.md) | Permissions, authority, external effects, unsafe instructions (`T-07`) |
| [Observability & Feedback](../agent-observability-and-feedback/SKILL.md) | Traces, failure paths, feedback (`T-08`) |
| [Skill Lifecycle & Release](../skill-lifecycle-and-release/SKILL.md) | Versions, evaluation coverage, portability (`T-09`) |

Explore **teaches relevant concepts** using target evidence. It does not need an observed failure, and it does not invoke specialist skills unless you separately request that workflow.

## Audit and Compare modes

These preserve the original five-phase assessment workflow. **Overlap analysis is optional in Audit and active in Compare**; learning about a single skill does not require another skill.

| Phase | Audit (one skill) | Compare (two or more skills) |
| --- | --- | --- |
| **1. Inventory** | Extract Skill Contract | Extract each Skill Contract |
| **2. Workflow** | Map decisions, source evidence and handoffs | Map each workflow and evidence |
| **3. Overlap** | Skip (`NOT ASSESSED`) | Find shared context, duplicate decisions, conflicts and missing handoffs |
| **4. Validation** | Review existing safeguards, then rank supported gaps and risks | Review safeguards and gaps, including cross-skill inconsistencies |
| **5. Test design** | Propose three representative behavioral cases, **NOT RUN** | Propose cases testing each skill and key interfaces, **NOT RUN** |

The first Audit/Compare report presents an Executive Summary, Skill Contract(s), Evidence & Pattern Map, Workflow Map, Existing Validation, ranked Gaps & Risks, minimal proposed Validation Layer, three `NOT RUN` scenarios, and questions for human review. **Compare** also includes Overlap Analysis. After that, the user selects a finding to investigate.

The original [Sprint Assessment versus Refine Requirements audit prompt](references/sprint-assessment-audit.md) remains preserved as a comparison example. Its proposed division between requirements refinement and sprint planning is a **hypothesis** until both skill sources can be inspected.

## Evidence and safety boundaries

- **DOCUMENTED INSTRUCTIONS:** the skill says something should happen.
- **IMPLEMENTED CHECK:** an available script/test contains a check.
- **OBSERVED RESULT:** supplied or actually authorized test evidence demonstrates a result.
- **NOT VERIFIED:** unavailable source or missing execution evidence.

All three modes operate **read-only**. The agent does not change files, run target agents or scripts, commit, post to GitLab/GitHub, contact stakeholders, or execute evaluations. A convincing `SKILL.md` is not proof of reliable or safe behavior, and read-only prompt text does not enforce a sandbox; the consuming host must restrict access and tool effects.

For workplace use, inspect proprietary sources **only through approved access** and do not paste sensitive skill contents into the public DotSkills repository. If a source is missing, the response must identify the limitation rather than invent evidence.

## How to invoke

**Explore a single skill:**

```text
Use audit-skill in Explore Mode on our Sprint Assessment skill.
Read only. First give me a Skill Contract, workflow and evidence map,
then the complete initial menu of relevant questions across the learning
topics. Cite source files/lines or mark NOT VERIFIED.
Do not rank issues, design evals, modify files, or run anything.
Wait for me to choose a question or topic for a deep dive.
```

**Audit a single skill:**

```text
Use audit-skill in Audit Mode on Sprint Assessment.
Read only. Show its contract, workflow, existing safeguards,
evidence-backed validation gaps, and three proposed test cases.
Do not execute cases or edit the skill.
```

**Compare two skills:**

```text
Use audit-skill in Compare Mode on Sprint Assessment
and Refine Requirements, if both are accessible.
Compare decision ownership, overlap and handoffs, with source evidence.
Keep the first report concise; do not execute tests or edit files.
```

## Relationship to other DotSkills skills

| Skill | Responsibility |
| --- | --- |
| **Audit Skill** (this skill) | **Explore** how one skill works; **Audit** its documented safeguards and gaps; **Compare** skill responsibilities. Read-only, overview-first. |
| [Refine Skill](../refine-skill/SKILL.md) | Teaches eval design, supports authorized behavior testing, diagnoses failures with five lenses, and makes human-approved improvements. No bundled model runner. |
| [Learn Repo](../learn-repo/SKILL.md) | Teaches an **entire codebase** with a question-first learning menu and repo/book lenses. |
| [Refine Requirements](../refine-requirements/SKILL.md) | Refines feature requirements and design inputs; a possible **target** of Audit Skill. |

**Recommended sequence:** Explore to understand → Audit to assess (if needed) → Refine Skill to evaluate/improve (only after a separate, approved request). Modes are not automatically chained.

## Files and status

- [`SKILL.md`](SKILL.md) — runtime instructions and mode routing, including Explore's initial question-menu and deep-dive contract.
- [`README.md`](README.md) — human-facing overview, examples, safeguards and comparison of modes.
- [`references/sprint-assessment-audit.md`](references/sprint-assessment-audit.md) — preserved original Sprint Assessment comparison prompt.

**Status:** Explore Mode is an instruction workflow, not a new eval engine or an independently verified model behavior. Repository structural checks do not prove the mode behaves correctly in live model runs.
