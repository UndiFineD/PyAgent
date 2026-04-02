# agent-memory-persistence — Think

_Owner: @2think_

## Problem

Agents currently have no persistence layer for conversation context or task history. Between sessions, all memory is lost, forcing agents to rebuild context from scratch.

## Constraints

- Budget tier M — no external services (ChromaDB, Pinecone, Redis)
- Must integrate with existing backend FastAPI app
- Must not require database migrations
- Must work with existing `ContextTransaction` / `MemoryTransaction` patterns

## Design choices considered

| Option | Pros | Cons |
|---|---|---|
| SQLite via `aiosqlite` | Transactional, queryable | Extra dependency, schema migrations |
| JSON file per agent | Zero deps, human-readable, simple | No concurrent write safety at OS level |
| In-memory dict (no persist) | Trivially simple | Doesn't satisfy goal |
| Embedded vector DB (FAISS) | Semantic search | Overkill for P3/M budget |

## Selected direction

**JSON file per agent** stored under `data/agents/<agent_id>/memory.json`.

- One file per agent, append-only log of memory entries (list of dicts)
- Reads deserialize entire file; writes serialize entire list back (small files expected)
- File-level locking via `asyncio.Lock` (per-agent lock map in MemoryStore)
- Entry schema: `{id, role, content, timestamp, session_id}`

## Open questions resolved

- Q: Where to store files? A: `data/agents/<agent_id>/memory.json` (consistent with existing `data/agents/` directory)
- Q: Max entries? A: No hard cap in MVP; API supports `?limit=N` query param for reads
- Q: Auth? A: Use existing `require_auth` dependency pattern from `backend/app.py`
