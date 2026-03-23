# conky-real-metrics — Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-23_

## Implementation Summary
Added `GET /api/metrics/system` endpoint to `backend/app.py` using psutil for real-time CPU, memory, network IO, and disk IO metrics.
Interface filtering uses case-insensitive prefix matching to exclude loopback ("lo", "loopback"), docker, veth, br-*, virbr, vmnet, vbox interfaces.
Rewrote `web/apps/Conky.tsx` to consume real data via `fetch('/api/metrics/system')` every 2 s, with rolling 30-point history buffers for CPU and network charts, per-interface rows (≤4) or aggregate sum, OFFLINE amber badge on fetch failure, and real memory MB display.
Created `web/tsconfig.json` (project had none) to enable `npx tsc --noEmit`.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `backend/app.py` | Added `import time`, `import psutil`, module-level delta state, 5 Pydantic models, `/api/metrics/system` endpoint | +74 |
| `web/apps/Conky.tsx` | Full rewrite — real API data, SystemMetrics interfaces, OFFLINE badge, per-iface rows, disk section | ~170 |
| `web/tsconfig.json` | Created — enables `npx tsc --noEmit` | +20 |

## Test Run Results
```
============================================ test session starts ============================================
platform win32 -- Python 3.13.12, pytest-9.0.2
collected 9 items

tests/test_backend_system_metrics.py::test_endpoint_returns_200 PASSED                                 [ 11%]
tests/test_backend_system_metrics.py::test_response_has_correct_shape PASSED                           [ 22%]
tests/test_backend_system_metrics.py::test_cpu_percent_is_in_valid_range PASSED                        [ 33%]
tests/test_backend_system_metrics.py::test_memory_fields_correct PASSED                                [ 44%]
tests/test_backend_system_metrics.py::test_network_entries_have_required_fields PASSED                 [ 55%]
tests/test_backend_system_metrics.py::test_loopback_and_virtual_interfaces_excluded PASSED             [ 66%]
tests/test_backend_system_metrics.py::test_disk_fields_are_non_negative_numbers PASSED                 [ 77%]
tests/test_backend_system_metrics.py::test_sampled_at_is_positive_and_recent PASSED                    [ 88%]
tests/test_backend_system_metrics.py::test_first_call_returns_zero_rates PASSED                        [100%]

============================================= 9 passed in 2.43s ==============================================
```

## Deferred Items
None.
