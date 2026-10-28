# Skill Audit: Sprint Assessment

Analyze the existing Sprint Assessment skill and compare
it against the Refine Requirements skill, if available.
Operate in read-only mode. Do not modify any files.

## Objective

Understand the existing skill's architecture, workflow,
responsibilities, validation mechanisms, and potential gaps.
Do not propose implementation changes yet.

## Phase 1: Skill Inventory

Inspect the SKILL.md entry point and relevant supporting
references, templates, and scripts.

Identify:
- Purpose and activation conditions
- Required inputs
- Expected outputs
- Major workflow stages
- Decision points
- Validation mechanisms
- Dependencies and handoffs

Produce a concise Skill Contract.

## Phase 2: Workflow Analysis

Map the skill's execution flow.

For each major stage, identify:
- What the stage accomplishes
- What information it consumes
- What decisions it makes
- What evidence supports those decisions
- What it produces

Include file and line references.

## Phase 3: Overlap Analysis

Compare Sprint Assessment with Refine Requirements.

Identify:
- Shared responsibilities
- Duplicate analysis
- Distinct responsibilities
- Potentially conflicting instructions
- Opportunities for integration

Distinguish intentional overlap from unnecessary duplication.

## Phase 4: Validation Gap Analysis

Evaluate whether the skill adequately validates:
- Requirements completeness
- Evidence supporting conclusions
- Assumptions and uncertainty
- Acceptance criteria
- Functional and nonfunctional requirements
- Technical dependencies
- Estimation and sizing
- Sprint readiness

Identify existing safeguards before proposing new ones.
Rank findings by severity and provide supporting evidence.

## Phase 5: Evaluation Recommendations

Propose three representative test scenarios:
1. A well-defined, sprint-ready feature
2. A feature with ambiguous requirements
3. A feature with unresolved technical dependencies

For each scenario, define the expected behavior
and objective pass/fail criteria.

Do not execute tests yet.

## Output Format

Present an overview first:
1. Executive Summary
2. Skill Contract
3. Workflow Map
4. Overlap Analysis
5. Existing Validation Mechanisms
6. Validation Gaps and Risks
7. Recommended Validation Layer
8. Proposed Test Scenarios
9. Questions Requiring Human Decisions

Include an Evidence and Pattern Map with file references.
Keep the initial report concise.
Do not modify the skill or begin implementation.
Wait for review before investigating individual findings
in greater detail.
