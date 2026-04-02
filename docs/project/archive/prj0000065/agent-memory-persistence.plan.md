# agent-memory-persistence — Plan

_Owner: @4plan_

## Tasks

1. Create `backend/memory_store.py`
   - `MemoryStore` class with `append`, `read`, `clear`
   - Per-agent asyncio.Lock
   - Path: `data/agents/<agent_id>/memory.json`
   - Auto-create directory if missing

2. Update `backend/app.py`
   - Import `MemoryStore`
   - Add `GET /api/agent-memory/{agent_id}` — query param `limit: int | None = None`
   - Add `POST /api/agent-memory/{agent_id}` — body `{role, content, session_id?}`
   - Add `DELETE /api/agent-memory/{agent_id}` — protected by `require_auth`

3. Create `tests/test_agent_memory.py`
   - Test append + read round trip
   - Test limit param
   - Test clear
   - Test auth enforcement (unauthenticated gets 401/403)
   - Test entry schema validation (missing role → 422)

## Acceptance criteria

- [ ] `GET /api/agent-memory/{agent_id}` returns 200 with list of entries
- [ ] `POST /api/agent-memory/{agent_id}` returns 201 with created entry including generated `id` and `timestamp`
- [ ] `DELETE /api/agent-memory/{agent_id}` returns 204
- [ ] `?limit=N` returns only N most recent entries
- [ ] Unauthenticated requests return 401 or 403
- [ ] All tests pass with `pytest tests/test_agent_memory.py`

## Validation command

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
pytest tests/test_agent_memory.py -v
```
