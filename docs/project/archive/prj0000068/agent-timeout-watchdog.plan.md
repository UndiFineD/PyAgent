# agent-timeout-watchdog — Plan

_Owner: @4plan_

## Tasks

1. Create `backend/watchdog.py`
   - `AgentWatchdog` class with `run()`, `status()`, `dead_letter_queue`
   - Module-level singleton `watchdog`

2. Modify `backend/app.py`
   - Import `watchdog` from `.watchdog`
   - Add `GET /watchdog/status` to `_auth_router`

3. Create `tests/test_watchdog.py`
   - 6 tests

## Acceptance criteria
- [ ] Timeout triggers retry logic
- [ ] Retry budget exhaustion goes to DLQ
- [ ] `GET /api/watchdog/status` returns correct structure
- [ ] All 6 tests pass
