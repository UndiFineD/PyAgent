# agent-memory-persistence — Code Notes

_Owner: @6code_

## Files created/modified

### NEW: `backend/memory_store.py`
- `MemoryStore` singleton (module-level instance)
- `_locks: defaultdict(asyncio.Lock)` — per-agent lock
- `_path(agent_id)` — returns Path to `data/agents/<agent_id>/memory.json`
- `append(agent_id, entry)` — acquires lock, reads file, appends, writes back; generates UUID id + ISO timestamp
- `read(agent_id, limit)` — acquires lock, reads file, returns reversed list[:limit]
- `clear(agent_id)` — acquires lock, writes `[]` to file

### MODIFIED: `backend/app.py`
- Added `from .memory_store import memory_store` import
- Added 3 endpoint functions under `api_router`:
  - `read_agent_memory(agent_id, limit, user)`
  - `append_agent_memory(agent_id, body, user)`
  - `clear_agent_memory(agent_id, user)`
- Pydantic model `MemoryEntryRequest(role, content, session_id?)`

## Code health notes

- No new external dependencies required (uses stdlib `json`, `uuid`, `datetime`, `pathlib`, `asyncio`)
- Entry schema validated by Pydantic before reaching MemoryStore
- File not created until first `append` call (lazy init)
