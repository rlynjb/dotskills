# Refine Documentation

A reusable, domain-independent skill for tightening AI-generated or human-written documents without adding content.

Use it when a document is repetitive, wordy, or harder to understand than necessary. It makes a **minimal editorial pass**: cut filler, combine duplicate points, and use plain English while preserving meaning, important details, links, decisions, and action items.

## Use it

~~~text
Use refine-documentation to clean up this document.
Remove redundancy and irrelevant filler. Explain things in plain English.
Do not add new facts, examples, sections, recommendations, or assumptions.
Preserve all essential details, decisions, questions, action items,
deliverables, statuses, citations, links, and the existing structure.
Return the complete revised document.
~~~

For a repository file, specify the path and ask for an in-place edit. The skill only changes files when explicitly authorized and supported by the host.

## Not for

Research, fact-checking, expanding a draft, creating new requirements, making engineering decisions, or summarizing away unique information.

See [SKILL.md](SKILL.md) for the editing rules.
