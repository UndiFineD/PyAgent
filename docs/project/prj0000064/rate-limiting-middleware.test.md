# rate-limiting-middleware — Test Plan

_Owner: @5test | Status: DONE_

## Test file: `tests/test_rate_limiting.py`

| # | Test | Assertion |
|---|---|---|
| 1 | `test_health_exempt_from_rate_limit` | 200 regardless of RATE_LIMIT_REQUESTS=1 |
| 2 | `test_allowed_under_limit` | First request returns 200 |
| 3 | `test_rate_limit_triggers_429` | (N+1)th request returns 429 |
| 4 | `test_retry_after_header_present` | 429 response includes `retry-after` header |
| 5 | `test_rate_limiter_module_imports` | Module importable, classes exposed |
| 6 | `test_token_bucket_allows_then_blocks` | Unit test of TokenBucket directly |
