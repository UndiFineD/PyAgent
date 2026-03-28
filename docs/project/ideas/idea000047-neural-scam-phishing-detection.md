# idea-047 - neural-scam-phishing-detection

Planned project mapping: prj0000067 (rust-file-watcher, lane=Released), prj0000084 (immutable-audit-trail, lane=Released), prj0000075 (ci-simplification, lane=Released)

## Idea summary
This archive-derived idea targets neural scam and phishing detection layer in area 7 – CI. It is currently rated priority P2 with impact H and urgency M. The SWOT tag is T.

## Problem statement
Archive security section highlights scam/phishing detection for incoming peer messages, but no project artifacts define classifier scope, false-positive controls, and enforcement action policy.

## Detailed proposal
You can implement this safely as a constrained project with explicit acceptance criteria and rollback paths:
1. Define threat taxonomy and message features for detection signals.
2. Build a layered detector with deterministic rules plus optional ML scoring.
3. Add override and quarantine workflows to avoid operational lockouts.
4. Instrument precision/recall metrics and incident-review feedback loops.

## Acceptance criteria
- The project has a dedicated prj folder with plan/test/code/exec/ql/git artifacts.
- A measurable validation signal exists (tests, benchmarks, or CI checks) and fails before the fix.
- Runtime and operational behavior are documented, including failure and rollback handling.
- The implementation does not violate naming and conduct policies.

## Risks and mitigations
- Risk: overlap with existing released projects. Mitigation: constrain scope and define explicit delta from prior work.
- Risk: architecture drift from current codebase reality. Mitigation: validate assumptions with tests and targeted probes.
- Risk: over-engineering. Mitigation: ship a minimal usable slice first, then iterate via follow-up projects.

## Source references
- docs/architecture/archive/improvement_requirements.md
- docs/architecture/archive/agent_task_security_architecture.md
