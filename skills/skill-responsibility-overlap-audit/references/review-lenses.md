# Conference-Derived Review Lenses — Stage 2

Optional, expandable **investigation perspectives** for `skill-responsibility-overlap-audit`, not another skill or a new required report dimension. These are speaker takeaways from the user's **AGNTCon/MCPCon North America 2026** session PDFs, **not official AAIF/MCP requirements or proof of runtime behavior**.

**Source provenance:** The user’s saved Google Drive session-note folder contains the slide PDFs linked below. The original `collaborative-agent-skill-workflow.md` conference synthesis supplied the earlier lens mapping; the listed PDF content was inspected again in November 2026. Matching YouTube links come from the saved `AGNTCon_MCPCon_2026_YouTube_PDF_Map.xlsx` title/speaker match, and were **not independently watched or checked for ongoing playback**. If no video is matched, provide PDF only; do not invent video URLs.

## How to apply

- **Default off.** Load only for an explicit named `review_lenses: [context-engineering, security-and-trust]` or `review_lenses: relevant` request. In `relevant` mode choose only lenses justified by inspected skill material and briefly explain applicability; if none apply, explain and omit empty tables.
- Preserve **C1–C6**, the **four Stage 2 investigation steps** and **seven report sections**. Put any material issue in the relevant Cx table cell as an **F-xx** pointer and explain it once in its existing vertical Finding/Evidence/Assessment/Why/Recommendation note. A lens is a source of investigation questions, not a second set of numbered findings.
- Within **Section 2**, place optional **Quality Review Coverage** first if Q-01–Q-10 was enabled, then **Review Lens Coverage (optional)**. Its first column uses the selected lens name, full `Review questions`, and `Map to` C/Q references; skill columns have short evidence-backed observations and existing **F-xx (Cx)** only when genuinely material. With 3+ skills use at most two skill columns per lens table and repeat selected lens rows.
- **Immediately after lens coverage**, output **Conference Sources & Further Reading (optional)**: a separate compact Markdown table with **Lens / Topic | Session title & speaker | PDF | YouTube (when matched)**. Include the most relevant 1–3 source presentations **for each selected lens**, consolidate repeated sessions, and include direct links from the entries below. Even a lens with no material F-xx can provide reading if it was explicitly selected. Do not print this table for a default or Q-only run.
- **Source separation:** The inspected target skill, its cited files and supplied execution traces are evidence for F-xx. Conference sessions are *learning/rationale sources*, never evidence that a target skill enforces security, has a runtime failure, or passes an evaluation. Conference links must appear in the generated report, not merely in this reference.
- **Q mapping:** The referenced Q-01–Q-10 IDs describe related **optional** quality questions, **not questions separately assessed** in a lens-only run. Do not silently activate Q review or turn missing execution traces into generic VERIFY findings.
- **Boundary:** This Stage 2 audit investigates current responsibilities and makes human-reviewed proposals. It does not finalize input/output, behavior, approval, failure or orchestration contracts (Stage 3), edit skills, implement a coordinator or run tests. Preserve independent starting paths where actually documented; do not invent optional handoffs.

## Lens: context-engineering

