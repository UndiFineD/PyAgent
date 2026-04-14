# 5test Memory

This file tracks test plans, failing test findings, 
and validation outcomes.

## Auto-handoff

Once the tests are written and validated, 
the next agent in the pipeline is **@6code**. 
Invoke it via `agent/runSubagent` to continue the implementation workflow.

## Task Log

### task_id: prj0000100-repo-cleanup-docs-code-20260329-governance-tests
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000100-repo-cleanup-docs-code
- branch_expected: prj0000100-repo-cleanup-docs-code
- branch_observed: prj0000100-repo-cleanup-docs-code ✓
- scope:
	- add deterministic governance tests for canonical allowlist location/content requirements
	- add deterministic governance tests for codestructure schema and integer `line` column
	- add deterministic governance tests for local-search-first and canonical allowlist path references in Copilot instructions
	- run targeted lint and targeted pytest only for new test files
	- update project test artifact and milestone M4 status
- files_updated:
	- `tests/docs/test_allowed_websites_governance.py`
	- `tests/docs/test_codestructure_governance.py`
	- `tests/docs/test_copilot_instructions_governance.py`
	- `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.test.md`
	- `docs/project/prj0000100-repo-cleanup-docs-code/prj0000100-repo-cleanup-docs-code.project.md`
	- `.github/agents/data/5test.memory.md`
- lint_validation:
	- `.venv\Scripts\ruff.exe check --fix tests/docs/test_allowed_websites_governance.py tests/docs/test_codestructure_governance.py tests/docs/test_copilot_instructions_governance.py`: PASS (5 fixed)
	- `.venv\Scripts\ruff.exe check tests/docs/test_allowed_websites_governance.py tests/docs/test_codestructure_governance.py tests/docs/test_copilot_instructions_governance.py`: PASS
- validation_results:
	- `python -m pytest -v tests/docs/test_allowed_websites_governance.py tests/docs/test_codestructure_governance.py tests/docs/test_copilot_instructions_governance.py`
		- result: 6 passed in 5.15s
		- collection quality: no ImportError/AttributeError blockers
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- readiness: READY

### task_id: prj0000099-stub-module-elimination-20260329-focused-validation
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000099-stub-module-elimination
- branch_expected: prj0000099-stub-module-elimination
- branch_observed: prj0000099-stub-module-elimination ✓
- scope:
	- execute focused package validation suite for T2
	- update project test artifact with plan/cases/results and AC mapping
	- record concise validation memory entry
