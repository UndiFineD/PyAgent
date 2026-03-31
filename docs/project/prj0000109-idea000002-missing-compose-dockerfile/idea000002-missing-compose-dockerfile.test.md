# idea000002-missing-compose-dockerfile - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-31_

## Test Plan
- Scope: implement red-phase artifacts for T-DC-001, T-DC-003, T-DC-005, T-DC-007, and T-DC-011 only.
- Strategy: add deterministic deploy contract tests plus project-specific docs-policy tests that fail on real behavioral drift (path contract, service topology drift, branch/scope evidence omissions, AC mapping gaps).
- Non-goal: no production compose/runtime edits in @5test lane.
- Required validations:
	- targeted deploy selectors for new tests.
	- docs policy selector for project artifact assertions.
	- docs workflow policy command for project artifact changes.

## Branch and Scope Preconditions
- Expected branch: prj0000109-idea000002-missing-compose-dockerfile
- Observed branch: prj0000109-idea000002-missing-compose-dockerfile
- Project match: PASS
- Scope-bounded files reviewed:
	- tests/deploy/test_compose_dockerfile_paths.py
	- tests/deploy/test_compose_context_contract.py
	- tests/deploy/test_compose_dockerfile_regression_matrix.py
	- tests/deploy/test_compose_file_selection.py
	- tests/deploy/test_compose_non_goal_guardrails.py
	- tests/deploy/test_compose_scope_boundary_markers.py
	- tests/docs/test_agent_workflow_policy_docs.py
	- docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md
	- .github/agents/data/current.5test.memory.md
	- .github/agents/data/2026-03-31.5test.log.md
- Required evidence:
	- git branch --show-current
	- scoped changed-files review

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-DC-001 | compose.yaml pyagent dockerfile contract points to deploy/Dockerfile.pyagent | tests/deploy/test_compose_dockerfile_paths.py | RED_AUTHORED |
| TC-DC-002 | compose context resolves to clean-checkout repo root and dockerfile remains repo-relative | tests/deploy/test_compose_context_contract.py | RED_AUTHORED |
| TC-DC-003 | regression matrix for compose.yaml and docker-compose.yaml dockerfile bindings | tests/deploy/test_compose_dockerfile_regression_matrix.py | RED_AUTHORED |
| TC-DC-004 | compose file role-selection guard between canonical pyagent and fleet manifests | tests/deploy/test_compose_file_selection.py | RED_AUTHORED |
| TC-DC-005 | non-goal guardrails prevent topology consolidation drift in this lane | tests/deploy/test_compose_non_goal_guardrails.py | RED_AUTHORED |
| TC-DC-006 | scope-boundary marker checks preserve expected service dockerfile markers | tests/deploy/test_compose_scope_boundary_markers.py | RED_AUTHORED |
| TC-DC-007 | project test artifact enforces branch/scope precondition requirements | tests/docs/test_agent_workflow_policy_docs.py | RED_AUTHORED |
| TC-DC-008 | project test artifact enforces AC matrix, weak-test gate, and selector-order contracts | tests/docs/test_agent_workflow_policy_docs.py | RED_AUTHORED |

## AC-to-Test Matrix
| AC ID | Covered By | Concrete Cases |
|---|---|---|
| AC-DC-001 | T-DC-001 | TC-DC-001, TC-DC-002 |
| AC-DC-002 | T-DC-007 | TC-DC-007 |
| AC-DC-003 | T-DC-003 | TC-DC-003, TC-DC-004 |
| AC-DC-004 | T-DC-011 | TC-DC-008 |
| AC-DC-005 | T-DC-007, T-DC-011 | TC-DC-007, TC-DC-008 |
| AC-DC-006 | T-DC-005 | TC-DC-005, TC-DC-006 |

## Weak-Test Detection Gate
- Blocking rule: weak-test findings block handoff to @6code.
- Explicit gate: this gate blocks handoff to @6code if any test passes using placeholder-only assertions or import/existence-only checks.
- Rejected weak patterns:
	- placeholder/stub behavior (`pass`, `return None`) not challenged by assertions.
	- assertions limited to import success/type existence.
	- unconditional `assert True`.
	- TODO-only test bodies.
- Invalid red evidence signatures (blocked):
	- ImportError
	- AttributeError
- Required red evidence signatures:
	- assertion-level behavior mismatch messages tied to contract checks.

## Red-Phase Selector Order
| Selector | Command | Intent |
|---|---|---|
| S1 | python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py | Validate canonical compose dockerfile contract |
| S2 | python -m pytest -q tests/deploy/test_compose_context_contract.py | Validate clean-checkout context and repo-local dockerfile path |
| S3 | python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py | Validate cross-manifest dockerfile matrix |
| S4 | python -m pytest -q tests/deploy/test_compose_file_selection.py | Validate compose file role-selection and anti-ambiguity guard |
| S5 | python -m pytest -q tests/deploy/test_compose_non_goal_guardrails.py | Validate no topology consolidation drift |
| S6 | python -m pytest -q tests/deploy/test_compose_scope_boundary_markers.py | Validate service dockerfile boundary markers |
| S7 | python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py | Validate project docs-policy branch/scope and AC matrix assertions |

## Validation Results
| ID | Result | Output |
|---|---|---|
| Branch Gate | PASS | git branch --show-current => prj0000109-idea000002-missing-compose-dockerfile |
| S1 | PASS | python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py => 2 passed |
| S2 | PASS | python -m pytest -q tests/deploy/test_compose_context_contract.py => 2 passed |
| S3/S4 | FAIL (RED EVIDENCE) | python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py => 3 failed, 8 passed; failure: missing deploy/Dockerfile.fleet for fleet services |
| S5/S6 | PASS | python -m pytest -q tests/deploy/test_compose_non_goal_guardrails.py tests/deploy/test_compose_scope_boundary_markers.py => 4 passed |
| S7 | PASS | python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py => 15 passed |
| Docs Policy Gate | PASS | python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py => 15 passed |

## Unresolved Failures
- RED blocker for @6code: `tests/deploy/test_compose_dockerfile_regression_matrix.py::test_compose_referenced_dockerfiles_exist` fails for `fleet_master`, `agent_node_0`, `agent_node_1` because `deploy/Dockerfile.fleet` is absent.
- Failure signature quality: assertion-level contract mismatch only; no `ImportError` or `AttributeError` signatures observed.
