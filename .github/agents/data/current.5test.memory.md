# Current Memory - 5test

## Metadata
- agent: @5test
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-31
- rollover: At new project start, append this file's entries to history.5test.memory.md in chronological order, then clear Entries.

## Entries

### Entry 2026-04-01 - prj0000110 quality workflow branch trigger red contracts
- task_id: prj0000110-idea000004-quality-workflow-branch-trigger
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000110-idea000004-quality-workflow-branch-trigger
  - observed: prj0000110-idea000004-quality-workflow-branch-trigger
  - result: PASS
- scope:
  - tests/ci/test_ci_workflow.py
  - docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-01.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check tests/ci/test_ci_workflow.py
  - RED(expected): python -m pytest -q tests/ci/test_ci_workflow.py tests/test_enforce_branch.py (2 failed, 25 passed)
  - PASS: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (17 passed)
- red_failure_signatures:
  - AssertionError: explicit project branch glob missing from pull_request.branches
  - AssertionError: workflow name mismatch for required-check identity
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - update ci trigger branch pattern from `prj*` to explicit prjNNNNNNN-style glob
    - update workflow name to the required-check identity contract

#### Lesson
- Pattern: Trigger contracts become weak when wildcard branch filters are too broad (`prj*`) to encode branch policy intent.
- Root cause: Existing CI trigger accepted ambiguous wildcard and lacked explicit required-check identity naming contract.
- Prevention: Add contract tests that assert explicit branch glob shape and exact required-check workflow identity.
- First seen: 2026-04-01
- Seen in: prj0000110-idea000004-quality-workflow-branch-trigger
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-03-31 - prj0000109 missing compose dockerfile red-phase tests
- task_id: prj0000109-idea000002-missing-compose-dockerfile
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000109-idea000002-missing-compose-dockerfile
  - observed: prj0000109-idea000002-missing-compose-dockerfile
  - result: PASS
- scope:
  - docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.test.md
  - tests/deploy/test_compose_context_contract.py
  - tests/deploy/test_compose_dockerfile_regression_matrix.py
  - tests/deploy/test_compose_file_selection.py
  - tests/deploy/test_compose_non_goal_guardrails.py
  - tests/deploy/test_compose_scope_boundary_markers.py
  - tests/docs/test_agent_workflow_policy_docs.py
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-03-31.5test.log.md
- evidence:
  - authored deterministic red-phase selectors for T-DC-001, T-DC-003, T-DC-005, T-DC-007, T-DC-011
  - docs artifact includes branch/scope preconditions, AC-to-test matrix, weak-test gate, and selector order
  - selector S3 produced assertion-level RED evidence for missing deploy/Dockerfile.fleet
- failing_test_evidence:
  - python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py
  - result: 3 failed, 8 passed
  - failure signatures: AssertionError for missing C:/Dev/PyAgent/deploy/Dockerfile.fleet
  - invalid signatures absent: ImportError, AttributeError
- pass_fail_summary:
  - PASS: python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py (2 passed)
  - PASS: python -m pytest -q tests/deploy/test_compose_context_contract.py (2 passed)
  - FAIL(RED): python -m pytest -q tests/deploy/test_compose_dockerfile_regression_matrix.py tests/deploy/test_compose_file_selection.py (3 failed, 8 passed)
  - PASS: python -m pytest -q tests/deploy/test_compose_non_goal_guardrails.py tests/deploy/test_compose_scope_boundary_markers.py (4 passed)
  - PASS: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (15 passed)
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION_CONTRACTS
  - blocker_for_green: provide deploy/Dockerfile.fleet or align fleet compose dockerfile references to existing files

#### Lesson
- Pattern: Regression matrices that validate both dockerfile value and filesystem existence expose latent compose drift reliably.
- Root cause: Fleet compose references deploy/Dockerfile.fleet, but that file is absent in repository.
- Prevention: Keep matrix tests coupling compose dockerfile references with real file existence checks for all service entries.
- First seen: 2026-03-31
- Seen in: prj0000109-idea000002-missing-compose-dockerfile
- Recurrence count: 1
- Promotion status: Candidate