- validation_results:
	- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_rl_package.py tests/test_speculation_package.py tests/test_cort.py tests/test_memory_package.py tests/test_runtime.py`
		- attempt 1: interrupted during pytest terminal-summary plugin teardown (`KeyboardInterrupt` after tests completed)
		- attempt 2: PASS, `5 passed in 3.29s`
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- readiness: READY

### task_id: prj0000098-backend-health-check-endpoint-20260329
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000098-backend-health-check-endpoint
- branch_expected: prj0000098-backend-health-check-endpoint
- branch_observed: prj0000098-backend-health-check-endpoint ✓
- scope:
	- implement red-phase tests for probe contract, auth bypass, and rate-limit behavior for `/health`, `/livez`, `/readyz`
	- keep edits restricted to backend health endpoint test surfaces and project test artifacts
	- capture pytest evidence and update project artifact + handoff memory
- files_updated:
	- `tests/test_api_versioning.py`
	- `tests/test_backend_auth.py`
	- `tests/test_rate_limiting.py`
	- `docs/project/prj0000098-backend-health-check-endpoint/prj0000098-backend-health-check-endpoint.test.md`
	- `.github/agents/data/5test.memory.md`
- lint_validation:
	- `.venv\Scripts\ruff.exe check --fix tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py`: PASS
	- `.venv\Scripts\ruff.exe check tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py`: PASS
	- `.venv\Scripts\ruff.exe check --select D tests/test_api_versioning.py tests/test_backend_auth.py tests/test_rate_limiting.py`: PASS
- validation_results:
	- `python -m pytest -q tests/test_github_app.py tests/test_api_versioning.py --tb=short`
		- result: 23 passed, 1 warning
	- `python -m pytest -q tests/test_backend_auth.py --tb=short`
		- result: 19 passed, 1 warning
	- `python -m pytest -q tests/test_rate_limiting.py --tb=short`
		- result: 6 passed, 1 warning
- red_phase_status:
	- red failures not reproducible in scoped suites because target behavior is already implemented in codebase
	- code evidence:
		- `backend/app.py`: defines `/health`, `/livez`, `/readyz`
		- `backend/rate_limiter.py`: `_EXEMPT_PATHS` includes `/health`, `/livez`, `/readyz`
	- collection quality: no ImportError/AttributeError blockers in targeted runs
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- readiness: READY
	- note: implementation already satisfies current AC set on this branch; coordinate with @4plan if strict red-first evidence remains mandatory

### task_id: prj0000097-stub-module-elimination-20260329
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000097-stub-module-elimination
- branch_expected: prj0000097-stub-module-elimination
- branch_observed: prj0000097-stub-module-elimination ✓
- scope:
	- create Slice 1 red-phase tests in:
		- `tests/rl/test_discounted_return.py`
		- `tests/speculation/test_select_candidate.py`
		- `tests/rl/test_rl_deprecation.py`
		- `tests/speculation/test_speculation_deprecation.py`
		- `tests/guards/test_rl_speculation_import_scope.py`
	- keep tests deterministic and aligned to AC-001..AC-008 mapping
	- run targeted pytest commands and capture red evidence
	- update project test artifact with AC matrix and weak-test gate
- lint_validation:
	- `.venv\Scripts\ruff.exe check --fix tests/rl/test_discounted_return.py tests/speculation/test_select_candidate.py tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py tests/guards/test_rl_speculation_import_scope.py`: PASS (11 fixed)
	- `.venv\Scripts\ruff.exe check tests/rl/test_discounted_return.py tests/speculation/test_select_candidate.py tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py tests/guards/test_rl_speculation_import_scope.py`: PASS
	- `.venv\Scripts\ruff.exe check --select D tests/rl/test_discounted_return.py tests/speculation/test_select_candidate.py tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py tests/guards/test_rl_speculation_import_scope.py`: PASS
- red_phase_results:
	- `python -m pytest -q tests/rl/test_discounted_return.py --tb=short`
		- result: 7 failed in 1.76s (expected red)
		- failure mode: assertion-level missing behavior contract (`rl.discounted_return` callable absent)
	- `python -m pytest -q tests/speculation/test_select_candidate.py --tb=short`
		- result: 7 failed in 1.55s (expected red)
		- failure mode: assertion-level missing behavior contract (`speculation.select_candidate` callable absent)
	- `python -m pytest -q tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py --tb=short`
		- result: 2 failed in 0.82s (expected red)
		- failure mode: assertion-level warning contract gap (`DID NOT WARN`)
	- `python -m pytest -q tests/guards/test_rl_speculation_import_scope.py --tb=short`
		- result: 1 failed, 1 passed in 1.40s (expected red)
		- failure mode: assertion-level import-scope violation with concrete file:line evidence
	- collection quality: no ImportError/AttributeError blockers in targeted runs
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- required_scope:
		- implement `rl.discounted_return()` contract + input validation
		- implement `speculation.select_candidate()` contract + deterministic tie-break + validation
		- emit required deprecation warnings from both `validate()` shims while preserving call compatibility
		- replace/remove legacy import-smoke tests to satisfy import-scope guard and AC-007

### task_id: prj0000096-coverage-minimum-enforcement-20260328
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000096-coverage-minimum-enforcement
- branch_expected: prj0000096-coverage-minimum-enforcement
- branch_observed: prj0000096-coverage-minimum-enforcement ✓
- scope:
	- strengthen `tests/test_coverage_config.py` to enforce stage-1 `fail_under >= 40`
	- extend `tests/structure/test_ci_yaml.py` to require explicit blocking coverage-gate path
	- preserve workflow inventory constraints via `tests/ci/test_workflow_count.py`
	- update project test artifact with AC-to-test matrix and weak-test detection gate
- lint_validation:
	- `.venv\Scripts\ruff.exe check --fix tests/test_coverage_config.py tests/structure/test_ci_yaml.py`: PASS (1 fixed)
	- `.venv\Scripts\ruff.exe check tests/test_coverage_config.py tests/structure/test_ci_yaml.py`: PASS
	- `.venv\Scripts\ruff.exe check --select D tests/test_coverage_config.py tests/structure/test_ci_yaml.py`: PASS
- red_phase_results:
	- `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_coverage_config.py tests/structure/test_ci_yaml.py tests/ci/test_workflow_count.py --tb=short`
		- result: 3 failed, 17 passed in 2.64s (expected red)
		- failure mode: assertion-level contract gaps only
			- `assert 30 >= 40` for stage-1 threshold test
			- `assert []` for missing CI coverage gate step and dependent blocking check
		- collection quality: no ImportError/AttributeError blockers
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- required_scope:
		- set `[tool.coverage.report].fail_under` to 40 or higher in `pyproject.toml`
		- add blocking coverage gate path in `.github/workflows/ci.yml` `jobs.test.steps`
		- keep workflow-count constraints green (no new workflow files)

### task_id: prj0000094-idea-003-mypy-strict-enforcement-20260328
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000094-idea-003-mypy-strict-enforcement
- branch_expected: prj0000094-idea-003-mypy-strict-enforcement
- branch_observed: prj0000094-idea-003-mypy-strict-enforcement ✓
- scope:
	- execute T1 baseline verification command from plan
	- update Wave 1 strict-lane allowlist expectation in `tests/structure/test_mypy_strict_lane_config.py`
	- verify red-phase failure for missing Wave 1 implementation delta
	- update project test artifact with command evidence, AC-to-test mapping, and weak-test gate
- lint_validation:
	- `.venv\Scripts\ruff.exe check --fix tests/structure/test_mypy_strict_lane_config.py`: PASS
	- `.venv\Scripts\ruff.exe check tests/structure/test_mypy_strict_lane_config.py`: PASS
	- `.venv\Scripts\ruff.exe check --select D tests/structure/test_mypy_strict_lane_config.py`: PASS
- baseline_results:
	- `python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py`
		- result: 8 passed in 3.89s
- red_phase_results:
	- `python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/zzz/test_zzc_mypy_strict_lane_smoke.py --tb=short`
		- result: 1 failed, 7 passed in 5.68s (expected red)
		- failure mode: assertion-level allowlist contract mismatch (Wave 1 expected 10, config still 6)
		- collection quality: no ImportError/AttributeError blockers
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- required_scope:
		- implement T3 by expanding `mypy-strict-lane.ini` `[mypy] files` with Wave 1 candidates
		- keep CI strict-lane blocking semantics and smoke behavior contracts unchanged

### task_id: prj0000093-projectmanager-ideas-autosync-20260328
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000093-projectmanager-ideas-autosync
- branch_expected: prj0000093-projectmanager-ideas-autosync
- branch_observed: prj0000093-projectmanager-ideas-autosync ✓
- scope:
	- add backend RED tests in `tests/test_api_ideas.py`
	- cover `/api/ideas` corpus load, implemented filters, mode semantics, stable sort, malformed-file resilience
	- run lint/docstring gates and targeted pytest evidence capture
	- update project artifact for M4 completion and @6code handoff
- lint_validation:
	- `.venv\Scripts\ruff.exe check --fix tests/test_api_ideas.py`: PASS (6 fixed)
	- `.venv\Scripts\ruff.exe check tests/test_api_ideas.py`: PASS
	- `.venv\Scripts\ruff.exe check --select D tests/test_api_ideas.py`: PASS
- red_phase_results:
	- `python -m pytest -q tests/test_api_ideas.py --tb=short`
		- result: 5 failed in 15.17s (expected red)
		- failure mode: assertion-level contract gap (`/api/ideas` missing -> HTTP 404 vs expected 200)
		- collection quality: full collection/execution succeeded; no ImportError/AttributeError blockers
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- required_scope:
		- implement authenticated `GET /api/ideas` in `backend/app.py`
		- ingest ideas from `docs/project/ideas`
		- enforce `implemented` + `implemented_mode` filtering
		- support stable `rank` sorting with `idea_id` tie-break
		- skip malformed idea files without endpoint failure

### Lesson - 2026-03-28 (prj0000093)
- Pattern: Frontend ACs (empty ideas state and local ideas filter behavior) were documented in plan/design but not represented in the final test file despite passing integration tests.
- Root cause: Test scope converged on happy-path render + failure-isolation assertions and did not re-check full AC matrix at final handoff.
- Prevention: Add explicit AC-to-test closure step before marking DONE, including UI empty-state and any documented filter/interactivity assertions.
- First seen: prj0000093
- Seen in: prj0000093-projectmanager-ideas-autosync
- Recurrence count: 1
- Promotion status: CANDIDATE

### task_id: prj0000092-mypy-strict-enforcement-20260328
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000092-mypy-strict-enforcement
- branch_expected: prj0000092-mypy-strict-enforcement
- branch_observed: prj0000092-mypy-strict-enforcement ✓
- scope:
	- create RED tests in `tests/structure/test_mypy_strict_lane_config.py`
	- extend `tests/structure/test_ci_yaml.py` for blocking strict-lane mypy command contract
	- create deterministic fixture `tests/fixtures/mypy_strict_lane/bad_case.py`
	- create smoke test `tests/test_zzc_mypy_strict_lane_smoke.py`
	- run targeted pytest RED command and capture evidence in project test artifact
	- update project overview milestone/status for @6code handoff
- lint_validation:
	- `.venv\Scripts\ruff.exe check --fix tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/test_zzc_mypy_strict_lane_smoke.py`: PASS
	- `.venv\Scripts\ruff.exe check tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/test_zzc_mypy_strict_lane_smoke.py`: PASS
	- `.venv\Scripts\ruff.exe check --select D tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/test_zzc_mypy_strict_lane_smoke.py`: PASS
- red_phase_results:
	- `python -m pytest -q tests/structure/test_mypy_strict_lane_config.py tests/structure/test_ci_yaml.py tests/test_zzc_mypy_strict_lane_smoke.py --tb=short`
		- result: 5 failed, 3 passed in 3.85s (expected red)
		- failure mode: assertion-style contract gaps (missing strict config and missing strict-lane CI command)
		- collection quality: no import-time/attribute collection blockers
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- required_scope:
		- implement `mypy-strict-lane.ini` with strict options + locked phase-1 allowlist
		- add blocking `python -m mypy --config-file mypy-strict-lane.ini` step in `.github/workflows/ci.yml`

### task_id: prj0000091-missing-compose-dockerfile-20260328
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000091-missing-compose-dockerfile
- branch_expected: prj0000091-missing-compose-dockerfile
- branch_observed: prj0000091-missing-compose-dockerfile ✓
- scope:
	- create RED contract tests in `tests/deploy/test_compose_dockerfile_paths.py`
	- validate compose pyagent Dockerfile path contract and referenced path existence
	- run targeted pytest and record red evidence in project test artifact
	- update project overview milestone/status for @6code handoff
- lint_validation:
	- `.venv\Scripts\ruff.exe check --fix tests/deploy/test_compose_dockerfile_paths.py`: PASS
	- `.venv\Scripts\ruff.exe check tests/deploy/test_compose_dockerfile_paths.py`: PASS
	- `.venv\Scripts\ruff.exe check --select D tests/deploy/test_compose_dockerfile_paths.py`: PASS
- red_phase_results:
	- `python -m pytest -q tests/deploy/test_compose_dockerfile_paths.py --tb=short`
		- result: 2 failed in 3.19s (expected red)
		- failure mode: assertion-style contract mismatch (`dockerfile` value) and missing resolved Dockerfile path
		- red quality: no import-time/collection blockers
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- required_scope: update `deploy/compose.yaml` dockerfile path to `deploy/Dockerfile.pyagent` and add the referenced file

### task_id: prj0000090-private-key-remediation-20260328
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000090-private-key-remediation
- branch_expected: prj0000090-private-key-remediation
- branch_observed: prj0000090-private-key-remediation ✓
- scope:
	- create chunk 001 red tests in `tests/security/` for T1, T3, T5, T7
	- create scan fixtures in `tests/security/fixtures/`
	- run chunk 001 red-phase pytest commands from plan
	- update `docs/project/prj0000090-private-key-remediation/prj0000090-private-key-remediation.test.md`
- lint_validation:
	- `.venv\\Scripts\\ruff.exe check --fix` on new tests: PASS (auto-fixes applied)
	- `.venv\\Scripts\\ruff.exe check` on new tests: PASS
	- `.venv\\Scripts\\ruff.exe check --select D` on new tests: PASS
- red_phase_results:
	- `python -m pytest -q tests/security/test_secret_scan_service_contract.py tests/security/test_scan_report_schema.py`
		- result: 5 failed in 4.86s (expected red)
		- failure mode: assertion-style missing contract modules under `src.security.*`
	- `python -m pytest -q tests/security/test_rotation_checkpoint_service.py tests/security/test_rotation_gate_decision.py`
		- result: 3 failed in 4.32s (expected red)
		- failure mode: assertion-style missing `src.security.rotation_checkpoint_service`
	- `python -m pytest -q tests/security/test_secret_guardrail_policy.py tests/security/test_ci_secret_guardrail_job.py tests/security/test_pre_commit_secret_hook.py`
		- result: 7 failed in 2.15s (expected red)
		- failure mode: assertion-style missing policy module + concrete config assertion failures in workflow/pre-commit
	- `python -m pytest -q tests/security/test_containment_cleanup.py tests/security/test_private_key_artifact_absence.py`
		- result: 3 failed in 1.49s (expected red)
		- failure mode: missing runbook/verifier files + private key artifact still present
- quality_gate:
	- AC-to-test matrix present in project test artifact: PASS
	- weak-test detection gate executed and documented: PASS
- handoff:
	- target_agent: @6code
	- required_scope: implement chunk 001 production/config/docs artifacts to satisfy red tests

### task_id: prj0000087-n8n-workflow-bridge-20260327
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000087-n8n-workflow-bridge
- branch_expected: prj0000087-n8n-workflow-bridge
- branch_observed: prj0000087-n8n-workflow-bridge ✓
- scope:
	- create `tests/test_n8n_bridge.py`
	- create `tests/test_N8nBridgeConfig.py`
	- create `tests/test_N8nEventAdapter.py`
	- create `tests/test_N8nHttpClient.py`
	- create `tests/test_N8nBridgeCore.py`
	- create `tests/test_N8nBridgeMixin.py`
	- run red target and structure checks
	- update `docs/project/prj0000087-n8n-workflow-bridge/n8n-workflow-bridge.test.md`
- red_phase_results:
	- `pytest -q tests/test_n8n_bridge.py --tb=short` => 20 failed in 1.35s
		- failure mode: assertion-style `Failed:` messages for missing `src.core.n8nbridge.*`
		- collection quality: tests collected and executed (no import-time collection crash)
	- `pytest -q tests/structure --tb=short` => 1 failed, 128 passed
		- failure mode: existing `tests/structure/test_kanban.py::test_kanban_total_rows` mismatch (expected 88, found 91)
- handoff:
	- target_agent: @6code
	- required_scope: implement `src/core/n8nbridge/*` contracts to satisfy red-phase tests

### task_id: prj0000084-immutable-audit-trail-20260327
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000084-immutable-audit-trail
- branch_expected: prj0000084-immutable-audit-trail
- branch_observed: prj0000084-immutable-audit-trail ✓
- scope:
	- create `tests/test_audit_trail.py` with 18 red-phase contract tests
	- create `tests/test_AuditEvent.py`
	- create `tests/test_AuditHasher.py`
	- create `tests/test_AuditTrailCore.py`
	- create `tests/test_AuditTrailMixin.py`
	- create `tests/test_AuditVerificationResult.py`
	- run requested pytest commands and update prj0000084 test artifact
- red_phase_results:
	- `pytest tests/test_audit_trail.py -q --tb=short` => 18 failed in 0.98s
		- failure mode: assertion-style `Failed:` messages for missing `src.core.audit.*`
		- collection quality: tests collected and executed (no import-time collection crash)
	- `python -m pytest tests/structure -q --tb=short` => 129 passed in 4.30s
- handoff:
	- target_agent: @6code
	- required_scope: implement `src/core/audit/*` contracts to satisfy red-phase tests

### task_id: prj0000083-llm-circuit-breaker-20260327
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000083-llm-circuit-breaker
- branch_expected: prj0000083-llm-circuit-breaker
- branch_observed: prj0000083-llm-circuit-breaker ✓
- scope:
	- create tests/test_circuit_breaker.py with 20 red-phase contract tests
	- create per-module files: tests/test_CircuitBreakerConfig.py,
		tests/test_CircuitBreakerCore.py, tests/test_CircuitBreakerRegistry.py,
		tests/test_CircuitBreakerMixin.py
	- execute requested red-phase pytest commands
- handoff:
	- target_agent: @6code
	- required_scope: implement src/core/resilience/* to satisfy red-phase tests
- red_phase_results:
	- pytest tests/test_circuit_breaker.py -q --tb=short => ERROR at collection
		(ModuleNotFoundError: No module named 'src.core.resilience')
	- python -m pytest tests/structure -q --tb=short => 129 passed

### task_id: prj037-flake8-config-20260320
- lifecycle: IN_PROGRESS
- project: prj037-tools-crdt-security
- scope:
	- add `tests/test_zzc_flake8_config.py`
	- validate current flake8 command/config behavior only
- notes:
	- branch gate passed on `prj037-tools-crdt-security`
	- repository state includes a checked-in `.flake8`, which overrides the task context stating none existed
- handoff:
	- target_agent: @6code
	- required scope: none yet; focused test authoring in progress

### task_id: prj0000045-transaction-managers-full-20260322
- lifecycle: IN_PROGRESS -> BLOCKED -> DONE
- project: prj0000045-transaction-managers-full
- branch_expected: prj0000045-transaction-managers-full
- branch_observed (final): prj0000045-transaction-managers-full ✓
- block_resolved: @0master created branch; @5test re-invoked on correct branch
- files_created:
  - tests/test_MemoryTransactionManager.py (10 tests)
  - tests/test_StorageTransactionManager.py (13 tests)
  - tests/test_ProcessTransactionManager.py (12 tests)
  - tests/test_ContextTransactionManager.py (13 tests)
- red_phase_run: 48 collected | 4 passed | 1 failed | 43 skipped
  - 4 PASS: TC-M1..M4 (existing MemoryTransaction shim)
  - 1 FAIL: TC-M5 (AssertionError — validate() missing on shim, T10 pending) ✓ correct red
  - 43 SKIP: all tests requiring src.core.*/src.transactions.* (modules not yet created)
