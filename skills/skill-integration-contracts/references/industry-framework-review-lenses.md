# Industry Framework Review Lenses — Stage 3

Optional **industry-framework-aligned contract-design review** for `skill-integration-contracts`. This is a third independent optional perspective alongside (1) `contract-quality-review-questions.md` CQ-01–CQ-06 and (2) `review-lenses.md` AGNTCon/MCPCon conference perspectives. It evaluates **proposed IC-xx integration agreements** and preserves the normal four-step design procedure and seven report sections.

**Naming and scope:** These are five *different types* of authoritative industry resources, not five formal standards and not a new validation harness. One is an international standard; the other four are vendor architecture guidance, a voluntary public-sector AI risk framework, an architecture-evaluation method, and community security guidance. All questions below are **Stage 3 adaptations for learning and design review**, not quoted normative requirements, certifications, compliance gates, or evidence that an integrated agent ran.

## Optional invocation and output rules

- **Default off:** Do not read or render this reference in an ordinary Stage 3 design, a CQ-only review, or a conference-lens-only review.
- `industry_framework_review: relevant` — after drafting actual IC-xx cards, select only source-relevant industry frameworks and explain briefly why they matter. If no framework is material, explain that and omit empty coverage/source tables.
- `industry_framework_review: on` — consider all five entries proportionally, marking an entire irrelevant framework NOT APPLICABLE. This is more comprehensive design review, **not** a reason to create five separate contracts or warnings.
- `industry_frameworks: [aws-agentic-ai-lens, cmu-sei-atam]` — consider **only** named IDs, in the canonical order below. This subset takes precedence when combined with `on` or `relevant`. Do not silently expand the selection.
- **Review target:** Every applicable actual **IC-xx card** (a material producer-to-consumer connection or one skill's justified standalone entry/exit contract), **not** the underlying skills as a Stage 2 audit. Keep original current skill evidence, approved decisions, proposed terms, assumptions, and runtime-unknown status distinct.
- **Placement:** Within **Section 5 — Cross-Cutting Guarantees & Trade-offs**, after normal material notes, after optional Contract Quality Review Coverage, and after optional conference Review Lens Coverage and Conference Sources & Further Reading, insert **Industry Framework Review Coverage (optional)**. First column: selected framework title, full adapted Stage 3 questions and mapping to relevant contract dimensions. Remaining columns: 1–2 real IC-xx cards; with 3+ contracts, repeat selected rows in groups of at most two contract columns.
- **Coverage cells:** One concise `CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE` **design assessment** plus source/design reason and real IC-xx, D-xx and supplied Stage 2 F-xx (Cx) pointers where relevant. Treat `CLEAR` as a clear **proposal only**, not approved, implemented, tested or enforced. Missing host execution traces are ordinarily not a defect of an otherwise explicit design.
- **Further reading:** Immediately after coverage, append **Official Industry Framework Sources & Further Reading (optional)** within Section 5, using columns `Framework / type | Topic or official section | Publisher & version | Official URL`. Include one or two publisher URLs for **only** the selected frameworks. The ISO public abstract does not license reproducing the full standard.
- **Human decisions:** If a material framework question reveals ambiguity, refine the **existing IC-xx proposal** and link to an existing or newly justified **D-xx decision in Section 6**. Do not invent a second findings-ID scheme, automatically approve the design, or alter target skill files.
- **Independent modes:** Industry-only never activates CQ-01–CQ-06 or conference lenses. If multiple modes are requested, preserve the Section 5 order **core trade-offs → CQ (if enabled) → conference lenses/sources (if enabled) → industry frameworks/official sources (if enabled)**. Reuse the same IC/D decisions and avoid double-counting the same issue.
- **Stage boundaries:** This read-only Stage 3 review may identify proposed guarantees and Stage 4 handoff changes or Stage 5 validation candidates, but does not implement agents, invoke a coordinator, run evaluations, grant runtime authority or certify industry compliance. Keep standalone skill entry paths and real mandatory safety requirements.

## Industry framework lenses — Stage 3 contract-design adaptations

### Framework: iso-25010 — ISO/IEC 25010:2023 — Software Product Quality

- **Type:** Published International Standard (software and ICT product-quality model).
- **Version/edition:** ISO/IEC 25010:2023, edition 2 (November 2023).
- **Applicable to:** A proposed handoff makes material software-quality promises, or introduces trade-offs involving reliability, compatibility, maintainability, security or performance efficiency.
- **Review questions (Stage 3 adaptation, not verbatim published requirements):** Are the specific quality attributes relevant to this connection translated into clear, proportional IC-xx guarantees, rather than vague promises? Is the consumer told which guarantees it can rely on, with quality trade-offs and exception conditions disclosed where material? Does the agreement preserve the standalone functionality and maintainability of both skills?
- **Inspect:** Existing proposed IC-xx input/output, behavior and compatibility guarantees; source-backed constraints; affected D-xx choices and alternatives.
- **Map to contract dimensions:** Behavior; Compatibility and evolution; Interface; Failure, feedback and fault isolation.
- **Related optional CQ questions (references only):** CQ-02, CQ-06. Do not claim these were separately run in an industry-only review.
- **Boundary / source caution:** The standard defines a product-quality model with nine characteristics, not a certification for Markdown agent skills or an implementation-level contract checklist. Inspect only applicable characteristics. Its normative text is licensed; the public URL gives the official abstract. Do not claim ISO conformance or require a metric for every characteristic.
- **Official publisher sources:**
  - **Official ISO/IEC 25010:2023 publication and abstract:** https://www.iso.org/standard/78176.html

### Framework: aws-agentic-ai-lens — AWS Well-Architected Agentic AI Lens

- **Type:** Vendor-published architecture-design and operations guidance.
- **Version/edition:** Published June 10, 2026; confirm future documentation revisions before reuse.
- **Applicable to:** An intended producer-consumer handoff involves agent roles, context exchange, a coordinator, approval boundaries, failure recovery, observation or material token/latency/cost trade-offs.
- **Review questions (Stage 3 adaptation, not verbatim published requirements):** Do IC-xx cards identify producers, consumers and human owners without creating redundant coordination or coupling? Are consequential permissions, human gates, and failure/feedback outcomes clear for each material connection? Is a proposed coordinator justified against a simpler manual optional handoff? Are observability, cost and latency expectations proportional to the selected workflow rather than speculatively required?
- **Inspect:** IC-xx interfaces, behavior, trust/failure/observability clauses; D-xx routing and approval choices; current source evidence and known host limitations.
- **Map to contract dimensions:** Interface; Behavior; Security, authority and trust; Failure, feedback and fault isolation; Observability and evidence.
- **Related optional CQ questions (references only):** CQ-01, CQ-02, CQ-03, CQ-04, CQ-05, CQ-06. Do not claim these were separately run in an industry-only review.
- **Boundary / source caution:** AWS designed this lens for agentic AI workloads; it is not an AWS requirement for portable skills. Use its architectural ideas selectively, not a complete AWS Well-Architected assessment. Do not infer AWS deployment, working orchestration, guaranteed traces or measured operational outcomes.
- **Official publisher sources:**
  - **AWS Agentic AI Lens overview and design/operations pillars:** https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html

### Framework: nist-ai-rmf — NIST AI Risk Management Framework (AI RMF 1.0)

- **Type:** Voluntary AI governance and risk-management framework.
- **Version/edition:** NIST AI RMF 1.0 (January 2023); official site notes revision in progress as of November 2026.
- **Applicable to:** A proposed integration crosses human approval, data-trust, delegated decision, consequential output, untrusted context or oversight boundaries.
- **Review questions (Stage 3 adaptation, not verbatim published requirements):** Does the proposed integration identify who governs and approves consequential decisions, including where human intervention is required? Are material trust/authority assumptions and foreseeable harms explicit enough for the reviewer to choose or defer the agreement? Do source provenance, unresolved concerns and monitoring/validation ownership remain traceable without claiming that a risk-control mechanism already exists?
- **Inspect:** IC-xx trust and source-provenance clauses; proposed approval ownership; linked D-xx human choices, material uncertainties and future validation candidates (proposed only).
- **Map to contract dimensions:** Security, authority and trust; Observability and evidence; Behavior; Failure, feedback and fault isolation.
- **Related optional CQ questions (references only):** CQ-03, CQ-05, CQ-04. Do not claim these were separately run in an industry-only review.
- **Boundary / source caution:** Govern, Map, Measure and Manage are NIST's risk functions, not four additional Stage 3 steps or a mandatory implementation checklist. The NIST Playbook says its suggestions are voluntary and should be tailored. No NIST certification, completed risk assessment or control enforcement follows from a proposed contract.
- **Official publisher sources:**
  - **NIST AI RMF 1.0 official framework:** https://airc.nist.gov/airmf-resources/airmf/
  - **NIST AI RMF Playbook — voluntary suggestions:** https://airc.nist.gov/airmf-resources/playbook/

### Framework: cmu-sei-atam — CMU SEI Architecture Tradeoff Analysis Method (ATAM)

- **Type:** Established architecture-evaluation method (not a software product standard).
- **Version/edition:** CMU Software Engineering Institute ATAM method (original publications and collection).
- **Applicable to:** Multiple plausible connection designs, coordinator versus manual routing, conflicting quality goals, or approval/failure guarantees introduce meaningful trade-offs.
- **Review questions (Stage 3 adaptation, not verbatim published requirements):** Which user or stakeholder goal justifies the proposed handoff contract? What realistic quality scenario would expose the design's most important risk or ambiguity? Have the smallest viable option, alternative and trade-off been explained in the linked IC-xx/D-xx cards without pretending the alternative was implemented or tested?
- **Inspect:** Selected producer-consumer map, proposed IC-xx guarantees and D-xx alternatives, scenario assumptions, actual baseline evidence and documented risk/mitigation.
- **Map to contract dimensions:** Behavior; Failure, feedback and fault isolation; Compatibility and evolution; Security, authority and trust.
- **Related optional CQ questions (references only):** CQ-02, CQ-04, CQ-06. Do not claim these were separately run in an industry-only review.
- **Boundary / source caution:** This is an ATAM-inspired design-review question set, not a formal ATAM evaluation or substitute for one. Full ATAM requires stakeholder participation and explicit quality scenarios. Do not invent a utility tree, declare a design approved, or force an additional coordinator or architecture artifact.
- **Official publisher sources:**
  - **CMU SEI ATAM collection — architecture risks and quality trade-offs:** https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/

### Framework: owasp-agentic-top10-2026 — OWASP Top 10 for Agentic Applications (2026)

- **Type:** Community-developed agent-specific security risk guidance.
- **Version/edition:** OWASP GenAI Security Project, 2026.
- **Applicable to:** The proposed contract passes untrusted documents or mutable tool instructions, invokes tools/agents, transfers privileges, coordinates multiple agents or allows consequential side effects.
- **Review questions (Stage 3 adaptation, not verbatim published requirements):** Does the contract preserve the distinction between untrusted content and authorized instructions, with an identified human/tool decision boundary? Could the proposed handoff allow an agent or coordinator to misuse tools, broaden delegated authority, poison another skill's context, or create cascading failure? Are relevant mitigations, stop conditions and unresolved host-enforcement assumptions represented only where they are material?
- **Inspect:** IC-xx source/provenance, optional context/behavior, delegated authority, stop/failure terms; D-xx explicit approvals; actual supplied code/host evidence for any enforcement claim.
- **Map to contract dimensions:** Security, authority and trust; Interface; Failure, feedback and fault isolation; Compatibility and evolution.
- **Related optional CQ questions (references only):** CQ-01, CQ-03, CQ-04, CQ-06. Do not claim these were separately run in an industry-only review.
- **Boundary / source caution:** The OWASP list is a threat taxonomy, not evidence that a particular skill is vulnerable or an OWASP certification. Select relevant threat categories only; don't require all ten, imply an attack was observed, or prescribe a detailed runtime security system from a Stage 3 design review.
- **Official publisher sources:**
  - **OWASP Agentic Top 10 (2026) official project page:** https://genai.owasp.org/top-10-for-agentic-applications-2026/

## Illustrative use — optional PRD handoff

Suppose a user wants to optionally provide PRD context to Refine Requirements. The producer's source is inspected, but no runtime integration exists.

- **AWS Agentic AI Lens (design perspective):** Is a manual, user-chosen handoff sufficient, or is a coordinator demonstrably needed? The smallest independent handoff may be preferable.
- **NIST AI RMF (oversight perspective):** Does IC-01 clearly preserve the human approval state for any changes? If the approval owner is unresolved, mark D-01 `PROPOSED / NEEDS HUMAN`, not approved.
- **ATAM (trade-off perspective):** Compare manual optional exchange against coupled dispatch for one realistic failure scenario (e.g., the PRD is missing or stale); explain the benefit and downside without designing retries.
- **OWASP (risk perspective, only if material):** Does untrusted PRD text remain source data rather than permission to act or rewrite?
- **Evidence:** Cite current target SKILL.md and real Stage 2 findings, if provided, for claims about the skills. Cite these publishers **only** for the review method or further reading. No live execution, certification or approved contract is implied.

## Maintenance

Recheck official editions and publisher URLs when this reference is revised. Preserve the framework distinctions, treat Stage 3 review questions as our adaptations, and avoid duplicating the five conference lenses or CQ checklist. Add a new framework only if it addresses a justified gap in selected IC/D decisions, not to expand the checklist by default.
