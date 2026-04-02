# agent-memory-persistence — Design

_Owner: @3design_

## MemoryStore interface

```python
class MemoryStore:
    async def append(agent_id: str, entry: dict) -> dict      # returns entry with generated id
    async def read(agent_id: str, limit: int | None) -> list  # returns entries newest-first
    async def clear(agent_id: str) -> None
```

## Entry schema

```json
{
  "id": "<uuid4>",
  "role": "user | assistant | system",
  "content": "...",
  "timestamp": "2026-01-01T00:00:00Z",
  "session_id": "<uuid4 or null>"
}
```

## REST endpoints (added to `backend/app.py`)

| Method | Path | Description |
|---|---|---|
| GET | `/api/agent-memory/{agent_id}` | Read entries (optional `?limit=N`) |
| POST | `/api/agent-memory/{agent_id}` | Append entry; body = `{role, content, session_id?}` |
| DELETE | `/api/agent-memory/{agent_id}` | Clear all memory for agent |

All endpoints require `require_auth` dependency.

## Storage layout

```
data/
  agents/
    <agent_id>/
      memory.json   ← list of entry dicts
```

## Concurrency model

- Module-level `defaultdict(asyncio.Lock)` keyed by `agent_id`
- Lock acquired for duration of read/write to prevent concurrent corruption
- Single-process guarantee only (acceptable for MVP)
