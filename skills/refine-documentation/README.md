# Refine Documentation

A reusable, domain-independent skill for tightening AI-generated or human-written documents without adding content.

Use it when a document is repetitive, wordy, or harder to understand than necessary. It makes a **minimal editorial pass**: cut filler, combine duplicate points, and use plain English while preserving meaning, important details, links, decisions, and action items.

**Default style for any document:** Write for a junior developer onboarding to the topic; place direct source links beside supported claims rather than making readers consult evidence-key tables; and explain findings in plain English instead of requiring a status legend. Keep formal statuses/IDs when they are required and never invent sources or change the evidence.

## Use it

~~~text
Use refine-documentation to clean up this document.
Remove redundancy and irrelevant filler. Write for a junior developer.
Use direct source links and plain-English findings where possible.
Do not add new facts, examples, sections, recommendations, or assumptions.
Preserve all essential details, decisions, questions, action items,
deliverables, status meanings, required IDs, citations, links, and structure.
Return the complete revised document.
~~~

For a repository file, specify the path and ask for an in-place edit. The skill only changes files when explicitly authorized and supported by the host.

## Not for

Research, fact-checking, expanding a draft, creating new requirements, making engineering decisions, or summarizing away unique information.

See [SKILL.md](SKILL.md) for the editing rules.
