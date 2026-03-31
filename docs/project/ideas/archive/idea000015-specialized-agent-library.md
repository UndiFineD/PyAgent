# idea-015 - specialized-agent-library

Planned project mapping: prj0000086 (universal-agent-shell, lane=Released)

## Idea summary
This idea focuses on specialized agent library in area 1 – Python agents. The current signal indicates priority P3, impact H, and urgency M. The SWOT tag is O (Opportunity to improve capability).

## Problem statement
`src/agents/` contains only `BaseAgent.py`. The `docs/AGENTS.md` catalogue lists many specialized agents that have no Python-side implementation — only `.agent.md` definitions consumed by Copilot.

## Why this matters now
If you leave this area unresolved, it can create compounding risk in build stability, developer throughput, security posture, or operational reliability. Addressing the idea now helps keep project governance aligned with the current scale of active and released workstreams.

## Proposed implementation approach
1. Confirm the exact acceptance criteria and success metrics in a dedicated project overview.
2. Start with a minimal, testable implementation slice that proves the core behavior.
3. Add validation checks in CI or structure tests to prevent regression.
4. Document operational steps and rollback guidance in docs/project artifacts.
5. Promote the change through the normal @0master -> @9git workflow with branch and scope gates.

## Scope suggestion
- In scope: direct files and tests related to this idea topic.
- Out of scope: broad refactors unrelated to acceptance criteria.

## Dependencies and constraints
- Requires alignment with docs/project/code_of_conduct.md and docs/project/naming_standards.md.
- Must preserve one-project-one-branch policy and project artifact completeness.
- Should keep line length and lint/test gates green on all touched modules.

## Success metrics
- A project ID is allocated and tracked in kanban/projects registry.
- New or updated tests validate the behavior and fail without the fix.
- CI and structure checks pass with no policy regressions.
- Documentation reflects the final implementation and operational usage.

## Risks and mitigations
- Risk: scope creep into unrelated modules. Mitigation: strict file scope list in plan.
- Risk: fragile fixes that pass once. Mitigation: add deterministic tests and guardrails.
- Risk: policy drift. Mitigation: enforce naming and conduct references in agent handoffs.

## Source references
- docs\project\kanban.md
- docs\project\prj0000076\prj0000076.think.md
