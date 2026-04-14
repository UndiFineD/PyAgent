# idea000002-missing-compose-dockerfile - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-31_

## Overview
Deliver the design-selected Option B (incremental hardening) by converting the compose Dockerfile fix into a durable contract lane: deterministic deploy regression checks, strict branch/scope evidence, and non-goal guardrails that prevent compose-topology consolidation drift in this project.

This plan is decomposed into two executable chunks for downstream agents:
1. Chunk A - Contract and regression test hardening (~10 code files, ~10 test files).
2. Chunk B - Governance and handoff closure (~10 code files, ~10 test files).

## Scope Guardrails
- Expected branch: `prj0000109-idea000002-missing-compose-dockerfile`
- Allowed implementation scope for this roadmap:
	- `deploy/compose.yaml`
	- `deploy/docker-compose.yaml`
	- `deploy/Dockerfile.pyagent`
	- `tests/deploy/test_compose_dockerfile_paths.py`
	- `tests/docs/test_agent_workflow_policy_docs.py`
	- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md`
	- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.code.md`
	- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.exec.md`
	- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.ql.md`
	- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.git.md`
- Out of scope for this project phase:
	- Compose-topology consolidation and multi-file service graph rewrites.
	- Unrelated deployment runtime refactors outside compose Dockerfile path contract hardening.

## Chunk Plan

### Chunk A - Contract and Regression Hardening (Target: @5test -> @6code)

#### Target Code Files (~10)
- `deploy/compose.yaml`
- `deploy/docker-compose.yaml`
- `deploy/Dockerfile.pyagent`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.code.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.exec.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.ql.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.git.md`
- `.github/agents/data/current.5test.memory.md`
- `.github/agents/data/current.6code.memory.md`

#### Target Test Files (~10)
- `tests/deploy/test_compose_dockerfile_paths.py`
- `tests/docs/test_agent_workflow_policy_docs.py`
- `tests/deploy/test_compose_context_contract.py` (new)
- `tests/deploy/test_compose_dockerfile_regression_matrix.py` (new)
- `tests/deploy/test_compose_file_selection.py` (new)
- `tests/deploy/test_compose_non_goal_guardrails.py` (new)
- `tests/deploy/test_compose_path_error_messages.py` (new)
- `tests/deploy/test_compose_clean_checkout_assumptions.py` (new)
- `tests/deploy/test_compose_dockerfile_existence_scan.py` (new)
- `tests/deploy/test_compose_scope_boundary_markers.py` (new)

#### Tasks
| Task ID | Owner | Objective | Target Files | Acceptance Criteria | Validation Command |
|---|---|---|---|---|---|
| T-DC-001 | @5test | Add deterministic red tests for compose-to-Dockerfile contract validity on clean checkout semantics. | `tests/deploy/test_compose_dockerfile_paths.py`, `tests/deploy/test_compose_context_contract.py` | AC-DC-001 | `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py` |
| T-DC-002 | @6code | Implement minimal green changes only if tests fail, preserving current behavior and path contract invariants. | `deploy/compose.yaml`, `deploy/Dockerfile.pyagent` | AC-DC-001, AC-DC-003 | `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py tests/deploy/test_compose_context_contract.py` |
| T-DC-003 | @5test | Add regression matrix tests for both compose manifests to catch Dockerfile path drift and ambiguous fallback behavior. | `tests/deploy/test_compose_dockerfile_regression_matrix.py`, `tests/deploy/test_compose_file_selection.py` | AC-DC-003 | `python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py` |
| T-DC-004 | @6code | Apply minimal compose-path alignment changes only when matrix tests fail, with no topology consolidation. | `deploy/compose.yaml`, `deploy/docker-compose.yaml` | AC-DC-003, AC-DC-006 | `python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py` |
| T-DC-005 | @5test | Add non-goal guardrail tests preventing consolidation-only edits in this lane. | `tests/deploy/test_compose_non_goal_guardrails.py`, `tests/deploy/test_compose_scope_boundary_markers.py` | AC-DC-006 | `python -m pytest -q tests/deploy/test_compose_non_goal_guardrails.py tests/deploy/test_compose_scope_boundary_markers.py` |
| T-DC-006 | @6code | Update project execution artifacts to encode non-goal checks and deterministic failure messaging hooks. | `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md`, `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.exec.md` | AC-DC-005, AC-DC-006 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-DC-007 | @5test | Add explicit branch/scope precondition checks in project test artifact with pass/fail evidence requirements. | `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md`, `tests/docs/test_agent_workflow_policy_docs.py` | AC-DC-002, AC-DC-005 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-DC-008 | @6code | Ensure code/exec artifacts map each interface contract to concrete verification selectors and owners. | `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.code.md`, `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.exec.md` | AC-DC-004, AC-DC-005 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-DC-009 | @7exec | Execute deploy and docs gates in deterministic order and capture conclusive evidence for handoff. | `tests/deploy/test_compose_dockerfile_paths.py`, `tests/docs/test_agent_workflow_policy_docs.py` | AC-DC-001, AC-DC-002, AC-DC-003 | `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py; python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-DC-010 | @8ql | Perform quality/security closure on contract tests and docs-policy compliance before git handoff. | `tests/deploy/test_compose_dockerfile_paths.py`, `tests/docs/test_agent_workflow_policy_docs.py`, `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.ql.md` | AC-DC-005 | `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py tests/docs/test_agent_workflow_policy_docs.py` |

### Chunk B - Governance and Handoff Closure (Target: @5test -> @6code -> @7exec -> @8ql -> @9git)

#### Target Code Files (~10)
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.plan.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.code.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.exec.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.ql.md`
- `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.git.md`
- `.github/agents/data/current.5test.memory.md`
- `.github/agents/data/current.6code.memory.md`
- `.github/agents/data/current.7exec.memory.md`
- `.github/agents/data/current.8ql.memory.md`

