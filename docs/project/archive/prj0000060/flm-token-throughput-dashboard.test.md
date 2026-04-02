# flm-token-throughput-dashboard — Test Plan
_Owner: @5test | Status: DONE_

## Unit Tests (tests/test_flm_dashboard.py)

| # | Test Name | What It Verifies |
|---|---|---|
| 1 | `test_flm_metrics_endpoint_returns_200` | GET /api/metrics/flm returns HTTP 200 |
| 2 | `test_flm_response_has_samples_key` | Response JSON contains a "samples" key |
| 3 | `test_flm_samples_count_is_10` | The "samples" list has exactly 10 entries |
| 4 | `test_flm_sample_has_required_fields` | Each sample has timestamp, tokens_per_second, model, queue_depth |
| 5 | `test_flm_avg_tokens_is_numeric` | avg_tokens_per_second is a float or int (numeric) |

## Coverage Goals
- All five keys in the response envelope touched
- Sample structure fully validated on at least one entry
- Happy-path only (simulated data, no error injection needed)

## Test Client
Using `fastapi.testclient.TestClient(app)` — synchronous, no server needed.
The `/api/metrics/flm` endpoint is public (no auth dependency), so no auth
mocking is required.
