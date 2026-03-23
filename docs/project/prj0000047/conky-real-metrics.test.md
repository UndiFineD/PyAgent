# conky-real-metrics — Test Artifacts

_Status: HANDED_OFF_
_Tester: @5test | Updated: 2026-03-23_

## Test Plan

**Scope:** Unit tests for the new `GET /api/metrics/system` FastAPI endpoint in `backend/app.py`.  
**Approach:** TDD red phase — tests written before implementation exists.  All 9 tests currently
fail with `AssertionError: Expected HTTP 200 but got 404`(endpoint not yet implemented as of T3).  
**Framework:** pytest + `fastapi.testclient.TestClient`  
**Mocking:** `unittest.mock.patch("backend.app.psutil", create=True)` so no real hardware is required and
tests remain valid even before `import psutil` is added to `app.py`.  
**File:** `tests/test_backend_system_metrics.py`

## Test Cases

| ID  | Test Name                                        | File                                    | Status |
|-----|--------------------------------------------------|-----------------------------------------|--------|
| TC1 | `test_endpoint_returns_200`                      | tests/test_backend_system_metrics.py    | RED    |
| TC2 | `test_response_has_correct_shape`                | tests/test_backend_system_metrics.py    | RED    |
| TC3 | `test_cpu_percent_is_in_valid_range`             | tests/test_backend_system_metrics.py    | RED    |
| TC4 | `test_memory_fields_correct`                     | tests/test_backend_system_metrics.py    | RED    |
| TC5 | `test_network_entries_have_required_fields`      | tests/test_backend_system_metrics.py    | RED    |
| TC6 | `test_loopback_and_virtual_interfaces_excluded`  | tests/test_backend_system_metrics.py    | RED    |
| TC7 | `test_disk_fields_are_non_negative_numbers`      | tests/test_backend_system_metrics.py    | RED    |
| TC8 | `test_sampled_at_is_positive_and_recent`         | tests/test_backend_system_metrics.py    | RED    |
| TC9 | `test_first_call_returns_zero_rates`             | tests/test_backend_system_metrics.py    | RED    |

## Validation Results

| ID  | Result  | Output |
|-----|---------|--------|
| TC1 | PENDING | —      |
| TC2 | PENDING | —      |
| TC3 | PENDING | —      |
| TC4 | PENDING | —      |
| TC5 | PENDING | —      |
| TC6 | PENDING | —      |
| TC7 | PENDING | —      |
| TC8 | PENDING | —      |
| TC9 | PENDING | —      |

## Red-Phase Evidence

All 9 tests collected and failing with the **correct** reason (endpoint missing, not ImportError):

```
FAILED tests/test_backend_system_metrics.py::test_endpoint_returns_200
  AssertionError: Expected HTTP 200 but got 404. Endpoint not yet implemented (T3).
  assert 404 == 200

FAILED tests/test_backend_system_metrics.py::test_response_has_correct_shape
  assert 404 == 200

FAILED tests/test_backend_system_metrics.py::test_cpu_percent_is_in_valid_range
  assert 404 == 200

FAILED tests/test_backend_system_metrics.py::test_memory_fields_correct
  assert 404 == 200

FAILED tests/test_backend_system_metrics.py::test_network_entries_have_required_fields
  assert 404 == 200

FAILED tests/test_backend_system_metrics.py::test_loopback_and_virtual_interfaces_excluded
  assert 404 == 200

FAILED tests/test_backend_system_metrics.py::test_disk_fields_are_non_negative_numbers
  assert 404 == 200

FAILED tests/test_backend_system_metrics.py::test_sampled_at_is_positive_and_recent
  assert 404 == 200

FAILED tests/test_backend_system_metrics.py::test_first_call_returns_zero_rates
  assert 404 == 200

9 failed, 0 passed, 0 errors
```

## Unresolved Failures

All 9 tests are intentionally red. @6code must implement tasks T1, T2, T3 to make them green:
- **T1** — Add `psutil>=5.9` to `backend/requirements.txt` and install it
- **T2** — Add Pydantic models: `NetworkInterface`, `MemoryMetrics`, `DiskMetrics`, `SystemMetricsResponse`
- **T3** — Add module-level `_prev_net` / `_prev_disk` state, `_is_physical_iface()` filter, and
  `@app.get("/api/metrics/system", response_model=SystemMetricsResponse)` endpoint
