# agent-timeout-watchdog — Code Log

_Owner: @6code_

## Files changed

### `backend/watchdog.py` (NEW)
- `AgentWatchdog` + module-level singleton

### `backend/app.py`
- Import `watchdog` singleton
- `GET /watchdog/status` added to `_auth_router`

### `tests/test_watchdog.py` (NEW)
- 6 tests, all passing
