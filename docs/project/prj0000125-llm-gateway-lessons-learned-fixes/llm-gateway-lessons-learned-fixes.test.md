# llm-gateway-lessons-learned-fixes - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-04_

## Test Plan
Execute RED phase for Wave A and Wave B task skeletons only:
- T-LGW2-001: budget denial fail-closed contract
- T-LGW2-002: provider exception fail-closed contract
- T-LGW2-003: degraded telemetry return contract
- T-LGW2-005: event-log ordering detection RED sentinel

Scope-limited file edits to `tests/core/gateway/test_gateway_core_orchestration.py`; no production-code edits.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| T-LGW2-001-RED | `test_budget_denied_does_not_call_provider` | tests/core/gateway/test_gateway_core_orchestration.py | RED_CONFIRMED |
| T-LGW2-002-RED | `test_provider_exception_returns_failed_result` | tests/core/gateway/test_gateway_core_orchestration.py | RED_CONFIRMED |
| T-LGW2-003-RED | `test_degraded_telemetry_result_still_returned` | tests/core/gateway/test_gateway_core_orchestration.py | RED_CONFIRMED |
| T-LGW2-005-RED | `test_event_log_ordering_detects_reversed_execution` | tests/core/gateway/test_gateway_core_orchestration.py | RED_CONFIRMED |

## AC-To-Test Matrix
| AC ID | Requirement | Test Case ID |
|---|---|---|
| AC-A1 | Budget denied path must block provider and return denied with `budget_denied` error code | T-LGW2-001-RED |
| AC-A2 | Provider exception must not propagate and must return failed with failed budget status | T-LGW2-002-RED |
| AC-A3 | Telemetry emission failure must still return result with `telemetry.degraded=True` | T-LGW2-003-RED |
| AC-B1 | Shared chronological log must support deterministic order assertions and detect reversed sentinel | T-LGW2-005-RED |

## Weak-Test Detection Gate
| Check | Result | Evidence |
|---|---|---|
| Placeholder assertion ban (`assert True`, existence-only) | PASS | New tests assert concrete status/error/budget/event-order behavior |
| Stub-pass susceptibility | PASS | Tests fail against current implementation despite callable stubs |
| Failure-reason quality | PASS | Failures are assertion/runtime contract failures, not import/syntax collection failures |
| AC mapping completeness | PASS | All AC IDs above map to at least one test case |

## Validation Results
| ID | Result | Output |
|---|---|---|
| RED-ORCH-ALL | RED_EXPECTED | `pytest -q tests/core/gateway/test_gateway_core_orchestration.py` -> 4 failed, 4 passed |
| RED-001 | FAIL_EXPECTED | `test_budget_denied_does_not_call_provider` -> provider still called (`['provider_execute']`) |
| RED-002 | FAIL_EXPECTED | `test_provider_exception_returns_failed_result` -> `RuntimeError: provider down` propagates from `GatewayCore.handle()` |
| RED-003 | FAIL_EXPECTED | `test_degraded_telemetry_result_still_returned` -> `RuntimeError: telemetry down` propagates from `emit_result` |
| RED-005 | FAIL_EXPECTED | `test_event_log_ordering_detects_reversed_execution` -> reversed sentinel assertion fails (`assert 1 < 0`) |

## Unresolved Failures
- Runtime does not fail-closed on budget denial (`GatewayCore.handle()` still executes provider).
- Runtime does not catch provider execution exceptions.
- Runtime does not degrade/guard telemetry emit failures.
- Ordering RED sentinel intentionally failing pending Wave B GREEN test refactor handoff.