#### Target Test Files (~10)
- `tests/docs/test_agent_workflow_policy_docs.py`
- `tests/deploy/test_compose_dockerfile_paths.py`
- `tests/deploy/test_compose_context_contract.py` (new)
- `tests/deploy/test_compose_dockerfile_regression_matrix.py` (new)
- `tests/deploy/test_compose_file_selection.py` (new)
- `tests/deploy/test_compose_non_goal_guardrails.py` (new)
- `tests/deploy/test_compose_path_error_messages.py` (new)
- `tests/deploy/test_compose_clean_checkout_assumptions.py` (new)
- `tests/deploy/test_compose_dockerfile_existence_scan.py` (new)
- `tests/deploy/test_compose_scope_boundary_markers.py` (new)

#### Tasks
| Task ID | Owner | Objective | Target Files | Acceptance Criteria | Validation Command |
|---|---|---|---|---|---|
| T-DC-011 | @5test | Define red-phase end-to-end lane checks in the project test artifact for all ACs and risk mitigations. | `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md` | AC-DC-004, AC-DC-005 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-DC-012 | @6code | Update execution playbook with exact command ordering and rerun policy for interrupted/inconclusive runs. | `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.exec.md` | AC-DC-005 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-DC-013 | @7exec | Validate clean-checkout compose contract and deterministic selector behavior under runtime execution. | `tests/deploy/test_compose_dockerfile_paths.py`, `tests/deploy/test_compose_clean_checkout_assumptions.py` | AC-DC-001, AC-DC-003 | `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py tests/deploy/test_compose_clean_checkout_assumptions.py` |
| T-DC-014 | @8ql | Verify risk table coverage and quality closure linkage to concrete checks in QL artifact. | `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.ql.md` | AC-DC-005 | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| T-DC-015 | @9git | Enforce narrow staging and branch/scope gate before commit and PR handoff. | `docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.git.md` | AC-DC-002 | `git branch --show-current` |

## AC to Task and Command Mapping
| AC ID | Requirement | Primary Tasks | Owner Sequence | Command Gate |
|---|---|---|---|---|
| AC-DC-001 | Compose Dockerfile reference remains valid on clean checkout semantics | T-DC-001, T-DC-002, T-DC-013 | @5test -> @6code -> @7exec | `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py` |
| AC-DC-002 | Project execution remains on expected branch with scope-bounded artifacts only | T-DC-007, T-DC-009, T-DC-015 | @5test -> @7exec -> @9git | `git branch --show-current` |
| AC-DC-003 | Regression in compose Dockerfile contract is surfaced by deterministic tests | T-DC-003, T-DC-004, T-DC-013 | @5test -> @6code -> @7exec | `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py tests/deploy/test_compose_dockerfile_regression_matrix.py` |
| AC-DC-004 | Design artifact interfaces are fully decomposed into executable plan/test tasks | T-DC-008, T-DC-011 | @6code -> @5test | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| AC-DC-005 | Risks and mitigations are test-linked and policy-compliant for downstream agents | T-DC-006, T-DC-010, T-DC-012, T-DC-014 | @6code -> @8ql -> @7exec -> @8ql | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |
| AC-DC-006 | Non-goal boundary blocks compose-topology consolidation in this lane | T-DC-005, T-DC-004, T-DC-006 | @5test -> @6code | `python -m pytest -q tests/deploy/test_compose_non_goal_guardrails.py` |

## Task List
- [ ] T-DC-001 through T-DC-010 complete (Chunk A)
- [ ] T-DC-011 through T-DC-015 complete (Chunk B)

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Chunk A red tests authored | T-DC-001, T-DC-003, T-DC-005, T-DC-007 | PLANNED |
| M2 | Chunk A green implementation | T-DC-002, T-DC-004, T-DC-006, T-DC-008 | PLANNED |
| M3 | Runtime validation evidence | T-DC-009, T-DC-013 | PLANNED |
| M4 | Quality/security closure | T-DC-010, T-DC-014 | PLANNED |
| M5 | Branch-scope git handoff | T-DC-015 | PLANNED |

## Dependency Order
1. @5test creates deterministic red selectors and guardrail tests.
2. @6code applies minimal green updates only where selectors fail.
3. @7exec runs deterministic runtime validation and records conclusive evidence.
4. @8ql verifies risk/quality closure and policy alignment.
5. @9git performs branch/scope gate and narrow staging for handoff.

## Validation Commands
```powershell
& c:/Dev/PyAgent/.venv/Scripts/Activate.ps1
python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py
python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py
python -m pytest -q tests/deploy/test_compose_non_goal_guardrails.py
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
git branch --show-current
```
