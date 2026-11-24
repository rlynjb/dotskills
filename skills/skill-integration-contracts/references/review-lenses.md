# Stage 3 Conference-Derived Review Lenses

Optional lenses for `skill-integration-contracts`, grounded in the user's saved **AGNTCon/MCPCon North America 2026** session slide PDFs. Speaker lessons are **not official AAIF/MCP requirements, security certifications, or proof that a target workflow executed**.

## How to apply

- **Default off:** Load only on `review_lenses: relevant` or explicitly named lenses, e.g., `review_lenses: [context-engineering, security-and-trust]`.
- **Selection:** With `relevant`, include only lenses justified by the actual proposed IC-xx contract and inspected target sources; state why. With named lenses include only those names; mark a contract NOT APPLICABLE with a reason where appropriate.
- **Scope:** Review the actual proposed IC-xx cards, **not** target skill packages independently. Never create extra contracts, schemas, mandatory coordinators or runtime obligations just to fill a lens.
- **Report:** In Section 5, after ordinary cross-cutting notes and optional Contract Quality Review Coverage (if requested), show `Review Lens Coverage (optional)` comparing 1–2 actual IC-xx contract columns at a time. Include the lens name, full diagnostic questions and mapped contract dimensions in its first column. Each contract cell has concise design status, inspected target source and existing IC-xx/D-xx or supplied F-xx (Cx) pointers where material.
- **Related CQ references are optional cross-references only:** A lens-only review does not activate CQ-01–CQ-06. Show only contract dimension mappings in the lens-only report to avoid unexplained CQ IDs. If CQ review is also enabled, reuse the same IC/D issues without duplication.
- **Learning references:** When a lens is requested, always add `Conference Sources & Further Reading (optional)` immediately after the lens table in Section 5. List selected lens/topic, presentation title, speaker, and direct PDF link; include YouTube only where a session-matched link exists in the user's saved YouTube–PDF map. Do not invent links or present learning sources as factual evidence that the target IC is satisfied.
- **Links/provenance:** PDF links point to user-accessible Google Drive originals inspected for this research. Video links were matched by session title/speaker in `AGNTCon_MCPCon_2026_YouTube_PDF_Map.xlsx`; the videos were not independently watched or verified to continue playing. An absent match does not prove no recording exists.
- **Evidence caution:** Conference sources justify why a design issue matters, while inspected target files and human decisions justify what the actual contract needs. CLEAR means a clear proposal, not an approved, implemented, enforced or tested contract.

## Lens: context-engineering

