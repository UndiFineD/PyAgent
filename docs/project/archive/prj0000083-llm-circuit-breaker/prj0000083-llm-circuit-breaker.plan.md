# prj0000083 — llm-circuit-breaker — Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-27_

## Overview

Implement a per-provider LLM request circuit breaker inside `src/core/resilience/`.
The design follows a **`CircuitBreakerMixin` + `CircuitBreakerCore`** pattern mirroring
`SandboxMixin` / `SandboxConfig`. Pure state-machine logic lives in `CircuitBreakerCore`;
mutable per-provider state in `CircuitBreakerState`; a `CircuitBreakerRegistry` maps
`str` provider keys to states under an `asyncio.Lock`; the mixin exposes
`await self.cb_call(provider_key, coro)` to consuming agents. Seven new files are added
to `src/core/resilience/`; zero existing files are modified.

**TDD Approach:** `@5test` writes **all 20 failing tests first** against the public API
contracts defined in the design. `@6code` then makes them pass in the module order below.
Red → Green → Refactor cycle; no skips or placeholder bodies allowed.

---

## Module Implementation Order

`@6code` must write files in this exact order to avoid `ImportError` during incremental
test runs:

| # | File | Rationale |
|---|------|-----------|
| 1 | `src/core/resilience/exceptions.py` | No intra-package imports; needed by every other module |
| 2 | `src/core/resilience/CircuitBreakerConfig.py` | Pure `@dataclass`; imported by State, Core, Registry, Mixin |
| 3 | `src/core/resilience/CircuitBreakerState.py` | Depends on Config only |
| 4 | `src/core/resilience/CircuitBreakerCore.py` | Depends on State + Config |
| 5 | `src/core/resilience/CircuitBreakerRegistry.py` | Depends on Core + State + Config |
| 6 | `src/core/resilience/CircuitBreakerMixin.py` | Depends on Registry + exceptions |
| 7 | `src/core/resilience/__init__.py` | Re-exports all public names; written last to avoid circular imports |

---

## Task List

- [ ] T1 — Write `exceptions.py` | Files: `src/core/resilience/exceptions.py` | AC: `CircuitOpenError(provider_key, state)` and `AllCircuitsOpenError(tried_keys)` are importable and carry correct attributes
- [ ] T2 — Write `CircuitBreakerConfig.py` | Files: `src/core/resilience/CircuitBreakerConfig.py` | AC: dataclass instantiates with defaults; `validate()` returns True
- [ ] T3 — Write `CircuitBreakerState.py` | Files: `src/core/resilience/CircuitBreakerState.py` | AC: `CircuitState` enum has CLOSED/OPEN/HALF_OPEN; `CircuitBreakerState` dataclass holds all counters and flags
- [ ] T4 — Write `CircuitBreakerCore.py` | Files: `src/core/resilience/CircuitBreakerCore.py` | AC: all 9 unit tests U1-U9 pass against this module
- [ ] T5 — Write `CircuitBreakerRegistry.py` | Files: `src/core/resilience/CircuitBreakerRegistry.py` | AC: all 4 registry tests R1-R4 pass
- [ ] T6 — Write `CircuitBreakerMixin.py` | Files: `src/core/resilience/CircuitBreakerMixin.py` | AC: all 5 mixin tests M1-M5 pass
- [ ] T7 — Write `__init__.py` | Files: `src/core/resilience/__init__.py` | AC: `from src.core.resilience import CircuitBreakerMixin, CircuitBreakerRegistry, CircuitBreakerConfig` succeeds
- [ ] T8 — Integration tests pass | Files: `tests/test_circuit_breaker.py` | AC: I1 and I2 pass; ≥ 90 % branch coverage on entire `src/core/resilience/`
- [ ] T9 — Structure test regression | Files: `tests/structure/` | AC: `pytest tests/structure -q` passes unchanged

---

## Milestones

| # | Milestone | Tasks | Status |
|---|-----------|-------|--------|
| M1 | exceptions + config + state skeleton | T1, T2, T3 | ⬜ |
| M2 | core logic (state machine) green | T4 | ⬜ |
| M3 | registry green | T5 | ⬜ |
| M4 | mixin green | T6 | ⬜ |
| M5 | package exports + integration | T7, T8, T9 | ⬜ |

---

## Test File Mapping

