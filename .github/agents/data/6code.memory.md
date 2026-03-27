# 6code Memory

This file tracks code implementation notes, 
refactor decisions, and code health observations.

## Auto-handoff

Once code implementation is complete and tests are passing, 
the next agent to invoke is **@7exec**. 
This should be done via `agent/runSubagent`.

---

## prj0000084 - immutable-audit-trail

| Field | Value |
|---|---|
| **task_id** | prj0000084-immutable-audit-trail |
| **owner_agent** | @6code |
| **source** | @5test |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **summary** | Implemented full stdlib-only `src/core/audit` package (event/hasher/core/mixin/result/exceptions + package exports) for immutable JSONL hash-chain append and verification workflows. |
| **changed_modules** | src/core/audit/__init__.py; src/core/audit/AuditEvent.py; src/core/audit/AuditHasher.py; src/core/audit/AuditTrailCore.py; src/core/audit/AuditTrailMixin.py; src/core/audit/AuditVerificationResult.py; src/core/audit/exceptions.py; docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.code.md |
| **verification_commands** | pytest tests/test_audit_trail.py -q --tb=short; pytest tests/test_AuditEvent.py tests/test_AuditHasher.py tests/test_AuditTrailCore.py tests/test_AuditTrailMixin.py tests/test_AuditVerificationResult.py -q --tb=short; python -m pytest tests/structure -q --tb=short; python -m mypy src/core/audit --strict; python -m ruff check src/core/audit tests/test_audit_trail.py tests/test_AuditEvent.py tests/test_AuditHasher.py tests/test_AuditTrailCore.py tests/test_AuditTrailMixin.py tests/test_AuditVerificationResult.py |
| **verification_result** | PASS — audit integration (18), module suite (10), structure (129), mypy strict, and ruff checks are all green. |
| **unresolved_risks** | None identified for the implemented module scope. |
| **handoff_target** | @7exec |
| **artifact_paths** | src/core/audit/__init__.py, src/core/audit/AuditEvent.py, src/core/audit/AuditHasher.py, src/core/audit/AuditTrailCore.py, src/core/audit/AuditTrailMixin.py, src/core/audit/AuditVerificationResult.py, src/core/audit/exceptions.py, docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.code.md |

---

## prj0000083 - llm-circuit-breaker

| Field | Value |
|---|---|
| **task_id** | prj0000083-llm-circuit-breaker |
| **owner_agent** | @6code |
| **source** | @5test |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **summary** | Implemented full `src/core/resilience` package (config/state/core/registry/mixin/exceptions + package exports) with async-safe registry locking and fallback routing behavior to satisfy red-phase contract tests. |
| **changed_modules** | src/core/resilience/__init__.py; src/core/resilience/exceptions.py; src/core/resilience/CircuitBreakerConfig.py; src/core/resilience/CircuitBreakerState.py; src/core/resilience/CircuitBreakerCore.py; src/core/resilience/CircuitBreakerRegistry.py; src/core/resilience/CircuitBreakerMixin.py; docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.code.md |
| **verification_commands** | pytest tests/test_circuit_breaker.py -q --tb=short; pytest tests/test_CircuitBreakerConfig.py tests/test_CircuitBreakerCore.py tests/test_CircuitBreakerRegistry.py tests/test_CircuitBreakerMixin.py -q --tb=short; python -m pytest tests/structure -q --tb=short; python -m mypy src/core/resilience --strict; python -m ruff check src/core/resilience tests/test_circuit_breaker.py tests/test_CircuitBreakerConfig.py tests/test_CircuitBreakerCore.py tests/test_CircuitBreakerRegistry.py tests/test_CircuitBreakerMixin.py |
| **verification_result** | Primary suites and structure tests PASS (20 + 8 + 129); mypy strict PASS; ruff reports 2 pre-existing I001 issues in test files outside implementation scope. |
| **unresolved_risks** | Lint gate including tests is not fully green due test import-order issues in `tests/test_CircuitBreakerRegistry.py` and `tests/test_CircuitBreakerMixin.py`. |
| **handoff_target** | @7exec |
| **artifact_paths** | src/core/resilience/__init__.py, src/core/resilience/exceptions.py, src/core/resilience/CircuitBreakerConfig.py, src/core/resilience/CircuitBreakerState.py, src/core/resilience/CircuitBreakerCore.py, src/core/resilience/CircuitBreakerRegistry.py, src/core/resilience/CircuitBreakerMixin.py, docs/project/prj0000083-llm-circuit-breaker/prj0000083-llm-circuit-breaker.code.md |