- **Topic:** Interface context, provenance and source trust
- **Applicable to:** Contracts passing PRDs, tickets, summaries, retrieved text or repository context.
- **Review questions:** Does the handoff identify only the context the receiver actually needs, with source/revision and unresolved questions? Can the consumer separate upstream facts, assumptions and approvals? Does it treat untrusted source text as data, not authority?
- **Inspect:** IC-xx inputs/outputs, source links and standalone entry paths.
- **Map to contract dimensions:** Interface; Observability and evidence; Security, authority and trust.
- **Related CQ questions (references only):** CQ-01, CQ-05, CQ-06. No CQ questions are automatically assessed.
- **Presentation sources:**
  - **Topic:** Minimal interface contracts instead of shared agent contexts; explicit missing results. **Session:** Don't Share the Database: Interface Contracts Between Isolated AI Agents. **Speaker:** Martin Bliss. **PDF:** [Saved slides](https://drive.google.com/file/d/1E4J2rfYLoN-H9wnK_K3f6bGshiwmDUmo/view). **YouTube:** No matched link established.
  - **Topic:** Treat shared context as untrusted and verify provenance and code claims. **Session:** Trustworthy Context Is Untrusted by Default. **Speaker:** Shub Argha. **PDF:** [Saved slides](https://drive.google.com/file/d/19aoCF7WZ2GfVi7vb5ISZHIPKkQOtjjz1/view). **YouTube:** No matched link established.
  - **Topic:** Describe the agent-facing interface clearly and communicate next actions. **Session:** Patterns for Shifting from MCP as a Basic API to MCP as Agent Integration Interface. **Speaker:** James Ward and Alexander Ioffe. **PDF:** [Saved slides](https://drive.google.com/file/d/1a37Vr3kwddeoA-z1rNlsrjUQS-nUHuOZ/view). **YouTube:** [Matched recording](https://www.youtube.com/watch?v=Okw9oLIB-GU).

## Lens: security-and-trust

- **Topic:** Delegation authority, approval and trust boundaries
- **Applicable to:** Contracts with coordinator dispatch, privileged tools, writes, consent, untrusted instructions or approval gates.
- **Review questions:** Who requests and authorizes the next action? Can the receiving agent gain greater authority than the user or producer granted? Which permissions must be enforced by host/tool/server controls instead of prompt text, and what happens when trusted definitions change?
- **Inspect:** IC-xx authority clauses, D-xx decisions and actual accessible host permissions.
- **Map to contract dimensions:** Security, authority and trust; Behavior; Compatibility and evolution.
- **Related CQ questions (references only):** CQ-03, CQ-06. No CQ questions are automatically assessed.
- **Presentation sources:**
  - **Topic:** Authorize each delegation edge; never widen the authority supplied by the user. **Session:** When Agents Spawn Agents: Securing Recursive Delegation in Multi-Agent Systems. **Speaker:** Anishma Mavuram. **PDF:** [Saved slides](https://drive.google.com/file/d/1_jXpA_vFEBAAPYeklZmliAs9jNWZTyWx/view). **YouTube:** [Matched recording](https://www.youtube.com/watch?v=glxs_6J-7sQ).
  - **Topic:** User-scoped permissions and knowing which user and agent actually acted. **Session:** Stop Running Agents as Service Accounts: User-Scoped Access for Enterprise Tool Calls. **Speaker:** Masato Kozuka. **PDF:** [Saved slides](https://drive.google.com/file/d/1pFtRiB7w-_B4G10fbOwEZvq5PcAqf80Z/view). **YouTube:** No matched link established.
  - **Topic:** Previously approved tool definitions can change; consent and enforcement must reflect that. **Session:** MCP Rug Pulls in the Wild: Live Attacks and How to Stop Them. **Speaker:** Charit Upadhyay and Advait Patel. **PDF:** [Saved slides](https://drive.google.com/file/d/1X38wcquvL67JnJm_00zHY0E8rTjyTDrc/view). **YouTube:** [Matched recording](https://www.youtube.com/watch?v=EgkuEPUci24).

## Lens: reliability-and-workflow

- **Topic:** Handoff outcomes, feedback ownership and coordinator limits
- **Applicable to:** Connections with missing data, multiple steps, human escalation, partial results or asynchronous work.
- **Review questions:** Does the contract distinguish completed, needs-input, blocked, pending and failed states where necessary? Who owns each return path and next decision? Is optional coordinator routing separated from actual runtime dispatch, durable state and retries?
- **Inspect:** IC-xx postconditions and failure paths, D-xx approvals and documented coordinator capabilities.
- **Map to contract dimensions:** Behavior; Failure, feedback and fault isolation; Interface.
- **Related CQ questions (references only):** CQ-02, CQ-04, CQ-06. No CQ questions are automatically assessed.
- **Presentation sources:**
  - **Topic:** Request/response, input-required, task status and asynchronous messaging boundaries. **Session:** Agentic Messaging Primitives in MCP. **Speaker:** Caitie McCaffrey. **PDF:** [Saved slides](https://drive.google.com/file/d/1OwyNvZGpIFDnc9KchDq5uER9DpgzLG4g/view). **YouTube:** [Matched recording](https://www.youtube.com/watch?v=iNV5-YkPHW4&t=21711s).
  - **Topic:** Keep model reasoning flexible while the workflow layer owns checkpoints and approvals. **Session:** Non-Deterministic Minds, Deterministic Tools. **Speaker:** Adrian Warman. **PDF:** [Saved slides](https://drive.google.com/file/d/1NNGBWE4u2cm0Ia4qAmUXPonxEKnxTwdf/view). **YouTube:** No matched link established.

## Lens: evaluation-and-observability

- **Topic:** Evidence continuity and diagnostic visibility (design only)
- **Applicable to:** Handoffs needing decisions, artifact provenance, revisions, correlation, statuses or future runtime auditability.
- **Review questions:** Can a reviewer trace each material IC-xx term to the inspected source and the relevant D-xx decision? Which minimal identifiers, statuses and error reasons must survive a handoff? Does the contract distinguish documented intent from observed execution without demanding unnecessary telemetry?
- **Inspect:** IC-xx evidence fields, original links, D-xx decisions, supplied F-xx (Cx) and host assumptions.
- **Map to contract dimensions:** Observability and evidence; Interface; Security, authority and trust.
- **Related CQ questions (references only):** CQ-05, CQ-03. No CQ questions are automatically assessed.
- **Presentation sources:**
  - **Topic:** Capture useful evidence at the execution boundary; separate verified from unverifiable. **Session:** Prove What Your Agent Did: Tamper-Evident Audit Trails for MCP Tool Calls. **Speaker:** Vikas Luthra. **PDF:** [Saved slides](https://drive.google.com/file/d/1ZiZn1h8IuQDEjBVibU8gzortXJABLidk/view). **YouTube:** No matched link established.
  - **Topic:** Carry IDs, time windows and correlation across components without losing source context. **Session:** One Server, Many Apps: A Composable MCP Architecture for Observability. **Speaker:** Pratik Shenoy and Kyle Hounslow. **PDF:** [Saved slides](https://drive.google.com/file/d/1JLuGIWjrvPSipYQKftpcBKsuer9Q6tUC/view). **YouTube:** No matched link established.

## Lens: lifecycle-and-portability

- **Topic:** Versions, changing interfaces and host compatibility
- **Applicable to:** Shared/versioned skills, changing tool descriptions, cross-host flows or coordinator assumptions.
- **Review questions:** Can the consumer tell which source and contract revision its inputs reflect? Which changes require a new review or approval? Can each skill still run independently if a connected skill, tool definition or host capability changes?
- **Inspect:** IC-xx compatibility clauses, D-xx decisions, sources/revisions and intended host details.
- **Map to contract dimensions:** Compatibility and evolution; Interface; Security, authority and trust.
- **Related CQ questions (references only):** CQ-06, CQ-01, CQ-05. No CQ questions are automatically assessed.
- **Presentation sources:**
  - **Topic:** Know the exact skill, tool, instruction and runtime version used for a release. **Session:** Stop Writing Agents, Declare Them: Declarative Agent Architecture in Production. **Speaker:** Chris Knuteson. **PDF:** [Saved slides](https://drive.google.com/file/d/1f9v2ZupSLbcik_AkKJgtfVu9mmVZ5jjI/view). **YouTube:** No matched link established.
  - **Topic:** Keep discovery scoped, distinguish visibility from permission and account for host behavior. **Session:** The MCP Cold-Start Problem: When Your Agent Has 100 Tools and Has to Pick One. **Speaker:** Karthik Karunanithi. **PDF:** [Saved slides](https://drive.google.com/file/d/1AT1V9r0LR0E8LeXN6A7AOqfNcgwoYjX4/view). **YouTube:** [Matched recording](https://www.youtube.com/watch?v=eB9I4Ixx2wc&t=7652s).

## Future additions

Add only session lessons with verified title, speaker, source URL, applicable contract question and an evidence-aware boundary. Do not turn speaker advice into mandatory engineering standards or expand the default review.