- test_transaction_managers.py: ERROR at collection (ModuleNotFoundError for src.core.StorageTransactionManager) — pre-existing, resolved by T07
- handoff:
  - target_agent: @6code
  - required_tasks: T00–T10 from transaction-managers-full.plan.md
  - key_files: src/transactions/__init__.py, src/transactions/BaseTransaction.py,
    src/transactions/StorageTransactionManager.py, src/transactions/ProcessTransactionManager.py,
    src/transactions/ContextTransactionManager.py, src/transactions/MemoryTransactionManager.py,
    src/core/StorageTransactionManager.py (shim), src/core/ProcessTransactionManager.py (shim),
    src/core/ContextTransactionManager.py (shim), src/MemoryTransactionManager.py (shim body)

- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj006-unified-transaction-manager
- red/green summary:
	- `tests/test_unified_transaction_manager.py`: PASS (4/4)
	- focused regression bundle: PASS (10/10)
- post-implementation validation:
	- `python -m pytest tests/test_unified_transaction_manager.py tests/test_UnifiedTransactionManager.py tests/test_async_loops.py tests/test_core_quality.py -q` => 12 passed
- full-suite evidence:
	- `python -m pytest -q` => 4 failed, 201 passed, 5 warnings
	- prj006-related failures: resolved
	- unrelated branch-baseline failures:
		- `tests/test_crdt_bridge.py::test_crdt_bridge_merge_returns_ok`
		- `tests/test_security_bridge.py::test_security_bridge_encrypt_decrypt_roundtrip`
		- `tests/test_quality_yaml.py::test_github_actions_has_check_job`
		- `tests/test_quality_yaml.py::test_ci_yaml_check_job_has_install_step`