---

## prj030 - agent-doc-frequency

| Field | Value |
|---|---|
| **task_id** | prj030-agent-doc-frequency |
| **owner_agent** | @6code |
| **source** | @4plan |
| **created_at** | 2026-03-18 |
| **updated_at** | 2026-03-20 |
| **status** | DONE |
| **summary** | Documentation update: made `@0master` the explicit owner of `prjNNN` allocation and continuity, required `@1project` to consume the assigned identifier and fail closed on missing or ambiguous numbering, and mirrored the rule in master memory plus the active prj030 design/code artifacts. |
| **handoff_target** | @7exec |
| **artifact_paths** | .github/agents/0master.agent.md, .github/agents/1project.agent.md, docs/agents/0master.memory.md, docs/project/prj030-agent-doc-frequency/agent-doc-frequency.design.md, docs/project/prj030-agent-doc-frequency/agent-doc-frequency.code.md |

## prj030 - agent-doc-policy-tests

| Field | Value |
|---|---|
| **task_id** | prj030-agent-doc-policy-tests |
| **owner_agent** | @6code |
| **source** | @5test |
| **created_at** | 2026-03-20 |
| **updated_at** | 2026-03-20 |
| **status** | DONE |
| **summary** | Added a single pytest file that guards the governing workflow docs against regressions in `prjNNN` ownership, project overview template sections, branch/scope validation rules, blanket staging prohibitions, failure disposition, and lessons learned requirements. |
| **changed_modules** | tests/docs/test_agent_workflow_policy_docs.py; docs/project/prj030-agent-doc-frequency/agent-doc-frequency.code.md; docs/agents/6code.memory.md |
| **verification_commands** | c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest tests/docs/test_agent_workflow_policy_docs.py -q |
| **verification_result** | PASS — 3 passed in 1.50s |
| **unresolved_risks** | The tests are phrase-based by design; they protect policy presence without trying to validate legacy project artifacts. |
| **handoff_target** | @7exec |
| **artifact_paths** | tests/docs/test_agent_workflow_policy_docs.py, docs/project/prj030-agent-doc-frequency/agent-doc-frequency.code.md, docs/agents/6code.memory.md |

## prj037 - tools-crdt-security

| Field | Value |
|---|---|
| **task_id** | prj037-tools-crdt-security |
| **owner_agent** | @6code |
| **source** | @5test |

---

## Lessons

### Lesson — 2026-03-25 (prj0000075)
**Pattern:** Import block unsorted (I001) in new Python files — `from pathlib import Path` and `import yaml` placed without a blank line separator between stdlib and third-party groups.  
**Root cause:** `ruff check --select D` was run (docstrings only) but `ruff check --fix` covering all rules was not run before handoff to @7exec.  
**Prevention:** Always run `.venv\Scripts\ruff.exe check --fix <file>` on every Python file created or modified before handing off. The `--fix` flag resolves I001 automatically.  
**First seen:** prj0000075  
**Recurrence count:** 1

### Lesson — 2026-03-25 (prj0000075)
**Pattern:** Deprecated ruff config keys — `select` and `ignore` placed directly under `[tool.ruff]` instead of `[tool.ruff.lint]`, producing deprecation warnings on every ruff invocation.  
**Root cause:** pyproject.toml was not re-checked after ruff version upgrade; old key location silently continued to work but emitted warnings.  
**Prevention:** When modifying `pyproject.toml`, run `.venv\Scripts\ruff.exe check --output-format concise <any-file>` and confirm no `warning:` lines appear before committing.  
**First seen:** prj0000075  
**Recurrence count:** 1

