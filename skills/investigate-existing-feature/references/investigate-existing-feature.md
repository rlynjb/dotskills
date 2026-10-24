# Existing Feature Investigation Prompt Library

A reusable, **read-only feature investigation** prompt for an AI coding agent. Use it when a feature already exists and you need to understand not only the code, but also **how the feature was assembled**: the original inputs, assets, data, services, third-party tools, manual preparation, repository history, setup, and people or teams who may own missing resources.

**Core question:** What would I need to find, obtain, configure, or reproduce to build another instance of this existing feature?

This is an investigation of **feature provenance and prerequisites**, not a code review, a feature design spec, or an implementation request. For deeper explanations of a specific implementation, see [System Learning Implementation](system-learning-implementation.md); for whole-repository context, see [System Learning Repo](system-learning-repo.md).

---

## Index

| # | Prompt | Reach for it when |
| --- | --- | --- |
| 0 | [Master feature investigation](#0-master-feature-investigation-prompt) | You need to reconstruct the full feature, including external origins and historical setup |
| ★ | [Compact daily investigation](#compact-daily-investigation-prompt) | You need a quick answer about what a feature depends on |
| 1 | [Find the source of an asset](#1-find-the-source-of-an-asset) | You cannot tell whether a graphic, map, file, or model is generated, fetched, or supplied |
| 2 | [Reconstruct the original setup](#2-reconstruct-the-original-setup) | You want to know what previous developers likely had to obtain or configure |
| 3 | [Compare an existing feature with a new instance](#3-compare-an-existing-feature-with-a-new-instance) | You are adding another facility, tenant, customer, integration, or similar resource |
| — | [Five book lenses](#five-book-lenses-for-feature-investigation) | Use your five reading lenses to explain evidence without turning this into a code review |
| — | [How this differs from existing prompts](#how-this-differs-from-existing-prompts) | You need to choose the correct prompt for the task |

---

## Five book lenses for feature investigation

Apply the same five lenses as [Code Review](code-review.md), but **use them to learn how an existing feature came to be**, not to score code quality or recommend refactors. **Investigate the actual feature and its resource origins first; only then apply lenses where evidence supports them.**

| Lens | Full book title | What to investigate in an existing feature |
| --- | --- | --- |
| **APOSD** | *A Philosophy of Software Design* | Which module owns the feature? Where are details about asset preparation, configuration, and external resources hidden behind interfaces? What knowledge must a developer possess to add another instance? |
| **AT** | *Algorithmic Thinking* | Does code create or transform geometry, coordinates, SVG paths, layers, or spatial mappings? Which algorithms and data structures are involved, and what inputs do they require? If the floor plan is supplied unchanged, don't invent an algorithm. |
| **DDIA** | *Designing Data-Intensive Applications* | Which system or asset is authoritative? How are IDs, versions, mappings, updates, caches, and stored state kept correct? What happens when the asset and its metadata disagree or a dependency fails? |
| **FODE** | *Fundamentals of Data Engineering* | What is the upstream source of the data or asset? How is it acquired, exported, converted, validated, stored, and delivered? What are its lineage, owner, and operational handoffs? |
| **SDI** | *System Design Interview* | Which components, teams, APIs, storage services, or third-party systems participate? Where are the integration boundaries and setup dependencies? Which requirements or constraints might explain this arrangement? |

**Lens policy:** Define abbreviations on first use. Cite the repo or historical evidence for each meaningful observation. Distinguish historical fact from your own engineering interpretation. Mark a lens **not applicable** with a short reason when the feature doesn't engage it. Synthesize overlapping observations rather than producing five repetitive summaries. In particular, FODE traces *where a resource comes from*; DDIA examines *what guarantees keep it correct*; SDI shows *how components and external systems fit together*; AT explains *relevant computation*; APOSD examines *responsibility and hidden complexity*.

---

## 0. Master feature investigation prompt

**What it does:** Reverse-engineers an existing feature from its visible behavior back through its code, data, assets, external dependencies, original setup, and available historical evidence.

**How to use:** Run this prompt in a repository with access to relevant code and, if available, a screenshot, an example feature, a ticket, related documentation, and repository history. Replace the request and context fields. The investigation must still be useful when only the codebase is accessible.

~~~text
# Existing Feature Provenance Investigator

Act as a senior engineer helping me investigate an existing feature that
someone else implemented.

I am NOT asking you to implement the feature, review code quality, write a
design spec, or create an implementation plan yet.

My goal is to work backward from the existing behavior and discover:

1. How the feature currently works, from user input to visible result.
2. What original inputs, datasets, files, assets, or specifications it needs.
3. Whether those inputs are generated by code, returned by an API, loaded
   from storage, embedded in the repository, or prepared outside the app.
4. Which third-party services, applications, design tools, libraries,
   infrastructure, or human/manual steps might have been involved.
5. What the available evidence reveals about how a previous developer or
   team set it up and why they chose that approach.
6. What I would need to obtain, confirm, configure, or ask for before
   reproducing a similar feature.

## Investigation request

Existing feature:
<NAME OR DESCRIPTION OF THE FEATURE>

Example route, screen, facility, record, screenshot, or behavior:
<OPTIONAL EXAMPLE>

What I want to do next:
<E.G., ADD A NEW FACILITY FLOOR PLAN USING THE EXISTING FEATURE>

Available context:
<REPOSITORY / BRANCH, TICKET, DOCUMENTS, PRS, ASSETS, OR LINKS>

## Investigation rules

- Follow repository instructions and inspect available documentation,
  code, configuration, tests, assets, and history before drawing conclusions.
- Work READ-ONLY. Do not implement, refactor, create files, commit, alter
  infrastructure, deploy, or call write APIs.
- Do not access production, external accounts, paid services, or private
  systems without authorization. Never expose credential values, secret
  configuration, customer data, or private file contents. Report only
  relevant configuration key names and resource types when appropriate.
- Use the actual tools available in this workspace. If git history,
  tickets, network traces, external accounts, or design files are not
  accessible, say so. Do not pretend to have inspected them.
- Follow promising references into relevant files, call sites, related
  feature instances, asset directories, scripts, configuration, and tests.
  Do not read every file indiscriminately.
- Cite evidence using file paths and line numbers or symbols, relevant
  commits/PRs/tickets, filenames, configuration keys, or observed network
  requests. Give a precise path or reproducible search for every claim
  that matters.
- Separate:
  CONFIRMED: directly supported by inspected evidence.
  INFERRED: consistent with evidence but not directly established.
  POSSIBLE: a hypothesis requiring a discriminating check.
  UNKNOWN: not established with currently accessible sources.
- Distinguish current runtime behavior from historical implementation
  steps. The fact that the app loads an SVG today does not prove who
  created it or which design application produced it.
- Do not invent previous developers' actions, tools, motivations, service
  accounts, resource owners, or access procedures.
- Ask a focused question only when it would materially change the
  investigation; otherwise proceed and report what remains unknown.
- Start by finding the actual feature; do not assume the feature is built
  the way its name or UI appearance suggests.

## 1. Locate the existing feature

Establish the observable starting point.

Find:
- Route/page/entry point and the feature's user-facing behavior.
- Representative input, such as a facility ID, selection, URL, file,
  record, API response, or user action.
- UI component, server handler, service, model, or job responsible.
- Related implementations of the same feature for other facilities,
  customers, tenants, or records.
- Tests, fixtures, screenshots, documentation, and configuration that
  demonstrate expected behavior.

Give me a focused feature map:
Entry point -> relevant modules -> source(s) -> transformation ->
renderer/output.

For every major component, identify its responsibility and evidence.

## 2. Determine where the feature's content originates

Do not confuse where content is displayed with where it was CREATED.

Identify which of these origins are evidenced, and rule out alternatives
when the evidence supports doing so:

- A static file committed to the repository (SVG, PNG, PDF, JSON, CAD,
  GeoJSON, image, model, etc.).
- A file hosted outside the repository (object storage, CDN, media
  service, document platform, or a separately managed asset repository).
- An API or backend service returning an asset URL, raw markup,
  metadata, geometric coordinates, or render-ready data.
- Data generated or transformed by application code at runtime.
- A database record or configuration mapping a facility to an asset.
- A canvas, SVG DOM, map, diagram, or WebGL renderer built dynamically
  from coordinates or records.
- A third-party embed, map/tile service, visualization SDK, or iframe.
- A hybrid approach: externally supplied base asset PLUS code-generated
  markers, overlays, room labels, access controls, or live status.
- Another origin demonstrated by the actual implementation.

For each relevant source, follow the reference back to the earliest
accessible point. If the application fetches an SVG URL, find where
that URL is defined, how it is selected, and how the SVG got there
if the evidence is available.

Clearly answer: What is generated by code? What is supplied as data or
an asset? What must already exist before the feature can work?

## 3. Trace the concrete runtime flow

Choose one representative existing instance and trace it end-to-end:

1. Starting user action or request.
2. Identifiers, parameters, config, and initial values.
3. API/service/storage requests and response contracts.
4. Data retrieval, parsing, validation, conversion, or enrichment.
5. Asset loading, caching, and error/fallback handling.
6. Rendering and user interactions.
7. Any persisted changes, side effects, or updates.

At each step:
- Cite a file and symbol, endpoint, contract, or other evidence.
- Show what input enters and what output leaves.
- Note where values are renamed, transformed, mapped, or merged.
- Separate frontend behavior from backend behavior and external systems.
- State what is not visible from repository code alone.

Produce a simple ASCII RUNTIME diagram.

## 4. Trace provenance and the upstream creation workflow

Now go BEYOND the runtime code.

Investigate the asset's or data's upstream origin:
- What original source material could it derive from? Identify the
  actual source when evidence exists.
- Was an artifact manually created, edited, exported, converted,
  uploaded, or imported? Find evidence of those steps.
- What are the input and output formats for each evidenced step?
- Is there a conversion script, build tool, CLI, design export,
  ingestion pipeline, admin UI, or scheduled job?
- Where is the authoritative source of truth versus a derived/exported
  copy used by the app?
- How is an asset associated with the correct facility or entity?
- How are revisions or new versions published?
- What must a developer, designer, operations person, or another team
  provide before the application code can consume it?
- Who appears to own each external dependency? Mark ownership as
  UNKNOWN if you cannot establish it.

If provenance crosses outside the repository, follow accessible
references into docs, tickets, linked PRs, scripts, dependency docs,
configuration, asset metadata, or external integration references.
Do not assume outside access is available.

Produce a separate ASCII PROVENANCE diagram showing:
Original source / person / tool -> exported asset or data ->
storage or import -> application -> user.

A runtime diagram and a provenance diagram answer different questions;
do not collapse them into one.

## 5. Inventory external tools, services, and prerequisites

Look for documented or observable dependencies such as:
- Design or authoring applications (for example Figma, CAD, Illustrator,
  or diagram tools), but only identify a specific one as used if proven.
- Third-party APIs, SDKs, mapping/visualization libraries, and services.
- Storage buckets, CDN paths, asset servers, databases, or admin tools.
- Import/export, conversion, and processing utilities.
- Environment variables, configuration names, build steps, deployment
  steps, access permissions, and external approvals.
- Manual coordinate mapping, dimensions, annotations, validation,
  licensing, or quality-review steps.

For each finding report:
Dependency/resource:
Role in the feature:
Input supplied / output produced:
Where it lives or is configured:
Required access or owner, if established:
Setup or update process, if established:
Evidence:
Confidence: CONFIRMED / INFERRED / POSSIBLE / UNKNOWN

Do not label a library as an external service merely because it is a
third-party package; distinguish a locally installed dependency from
a remotely hosted service or an authoring application.

## 6. Reconstruct the earlier implementation with historical evidence

Where accessible, inspect:
- git log, blame, commits, and file or asset introduction history.
- PRs, issues, commit messages, design docs, decision records.
- Added or changed dependencies, scripts, schemas, configs, and assets.
- Earlier versions and differences across similar feature instances.
- Tests and fixtures added alongside the feature.

Reconstruct the sequence ONLY to the extent supported:
Requirements or request -> asset/data preparation -> integration ->
rendering and interaction -> deployment/operation.

For each historical claim, attach its commit, PR, ticket, document,
or file evidence. If you cannot know what a developer did outside
GitHub or why a decision was made, state UNKNOWN.

When direct evidence is absent, present up to three plausible methods
as HYPOTHESES, not historical facts, and identify the cheapest specific
check that would distinguish them.

## 7. Compare existing instances and identify reusable contracts

If another facility, customer, or similar instance is the goal:

- Compare two or more existing instances when available.
- Separate reusable code from instance-specific assets or data.
- Identify required identifiers, paths, formats, dimensions, layers,
  schemas, coordinate systems, metadata, and permissions.
- Detect hard-coded names, URLs, mappings, or assumptions that could
  prevent reuse.
- Identify whether new instances require only a new source asset,
  database/config entry, service setup, or additional application work.
- Flag missing or incompatible inputs, and how they can be validated.

Do not propose rewriting the feature when reproducing the established
workflow would suffice.

## 8. Understand the feature through the five book lenses

After establishing the runtime flow, upstream provenance, external
prerequisites, and historical evidence, explain the observed feature
using these five lenses from my Code Review Prompt Library.

This is for UNDERSTANDING AND RECONSTRUCTION, not auditing code quality.
For each applicable lens: give a concrete observation, the supporting
file/symbol/commit/asset or other evidence, why it matters for
reproducing the feature, and any unresolved question.

- APOSD — A Philosophy of Software Design:
  Identify the module or interface that owns the feature and where
  asset-specific or integration-specific complexity is encapsulated.
  What must a developer know beyond simply calling the component?
  What are the boundaries between reusable code and per-instance setup?

- AT — Algorithmic Thinking:
  If code actually builds or transforms the feature, trace the relevant
  parsing, geometric calculations, coordinate mapping, SVG/canvas
  rendering, data structures, and input assumptions. Explain why the
  computation works using a concrete example. If an SVG or other
  supplied asset is rendered without a relevant algorithm, mark this
  lens not applicable instead of fabricating one.

- DDIA — Designing Data-Intensive Applications:
  Determine the source of truth and any persisted identifiers, asset
  versions, database mappings, caches, consistency assumptions, or
  failure/recovery behavior. If an SVG changes independently of room
  metadata, what currently keeps them aligned? Distinguish guarantees
  observed in the repo from potential risks.

- FODE — Fundamentals of Data Engineering:
  Trace the asset/data lifecycle from the ORIGINAL source, person,
  application, or vendor through export, conversion, ingestion,
  validation, storage, updates, and final consumption. Identify
  lineage, required quality checks, ownership, and manual handoffs.
  Make inaccessible upstream steps explicit.

- SDI — System Design Interview:
  Map feature requirements, system boundaries, API/storage/service
  responsibilities, external design or authoring dependencies, and
  operational constraints. Explain which observed design choices
  support reuse across facilities or other instances.

For each lens state: APPLICABLE or NOT APPLICABLE (and why).
Cite evidence for findings. Separate verified original rationale from
your interpretation of possible trade-offs. If multiple lenses lead
to the same insight, synthesize it once rather than repeating it.

End with a short cross-lens synthesis:
- What do the five perspectives collectively clarify about how
  the feature was originally assembled and currently operates?
- Which essential dependencies are outside the codebase?
- What is the next best evidence-based question before adding a new
  instance of the feature?

## 9. Determine what is needed to reproduce the feature

Without writing code, provide a practical checklist divided into:

ALREADY AVAILABLE
- Reusable modules, assets, scripts, services, documentation, examples.

MUST OBTAIN / CREATE
- New external asset or data, file format, source material, mapping,
  identifiers, permissions, storage/config entry, or design approval.

MUST VERIFY
- Assumptions, contracts, asset dimensions, output correctness,
  ownership, access, data freshness, error handling, security concerns.

QUESTIONS FOR OTHERS
- Exact question, why it matters, likely person/team/system to ask,
  and whether it blocks progress.

State a justified outcome:
A. Reusable with existing inputs
B. Requires a new asset/data or external setup
C. Requires code changes
D. Cannot determine yet

A feature can need both B and C. Explain the evidence for each.

## 10. Required final report

Return this structure, in order:

1. **Short answer**: In plain language, where does this feature come
   from and what does it depend on? Mark unresolved parts clearly.
2. **What I inspected**: Repo areas, sample instances, docs, history,
   external sources; and access limitations.
3. **Origin decision matrix**: Possible origin / evidence for or
   against / status / next check. Do not list irrelevant guesses.
4. **Runtime flow**: ASCII diagram and cited step-by-step trace.
5. **Provenance flow**: Separate ASCII diagram; source, preparatory
   steps, assets, storage/import, application.
6. **External dependency and setup inventory**: Inputs, tools,
   third-party resources, formats, ownership, permissions, evidence.
7. **Historical reconstruction**: What is known about the original
   implementation, and what cannot be recovered.
8. **Reusable vs instance-specific**: Relevant differences and
   contracts for building another instance.
9. **Five-book lens synthesis**: Brief evidence-backed APOSD, AT, DDIA,
   FODE, and SDI observations; mark inapplicable lenses explicitly.
   Emphasize what each reveals about inputs, architecture, origin,
   correctness, or prerequisites rather than code-review findings.
10. **Unknowns and discriminating checks**: Prioritized by impact.
11. **Reproduction readiness**: Already available / must obtain /
    must verify / people to ask / classification A-D.
12. **Recommended investigation path**: Up to five concrete searches,
    files, historical records, or non-destructive checks to perform next.

Keep the narrative concise and specific. Prioritize finding the true
origin of required inputs over describing incidental implementation
details. Do not claim that a plausible workflow is what the previous
developer actually did.
~~~

---

## Compact daily investigation prompt

**What it does:** A short first pass for ordinary work, especially when the question is "where does this resource come from?"

~~~text
Investigate the existing feature: <FEATURE / SCREEN / ROUTE>.

My next goal is: <WHAT I WANT TO REPRODUCE OR EXTEND>.

Work read-only. Start from one working example and trace:
1. Where the feature is rendered, and the files/symbols responsible.
2. What runtime inputs, data, files, URLs, APIs, and services it uses.
3. Whether its main content is code-generated, fetched, stored,
   committed as an asset, prepared externally, or a hybrid.
4. Where the source asset/data originally comes from, as far as
   accessible code, docs, scripts, commits, and PRs show.
5. Any third-party application, manual preparation, import/export,
   access, configuration, or team handoff needed before code can use it.
6. What is reusable and what must change for another instance.
7. What is known, inferred, possible, and still unknown.
8. Where the five book lenses help explain the evidence:
   APOSD (module ownership), AT (any real computation), DDIA (source
   of truth and guarantees), FODE (asset/data lineage), and SDI
   (system boundaries and external dependencies). Mark irrelevant
   lenses not applicable rather than forcing them.

Give me:
- One-sentence answer to "where does it come from?"
- Runtime path: input -> source -> transformation -> UI
- Upstream path: original source/tool -> asset/data -> app
- Required inputs and external dependencies
- Compact evidence-backed five-lens synthesis, only where relevant
- Evidence with exact file/symbol/commit references
- Up to five specific next checks or questions
- Readiness: reuse as-is / obtain external resource / code changes /
  cannot determine yet

Do not invent the original developer's workflow. If it is not
observable from available evidence, tell me what would prove it.
Do not implement anything yet.
~~~

---

## 1. Find the source of an asset

**Use when:** You see a floor plan, diagram, logo, exported chart, image, or document, but don't know whether it is generated or obtained elsewhere.

~~~text
In this existing feature: <FEATURE / EXAMPLE>,
trace the displayed asset back to its earliest accessible source.

Test the evidence for:
- Static repository asset
- Hosted file / CDN / object storage
- API-returned URL, markup, bytes, geometry, or metadata
- Database/config association
- Runtime-generated SVG, canvas, map, or other graphics
- Externally prepared or exported asset plus dynamic overlays

Find exactly where it is referenced, selected, downloaded, parsed,
transformed, and rendered. Follow asset paths, facility IDs, model
fields, service calls, conversion scripts, and related examples.

Look for provenance in file history, docs, PRs, tickets, and scripts
when accessible. Don't infer the original design tool from the SVG
format alone.

Finish with:
- Confirmed source and format, or the remaining alternatives
- Runtime flow and upstream origin (two distinct short diagrams)
- Required source input and who/what supplies it, if known
- Supporting file/symbol/history evidence
- The next specific check that settles any remaining ambiguity

Read-only; no implementation.
~~~

---

## 2. Reconstruct the original setup

**Use when:** The code works, but you don't know the setup steps or external resources a previous developer used.

~~~text
Investigate how <EXISTING FEATURE> appears to have been originally
set up, using repository and historical evidence rather than guesses.

Trace the earliest relevant commits, PRs, tickets, docs, scripts,
assets, dependencies, and configuration you can access.

Separate:
1. Proven implementation steps with citations.
2. Current configuration or runtime behavior.
3. Plausible but unconfirmed external/manual steps.
4. Missing ownership, access, or setup information.

Create an ordered prerequisite chain:
source material -> preparation/export/conversion -> storage/import ->
configuration -> application integration -> verification.

For each required resource or external tool, give its role, format,
location, evidence, access requirements, and likely owner if known.
Do not assert which design tool or method was used without evidence.

Conclude with a reproduction checklist and concrete questions for
the original developer, designers, operations team, or resource owner.
Read-only; do not create a plan or change code.
~~~

---

## 3. Compare an existing feature with a new instance

**Use when:** You need to reproduce a feature for a new facility, customer, tenant, or dataset.

~~~text
Use <EXISTING WORKING INSTANCE> as the reference for
<NEW INSTANCE OR FEATURE REQUEST>.

Before proposing code changes, investigate:
- The working instance's route, inputs, assets, services, and
  complete runtime/data flow.
- Its source material and any external preparation/import process.
- Which values are shared and which are specific to the instance.
- Asset and data contracts, including names, IDs, formats, dimensions,
  coordinate systems, mappings, storage paths, layers, and permissions.
- Whether a similar instance can be added with a new asset or config
  alone, or whether code changes are actually necessary.
- What historical evidence or other team input would confirm this.

Return:
1. Reusable parts.
2. Instance-specific inputs and setup steps.
3. External dependencies and resource owners.
4. Missing inputs or blockers.
5. Exact file/symbol/config evidence.
6. Recommended non-destructive verification.
7. Classification: reuse / new asset or data / code change / unknown.

Do not implement yet. Treat hypotheses as hypotheses.
Use APOSD, AT, DDIA, FODE, and SDI as optional learning lenses;
briefly explain only those that materially clarify the existing
workflow, its contracts, or reproduction prerequisites.
~~~

---

## Example: new facility floor plan

**Investigation question:** "There is already a facility floor plan in our application. I need to add a new facility. Is the existing plan created by code, fetched through an API, or supplied as an SVG or another external asset? What did the original setup require?"

A useful answer must distinguish possibilities such as:

| Possibility | Evidence to look for | What the new facility may need |
| --- | --- | --- |
| SVG committed in repo | Import/path to an SVG; asset history | New source SVG plus any ID/layer mappings |
| SVG in CDN or object storage | Asset URL, storage config, retrieval call | Obtain/upload file; configure storage path and permissions |
| API-generated geometry or markup | Endpoint contract and server rendering code | New API data/geometry and mapping |
| SVG/canvas rendered from data | Components building paths/shapes from coordinates | Floor geometry records, conversion, and coordinate rules |
| Base image plus live overlays | Image/SVG source and separate marker queries | New background asset and spatial mappings |
| Export from external design tool | Exported asset plus evidence in docs, scripts, or ticket | Source design file or approved export and import process |

**Important:** These are investigation branches, **not claims** about how any particular floor plan was implemented. An SVG file alone does not establish whether it came from Figma, Illustrator, CAD software, a manual editor, or a generator.

For this example, **FODE** would examine where the floor plan originates and how it is exported or imported; **DDIA** would examine which version and room mappings are authoritative; **SDI** would map the UI, asset storage, API, and any upstream provider; **AT** would explain coordinate or geometry processing *if present*; and **APOSD** would explain which interfaces separate the reusable viewer from facility-specific setup. Those are questions to investigate, not assumptions about the implementation.

---

## How this differs from existing prompts

| Prompt | Main question |
| --- | --- |
| **Existing Feature Investigation** (this file) | Where did this existing feature and its required resources come from, and what would it take to reproduce it? |
| [New Feature Discovery](investigate-new-feature.md) | What do users need from a new feature, and what requirements and options should we explore? |
| [Refine Feature Requirements](refine-feature-requirements.md) | Which requirements are ready, what needs stakeholder confirmation, and what can Superpowers design next? |
| [System Learning Implementation](system-learning-implementation.md) | How does the implementation execute, and why do its mechanisms work? |
| [System Learning Repo](system-learning-repo.md) | How is the whole codebase organized? |
| [Code Review](code-review.md) | Is a specific implementation or change correct and maintainable? |

**Suggested order for a new feature based on an old one:** Clarify the request or ticket (if there is one) -> investigate the existing feature and its provenance -> understand a tricky mechanism (if needed) -> confirm requirements -> design the change -> plan implementation -> implement and review.

Do not automatically run all prompts for every task. Use the shortest investigation that resolves the actual uncertainty.
