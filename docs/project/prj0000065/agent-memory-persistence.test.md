# agent-memory-persistence — Test Plan

_Owner: @5test_

## Test file: `tests/test_agent_memory.py`

### Tests

| # | Name | Type | Description |
|---|---|---|---|
| 1 | `test_append_creates_entry` | unit | POST returns 201 with id + timestamp |
| 2 | `test_read_returns_entries` | unit | GET returns list including appended entry |
| 3 | `test_read_limit_param` | unit | GET ?limit=1 returns only 1 entry |
| 4 | `test_clear_removes_entries` | unit | DELETE returns 204; subsequent GET returns [] |
| 5 | `test_unauthenticated_get_rejected` | security | GET without auth token → 401/403 |
| 6 | `test_invalid_role_rejected` | validation | POST with invalid body → 422 |

## Test environment notes

- Uses `httpx.AsyncClient` + `pytest-asyncio` pattern matching existing test files
- Patches file I/O at MemoryStore level to avoid writing to disk during tests
- Auth token: use same `Authorization: Bearer test-token` pattern from existing tests

## Coverage targets

- `backend/memory_store.py`: 90%+
- Endpoint handlers: 100%
