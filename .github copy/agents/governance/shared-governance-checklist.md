# Shared Governance Checklist

This checklist is the canonical cross-agent governance source for branch, scope,
docs-policy, and handoff quality gates.

## Always Required
- Confirm project boundary first: prj id, expected branch, and allowed scope files.
- Never proceed on main for project-scoped work.
- Never use blanket staging for project work.
- Use parallel execution only for independent work packages with explicit file ownership boundaries.
- Use `.github/agents/data/parallel_agents_register.json` as the shared source for active parallel packages, touched files, and locks.
- Before starting parallel work, confirm no conflicting lock exists for files in your package scope.
- Use `python scripts/parallel_register.py` for register mutations so lock/touch updates are atomic and consistent.
- Require one sync barrier before implementation if multiple parallel planning/research threads are used.
- Keep git-affecting operations sequential: branch switch, staging, commit, push, PR, and release closure.
- When closing a project to `Released` and the project has an `ideaNNNNNN` tag, move the matching idea file from `docs/project/ideas/` to `docs/project/ideas/archive/` in the same closure workflow.
- Use `docs/project/kanban.json` as the canonical source to determine release state and idea tags for archival decisions.
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
- For parallel phases, record the dependency graph and convergence decision before downstream handoff.
- For parallel phases, record register updates that include lock acquisition/release and touched-file ownership changes.
- Preferred command patterns:
  - `python scripts/parallel_register.py acquire-lock --agent <agent> --work-package-id <wave.wp> --file <path> --project-id <prj> --branch <branch> --wave-id <wave>`
  - `python scripts/parallel_register.py touch-file --agent <agent> --work-package-id <wave.wp> --file <path> --kind planned|touching --project-id <prj> --branch <branch> --wave-id <wave>`
  - `python scripts/parallel_register.py release-lock --agent <agent> --lock-id <lock-id> --wave-id <wave>`
  - `python scripts/parallel_register.py close-wave --actor @0master --wave-id <wave> --note <summary>`

## Role-Specific Focus
- 0master: enforce pre-delegation scorecard and branch gate before downstream handoff, define parallel work packages with ownership boundaries, maintain the parallel register, and require idea-file archival as part of post-merge release closure.
- 1project: ensure project artifacts include Branch Plan, Branch Validation, Scope Validation, and Failure Disposition.
- 2think: keep analysis in-scope, tie options to project boundary constraints, and return merge-ready option artifacts.
- 3design: ensure interface and ADR impact are explicit and testable, and resolve competing parallel options into one design.
- 4plan: map acceptance criteria to executable commands and owners, including which tasks can run in parallel.
- 5test: provide deterministic failing/green test evidence tied to plan items.
- 6code: apply minimal scoped edits, avoid placeholder or drift changes, and do not edit files owned by concurrent work packages.
- 7exec: runtime validation must finish with normal pass/fail outcomes; interrupted runs are blocked.
- 8ql: security/quality closure requires exact blocker-remediation evidence.
- 9git: branch/scope validation, narrow staging, post-staging pre-commit, authenticated gh PR flow, and include required idea-file archive moves in release-closure commits.
