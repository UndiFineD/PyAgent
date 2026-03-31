# Shared Governance Checklist

This checklist is the canonical cross-agent governance source for branch, scope,
docs-policy, and handoff quality gates.

## Always Required
- Confirm project boundary first: prj id, expected branch, and allowed scope files.
- Never proceed on main for project-scoped work.
- Never use blanket staging for project work.
- Validate docs policy when project artifacts under docs/project/prjNNNNNNN/ are changed:
  - python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
- Validate registry/kanban consistency when docs/project/kanban.json or data/projects.json changes:
  - python scripts/project_registry_governance.py validate
- Validate ADR governance when docs/architecture or docs/architecture/adr changes:
  - python scripts/architecture_governance.py validate

## Handoff Evidence
- Record concrete command evidence for every required gate.
- If a blocker is fixed, re-run the exact previously failing selector first.
- Do not mark DONE on interrupted or inconclusive full-suite runs.

## Role-Specific Focus
- 0master: enforce pre-delegation scorecard and branch gate before downstream handoff.
- 1project: ensure project artifacts include Branch Plan, Branch Validation, Scope Validation, and Failure Disposition.
- 2think: keep analysis in-scope and tie options to project boundary constraints.
- 3design: ensure interface and ADR impact are explicit and testable.
- 4plan: map acceptance criteria to executable commands and owners.
- 5test: provide deterministic failing/green test evidence tied to plan items.
- 6code: apply minimal scoped edits and avoid placeholder or drift changes.
- 7exec: runtime validation must finish with normal pass/fail outcomes; interrupted runs are blocked.
- 8ql: security/quality closure requires exact blocker-remediation evidence.
- 9git: branch/scope validation, narrow staging, post-staging pre-commit, then authenticated gh PR flow.