| Test file | Source module(s) under test |
|-----------|----------------------------|
| `tests/test_CircuitBreakerConfig.py` | `CircuitBreakerConfig.py` |
| `tests/test_CircuitBreakerCore.py` | `CircuitBreakerCore.py` + `CircuitBreakerState.py` |
| `tests/test_CircuitBreakerRegistry.py` | `CircuitBreakerRegistry.py` |
| `tests/test_CircuitBreakerMixin.py` | `CircuitBreakerMixin.py` |
| `tests/test_circuit_breaker.py` | Full integration — all modules |

---

## Test Cases

### Unit Tests — CircuitBreakerCore (U1–U9)

| ID | Test name | Given | When | Then |
|----|-----------|-------|------|------|
| U1 | `test_core_initial_state_closed` | A fresh `CircuitBreakerState(provider_key="p")` with all defaults | Inspect `.state`, `.consecutive_failures`, `.probe_in_flight` | `state == CLOSED`; `consecutive_failures == 0`; `probe_in_flight == False` |
| U2 | `test_core_record_failure_increments_consecutive` | CLOSED state, config with `failure_threshold=5` | `core.record_failure(state, config)` called once | `state.consecutive_failures == 1`; `state.total_failures == 1`; state remains `CLOSED` |
| U3 | `test_core_opens_after_failure_threshold` | CLOSED state, `failure_threshold=3` | `record_failure(state, config)` called exactly 3 times | `state.state == CircuitState.OPEN`; `consecutive_failures == 3`; `last_failure_time > 0` |
| U4 | `test_core_half_open_after_recovery_timeout` | OPEN state, `last_failure_time = time.monotonic() - 60`, `recovery_timeout=30` | `core.should_allow(state, config)` | Returns `True`; state promoted to `HALF_OPEN`; `probe_in_flight == True` |
| U5 | `test_core_probe_success_transitions_to_closed` | `HALF_OPEN` state, `probe_in_flight=True` | `core.record_success(state)` | `state.state == CLOSED`; `consecutive_failures == 0`; `probe_in_flight == False`; `total_successes == 1` |
| U6 | `test_core_probe_failure_resets_to_open` | `HALF_OPEN` state, `probe_in_flight=True`, `failure_threshold=5` | `core.record_failure(state, config)` | `state.state == OPEN`; `probe_in_flight == False`; `last_failure_time` refreshed to `≈ time.monotonic()` |
| U7 | `test_core_half_open_probe_exclusivity` | `HALF_OPEN` state, `probe_in_flight=True` (probe already in flight) | `core.should_allow(state, config)` called a second time | Returns `False`; `probe_in_flight` still `True`; state unchanged |
| U8 | `test_core_reset_forces_closed` | OPEN state, `consecutive_failures=10`, `probe_in_flight=False` | `core.reset(state)` | `state.state == CLOSED`; `consecutive_failures == 0`; `probe_in_flight == False` |
| U9 | `test_core_record_success_increments_counters` | CLOSED state, `total_successes=0` | `core.record_success(state)` called once | `state.total_successes == 1`; `consecutive_failures` remains `0`; state remains `CLOSED` |

### Unit Tests — CircuitBreakerRegistry (R1–R4)

| ID | Test name | Given | When | Then |
|----|-----------|-------|------|------|
| R1 | `test_registry_get_or_create_same_key_returns_same_object` | Empty async registry | `await get_or_create("k", config)` called twice with same key | Both awaits return the **identical** `CircuitBreakerState` object (`is` identity check passes) |
| R2 | `test_registry_get_fallback_returns_first_closed_provider` | Config with `fallback_providers=["a","b"]`; state for `"a"` is `OPEN`, state for `"b"` is `CLOSED`; both registered | `await registry.get_fallback("primary")` | Returns `"b"`; skips `"a"` because it is OPEN |
| R3 | `test_registry_get_fallback_returns_none_when_all_open` | Config with `fallback_providers=["a"]`; state for `"a"` is `OPEN`; registered | `await registry.get_fallback("primary")` | Returns `None`; no CLOSED fallback available |
| R4 | `test_registry_record_and_allow_delegate_to_core` | Freshly seeded registry for key `"p"`, `failure_threshold=3` | `await registry.record_failure("p")` called 3 times, then `await registry.should_allow("p")` | `should_allow` returns `False`; state for `"p"` is `OPEN` |

### Unit Tests — CircuitBreakerMixin (M1–M5)

