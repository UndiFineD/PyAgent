# agent-timeout-watchdog — Test Plan

_Owner: @5test_

## Tests in `tests/test_watchdog.py`

| # | Name | Description |
|---|------|-------------|
| 1 | `test_run_success` | Coroutine completes in time → returns `{"status":"ok"}` |
| 2 | `test_run_timeout_increments_retry` | Coroutine times out → retry_counts incremented |
| 3 | `test_run_dead_letter_after_retries` | Exhaust max_retries → task ends up in DLQ |
| 4 | `test_status_returns_correct_shape` | `status()` dict has required keys |
| 5 | `test_dlq_contains_correct_entry` | DLQ entry has agent_id and timestamp |
| 6 | `test_watchdog_status_endpoint` | `GET /api/watchdog/status` returns 200 + JSON |
