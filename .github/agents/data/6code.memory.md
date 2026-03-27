# 6code Memory

This file tracks code implementation notes, 
refactor decisions, and code health observations.

## Auto-handoff

Once code implementation is complete and tests are passing, 
the next agent to invoke is **@7exec**. 
This should be done via `agent/runSubagent`.

## prj0000088 - ai-fuzzing-security

| Field | Value |
|---|---|
| **task_id** | prj0000088-ai-fuzzing-security |
| **owner_agent** | @6code |
| **source** | @5test |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **summary** | Implemented deterministic fuzzing core v1 in `src/core/fuzzing` including exceptions, immutable `FuzzCase`, typed `FuzzResult` aggregation, local/budget `FuzzSafetyPolicy`, deduplicating `FuzzCorpus`, deterministic `FuzzMutator`, and bounded deterministic `FuzzEngineCore.schedule_cases` with `validate()` helpers. |
| **changed_modules** | src/core/fuzzing/exceptions.py; src/core/fuzzing/FuzzCase.py; src/core/fuzzing/FuzzResult.py; src/core/fuzzing/FuzzSafetyPolicy.py; src/core/fuzzing/FuzzCorpus.py; src/core/fuzzing/FuzzMutator.py; src/core/fuzzing/FuzzEngineCore.py; src/core/fuzzing/__init__.py; docs/architecture/0overview.md; docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.code.md; .github/agents/data/6code.memory.md |
| **verification_commands** | python -m pytest -q tests/test_fuzzing_core.py tests/test_FuzzCase.py tests/test_FuzzMutator.py tests/test_FuzzCorpus.py tests/test_FuzzEngineCore.py tests/test_FuzzSafetyPolicy.py tests/test_FuzzResult.py; python -m mypy --strict src/core/fuzzing; .venv\Scripts\ruff.exe check src/core/fuzzing tests/test_fuzzing_core.py tests/test_FuzzCase.py tests/test_FuzzMutator.py tests/test_FuzzCorpus.py tests/test_FuzzEngineCore.py tests/test_FuzzSafetyPolicy.py tests/test_FuzzResult.py; rg --type py "raise NotImplementedError|raise NotImplemented\b|#\s*(TODO|FIXME|HACK|STUB|PLACEHOLDER)" src/core/fuzzing tests/; rg --type py "^\s*\.\.\.\s*$" src/core/fuzzing |
| **verification_result** | PASS — fuzzing tests 24/24, mypy strict clean for fuzzing scope, ruff clean for fuzzing scope and targeted tests, placeholder scan clean. |
| **unresolved_risks** | None identified in implemented scope. |
| **handoff_target** | @7exec |
| **artifact_paths** | src/core/fuzzing/exceptions.py, src/core/fuzzing/FuzzCase.py, src/core/fuzzing/FuzzResult.py, src/core/fuzzing/FuzzSafetyPolicy.py, src/core/fuzzing/FuzzCorpus.py, src/core/fuzzing/FuzzMutator.py, src/core/fuzzing/FuzzEngineCore.py, src/core/fuzzing/__init__.py, docs/architecture/0overview.md, docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.code.md, .github/agents/data/6code.memory.md |

## prj0000088 - ai-fuzzing-security (coverage blocker follow-up)

| Field | Value |
|---|---|
| **task_id** | prj0000088-ai-fuzzing-security |
| **owner_agent** | @6code |
| **source** | User coverage blocker request |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **summary** | Raised `tests/test_fuzzing_core.py` command-scoped coverage for `src/core/fuzzing` from 76.18% to 99.06% by adding deterministic branch-focused tests for negative/validation paths and zero-case scheduling. |
| **changed_modules** | tests/test_fuzzing_core.py; docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.code.md; .github/agents/data/6code.memory.md |
| **verification_commands** | pytest tests/test_fuzzing_core.py -q --tb=short; pytest tests/test_fuzzing_core.py --cov=src/core/fuzzing --cov-report=term-missing --cov-fail-under=90 -q; python -m mypy src/core/fuzzing --strict; python -m ruff check src/core/fuzzing tests/test_fuzzing_core.py tests/test_FuzzCase.py tests/test_FuzzMutator.py tests/test_FuzzCorpus.py tests/test_FuzzEngineCore.py tests/test_FuzzSafetyPolicy.py tests/test_FuzzResult.py |
| **verification_result** | PASS — 38/38 tests in `tests/test_fuzzing_core.py`; coverage 99.06% (gate >=90); mypy strict clean on `src/core/fuzzing`; ruff clean for requested file set. |
| **unresolved_risks** | None identified in current scope. |
| **handoff_target** | @7exec |
| **artifact_paths** | tests/test_fuzzing_core.py, docs/project/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.code.md, .github/agents/data/6code.memory.md |