| ID | Test name | Given | When | Then |
|----|-----------|-------|------|------|
| M1 | `test_mixin_cb_call_returns_coro_result_on_success` | Mixin agent with registry; circuit `CLOSED` for `"p"` | `await agent.cb_call("p", async_lambda_returning_42)` | Returns `42`; `registry.record_success("p")` called exactly once |
| M2 | `test_mixin_cb_call_records_failure_and_reraises` | Mixin agent; circuit `CLOSED` for `"p"` | `await agent.cb_call("p", coro_raising_RuntimeError)` | `RuntimeError` propagated to caller; `registry.record_failure("p")` called exactly once |
| M3 | `test_mixin_cb_call_open_circuit_raises_circuit_open_error_without_calling_coro` | Mixin agent; circuit `OPEN` for `"p"` (no fallbacks configured) | `await agent.cb_call("p", mock_coro)` | `CircuitOpenError` raised; `mock_coro` coroutine **never awaited** |
| M4 | `test_mixin_cb_call_routes_to_fallback_when_primary_open` | Mixin agent; `"primary"` `OPEN`, `"fallback"` `CLOSED`; fallback list `["fallback"]` | `await agent.cb_call("primary", coro)` | Coro is awaited under `"fallback"` context; `registry.record_success("fallback")` called; no `CircuitOpenError` raised |
| M5 | `test_mixin_cb_call_raises_all_circuits_open_when_exhausted` | Mixin agent; `"primary"` `OPEN`; all fallbacks `OPEN` | `await agent.cb_call("primary", coro)` | `AllCircuitsOpenError` raised; `error.tried_keys` contains `primary` + all fallback key names |

### Integration Tests (I1–I2)

| ID | Test name | Given | When | Then |
|----|-----------|-------|------|------|
| I1 | `test_integration_open_then_half_open_then_closed_full_cycle` | Registry with `failure_threshold=3`, `recovery_timeout=0.05` (50 ms) | ① Record 3 failures → assert `OPEN`; ② `asyncio.sleep(0.06)`; ③ call `should_allow` → assert `HALF_OPEN`; ④ `record_success` | Final state is `CLOSED`; `total_failures == 3`; `total_successes == 1`; full state cycle verified |
| I2 | `test_integration_concurrent_half_open_only_one_probe_passes` | Registry key in `HALF_OPEN` state (`probe_in_flight=False`) at test start | 10 concurrent `asyncio.Task`s each call `await registry.should_allow(key)` under shared lock | Exactly **1** task received `True`; 9 tasks received `False`; no race condition or deadlock |

---

## Acceptance Criteria Coverage

| AC | Criterion (summary) | Test IDs |
|----|--------------------|---------:|
| AC1 | Circuit opens after `failure_threshold` consecutive failures within `window_seconds` | U3, R4, I1 |
| AC2 | OPEN circuit raises `CircuitOpenError` without making an outbound call | M3 |
| AC3 | After `recovery_timeout` → HALF_OPEN; exactly one probe allowed | U4, U7, I1, I2 |
| AC4 | Successful probe closes; failed probe resets OPEN timer | U5, U6, I1 |
| AC5 | Fallback routing when primary is OPEN | R2, M4 |
| AC6 | `AllCircuitsOpenError` when all fallbacks also OPEN | R3, M5 |
| AC7 | Prometheus metrics exported (deferred — no test coverage required this sprint) | — |
| AC8 | `pytest tests/structure -q` passes with no structural regressions | T9 |
| AC9 | ≥ 90 % branch coverage on `src/core/resilience/` | T8 |

---

## Validation Commands

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Run per-module unit tests
python -m pytest tests/test_CircuitBreakerConfig.py tests/test_CircuitBreakerCore.py `
    tests/test_CircuitBreakerRegistry.py tests/test_CircuitBreakerMixin.py -v

# Run full integration test file
python -m pytest tests/test_circuit_breaker.py -v

# Coverage gate (≥ 90 %)
python -m pytest tests/test_circuit_breaker.py tests/test_CircuitBreakerCore.py `
    tests/test_CircuitBreakerRegistry.py tests/test_CircuitBreakerMixin.py `
    --cov=src/core/resilience --cov-report=term-missing --cov-fail-under=90

# Type checking
python -m mypy src/core/resilience/ --strict

# Linting
python -m ruff check src/core/resilience/

# Structure regression
python -m pytest tests/structure -q
```
