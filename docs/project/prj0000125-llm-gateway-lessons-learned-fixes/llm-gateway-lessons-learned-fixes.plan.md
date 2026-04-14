# llm-gateway-lessons-learned-fixes — Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-04_

## Branch Gate

| Check | Result |
|---|---|
| Expected branch | `prj0000125-llm-gateway-lessons-learned-fixes` |
| Observed branch (`git branch --show-current`) | `prj0000125-llm-gateway-lessons-learned-fixes` |
| Gate | **PASS** |

## Input Artifacts

| File | Purpose | Status |
|---|---|---|
| `docs/project/prj0000125-llm-gateway-lessons-learned-fixes/llm-gateway-lessons-learned-fixes.design.md` | Primary design — 4 waves, interface contract, ACs | READ |
| `docs/project/prj0000125-llm-gateway-lessons-learned-fixes/llm-gateway-lessons-learned-fixes.project.md` | Scope boundary, branch plan, milestones | READ |
| `src/core/gateway/gateway_core.py` | Current implementation (gaps to fill in Wave A) | READ |
| `tests/core/gateway/test_gateway_core_orchestration.py` | Current orchestration tests (non-deterministic ordering to fix in Wave B) | READ |
| `tests/core/gateway/test_gateway_core.py` | Quality-contract test (must stay passing throughout) | READ |
| `docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md` | ADR already amended by @3design in commit 1c16acfde6 | READ |
| `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` | Source project milestones already updated in commit 1c16acfde6 | READ |

## Wave Status Summary

| Wave | Label | Remaining Tasks | Evidence |
|---|---|---|---|
| A | Runtime Correctness | **4 tasks** (T-LGW2-001..004) | `gateway_core.py` missing budget-denied check, unguarded provider call, bare telemetry emit |
| B | Test Determinism | **2 tasks** (T-LGW2-005..006) | `test_gateway_core_orchestration.py` uses broken `stub_a.calls + stub_b.calls` ordering assertion |
| C | Docs Truth Sync | **Zero** (already done) | `rg NOT_STARTED docs/project/prj0000124-llm-gateway/` → 0 matches; ADR 0009 has Part 2 section — both in commit 1c16acfde6 |
| D | Naming Decision Record | **Zero** (already done) | Decision recorded in design.md; `rg "from .gateway_core import" src/core/gateway/` → 1 match in `__init__.py` |

## Executable Validation Commands

```powershell
# Activate environment
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Wave A gate — all three scenarios pass
python -m pytest -q tests/core/gateway/test_gateway_core_orchestration.py -k "budget_denied or provider_exception or degraded_telemetry"

# Wave B gate — ordering assertions deterministic, full suite passes
python -m pytest -q tests/core/gateway/test_gateway_core_orchestration.py

# Quality-contract gate — must never regress
python -m pytest -q tests/core/gateway/test_gateway_core.py

# Full gateway suite convergence gate
python -m pytest -q tests/core/gateway/

# Docs policy gate (17 passed required)
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py

# ADR governance gate
python scripts/architecture_governance.py validate
```

---

## Task Breakdown

### Wave A — Runtime Correctness (4 tasks)

| Task ID | Title | Type | Owner | Files | Depends on | Acceptance Criteria |
|---|---|---|---|---|---|---|
| T-LGW2-001 | RED: budget-denied path blocks provider | RED | @5test | `tests/core/gateway/test_gateway_core_orchestration.py` | NONE | `pytest -q -k "budget_denied" tests/core/gateway/test_gateway_core_orchestration.py` → 1 FAILED |
| T-LGW2-002 | RED: provider-exception fail-closed | RED | @5test | `tests/core/gateway/test_gateway_core_orchestration.py` | NONE | `pytest -q -k "provider_exception" tests/core/gateway/test_gateway_core_orchestration.py` → 1 FAILED |
| T-LGW2-003 | RED: degraded-telemetry guard | RED | @5test | `tests/core/gateway/test_gateway_core_orchestration.py` | NONE | `pytest -q -k "degraded_telemetry" tests/core/gateway/test_gateway_core_orchestration.py` → 1 FAILED |
| T-LGW2-004 | GREEN: implement fail-closed runtime in handle() | GREEN | @6code | `src/core/gateway/gateway_core.py` | T-LGW2-001, T-LGW2-002, T-LGW2-003 | `pytest -q tests/core/gateway/` → all pass (0 FAILED) |