- **Applicable to:** Skills accepting retrieved documents, tickets, repository context, memory, or other skills' artifacts.
- **Review questions:** Are provenance, revisions, evidence gaps and contradictions preserved? Is the source of truth identified? Are instructions found inside untrusted documents treated as data rather than authority? Does a consumer treat another skill's output as evidence rather than silently inheriting its decision authority?
- **Targeted follow-ups:** Is a handoff passing more context than needed? Is shared input correctly distinguished from duplicated responsibility? These are questions to investigate, not a requirement to mandate a new context schema.
- **Inspect:** Input and handoff instructions, producer/consumer responsibilities, source links or revisions, permission language and supplied traces (if available).
- **Map to:** C1 Inputs; C4 Handoffs; C5 Boundaries. Q-03, Q-06.
- **Stage 2 boundary:** Do not claim a context-security failure or costly handoff from an absent run trace; do not define a new interface contract in Stage 2.
- **Conference sessions & reading:**
  - **Topic:** Provenance and untrusted stored context. **Session:** Trustworthy Context Is Untrusted by Default. **Speaker:** Shub Argha. **PDF:** [Saved presentation](https://drive.google.com/file/d/19aoCF7WZ2GfVi7vb5ISZHIPKkQOtjjz1/view). **YouTube:** No matched video link in saved index.
  - **Topic:** Narrow, explicit handoffs; separate context from authority. **Session:** Don't Share the Database: Interface Contracts Between Isolated AI Agents. **Speaker:** Martin Bliss. **PDF:** [Saved presentation](https://drive.google.com/file/d/1E4J2rfYLoN-H9wnK_K3f6bGshiwmDUmo/view). **YouTube:** No matched video link in saved index.
  - **Topic:** Agent-facing interfaces and examples versus excessive instructions. **Session:** Patterns for Shifting from MCP as a Basic API to MCP as Agent Integration Interface. **Speaker:** James Ward and Alexander Ioffe. **PDF:** [Saved presentation](https://drive.google.com/file/d/1a37Vr3kwddeoA-z1rNlsrjUQS-nUHuOZ/view). **YouTube:** [Matched session video](https://www.youtube.com/watch?v=Okw9oLIB-GU).

## Lens: security-and-trust

- **Applicable to:** Skills with tool access, delegated work, optional coordinators, writes, external data, credentials, or human approvals.
- **Review questions:** What is the real permission boundary? Is least privilege enforced by tool/host/server controls? How does the skill handle untrusted instructions, missing approval and unauthorized effects? If one skill or coordinator delegates to another, who authorizes the next action and what authority actually transfers?
- **Targeted follow-ups:** Look for unintended authority escalation, cross-skill rewriting or publishing, approval treated as implicit, and tool definitions that may drift after approval. A written rule is not proof of actual enforcement.
- **Inspect:** Documented approval owners and side effects, coordinator/delegation descriptions, available host/tool permissions or manifests, mutable tool references, and real supplied security evidence.
- **Map to:** C1 Inputs; C4 Handoffs; C5 Boundaries; C6 Feedback. Q-06, Q-07.
- **Stage 2 boundary:** Report grounded authority ambiguity or risk; do not prescribe OAuth, cryptographic delegation, runtime controls or security implementation in Stage 2.
- **Conference sessions & reading:**
  - **Topic:** Delegation boundaries, who acts under whose authority. **Session:** When Agents Spawn Agents: Securing Recursive Delegation in Multi-Agent Systems. **Speaker:** Anishma Mavuram. **PDF:** [Saved presentation](https://drive.google.com/file/d/1_jXpA_vFEBAAPYeklZmliAs9jNWZTyWx/view). **YouTube:** [Matched session video](https://www.youtube.com/watch?v=glxs_6J-7sQ).
  - **Topic:** Mutable tool definitions and renewed approval. **Session:** MCP Rug Pulls in the Wild: Live Attacks and How to Stop Them. **Speaker:** Charit Upadhyay and Advait Patel. **PDF:** [Saved presentation](https://drive.google.com/file/d/1X38wcquvL67JnJm_00zHY0E8rTjyTDrc/view). **YouTube:** [Matched session video](https://www.youtube.com/watch?v=EgkuEPUci24).
  - **Topic:** Identity and least-privilege authority when agents call tools. **Session:** Stop Running Agents as Service Accounts: User-Scoped Access for Enterprise Tool Calls. **Speaker:** Masato Kozuka. **PDF:** [Saved presentation](https://drive.google.com/file/d/1pFtRiB7w-_B4G10fbOwEZvq5PcAqf80Z/view). **YouTube:** No matched video link in saved index.

## Lens: reliability-and-workflow

- **Applicable to:** Skills with multiple steps, optional handoffs, missing inputs, partial results, human escalation or coordinator proposals.
- **Review questions:** Are conditions for proceeding, stopping or returning clear? Are failed/missing handoffs surfaced rather than hidden? Does a proposed coordinator actually solve an evidenced coordination issue? When a result is incomplete, blocked, pending or needs human input, is the next responsible owner identifiable?
- **Targeted follow-ups:** Can each skill still start and finish on its own when optional context is unavailable? Does the coordinator own only routing/context continuity, or does it wrongly take over domain decisions? Distinguish a documented optional handoff from an actually implemented dispatch.
- **Inspect:** Documented steps, handoff clauses, completion/error labels, return/feedback paths, human gates, coordinator responsibilities, and supplied journey traces if available.
- **Map to:** C2 Responsibilities; C4 Handoffs; C5 Boundaries; C6 Feedback. Q-04, Q-05, Q-08.
- **Stage 2 boundary:** Stage 2 identifies missing or conflicting ownership/status evidence. Stage 3 defines the precise error, interface or dispatch contract; Stage 4 implements it.
- **Conference sessions & reading:**
  - **Topic:** Completion, additional-input, asynchronous and progress states. **Session:** Agentic Messaging Primitives in MCP. **Speaker:** Caitie McCaffrey. **PDF:** [Saved presentation](https://drive.google.com/file/d/1OwyNvZGpIFDnc9KchDq5uER9DpgzLG4g/view). **YouTube:** [Matched session video](https://www.youtube.com/watch?v=iNV5-YkPHW4&t=21711s).
  - **Topic:** Separate agent reasoning from controlled workflow execution. **Session:** Non-Deterministic Minds, Deterministic Tools. **Speaker:** Adrian Warman. **PDF:** [Saved presentation](https://drive.google.com/file/d/1NNGBWE4u2cm0Ia4qAmUXPonxEKnxTwdf/view). **YouTube:** No matched video link in saved index.
  - **Topic:** Narrow, explicit handoffs; separate context from authority. **Session:** Don't Share the Database: Interface Contracts Between Isolated AI Agents. **Speaker:** Martin Bliss. **PDF:** [Saved presentation](https://drive.google.com/file/d/1E4J2rfYLoN-H9wnK_K3f6bGshiwmDUmo/view). **YouTube:** No matched video link in saved index.

## Lens: evaluation-and-observability

- **Applicable to:** Skills claiming reliable outcomes, evaluation coverage, production-readiness, traceability, dispatch correctness or measurable cost; also material multi-skill duplication claims.
- **Review questions:** Are critical user journeys, fixtures, baselines and evaluation criteria clear? Are output, trajectory and outcome distinguished? Are eval definitions separated from actual runs, tool traces, token cost and failure evidence? Is an apparently redundant skill or additional layer backed by a concrete responsibility or meaningful outcome rather than a speculative cost claim?
- **Targeted follow-ups:** Are findings material and actionable rather than generic VERIFY noise? Does a supposed token or latency burden have actual evidence, or is it a hypothesis for later measurement? Check whether a specialized skill adds a distinct responsibility before recommending removal.
- **Inspect:** Existing test definitions versus runs, supplied trajectories and outcome evidence, actual source-based responsibility boundaries, material duplicate behaviors, and recorded review decisions.
- **Map to:** C2 Responsibilities; C3 Outputs; C6 Feedback. Q-09.
- **Stage 2 boundary:** Do not run evals, calculate invented scores or mark unseen behavior as failed. Missing execution traces for a documented handoff are ordinarily a scope note; recommend Stage 5 verification only with a material trigger.
- **Conference sessions & reading:**
  - **Topic:** Critical user journeys and costs of over-broad skills. **Session:** Building an Agentic Eval Pipeline: Battle-Tested Lessons with EvalBench. **Speaker:** Kurtis Van Gent and Haoyu Wang. **PDF:** [Saved presentation](https://drive.google.com/file/d/1us0-hWJPMvH7dw2ZGoCvbRRUtJBFSyBf/view). **YouTube:** No matched video link in saved index.
  - **Topic:** Finding precision, actionable review outcomes and noise. **Session:** Cut the Noise: Building a Code Reviewer You Can Trust. **Speaker:** Joah Gerstenberg. **PDF:** [Saved presentation](https://drive.google.com/file/d/1_jUfEJLY9lntZOvls2RWl-65oT_te4Zt/view). **YouTube:** No matched video link in saved index.
  - **Topic:** Tool/skill discovery overhead and mistaken domain routing. **Session:** The MCP Cold-Start Problem: When Your Agent Has 100 Tools and Has to Pick One. **Speaker:** Karthik Karunanithi. **PDF:** [Saved presentation](https://drive.google.com/file/d/1AT1V9r0LR0E8LeXN6A7AOqfNcgwoYjX4/view). **YouTube:** [Matched session video](https://www.youtube.com/watch?v=eB9I4Ixx2wc&t=7652s).

## Lens: lifecycle-and-portability

- **Applicable to:** Shared, updated or versioned skills; monorepos with multiple instruction files; cross-harness or coordinator claims.
- **Review questions:** Is there one current source of truth, with recorded owner/version? Are linked resources present? Are claimed hosts actually tested? Is review, rollback and release evidence available? Do multiple skills or instruction files repeat conflicting or stale versions of the same boundary rule?
- **Targeted follow-ups:** Are SKILL.md, AGENTS.md or adapter instructions duplicating authority rather than pointing to one canonical source? Are tool/host assumptions explicitly documented versus verified, especially when versions change?
- **Inspect:** SKILL.md and linked references, neighboring instruction/adapter files, source-control revisions, documented owners and host/dependency claims, available CI/runtime evidence.
- **Map to:** Cross-cutting C2 Responsibilities; C4 Handoffs; C5 Boundaries. Q-03, Q-10.
- **Stage 2 boundary:** File-format checks and successful CI do not prove cross-host runtime compatibility. Recommend the smallest source-of-truth clarification, not an unrequested release system.
- **Conference sessions & reading:**
  - **Topic:** One source of truth; concise instructions and stale-rule detection. **Session:** AGENTS.md Is the New CONTRIBUTING.md: A Field Report from One Year of Agent-Friendly Monorepos. **Speaker:** Unnati Mishra. **PDF:** [Saved presentation](https://drive.google.com/file/d/1ICV_vH6Q5qAAu-2sodIs03Ffbxv6Tl4P/view). **YouTube:** No matched video link in saved index.
  - **Topic:** Effective agent definitions, ownership, version and release provenance. **Session:** Stop Writing Agents, Declare Them: Declarative Agent Architecture in Production. **Speaker:** Chris Knuteson. **PDF:** [Saved presentation](https://drive.google.com/file/d/1f9v2ZupSLbcik_AkKJgtfVu9mmVZ5jjI/view). **YouTube:** No matched video link in saved index.
  - **Topic:** Skill versioning, portability assumptions and review/scan boundaries. **Session:** Shipping Agent Skills Safely: CI/CD, Evals, and Guardrails. **Speaker:** Michael Larson. **PDF:** [Saved presentation](https://drive.google.com/file/d/1eU_vKOAiG-8nZzbYNWaTBZE-TvFxw6j3/view). **YouTube:** No matched video link in saved index.

## Add future learning without changing the core audit

Only add a sourced topic when its applicability, Stage 2 question, C/Q relationship and actual evidence needed are clear. Preserve the five optional lenses unless a separate user decision justifies changing them.

- **Source fields:** Topic, exact session title, speaker, saved PDF link and matched YouTube link when available; make actual output links direct and readable.
- **Analysis fields:** Specific review question, what to inspect in the target skill, relevant Cx or Q reference, and what the source cannot establish about the target.
- **Output:** Normal F-xx only if a meaningful source-backed issue exists; optional Further Reading stays separate from finding evidence.

Never add a seventh consideration, another numbered report section, mandatory extra Qs, an automatic coordinator, security controls or unrequested evaluation.

**Session context:** [AGNTCon/MCPCon 2026 saved session folder](https://drive.google.com/drive/folders/1xoTFt4SqFKQjf-rXu1OihsKhg7jAylzN) (source collection, not evidence of session attendance).
