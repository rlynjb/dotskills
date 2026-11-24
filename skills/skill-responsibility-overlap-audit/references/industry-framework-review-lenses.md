# Industry Framework Review Lenses — Stage 2

Optional **industry-framework-aligned investigation** for `skill-responsibility-overlap-audit`. This is a **third optional review perspective**, separate from (1) `quality-review-questions.md` Q-01–Q-10 and (2) `review-lenses.md` AGNTCon/MCPCon conference lenses. It supplements the **same Stage 2 C1–C6 responsibility investigation**; it is not a separate skill or a new engineering stage.

**Important naming:** These entries are not all formal standards. One is a published international standard; the others are vendor architecture guidance, a voluntary public-sector AI risk framework, an academic architecture-evaluation method, and a community security-risk reference. Do not call the whole group 'standards certification' or infer full compliance.

## Optional invocation and output rules

- **Default: off.** Do not read this file or print industry coverage during a normal audit, Q-only review or conference-lens-only review.
- `industry_framework_review: relevant` — inspect the named targets first, select only frameworks pertinent to material source-backed issues, and state why each was selected. If none apply, explain in one sentence and omit empty coverage/source tables.
- `industry_framework_review: on` — consider all five entries **briefly**, marking clearly inapplicable ones NOT APPLICABLE. This is a broader review, not an obligation to create a finding for each framework.
- `industry_frameworks: [aws-agentic-ai-lens, cmu-sei-atam]` — consider **only** explicitly named framework IDs in the canonical order below; can be used without `industry_framework_review: on`. If combined with `on` or `relevant`, the explicit subset wins. Do not silently broaden the selection.
- **Stage 2 only:** Compare documented *current* inputs, responsibilities, outputs, handoffs, boundaries and feedback. Do not design interface schemas, implementation controls, approval mechanisms, invariants, orchestration or evaluation plans under this mode.
- **Output in Section 2:** After core C1–C6 tables and detailed F-xx notes, and **after** optional Q coverage and/or conference lens coverage plus conference reading when those were selected, insert **Industry Framework Review Coverage (optional)**. Use a Markdown comparison table with first column **Framework & investigation questions** (actual full adapted question text and C/Q mapping), then one or two inspected skill columns. For 3+ skills repeat selected framework rows in groups of at most two skill columns.
- **Coverage cells:** use one concise `PRESENT / PARTIAL / MISSING / NOT VERIFIED / NOT APPLICABLE` documentation/inspection status with a direct inspected target source link or explicit evidence limit and **existing F-xx (Cx)** only when an actual material finding exists. The row is a diagnostic index; all detailed findings remain once in their original Cx vertical blocks. Lack of runtime traces alone does not automatically create F-xx VERIFY.
- **Immediately after coverage:** Show **Official Industry Framework Sources & Further Reading (optional)** with **Framework / type | Topic or official section | Publisher & version | Official URL**. List one or two actual official links for each selected framework, consolidate duplicates, and don't invent unavailable normative details. A formal standard may have only a public abstract because its full text is licensed.
- **Evidence vs guidance:** Framework publications explain the **industry review perspective**. The audited target files and real supplied traces support specific findings. Do not claim full adherence, AWS Well-Architected assessment completion, NIST certification, completed ATAM, OWASP vulnerability discovery or tested behavior from this desk review.
- **No duplicated findings:** If Q review, conference lenses and industry frameworks identify one root issue, use **one existing F-xx (Cx)** rather than new 'industry' finding IDs. The review modes are independent opt-ins; activating this one does not silently activate the others.
- **Preserve the layout:** Six original C considerations, four investigation steps, seven numbered report sections, no HTML line breaks, no extra default table, no large cells, and human approval remains necessary for proposed changes.

## Industry framework lenses — adapted questions for Stage 2

### Framework: iso-25010 — ISO/IEC 25010:2023 — Software Product Quality