**Task T-LGW2-001 detail — RED (budget_denied):**
- Add test `test_budget_denied_does_not_call_provider` in `test_gateway_core_orchestration.py`.
- Stub: `_BudgetManagerStub` returns `{"allowed": False, "reservation_id": "rsv-deny-1"}`.
- Assert: `await gateway.handle(envelope)` returns `result["status"] == "denied"` and `result["error"]["error_code"] == "budget_denied"` and `provider_runtime.execute` was NOT called.
- Acceptance: `pytest -q -k "budget_denied" tests/core/gateway/test_gateway_core_orchestration.py` → 1 FAILED while `gateway_core.py` passes through to provider.

**Task T-LGW2-002 detail — RED (provider_exception):**
- Add test `test_provider_exception_returns_failed_result` in `test_gateway_core_orchestration.py`.
- Stub: `_ProviderRuntimeStub.execute` raises `RuntimeError("provider down")`.
- Assert: `await gateway.handle(envelope)` returns (no propagation), `result["status"] == "failed"`, `result["budget"]["status"] == "failed"`, `result["error"]["error_code"] == "provider_exception"`.
- Acceptance: `pytest -q -k "provider_exception" tests/core/gateway/test_gateway_core_orchestration.py` → 1 FAILED while exception still propagates.

**Task T-LGW2-003 detail — RED (degraded_telemetry):**
- Add test `test_degraded_telemetry_result_still_returned` in `test_gateway_core_orchestration.py`.
- Stub: `_TelemetryEmitterStub.emit_result` raises `RuntimeError("telemetry down")`.
- Assert: `await gateway.handle(envelope)` returns (no propagation), `result["telemetry"]["degraded"] is True`, all other result keys present.
- Acceptance: `pytest -q -k "degraded_telemetry" tests/core/gateway/test_gateway_core_orchestration.py` → 1 FAILED while exception propagates.

**Task T-LGW2-004 detail — GREEN (fail-closed runtime):**

Implement three guards in `GatewayCore.handle()`:

1. **A1 — Budget-denied check** (after `reservation = self._budget_manager.reserve(envelope)`):
```python
if not reservation.get("allowed", True):
    result = self._build_budget_denied_result(envelope, reservation)
    # emit telemetry with degraded guard (A3)
    return result
```

2. **A2 — Provider exception guard** (wrapping `self._provider_runtime.execute(route, envelope)`):
```python
try:
    response = await self._provider_runtime.execute(route, envelope)
except Exception as exc:
    budget_commit = self._budget_manager.commit_failure(
        reservation,
        {"error_code": "provider_exception", "category": "provider"},
    )
    result = self._build_provider_exception_result(envelope, route, budget_commit, str(exc))
    # emit telemetry with degraded guard (A3)
    return result
```

3. **A3 — Degraded telemetry guard** (wrapping final `emit_result`):
```python
try:
    self._telemetry_emitter.emit_result(result)
except Exception:
    result = dict(result)
    result["telemetry"] = {"degraded": True}
return result
```

Helper methods `_build_budget_denied_result` and `_build_provider_exception_result` return the full result envelopes specified in the design.

---

### Wave B — Test Determinism (2 tasks)

| Task ID | Title | Type | Owner | Files | Depends on | Acceptance Criteria |
|---|---|---|---|---|---|---|
| T-LGW2-005 | RED: deterministic ordering skeleton | RED | @5test | `tests/core/gateway/test_gateway_core_orchestration.py` | NONE | `pytest -q tests/core/gateway/test_gateway_core_orchestration.py` → new ordering test FAILS on trivially-true detection scenario |
| T-LGW2-006 | GREEN: replace broken ordering assertion with shared event_log | GREEN | @6code | `tests/core/gateway/test_gateway_core_orchestration.py` | T-LGW2-005 | `pytest -q tests/core/gateway/` → all pass; `rg "\.calls \+" tests/core/gateway/test_gateway_core_orchestration.py` → zero matches |

**Task T-LGW2-005 detail — RED (deterministic ordering skeleton):**
- Add a new test `test_event_log_ordering_detects_reversed_execution` that:
  - Instantiates stubs sharing a single `event_log: list[str]`.
  - Asserts `event_log.index("budget_reserve") < event_log.index("provider_execute")`.
- This test FAILS because existing stubs do not yet accept `event_log` — providing the RED evidence.
- Acceptance: new test added and `pytest -q -k "test_event_log_ordering" tests/core/gateway/test_gateway_core_orchestration.py` → 1 FAILED.

