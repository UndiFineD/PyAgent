# 5test Memory

This file tracks test plans, failing test findings, 
and validation outcomes.

## Auto-handoff

Once the tests are written and validated, 
the next agent in the pipeline is **@6code**. 
Invoke it via `agent/runSubagent` to continue the implementation workflow.

## Task Log

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