- **Type:** International Standard (product quality model).
- **Version/edition:** ISO/IEC 25010:2023 (second edition).
- **Applicable to:** When a skill's scope, outputs or handoffs make meaningful claims about software quality requirements or non-functional characteristics.
- **Review questions (Stage 2 adaptation, *not a verbatim official checklist*):** Which relevant product-quality concerns (for example, functional suitability, reliability, security, maintainability, compatibility or performance efficiency) are within this skill's responsibility? Are those expectations, outputs and exclusions documented rather than merely implied? Does a shared quality concern cause an actual ownership gap or only legitimate collaboration?
- **Inspect in the actual target:** Skill purpose and exclusions; input requirements; output claims and acceptance criteria; ownership of relevant quality expectations; supplied evidence.
- **Map to existing audit considerations:** C1 Inputs; C2 Responsibilities; C3 Outputs; C5 Boundaries. Related optional Q-01, Q-03, Q-05.
- **Boundary / source caution:** ISO defines a nine-characteristic quality model for ICT and software products, not a certification for individual Markdown agent skills. Only inspect relevant characteristics; do not claim full coverage, ISO conformance or an official ISO assessment without a separately authorized conformity method and access to the licensed normative text.
- **Official source links:**
  - **Official ISO/IEC 25010:2023 publication/abstract:** https://www.iso.org/standard/78176.html
  - **ISO committee listing of the published edition:** https://committee.iso.org/cms/live/live/en/sites/isoorg/contents/data/standard/07/81/78176.html

### Framework: aws-agentic-ai-lens — AWS Well-Architected Agentic AI Lens

- **Type:** Vendor-published architecture review guidance (not an international standard).
- **Version/edition:** Agentic AI Lens, published June 10, 2026 (verify revisions before future use).
- **Applicable to:** Skills involving agent roles, handoffs, orchestration, tool access, approval, cost/latency claims or real agent-system operational assumptions.
- **Review questions (Stage 2 adaptation, *not a verbatim official checklist*):** Are current agent/skill roles, success boundaries and intended handoffs clear, including who owns each part? Are tool/security boundaries, human gates, failure expectations and monitoring claims appropriately documented? Is a coordinator's responsibility supported by real workflow needs rather than assumed to be mandatory?
- **Inspect in the actual target:** SKILL.md purpose/activation, responsibilities and exclusions; documented handoffs and coordinator; tool permission declarations; output/failure handling and actual supplied traces if any.
- **Map to existing audit considerations:** C2 Responsibilities; C3 Outputs; C4 Handoffs; C5 Boundaries; C6 Feedback. Related optional Q-04, Q-05, Q-07, Q-08, Q-09.
- **Boundary / source caution:** AWS guidance is tailored to agentic AI workloads and AWS environments. Apply the questions by analogy when reviewing portable skills; do not imply an AWS deployment, official Well-Architected review, tested capability or production readiness. Stage 2 identifies gaps and risks; it does not implement AWS patterns.
- **Official source links:**
  - **AWS Agentic AI Lens overview, including six pillars and adoption paths:** https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html
  - **AWS AGENTOPS01 operational practices, role and handoff guidance:** https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentops01.html

### Framework: nist-ai-rmf — NIST AI Risk Management Framework (AI RMF 1.0)

- **Type:** Voluntary public-sector AI risk-management framework.
- **Version/edition:** NIST AI RMF 1.0, January 2023; official site reports revision in progress as of November 2026.
- **Applicable to:** Agent skills that make consequential AI decisions, accept untrusted inputs, delegate permissions or involve users, approvals, sensitive data, oversight or meaningful governance questions.
- **Review questions (Stage 2 adaptation, *not a verbatim official checklist*):** Who currently owns risk decisions, human oversight, change authorization and escalation for the selected skill? Are the intended uses, assumptions, boundaries and material AI risks documented? Are governance, risk assessment and claimed measurement/monitoring responsibilities distinguished from evidence that those practices actually occur?
- **Inspect in the actual target:** SKILL.md purpose, authorization limits and provenance rules; owner/approver notes; feedback/escalation; actual evaluation or incident evidence only if supplied.
- **Map to existing audit considerations:** C1 Inputs; C2 Responsibilities; C5 Boundaries; C6 Feedback. Related optional Q-01, Q-06, Q-07, Q-09.
- **Boundary / source caution:** NIST describes Govern, Map, Measure and Manage as continuous risk-management functions, not four mandatory Stage 2 steps. This light review is not a complete NIST AI RMF assessment, certification, regulatory audit or proof of risk mitigation. The NIST Playbook explicitly is not a required checklist.
- **Official source links:**
  - **NIST AI RMF 1.0 official framework overview:** https://airc.nist.gov/airmf-resources/airmf/
  - **NIST AI RMF Playbook — voluntary suggested actions:** https://airc.nist.gov/airmf-resources/playbook/