**Task T-LGW2-006 detail — GREEN (shared event_log fixture):**
- Refactor ALL stubs in `test_gateway_core_orchestration.py` to accept `event_log: list[str]` and append named event strings on each method call.
- Add `event_log` pytest fixture returning `[]`.
- Add `make_gateway` factory fixture wiring all stubs to `event_log`.
- Replace the broken `budget_manager.calls + provider_runtime.calls` assertion in `test_fail_closed_budget_reserve_occurs_before_provider_execute` with:
```python
assert event_log.index("budget_reserve") < event_log.index("provider_execute")
```
- Ensure no test in the file uses concatenated per-stub `.calls` lists for ordering assertions.
- Acceptance: `pytest -q tests/core/gateway/` all pass; `rg "\.calls \+" tests/core/gateway/test_gateway_core_orchestration.py` → zero matches.

---

### Wave C — Docs Truth Sync

**No remaining tasks.** Both C1 and C2 were completed in commit `1c16acfde6`:
- C1: `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` — all M1–M8 set to DONE, lane updated. Verified: `rg "NOT_STARTED" docs/project/prj0000124-llm-gateway/` → zero matches.
- C2: `docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md` — `## Part 2 — prj0000125 Remediation` section appended. Verified: section present at line 113.

---

### Wave D — Naming Decision Record

**No remaining tasks.** Decision recorded in design.md (`Wave D — Naming Convention Decision` section):
- `gateway_core.py` is COMPLIANT with `docs/project/naming_standards.md` (snake_case).
- No rename warranted.
- Verified: `rg "from .gateway_core import" src/core/gateway/` → one match in `__init__.py`. Decision closed.

---

## Full Task Dependency Graph

```
Wave A (parallel-safe RED tasks — independent, no shared file writes):
  T-LGW2-001 (RED: budget_denied)    ──┐
  T-LGW2-002 (RED: provider_exception)─┤──► T-LGW2-004 (GREEN: fail-closed handle())
  T-LGW2-003 (RED: degraded_telemetry)─┘

Wave B (sequential — RED before GREEN):
  T-LGW2-005 (RED: ordering skeleton) ──► T-LGW2-006 (GREEN: event_log fixture)

Wave C: DONE (no tasks)
Wave D: DONE (no tasks)

Convergence gate (all waves):
  T-LGW2-004 + T-LGW2-006 ──► pytest -q tests/core/gateway/ (all pass)
                           ──► pytest -q tests/docs/test_agent_workflow_policy_docs.py (17 passed)
                           ──► python scripts/architecture_governance.py validate
```

**Parallel-safe boundary:**
- T-LGW2-001, T-LGW2-002, T-LGW2-003, T-LGW2-005: parallel-safe (independent test functions; @5test serializes within session).
- T-LGW2-004: sequential-only (depends on T-LGW2-001, T-LGW2-002, T-LGW2-003 all RED).
- T-LGW2-006: sequential-only (depends on T-LGW2-005 RED).
- Convergence owner: @7exec runs full gateway suite and docs policy test after T-LGW2-004 and T-LGW2-006 complete.

---

## Milestones

| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Options explored | @2think | DONE |
| M2 | Design confirmed | @3design | DONE |
| M3 | Plan finalized | @4plan | DONE |
| M4 | Tests written | @5test | NOT_STARTED |
| M5 | Code implemented | @6code | NOT_STARTED |
| M6 | Integration validated | @7exec | NOT_STARTED |

---

## Handoff to @5test

**Start with (all parallel-safe — author all 4 RED tasks in one session):**
1. **T-LGW2-001** — Write `test_budget_denied_does_not_call_provider` in `tests/core/gateway/test_gateway_core_orchestration.py`. Must FAIL against current `gateway_core.py`.
2. **T-LGW2-002** — Write `test_provider_exception_returns_failed_result`. Must FAIL (exception propagates).
3. **T-LGW2-003** — Write `test_degraded_telemetry_result_still_returned`. Must FAIL (emit raise propagates).
4. **T-LGW2-005** — Write `test_event_log_ordering_detects_reversed_execution` (shared `event_log` skeleton). Must FAIL (stubs not yet wired).

**After RED tasks authored and failing:**
- Hand T-LGW2-004 to @6code (implement three fail-closed guards in `gateway_core.py`).
- Hand T-LGW2-006 to @6code (refactor stubs with shared `event_log`, replace ordering assertion).

**Convergence validation (owned by @7exec after T-LGW2-004 and T-LGW2-006 done):**
```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest -q tests/core/gateway/
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
python scripts/architecture_governance.py validate
```

## Validation Commands
```powershell
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
c:/Dev/PyAgent/.venv/Scripts/python.exe scripts/project_registry_governance.py validate
```