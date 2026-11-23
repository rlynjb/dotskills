# Conference-Derived Review Lenses

Optional, expandable quality-review questions for `skill-responsibility-overlap-audit`. These are **suggestions inspired by the user's saved AGNTCon/MCPCon 2026 conference synthesis**, not official AAIF requirements, security certifications or evidence that a skill ran correctly.

**Immediate source:** `collaborative-agent-skill-workflow.md` (saved November 1, 2026), section “Conference evidence behind the process.” The file is in the user's ChatGPT Library and is **not automatically included in a standalone coding-agent distribution**. Session references and slide-page pointers below come from that synthesis; check original slides if independent verification is needed.

## How to apply

- Load only on explicit request for one or more named lenses, or for **relevant lenses** when their applicability is established by inspected skill content. Default: none.
- Keep C1–C6 comparison tables unchanged. Route a material concern to an F-xx finding under its most relevant C-row. A lens is an investigation prompt, not a new report section, Q status, or reason to manufacture a problem.
- If Q-01–Q-10 review is also requested, merge overlapping lens/Q concerns into **one** F-xx finding and cross-reference the applicable Q; otherwise do not print a Q checklist.
- Cite the actual audited skill's evidence, not just a conference takeaway. Distinguish DOCUMENTED from OBSERVED and INFERRED. Never claim a prompt-only permission is enforced.

## Lens: context-engineering

- **Applicable to:** Skills accepting retrieved documents, tickets, repository context, memory, or cross-skill artifacts.
- **Review questions:** Are provenance, revisions, evidence gaps and contradictions preserved? Is the source of truth identified? Are instructions found inside untrusted documents treated as data rather than authority?
- **Inspect:** Input evidence rules, source links, freshness/contradiction handling and any provided context traces.
- **Map to:** C1 Inputs; C5 Boundaries. Q-03, Q-06.
- **Conference takeaway:** Shub Argha, “Trustworthy Context Is Untrusted by Default,” `trustworthy-context-is-untrusted-by-default.pdf` (synthesis cites pp. 11–16, 21–22). Unnati Mishra's AGENTS.md talk also addresses stale instructions.

## Lens: security-and-trust

- **Applicable to:** Tools, writes, external access, credentials, untrusted text, human approvals or boundary crossings.
- **Review questions:** What is the real permission boundary? Is least privilege enforced by tool/host/server controls? How does the skill handle untrusted instructions, missing approval and unauthorized effects?
- **Inspect:** Skill boundaries, tool permissions where accessible, relevant security fixtures and actual supplied traces.
- **Map to:** C1 Inputs; C5 Boundaries; C6 Feedback. Q-06, Q-07.
- **Conference takeaways:** Shub Argha's context-trust talk; Michael Larson, “Shipping Agent Skills Safely: CI/CD, Evals, and Guardrails,” `shipping_agent_skills_safely.pdf` (synthesis cites pp. 6–11, including scan/review/sandbox).

## Lens: reliability-and-workflow

- **Applicable to:** Multi-step skills, handoffs, error states, partial outputs and human escalation.
- **Review questions:** Are conditions for proceeding, stopping or returning clear? Are failed/missing handoffs surfaced rather than hidden? Does a proposed coordinator actually solve an evidenced coordination issue?
- **Inspect:** Documented state changes, failure paths, conditional inputs, status outputs and supplied journey traces.
- **Map to:** C2 Responsibilities; C4 Handoffs; C5 Boundaries; C6 Feedback. Q-04, Q-05, Q-08.
- **Conference takeaway:** Kurtis Van Gent and Haoyu Wang, “Building an Agentic Eval Pipeline: Battle-Tested Lessons with EvalBench,” `mcpcon-na-26-building-an-agentic-eval-pipeline_-battle-tested-lessons-with-evalbench-agntcon-2026.pdf` (synthesis cites pp. 8–12, 15, 18, 20, including critical user journeys).
- **Boundary:** Identify open questions in Stage 2; contract/failure policy design belongs to Stage 3.

## Lens: evaluation-and-observability

- **Applicable to:** Skills claiming reliable results, evaluation coverage, traceability, deployment readiness or measurable cost.
- **Review questions:** Are critical user journeys, fixtures, baselines and evaluation criteria clear? Are output, trajectory and outcome distinguished? Are eval definitions separated from actual runs, tool traces, token cost and failure evidence?
- **Inspect:** Eval definitions, trace/run outputs where supplied, judge criteria, regression history and version/host details.
- **Map to:** C3 Outputs; C6 Feedback. Q-09.
- **Conference takeaways:** Kurtis Van Gent and Haoyu Wang's EvalBench session; Joah Gerstenberg, “Cut the Noise: Building a Code Reviewer You Can Trust,” `cut-the-noise-joah-gerstenberg-agntcon-2026-1.pdf` (synthesis cites pp. 11–14, 21–25, emphasizing human review usefulness and precision).
- **Boundary:** Suggest candidate checks, but never execute or claim a passing evaluation in this audit.

## Lens: lifecycle-and-portability

- **Applicable to:** Updated, shared, versioned or cross-harness skills.
- **Review questions:** Is there one current source of truth, with recorded owner/version? Are linked resources present? Are claimed hosts actually tested? Is review, rollback and release evidence available?
- **Inspect:** SKILL.md, references, commit history, actual host evidence, release notes and CI outcomes if accessible.
- **Map to:** Cross-cutting C2, C4, C5 as applicable. Q-03, Q-10.
- **Conference takeaways:** Michael Larson's skill-release talk (version/evaluate/review/release); Unnati Mishra, “AGENTS.md Is the New CONTRIBUTING.md,” `agents.md-is-the-new-contributing.md-2.pdf` (synthesis cites pp. 8–10, 15, 18–20); Chris Knuteson, “Stop Writing Agents, Declare Them,” `declarative-agents-release-story-v2.pdf` (synthesis cites pp. 2, 5, 8, 18).
- **Boundary:** Passing file-format CI is not proof of cross-host runtime compatibility.

## Add future learning without changing the core audit

For a new, sourced review lens, use a short vertical entry:

- **Name:** Reusable lens title.
- **When relevant:** Skills/capabilities to which it applies.
- **Investigation question:** Specific unknown to investigate.
- **Evidence needed:** Files, traces, permissions or decisions required.
- **C/Q mapping:** Existing C1–C6 and optionally Q-01–Q-10.
- **Source:** Speaker, session, slide/document, page/date, link when verified.
- **Evidence caution:** What cannot be established without actual runtime evidence.
- **Output:** A normal F-xx finding only when meaningful.

Do not add a seventh consideration, another default report section, mandatory extra Qs, or an unrequested adapter.

**Public schedule context:** https://events.linuxfoundation.org/agntcon-mcpcon-north-america/program/schedule/ . This is schedule context, not independent verification of specific deck claims.