### Framework: cmu-sei-atam — CMU SEI Architecture Tradeoff Analysis Method (ATAM)

- **Type:** Research-based software architecture evaluation method (not a product standard).
- **Version/edition:** Established CMU SEI architecture evaluation method; not a new AAIF standard.
- **Applicable to:** Workflows with competing quality goals, meaningful multi-skill responsibility choices, integration-versus-independence trade-offs or unresolved architecture risk.
- **Review questions (Stage 2 adaptation, *not a verbatim official checklist*):** What stakeholder goal or quality scenario makes this responsibility/handoff question important? Which quality attributes or responsibilities could compete, such as reliability versus simplicity or security versus flexibility? Does current source evidence reveal a material risk, ambiguity or trade-off worth discussing with a human owner?
- **Inspect in the actual target:** Existing architecture context if supplied; target-skill boundaries, expected outcomes and user-visible responsibilities; known constraints, alternatives and sourced unknowns.
- **Map to existing audit considerations:** C2 Responsibilities; C3 Outputs; C4 Handoffs; C5 Boundaries; C6 Feedback. Related optional Q-01, Q-04, Q-05, Q-08.
- **Boundary / source caution:** Use *ATAM-inspired investigation questions*, not the full multi-day, stakeholder-led ATAM evaluation. Do not claim an ATAM was conducted, generate elaborate quality trees, approve architecture choices or finalize the Stage 3 contract.
- **Official source links:**
  - **CMU SEI ATAM collection — quality scenarios, risks and trade-offs:** https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/
  - **CMU SEI original ATAM report:** https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/

### Framework: owasp-agentic-top10-2026 — OWASP Top 10 for Agentic Applications (2026)

- **Type:** Community security-risk guidance (not certification or a regulatory standard).
- **Version/edition:** OWASP Top 10 for Agentic Applications 2026.
- **Applicable to:** Skills with autonomous tool calls, untrusted context, external resources, cross-agent delegation, memory, side effects or meaningful security/trust boundaries.
- **Review questions (Stage 2 adaptation, *not a verbatim official checklist*):** Does the inspected skill expose or delegate tool use, accept source instructions, retain memory or exchange context across agents, and if so who owns the risk? Are relevant threats such as tool misuse, identity/privilege abuse, memory/context poisoning, insecure inter-agent communication or cascading failures addressed or explicitly deferred? Are claimed security restrictions actually enforced by an inspected tool/host or merely written in prompt text?
- **Inspect in the actual target:** Tool inventory and effect permissions; external/context sources; handoff/delegation descriptions; approval and stop behavior; available code/host enforcement evidence only when accessible.
- **Map to existing audit considerations:** C1 Inputs; C2 Responsibilities; C4 Handoffs; C5 Boundaries; C6 Feedback. Related optional Q-06, Q-07, Q-08.
- **Boundary / source caution:** OWASP's ASI entries describe risk categories, not evidence that any audited skill is vulnerable. Do not list all ten issues for every skill, label a missing trace an exploit, claim OWASP compliance or prescribe a security control without target evidence.
- **Official source links:**
  - **OWASP GenAI Security Project — Top 10 for Agentic Applications 2026:** https://genai.owasp.org/top-10-for-agentic-applications-2026/

## Worked example — source evidence is still required

Given an inspected `SKILL.md` stating that its coordinator 'automatically invokes' a second skill but no actual host implementation is accessible:

- The **AWS** lens may raise a question about the current coordinator's documented role and handoff. The **ATAM** lens may raise a trade-off between an unnecessary coordination layer and clarity. The **OWASP** lens applies only if the actual handoff crosses a meaningful trust/privilege boundary.
- Place an F-xx (C4 or C5) only if the actual documented claim is materially unsupported, unsafe or conflicts with inspected evidence; otherwise record the evidence limitation. Distinguish **DOCUMENTED** text from **OBSERVED** execution.
- The proposed fix remains a **Stage 2 recommendation for human review**; exact contracts and how routing is implemented remain in Stages 3–4.
- The industry source links are **further reading**, never proof that either skill was executed or that a formal conformity assessment took place.

## Maintenance guidance

Reconfirm publisher pages and edition/revision dates before future additions. Label adapted questions as *our questions informed by* the named framework, not exact quotations or normative requirements. Preserve the core audit and other two optional review modes unchanged.