- handoff:
	- target_agent: @7exec
	- required scope: continue repository-level execution tracking with residual unrelated baseline failures

## Lessons

### Lesson - 2026-03-28 (prj0000096)
- Pattern: Coverage-policy tests are stronger when they parse `pyproject.toml` and assert numeric thresholds instead of string presence.
- Root cause: Presence-only checks can stay green while enforcement remains ineffective (`fail_under` too low or unused in CI).
- Prevention: Require a numeric stage assertion (`>= 40`) plus CI gate-path checks that reject soft-fail operators.
- First seen: 2026-03-28
- Seen in: prj0000096-coverage-minimum-enforcement
- Recurrence count: 1
- Promotion status: CANDIDATE

### Lesson - 2026-03-28 (prj0000090)
- Pattern: Red-phase tests can appear weak if they fail only on missing imports during collection.
- Root cause: Contract suites that import future modules directly trigger collection-time `ImportError` and mask expected behavior assertions.
- Prevention: Use assertion-style symbol loaders (`pytest.fail(..., pytrace=False)`) so failures remain explicit contract failures in executed tests.
- First seen: prj0000090-private-key-remediation
- Seen in: prj0000090-private-key-remediation
- Recurrence count: 1
- Promotion status: monitor

### Lesson - 2026-03-28 (prj0000090)
- Pattern: Chunk handoff quality degrades without a mandatory AC-to-test matrix and weak-test gate record.
- Root cause: Test artifacts often summarize failures but do not prove AC coverage or test-strength checks.
- Prevention: Always include AC mapping table and explicit weak-test detection section before @6code handoff.
- First seen: prj0000090-private-key-remediation
- Seen in: prj0000090-private-key-remediation
- Recurrence count: 1
- Promotion status: monitor

### Lesson — 2026-03-27 (prj0000084)
**Pattern:** Coverage gate for a new module failed target (`src/core/audit` at 83.07% vs required >=90%).
**Root cause:** Test suite emphasized contract path coverage but left multiple negative/error and no-core branches untested in `AuditTrailCore`, `AuditEvent`, and `AuditTrailMixin`.
**Prevention:** Before handing off, run the exact project target command with `--cov-fail-under` from the plan and add branch-focused tests until threshold is met.
**First seen:** prj0000084
**Recurrence count:** 1

### Lesson — 2026-03-27 (prj0000084)
**Pattern:** Plan validation commands referenced a non-existent test file (`tests/test_AuditExceptions.py`).
**Root cause:** Test artifact and plan command set diverged during implementation, but command list was not reconciled.
**Prevention:** During final test artifact update, verify every test file in plan commands exists on disk and matches the delivered test inventory.
**First seen:** prj0000084
**Recurrence count:** 1
	- do_not_touch: prj006-related fixes are complete and validated

### task_id: prj0000085-shadow-mode-replay-20260327
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000085-shadow-mode-replay
- branch_expected: prj0000085-shadow-mode-replay
- branch_observed (final): prj0000085-shadow-mode-replay ✓
- files_created:
	- tests/test_shadow_replay.py (18 core red tests: RT-01..RT-18)
	- tests/test_ReplayEnvelope.py
	- tests/test_ReplayStore.py
	- tests/test_ShadowExecutionCore.py
	- tests/test_ReplayOrchestrator.py
	- tests/test_ReplayMixin.py
- lint_validation:
	- `.venv\\Scripts\\ruff.exe check --fix` on all six new test files: PASS
	- `.venv\\Scripts\\ruff.exe check` on all six new test files: PASS
- red_phase_run:
	- target suite command:
		- `python -m pytest -q tests/test_shadow_replay.py tests/test_ReplayEnvelope.py tests/test_ReplayStore.py tests/test_ShadowExecutionCore.py tests/test_ReplayOrchestrator.py tests/test_ReplayMixin.py`
	- target result: 23 failed in 2.61s (expected red)
	- failure reason: explicit behavior failures due missing modules under `src.core.replay.*`
	- structure suite command:
		- `python -m pytest -q tests/structure --tb=short`
	- structure result: 129 passed in 2.78s
- handoff:
	- target_agent: @6code
	- required_tasks: T1-T7 from prj0000085-shadow-mode-replay.plan.md
	- key_failure_signal: all replay contracts still unimplemented in `src/core/replay/`

