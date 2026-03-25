# agent-memory-persistence — Project Overview

_Owner: @1project | Status: In Sprint_

**Goal:** Persist agent conversation context and task history across sessions using a JSON file-backed MemoryStore, accessible via backend REST endpoints.

**In scope:**
- `backend/memory_store.py` — JSON-backed MemoryStore (read/write/append/clear per agent)
- `backend/app.py` — `GET /api/agent-memory/{agent_id}`, `POST /api/agent-memory/{agent_id}`, `DELETE /api/agent-memory/{agent_id}`
- `tests/test_agent_memory.py` — tests
- `docs/project/prj0000065/` — 9 artifacts
- `data/projects.json` + `docs/project/kanban.md` — lane transitions

**Out of scope:** Vector embeddings, semantic search, multi-node shared memory, encryption at rest.

## Branch Plan

**Expected branch:** `prj0000065-agent-memory-persistence`

**Scope boundary:** Only the files listed above may be modified on this branch.

**Handoff rule:** `@9git` must confirm `OBSERVED_BRANCH == prj0000065-agent-memory-persistence` before staging, committing, or creating a PR.

**Failure rule:** If tests fail or branch mismatch is detected, stop and notify `@0master`.


## Legacy Project Overview Exception

This project overview predates the modern Project Identity / Goal and Scope / Branch Plan
template. It was authored with an earlier workflow format and has not been migrated.
The project was completed successfully; the deviation is a documentation formatting issue only.

Migration to the modern template is on record with @0master.