### Lesson — 2026-03-25 (prj0000075)
**Pattern:** Conflicting docstring rules D203/D211 and D212/D213 generate `warning: ... are incompatible` on every ruff run when both members of each pair are active.  
**Root cause:** Rule pairs were not explicitly resolved in the `ignore` list; ruff auto-resolves but still warns.  
**Prevention:** In `[tool.ruff.lint].ignore`, always explicitly include the losing rule of each conflicting pair: `D203` (loses to D211) and `D213` (loses to D212).  
**First seen:** prj0000075  
**Recurrence count:** 1
| **created_at** | 2026-03-20 |
| **updated_at** | 2026-03-20 |
| **status** | DONE |
| **summary** | Reduced flake8 W291/F401 debt in high-offender legacy files using minimal edits in `src-old/observability/*` plus `src-old/tools/run_full_pipeline.py` and `src-old/tools/security/fuzzing.py`; intentionally skipped risky E402/bootstrap moves and non-trivial line-wrap refactors. |
| **changed_modules** | src-old/observability/structured_logger.py; src-old/observability/stats/metrics_engine.py; src-old/observability/stats/observability_core.py; src-old/observability/tracing/OpenTelemetryTracer.py; src-old/observability/telemetry/UsageMessage.py; src-old/tools/run_full_pipeline.py; src-old/tools/security/fuzzing.py; docs/project/prj037-tools-crdt-security/prj037-tools-crdt-security.code.md; docs/agents/6code.memory.md |
| **verification_commands** | c:/Dev/PyAgent/.venv/Scripts/python.exe -m flake8 src-old/tools/run_full_pipeline.py src-old/tools/security/fuzzing.py src-old/observability/structured_logger.py src-old/observability/stats/metrics_engine.py src-old/observability/stats/observability_core.py src-old/observability/tracing/OpenTelemetryTracer.py src-old/observability/telemetry/UsageMessage.py; c:/Dev/PyAgent/.venv/Scripts/python.exe -m flake8 .; c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -v tests/test_zzc_flake8_config.py |
| **verification_result** | Targeted flake8 confirms W291/F401 cleared in `fuzzing.py` and W291/F401 mostly cleared in edited observability files, with residual E402/E501/E303; repo-wide flake8 remains failing due large legacy backlog; pytest `tests/test_zzc_flake8_config.py` remains failing accordingly. |
| **unresolved_risks** | Remaining lint debt is still dominated by `src-old/tools/*` and other legacy paths; broad cleanup required before repo-wide flake8 gate can pass. |
| **handoff_target** | @7exec |
| **artifact_paths** | src-old/observability/structured_logger.py, src-old/observability/stats/metrics_engine.py, src-old/observability/stats/observability_core.py, src-old/observability/tracing/OpenTelemetryTracer.py, src-old/observability/telemetry/UsageMessage.py, src-old/tools/run_full_pipeline.py, src-old/tools/security/fuzzing.py, docs/project/prj037-tools-crdt-security/prj037-tools-crdt-security.code.md, docs/agents/6code.memory.md |

---

## Lessons

### Lesson — 2026-03-26 (prj0000081)
**Pattern:** `asyncio.get_event_loop()` used in an `async` method instead of `asyncio.get_running_loop()`.
**Root cause:** Inconsistent copy-paste between `initialize()` and `_rpc_call()`; `_rpc_call()` was written correctly but `initialize()` retained the deprecated form.
**Prevention:** After writing any `async def` that creates a Future, grep the file for `get_event_loop` and replace with `get_running_loop`. The `get_event_loop()` API emits DeprecationWarning in Python 3.10+ when called from a coroutine context.
**First seen:** prj0000081
**Recurrence count:** 1