### task_id: prj0000088-ai-fuzzing-security-20260327
- lifecycle: OPEN -> IN_PROGRESS -> DONE
- project: prj0000088-ai-fuzzing-security
- branch_expected: prj0000088-ai-fuzzing-security
- branch_observed: prj0000088-ai-fuzzing-security ✓
- files_created:
	- tests/test_fuzzing_core.py (18 mapped red tests: TEST-01..TEST-18)
	- tests/test_FuzzCase.py
	- tests/test_FuzzMutator.py
	- tests/test_FuzzCorpus.py
	- tests/test_FuzzEngineCore.py
	- tests/test_FuzzSafetyPolicy.py
	- tests/test_FuzzResult.py
- lint_validation:
	- `.venv\\Scripts\\ruff.exe check --fix` on all seven new test files: PASS
	- `.venv\\Scripts\\ruff.exe check` on all seven new test files: PASS
- red_phase_run:
	- target suite command:
		- `python -m pytest -q tests/test_fuzzing_core.py tests/test_FuzzCase.py tests/test_FuzzMutator.py tests/test_FuzzCorpus.py tests/test_FuzzEngineCore.py tests/test_FuzzSafetyPolicy.py tests/test_FuzzResult.py --tb=short`
	- target result: 24 failed in 3.37s (expected red)
	- failure reason: explicit behavior failures indicating missing `src.core.fuzzing.*` modules
	- structure command:
		- `python -m pytest -q tests/structure --tb=short`
	- structure result: 1 failed, 128 passed in 2.47s
	- structure failure: `tests/structure/test_kanban.py::test_kanban_total_rows` (expected 88 rows, found 90)
- handoff:
	- target_agent: @6code
	- required_scope: implement `src/core/fuzzing/*` modules and package exports to satisfy red-phase contracts


## Rollup 2026-03-30 before prj0000106
### Entry 2026-03-30 - prj0000105 red-phase execution
- task_id: prj0000105-idea000016-mixin-architecture-base
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
	- expected: prj0000105-idea000016-mixin-architecture-base
	- observed: prj0000105-idea000016-mixin-architecture-base
	- result: PASS
