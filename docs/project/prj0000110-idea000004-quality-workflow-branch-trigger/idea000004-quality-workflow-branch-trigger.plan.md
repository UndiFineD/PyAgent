# idea000004-quality-workflow-branch-trigger - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-01_

## Overview
Deliver a project-branch PR governance quality gate that stays lightweight, reuses canonical enforcement, and keeps full-suite CI/security checks `main`-centric. This plan maps design interfaces and acceptance criteria into executable owner-sequenced tasks for `@5test` through `@9git`.

## Scope and Boundaries
- In scope: workflow trigger/governance updates, branch/docs policy wiring, workflow contract tests, and governance docs updates needed for traceability.
- Out of scope: broad CI topology redesign, deprecated legacy workflow resurrection, and unrelated repository policy changes.
- Branch gate: all implementation and validation remains on `prj0000110-idea000004-quality-workflow-branch-trigger`.

## AC and Interface Traceability
| Task ID | Design Plan Ref | Interfaces | Acceptance Criteria |
|---|---|---|---|
| T-QWB-001 | PLAN-QWB-005 | IFACE-QWB-001, IFACE-QWB-004 | AC-QWB-001, AC-QWB-004 |
| T-QWB-002 | PLAN-QWB-001 | IFACE-QWB-001, IFACE-QWB-004 | AC-QWB-001, AC-QWB-004 |
| T-QWB-003 | PLAN-QWB-002 | IFACE-QWB-002, IFACE-QWB-005 | AC-QWB-002 |
| T-QWB-004 | PLAN-QWB-003 | IFACE-QWB-003 | AC-QWB-003 |
| T-QWB-005 | PLAN-QWB-004 | IFACE-QWB-006 | AC-QWB-005 |
| T-QWB-006 | PLAN-QWB-006 | IFACE-QWB-007 | AC-QWB-006 |
| T-QWB-007 | PLAN-QWB-005 | IFACE-QWB-001, IFACE-QWB-004, IFACE-QWB-006 | AC-QWB-001, AC-QWB-004, AC-QWB-005 |
| T-QWB-008 | PLAN-QWB-002, PLAN-QWB-003 | IFACE-QWB-002, IFACE-QWB-003, IFACE-QWB-005 | AC-QWB-002, AC-QWB-003 |

## Chunk Plan
### Chunk A - Contract-first guardrail tests and trigger wiring
Target size: ~4 code/workflow files and ~4 test/doc policy files.

1. T-QWB-001
Objective: Add/extend failing workflow contract tests for trigger pattern and required check identity before workflow changes.
Owner: @5test
Target files: tests/ci/test_ci_workflow.py; tests/test_enforce_branch.py; tests/docs/test_agent_workflow_policy_docs.py
Acceptance linkage: AC-QWB-001, AC-QWB-004
Validation command: python -m pytest -q tests/ci/test_ci_workflow.py tests/test_enforce_branch.py

2. T-QWB-002
Objective: Update CI workflow triggers to include project-branch PR governance contract while preserving `main` full-quality semantics.
Owner: @6code
Target files: .github/workflows/ci.yml
Acceptance linkage: AC-QWB-001, AC-QWB-004
Validation command: python -m pytest -q tests/ci/test_ci_workflow.py

3. T-QWB-003
Objective: Add governance gate execution step(s) that invoke canonical branch enforcement and fail closed on violations.
Owner: @6code
Target files: .github/workflows/ci.yml; scripts/enforce_branch.py
Acceptance linkage: AC-QWB-002
Validation command: python -m pytest -q tests/test_enforce_branch.py

4. T-QWB-004
Objective: Wire docs policy selector into governance gate and block on non-zero outcome.
Owner: @6code
Target files: .github/workflows/ci.yml
Acceptance linkage: AC-QWB-003
Validation command: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

### Chunk B - Permission hardening, documentation traceability, and closure gates
Target size: ~3 code/workflow files and ~3 test/doc files.

5. T-QWB-005
Objective: Ensure least-privilege permissions and non-escalating event safety remain explicit and stable.
Owner: @6code
Target files: .github/workflows/ci.yml; .github/workflows/security.yml
Acceptance linkage: AC-QWB-005
Validation command: python -m pytest -q tests/ci/test_ci_workflow.py tests/security/test_secret_guardrail_policy.py

6. T-QWB-006
Objective: Update project governance docs with explicit gate scope and required-check identity contract wording.
Owner: @6code
Target files: docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.exec.md; docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.ql.md; docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.git.md
Acceptance linkage: AC-QWB-006
Validation command: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

7. T-QWB-007
Objective: Run deterministic integration evidence for trigger contract, check identity, and permission map assertions after implementation.
Owner: @7exec
Target files: .github/workflows/ci.yml; tests/ci/test_ci_workflow.py
Acceptance linkage: AC-QWB-001, AC-QWB-004, AC-QWB-005
Validation command: python -m pytest -q tests/ci/test_ci_workflow.py

8. T-QWB-008
Objective: Execute governance policy closure checks and capture security/quality evidence for handoff.
Owner: @8ql
Target files: scripts/enforce_branch.py; tests/test_enforce_branch.py; tests/docs/test_agent_workflow_policy_docs.py
Acceptance linkage: AC-QWB-002, AC-QWB-003
Validation command: python -m pytest -q tests/test_enforce_branch.py tests/docs/test_agent_workflow_policy_docs.py

## Dependency Order
1. @5test executes T-QWB-001 (red contract baseline).
2. @6code executes T-QWB-002 through T-QWB-006 (green implementation and docs traceability).
3. @7exec executes T-QWB-007 (integration/runtime evidence).
4. @8ql executes T-QWB-008 (quality/security closure evidence).
5. @9git stages only in-scope files and finalizes commit/PR handoff.

## Milestones
| # | Milestone | Tasks | Owner | Status |
|---|---|---|---|---|
| M1 | Contract baseline ready | T-QWB-001 | @5test | NOT_STARTED |
| M2 | Governance gate implemented | T-QWB-002, T-QWB-003, T-QWB-004, T-QWB-005 | @6code | NOT_STARTED |
| M3 | Traceability docs updated | T-QWB-006 | @6code | NOT_STARTED |
| M4 | Integration evidence captured | T-QWB-007 | @7exec | NOT_STARTED |
| M5 | Quality/security closure | T-QWB-008 | @8ql | NOT_STARTED |
| M6 | Narrow stage and handoff | commit + PR notes | @9git | NOT_STARTED |

## Validation Commands
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/ci/test_ci_workflow.py
python -m pytest -q tests/test_enforce_branch.py
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
python -m pytest -q tests/security/test_secret_guardrail_policy.py
```

## Handoff
Next owner: @5test
First handoff bundle: T-QWB-001 with failing-then-green contract evidence for trigger and required-check identity before `@6code` implementation.