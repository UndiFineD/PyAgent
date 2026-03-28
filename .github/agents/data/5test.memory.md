# 5test Memory

This file tracks test plans, failing test findings, 
and validation outcomes.

## Auto-handoff

Once the tests are written and validated, 
the next agent in the pipeline is **@6code**. 
Invoke it via `agent/runSubagent` to continue the implementation workflow.

## Task Log

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