## prj0000086 - universal-agent-shell

| Field | Value |
|---|---|
| **task_id** | prj0000086-universal-agent-shell |
| **owner_agent** | @6code |
| **source** | @5test |
| **created_at** | 2026-03-27 |
| **updated_at** | 2026-03-27 |
| **status** | DONE |
| **summary** | Implemented `src/core/universal` facade v1 (`UniversalIntentRouter`, `UniversalCoreRegistry`, `UniversalAgentShell`, `exceptions`, package `__init__`) with deterministic routing, strict registry contracts, single fallback to legacy, stable exports, and `validate()` helpers. |
| **changed_modules** | src/core/universal/UniversalIntentRouter.py; src/core/universal/UniversalCoreRegistry.py; src/core/universal/UniversalAgentShell.py; src/core/universal/exceptions.py; src/core/universal/__init__.py; docs/project/prj0000086-universal-agent-shell/universal-agent-shell.code.md; .github/agents/data/6code.memory.md |
| **verification_commands** | python -m pytest -q tests/test_universal_shell.py tests/test_UniversalIntentRouter.py tests/test_UniversalCoreRegistry.py tests/test_UniversalAgentShell.py; python -m pytest -q tests/structure; python -m mypy --strict src/core/universal; python -m ruff check src/core/universal tests/test_universal_shell.py tests/test_UniversalIntentRouter.py tests/test_UniversalCoreRegistry.py tests/test_UniversalAgentShell.py |
| **verification_result** | PASS — universal tests 21/21, structure tests 129/129, mypy strict clean on universal scope, ruff clean on universal scope. |
| **unresolved_risks** | No unresolved risks in universal scope; integration with live core/legacy orchestrators remains for @7exec runtime validation. |
| **handoff_target** | @7exec |
| **artifact_paths** | src/core/universal/UniversalIntentRouter.py, src/core/universal/UniversalCoreRegistry.py, src/core/universal/UniversalAgentShell.py, src/core/universal/exceptions.py, src/core/universal/__init__.py, docs/project/prj0000086-universal-agent-shell/universal-agent-shell.code.md, .github/agents/data/6code.memory.md |

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
| **summary** | Resolved @8ql blocker set: increased `src/core/audit` coverage from 82.11% to 99.36% via targeted branch tests in `tests/test_audit_trail.py`, added `tests/test_AuditExceptions.py`, and aligned `plan/test/code/exec` docs with threshold policy wording. |
| **changed_modules** | tests/test_audit_trail.py; tests/test_AuditExceptions.py; docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.test.md; docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.exec.md; docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.code.md; .github/agents/data/6code.memory.md |
| **verification_commands** | pytest tests/test_audit_trail.py -q --tb=short; pytest tests/test_AuditEvent.py tests/test_AuditHasher.py tests/test_AuditTrailCore.py tests/test_AuditTrailMixin.py tests/test_AuditVerificationResult.py tests/test_AuditExceptions.py -q --tb=short; pytest tests/test_audit_trail.py --cov=src/core/audit --cov-report=term-missing --cov-fail-under=90 -q; python -m pytest tests/structure -q --tb=short; python -m mypy src/core/audit --strict; python -m ruff check src/core/audit tests/test_audit_trail.py tests/test_AuditEvent.py tests/test_AuditHasher.py tests/test_AuditTrailCore.py tests/test_AuditTrailMixin.py tests/test_AuditVerificationResult.py tests/test_AuditExceptions.py |
| **verification_result** | PASS — audit integration (41), module suite (12), coverage gate (99.36% >= 90%), structure (129), mypy strict, and ruff checks all green. |
| **unresolved_risks** | None identified for the implemented module scope. |
| **handoff_target** | @7exec |
| **artifact_paths** | tests/test_audit_trail.py, tests/test_AuditExceptions.py, docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.test.md, docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.exec.md, docs/project/prj0000084-immutable-audit-trail/prj0000084-immutable-audit-trail.code.md, .github/agents/data/6code.memory.md |

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