- scope: initial Chunk A red tests under tests/core/base/mixins plus @5test docs/memory/log artifacts
- evidence:
	- authored red test files:
		- tests/core/base/mixins/test_export_contract.py
		- tests/core/base/mixins/test_host_contract.py
		- tests/core/base/mixins/test_host_validation_in_mixins.py
		- tests/core/base/mixins/test_legacy_shim_imports.py
		- tests/core/base/mixins/test_shim_deprecation_policy.py
	- lint/docstring gates:
		- .venv\\Scripts\\ruff.exe check --fix tests/core/base/mixins/*.py -> PASS
		- .venv\\Scripts\\ruff.exe check tests/core/base/mixins/*.py -> PASS
		- .venv\\Scripts\\ruff.exe check --select D tests/core/base/mixins/*.py -> PASS
	- red selectors executed:
		- python -m pytest -q tests/core/base/mixins/test_export_contract.py -> 2 failed
		- python -m pytest -q tests/core/base/mixins/test_host_contract.py -> 2 failed
		- python -m pytest -q tests/core/base/mixins/test_host_validation_in_mixins.py -> 2 failed
		- python -m pytest -q tests/core/base/mixins/test_legacy_shim_imports.py -> 3 failed
		- python -m pytest -q tests/core/base/mixins/test_shim_deprecation_policy.py -> 3 failed
		- python -m pytest -q tests/core/base/mixins -> 12 failed
	- weak-test gate:
		- rg -n "assert\\s+True|TODO: implement|is\\s+not\\s+None|isinstance\\(" tests/core/base/mixins -> no matches (PASS)
	- docs policy gate:
		- python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -> 12 passed
- failing_test_evidence:
	- canonical namespace contract absent (`src.core.base.mixins` missing)
	- host contract API missing (`validate_host_contract` absent)
	- host contract migration events not emitted in audit/sandbox flows
	- shim metadata absent (`__shim_target__`, `__shim_removal_wave__`)
- pass_fail_summary:
	- PASS: branch validation
	- PASS: red tests authored for Chunk A AC/T mappings
	- PASS: deterministic red failure evidence captured
	- PASS: weak-test gate and lint/docstring gates
	- PASS: docs workflow policy gate
	- FAIL (expected red): Chunk A contract behavior not yet implemented
- handoff_notes:
	- @6code readiness: READY
	- implement T001-T006 to satisfy red suite and preserve behavioral assertions

#### Lesson
- Pattern: Red-phase suites are strongest when they assert behavior plus migration metadata in the same test path.
- Root cause: Early red drafts can drift toward symbol-existence checks if canonical modules are not yet present.
- Prevention: Pair each import/surface expectation with a concrete runtime behavior assertion on existing modules.
- First seen: 2026-03-30
- Seen in: prj0000105-idea000016-mixin-architecture-base
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-03-30 - prj0000104 red-phase execution
- task_id: prj0000104-idea000014-processing
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
	- expected: prj0000104-idea000014-processing
	- observed: prj0000104-idea000014-processing
	- result: PASS
- scope: test planning/doc artifacts and memory/log updates only
- evidence:
	- authored planned red test files and fixtures under tests/deps/
	- executed red selectors with deterministic failure profile: tests/deps => 0 passed, 10 failed
	- weak-test heuristic gate command returned no matches: rg -n "assert True|TODO|is not None|isinstance\(" tests/deps
	- updated docs/project/prj0000104-idea000014-processing/idea000014-processing.test.md with concrete red evidence and READY handoff state
	- docs policy gate command observed green in session context: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
- failing_test_evidence:
	- python -m pytest -q tests/deps/test_generate_requirements_deterministic.py => 0 passed, 3 failed
	- python -m pytest -q tests/deps/test_dependency_parity_gate.py => 0 passed, 3 failed
	- python -m pytest -q tests/deps/test_pyproject_parse_failure.py tests/deps/test_manual_requirements_edit_detected.py => 0 passed, 2 failed
	- python -m pytest -q tests/deps/test_install_compatibility_contract.py => 0 passed, 2 failed
	- python -m pytest -q tests/deps => 0 passed, 10 failed
- pass_fail_summary:
	- PASS: branch validation
	- PASS: planned red tests authored and lint/docstring gates satisfied
	- PASS: red execution evidence captured for all planned selectors
	- PASS: weak-test gate checks
	- PASS: failure signatures contain no ImportError/AttributeError
- handoff_notes:
	- @6code readiness: READY
	- blocker removed: red tests authored/executed with assertion-level failure evidence and weak-test gate PASS

#### Lesson
- Pattern: Red-phase planning without immediate test file authoring requires explicit "not-ready" handoff semantics.
- Root cause: Preparation task can be mistaken for completed red phase when selectors are listed but not executed.
- Prevention: Always record failing-test evidence status separately from artifact readiness and mark @6code gate as blocked until red evidence exists.
- First seen: 2026-03-30
- Seen in: prj0000104-idea000014-processing
- Recurrence count: 1
- Promotion status: Candidate




## Rollover 2026-03-31 prj0000109 start

# Current Memory - 5test

## Metadata
- agent: @5test
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-03-30
- rollover: At new project start, append this file's entries to history.5test.memory.md in chronological order, then clear Entries.

## Entries

### Entry 2026-03-30 - prj0000106 artifact and selector completion
- task_id: prj0000106-idea000080-smart-prompt-routing-system
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
- expected: prj0000106-idea000080-smart-prompt-routing-system
- observed: prj0000106-idea000080-smart-prompt-routing-system
- result: PASS
- scope:
- docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.test.md
- .github/agents/data/current.5test.memory.md
- .github/agents/data/2026-03-30.5test.log.md
- evidence:
- completed @5test artifact with AC-to-test matrix, deterministic red selectors, expected failing behavior contracts, and weak-test gate policy
- branch gate validated against project artifact branch plan
- project-boundary-only edits preserved
- failing_test_evidence:
- not executed in this step; selectors and expected failure contracts defined deterministically for next red execution cycle
- pass_fail_summary:
- PASS: branch validation
- PASS: deterministic red selector and contract definition
- PASS: AC-to-test matrix coverage for AC-SPR-001..AC-SPR-008
- PASS: weak-test gate definition and block conditions documented
- PENDING: runtime red selector evidence
- handoff_notes:
- @6code readiness: READY_FOR_IMPLEMENTATION_CONTRACTS
- @5test follow-up: execute selectors and capture red evidence before green-phase sign-off

#### Lesson
- Pattern: Artifact-first completion can safely unblock implementation contracts when selector determinism and weak-test gates are explicit.
- Root cause: Lifecycle handoffs can drift when AC mapping and failing signatures are implicit.
- Prevention: Always include AC-to-test matrix, invalid red signature list, and deterministic selector order in @5test artifact.
- First seen: 2026-03-30
- Seen in: prj0000106-idea000080-smart-prompt-routing-system
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-03-31 - prj0000107 specialized agent library @5test artifact completion
- task_id: prj0000107-idea000015-specialized-agent-library
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
	- expected: prj0000107-idea000015-specialized-agent-library
	- observed: prj0000107-idea000015-specialized-agent-library
	- result: PASS
- scope:
	- docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.test.md
	- .github/agents/data/current.5test.memory.md
	- .github/agents/data/2026-03-31.5test.log.md
- evidence:
	- completed full @5test artifact with deterministic red selectors for T-SAL-001..T-SAL-008 and T-SAL-011..T-SAL-016
	- added AC-to-test matrix for AC-SAL-001..AC-SAL-008
	- documented expected failing behavior contracts and forbidden weak-failure signatures
	- enforced weak-test detection blocking gate policy in artifact
- failing_test_evidence:
	- selectors and expected red signatures defined; execution evidence pending in current cycle
- pass_fail_summary:
	- PASS: branch validation
	- PASS: AC-to-test matrix completeness
	- PASS: weak-test gate policy definition
	- PASS: docs policy validation command execution (12 passed)
	- PASS: narrow commit and push (36b706274)
- handoff_notes:
	- @6code readiness: READY_FOR_IMPLEMENTATION_CONTRACTS

#### Lesson
- Pattern: Deterministic selector ordering plus explicit forbidden red signatures prevents false red evidence and weak contract handoff.
- Root cause: Red-phase work can be marked complete without clear failure-shape constraints, causing ambiguous @6code targets.
- Prevention: Require selector order, expected assertion-level failures, and forbidden import/existence-only signatures in every @5test artifact.
- First seen: 2026-03-31
- Seen in: prj0000107-idea000015-specialized-agent-library
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-03-31 - prj0000108 CRDT Python FFI bindings @5test artifact completion
- task_id: prj0000108-idea000019-crdt-python-ffi-bindings
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
	- expected: prj0000108-idea000019-crdt-python-ffi-bindings
	- observed: prj0000108-idea000019-crdt-python-ffi-bindings
	- result: PASS
- scope:
	- docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.test.md
	- .github/agents/data/current.5test.memory.md
	- .github/agents/data/2026-03-31.5test.log.md
- evidence:
	- finalized @5test artifact with deterministic selector order S1..S10 for AC-CRDT-001..AC-CRDT-008 plus NFR performance gate
	- added explicit expected failing contracts per selector and forbidden weak-failure signatures
	- added complete AC-to-test matrix with concrete case IDs TC-CRDT-001..TC-CRDT-015
	- defined blocking weak-test detection gate tied to handoff status
	- executed docs policy validation command successfully (12 passed)
- failing_test_evidence:
	- selectors and expected red signatures defined deterministically; runtime red execution deferred to implementation cycle
- pass_fail_summary:
	- PASS: branch validation
	- PASS: deterministic red selector and contract definition
	- PASS: AC-to-test matrix completeness
	- PASS: weak-test gate definition and blocking policy
	- PASS: docs policy validation command execution (12 passed)
	- PENDING: commit/push evidence capture
- handoff_notes:
	- @6code readiness: READY_FOR_IMPLEMENTATION_CONTRACTS

#### Lesson
- Pattern: Deterministic selector ordering and explicit failure-shape contracts are required to avoid weak red evidence in interface migration projects.
- Root cause: Without explicit failure-shape constraints, red phase can pass with import/existence checks that do not verify CRDT semantics.
- Prevention: Every @5test artifact must include AC-to-test mapping, ordered selectors, expected behavioral failure contracts, and forbidden weak signatures.
- First seen: 2026-03-31
- Seen in: prj0000107-idea000015-specialized-agent-library; prj0000108-idea000019-crdt-python-ffi-bindings
- Recurrence count: 2
- Promotion status: Promoted to hard rule



--- Appended from current ---

# Current Memory - 5test

## Metadata
- agent: @5test
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-04
- rollover: At new project start, append this file's entries to history.5test.memory.md in chronological order, then clear Entries.

## Entries

### Entry 2026-04-04 - prj0000127 mypy strict enforcement RED phase T-MYPY-001..003
- task_id: prj0000127-mypy-strict-enforcement
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000127-mypy-strict-enforcement
  - observed: prj0000127-mypy-strict-enforcement
  - result: PASS
- scope:
  - tests/docs/test_agent_workflow_policy_docs.py
  - docs/project/prj0000127-mypy-strict-enforcement/mypy-strict-enforcement.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-04.5test.log.md
- pass_fail_summary:
  - RED(expected): python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py -k "prj0000127 or mypy or promotion" (2 failed, 17 deselected)
- red_failure_signatures:
  - AssertionError: strict-lane CI command contract missing `python -m mypy --config-file pyproject.toml` in `.github/workflows/ci.yml`
  - AssertionError: promotion contract missing explicit `n=5` markers in `mypy-strict-enforcement.exec.md`
  - non-qualifying failures absent: ImportError, AttributeError, SyntaxError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add strict-lane CI command contract with explicit `--config-file pyproject.toml` and phase-1 allowlist module list
    - add explicit `N=5` warn->required promotion evidence contract to `mypy-strict-enforcement.exec.md`

#### Lesson
- Pattern: RED docs-policy assertions should target implementation-facing workflow and execution artifacts, not only plan text that may already satisfy requirements.
- Root cause: Plan/design documented strict and promotion contracts, but workflow and execution artifacts did not yet encode them.
- Prevention: Anchor RED selectors to CI workflow and execution logs for enforceable contract verification before GREEN implementation.
- First seen: 2026-04-04
- Seen in: prj0000127-mypy-strict-enforcement
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-04 - prj0000125 llm gateway lessons learned fixes RED wave A/B
- task_id: prj0000125-llm-gateway-lessons-learned-fixes
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000125-llm-gateway-lessons-learned-fixes
  - observed: prj0000125-llm-gateway-lessons-learned-fixes
  - result: PASS
- scope:
  - tests/core/gateway/test_gateway_core_orchestration.py
  - docs/project/prj0000125-llm-gateway-lessons-learned-fixes/llm-gateway-lessons-learned-fixes.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-04.5test.log.md
- pass_fail_summary:
  - RED(expected): pytest -q tests/core/gateway/test_gateway_core_orchestration.py (4 failed, 4 passed)
- red_failure_signatures:
  - AssertionError: provider execute occurred despite denied budget reservation in test_budget_denied_does_not_call_provider
  - RuntimeError: provider down propagated from GatewayCore.handle in test_provider_exception_returns_failed_result
  - RuntimeError: telemetry down propagated from emit_result in test_degraded_telemetry_result_still_returned
  - AssertionError: reversed ordering sentinel failed (assert 1 < 0) in test_event_log_ordering_detects_reversed_execution
  - non-qualifying failures absent: ImportError, AttributeError, SyntaxError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add budget-denied guard returning denied result and block provider execution
    - wrap provider execution in fail-closed exception handling with failed budget commit
    - wrap telemetry emit_result in degraded guard and preserve response return
    - perform Wave B GREEN deterministic ordering refactor after RED sentinel

#### Lesson
- Pattern: RED tests that encode fail-closed gateway contracts reveal runtime exception propagation and policy bypass paths immediately.
- Root cause: GatewayCore.handle currently lacks budget-denied short-circuit, provider exception guard, and telemetry emit_result degradation guard.
- Prevention: Keep fail-closed invariants as dedicated async tests asserting status, error code, budget state, and non-propagation behavior.
- First seen: 2026-04-04
- Seen in: prj0000125-llm-gateway-lessons-learned-fixes
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-04 - prj0000124 llm gateway red slice RED-SLICE-LGW-001
- task_id: prj0000124-llm-gateway
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000124-llm-gateway
  - observed: prj0000124-llm-gateway
  - result: PASS
- scope:
  - tests/core/gateway/test_gateway_core_orchestration.py
  - docs/project/prj0000124-llm-gateway/llm-gateway.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-04.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/core/gateway/test_gateway_core_orchestration.py
  - PASS: .venv\Scripts\ruff.exe check tests/core/gateway/test_gateway_core_orchestration.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/core/gateway/test_gateway_core_orchestration.py
  - RED(expected): c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/core/gateway/test_gateway_core_orchestration.py -k fail_closed (3 failed, 1 deselected)
  - RED(expected): c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/core/gateway/test_gateway_core_orchestration.py (4 failed)
  - PASS: c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (17 passed)
- red_failure_signatures:
  - Failed: Missing module contract src.core.gateway.gateway_core required for RED-SLICE-LGW-001.
  - non-qualifying failures absent: SyntaxError, ImportError at collection time, test setup crash
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add src/core/gateway/gateway_core.py with GatewayCore orchestration contract
    - satisfy fail-closed and ordering invariants encoded in tests/core/gateway/test_gateway_core_orchestration.py

#### Lesson
- Pattern: RED-first gateway tests should encode orchestration invariants with dependency stubs and explicit contract-loader failures.
- Root cause: `src.core.gateway.gateway_core` contract module/class does not exist yet.
- Prevention: Keep loader-level RED signal explicit while preserving behavioral assertions that will activate immediately once contract module lands.
- First seen: 2026-04-04
- Seen in: prj0000124-llm-gateway
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-04 - prj0000122 jwt refresh-token support red slice T-JRT-001
- task_id: prj0000122-jwt-refresh-token-support
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000122-jwt-refresh-token-support
  - observed: prj0000122-jwt-refresh-token-support
  - result: PASS
- scope:
  - tests/test_backend_refresh_sessions.py
  - docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-04.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/test_backend_refresh_sessions.py
  - PASS: .venv\Scripts\ruff.exe check tests/test_backend_refresh_sessions.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/test_backend_refresh_sessions.py
  - RED(expected): c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py (5 failed in 4.77s)
- red_failure_signatures:
  - AssertionError: assert 404 == 200 for POST /v1/auth/session bootstrap success contract
  - AssertionError: assert 404 == 401 for invalid API-key bootstrap rejection contract
  - AssertionError: downstream refresh/logout/hash-at-rest checks blocked behind missing bootstrap route behavior
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add POST /v1/auth/session route with API-key bootstrap contract
    - add POST /v1/auth/refresh and POST /v1/auth/logout contracts
    - add backend-managed refresh-session persistence with no plaintext refresh token at rest

#### Lesson
- Pattern: Red contracts for new route families are strongest when tests assert concrete status/payload behavior against real endpoints and fail on 404/contract mismatches.
- Root cause: Phase-one auth-session routes and persistence behavior are not implemented yet.
- Prevention: Keep first-slice tests anchored to bootstrap success/rejection, then chain refresh, replay, and logout assertions through that bootstrap contract.
- First seen: 2026-04-04
- Seen in: prj0000122-jwt-refresh-token-support
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-03 - prj0000120 openapi spec generation red contracts
- task_id: prj0000120-openapi-spec-generation
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000120-openapi-spec-generation
  - observed: prj0000120-openapi-spec-generation
  - result: PASS
- scope:
  - tests/docs/test_backend_openapi_drift.py
  - docs/project/prj0000120-openapi-spec-generation/openapi-spec-generation.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-03.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/docs/test_backend_openapi_drift.py
  - PASS: .venv\Scripts\ruff.exe check tests/docs/test_backend_openapi_drift.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/docs/test_backend_openapi_drift.py
  - RED(expected): python -m pytest -q tests/docs/test_backend_openapi_drift.py (2 failed, 1 passed in 4.92s)
  - PASS: python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (17 passed in 5.61s)
- red_failure_signatures:
  - AssertionError: Missing committed backend OpenAPI artifact at C:\Dev\PyAgent\docs\api\openapi\backend_openapi.json. @6code must add the generator and commit the backend-only schema before drift checks can pass.
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add scripts/generate_backend_openapi.py with backend.app as the only phase-one import target
    - commit docs/api/openapi/backend_openapi.json generated from backend.app.openapi()
    - preserve read-only drift verification semantics in tests/docs/test_backend_openapi_drift.py
    - avoid importing src.github_app or src.chat.api in the generator, test lane, or CI selector

#### Lesson
- Pattern: OpenAPI drift red contracts are strongest when one selector proves the committed artifact is missing or stale and another proves parity checks stay read-only.
- Root cause: The repository exposes backend.app.openapi() at runtime, but the phase-one generator and committed backend artifact do not exist yet.
- Prevention: Keep generation, committed artifact ownership, and drift verification separate so missing freshness fails via assertion-level contract checks instead of import-level failures.
- First seen: 2026-04-03
- Seen in: prj0000120-openapi-spec-generation
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-03 - prj0000118 amd npu feature documentation red contracts
- task_id: prj0000118-amd-npu-feature-documentation
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000118-amd-npu-feature-documentation
  - observed: prj0000118-amd-npu-feature-documentation
  - result: PASS
- scope:
  - tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py
  - docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-03.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py
  - PASS: .venv\Scripts\ruff.exe check tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py
  - RED(expected): python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py (6 failed in 6.68s)
- red_failure_signatures:
  - AssertionError: missing canonical runtime guidance marker section for amd_npu
  - AssertionError: missing feature-off and feature-on command examples
  - AssertionError: missing AMD_NPU_STATUS_UNAVAILABLE and -1 fallback semantics
  - AssertionError: missing Windows x86_64 + AMD Ryzen AI SDK boundary and unsupported path phrase
  - AssertionError: missing mandatory evidence schema fields
  - AssertionError: missing non-goals and CI defer contract text
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - update docs/performance/HARDWARE_ACCELERATION.md to satisfy AC-AMD-001..006 selectors

#### Lesson
- Pattern: Docs-only red contracts are strongest when each AC maps to one assertion-focused selector and one aggregate selector.
- Root cause: AMD NPU guidance lacks canonical marker, command parity, fallback semantics, environment boundary, evidence schema, and defer/non-goals language.
- Prevention: Keep phrase-level selectors aligned to AC text and fail on missing contract language, not file existence.
- First seen: 2026-04-03
- Seen in: prj0000118-amd-npu-feature-documentation
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-03 - prj0000117 rust sub-crate workspace unification red contracts
- task_id: prj0000117-rust-sub-crate-unification
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000117-rust-sub-crate-unification
  - observed: prj0000117-rust-sub-crate-unification
  - result: PASS
- scope:
  - tests/rust/test_workspace_unification_contracts.py
  - tests/ci/test_ci_workspace_unification_contracts.py
  - docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-03.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py
  - PASS: .venv\Scripts\ruff.exe check tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py
  - RED(expected): python -m pytest -q tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py (3 failed, 4 passed)
  - BASELINE_FAIL(known): python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (1 failed, 16 passed)
- red_failure_signatures:
  - AssertionError: rust_core/Cargo.toml [workspace].members must include 'crdt', 'p2p', and 'security'
  - AssertionError: Workspace lockfile contract violation due to existing member Cargo.lock files
  - AssertionError: rust_core/Cargo.toml must own [patch.crates-io] for workspace-wide dependency overrides
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add [workspace] members (crdt, p2p, security) to rust_core/Cargo.toml
    - remove member Cargo.lock files and keep rust_core/Cargo.lock as singleton
    - move [patch.crates-io] ownership to rust_core/Cargo.toml from member manifests

#### Lesson
- Pattern: Workspace-migration red contracts are strongest when they combine TOML structure checks for workspace membership and patch ownership with lockfile singleton assertions.
- Root cause: Current Rust layout is mixed standalone crates with member lockfiles and crate-local patch governance, not root-workspace governance.
- Prevention: Keep three independent selectors for workspace membership, lockfile singleton, and root patch ownership so implementation deltas are explicit.
- First seen: 2026-04-03
- Seen in: prj0000117-rust-sub-crate-unification
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-03 - prj0000116 rust criterion benchmark baseline red contracts
- task_id: prj0000116-rust-criterion-benchmarks
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000116-rust-criterion-benchmarks
  - observed: prj0000116-rust-criterion-benchmarks
  - result: PASS
- scope:
  - tests/rust/test_rust_criterion_baseline.py
  - tests/ci/test_ci_workflow.py
  - docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-03.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check --fix tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py
  - PASS: .venv\Scripts\ruff.exe check tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py
  - PASS: .venv\Scripts\ruff.exe check --select D tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py
  - RED(expected): python -m pytest -q tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py::test_ci_workflow_has_single_rust_benchmark_smoke_step_without_threshold_gate (4 failed in 4.74s)
  - BASELINE_FAIL(known): python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py (1 failed, 16 passed)
- red_failure_signatures:
  - AssertionError: rust_core/Cargo.toml must add criterion under [dev-dependencies] for stats baseline bench
  - AssertionError: rust_core/benches/stats_baseline.rs must exist
  - AssertionError: ci.yml must contain exactly one benchmark smoke command: 'cargo bench --bench stats_baseline -- --noplot'
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add criterion under rust_core/Cargo.toml [dev-dependencies]
    - add [[bench]] target name=stats_baseline with harness=false
    - add rust_core/benches/stats_baseline.rs with Criterion harness + naming contract
    - add single CI smoke benchmark command and artifact check in .github/workflows/ci.yml

#### Lesson
- Pattern: Red-phase benchmark contracts are strongest when they validate Cargo wiring, Criterion macros, and CI command semantics as text-level structure checks.
- Root cause: Repository has no Criterion dev-dependency, no stats benchmark harness file, and no CI smoke benchmark command yet.
- Prevention: Keep three independent contract selectors for Cargo, bench source, and CI smoke so @6code receives precise implementation deltas.
- First seen: 2026-04-03
- Seen in: prj0000116-rust-criterion-benchmarks
- Recurrence count: 1
- Promotion status: Candidate

### Entry 2026-04-02 - prj0000115 ci-security-quality workflow consolidation wave A
- task_id: prj0000115-ci-security-quality-workflow-consolidation
- status: DONE
- lifecycle_transition: OPEN -> IN_PROGRESS -> DONE
- branch_gate:
  - expected: prj0000115-ci-security-quality-workflow-consolidation
  - observed: prj0000115-ci-security-quality-workflow-consolidation
  - result: PASS
- scope:
  - tests/ci/test_security_workflow.py
  - tests/ci/test_ci_workflow.py
  - docs/project/prj0000115-ci-security-quality-workflow-consolidation/ci-security-quality-workflow-consolidation.test.md
  - .github/agents/data/current.5test.memory.md
  - .github/agents/data/2026-04-02.5test.log.md
- pass_fail_summary:
  - PASS: .venv\Scripts\ruff.exe check tests/ci/test_security_workflow.py tests/ci/test_ci_workflow.py
  - RED(expected): python -m pytest -q tests/ci/test_security_workflow.py (7 failed in 4.56s)
  - PASS: python -m pytest -q tests/ci/test_ci_workflow.py (7 passed in 3.68s)
- red_failure_signatures:
  - AssertionError: security workflow file does not exist yet (.github/workflows/security-scheduled.yml)
  - FileNotFoundError: no such file or directory .github/workflows/security-scheduled.yml
  - non-qualifying failures absent: ImportError, AttributeError
- handoff_notes:
  - target_agent: @6code
  - readiness: READY_FOR_IMPLEMENTATION
  - implementation_delta_required:
    - add .github/workflows/security-scheduled.yml meeting AC-SEC-001..003

#### Lesson
- Pattern: Security workflow contracts are strongest when tests validate trigger shape, permissions, and CodeQL init arguments instead of only job existence.
- Root cause: No scheduled security workflow file exists yet, so all contract selectors fail as intended in red phase.
- Prevention: Keep one explicit existence test plus behavior assertions that fail on missing/incorrect YAML content.
- First seen: 2026-04-02
- Seen in: prj0000115-ci-security-quality-workflow-consolidation
- Recurrence count: 1
- Promotion status: Candidate

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
