# transaction-managers-full — Project Overview

_Status: HANDED_OFF_
_Owner: @1project | Updated: 2026-03-22_

## Project Identity
**Project ID:** prj0000045
**Short name:** transaction-managers-full
**Project folder:** `docs/project/prj0000045/`

## Project Overview
Deliver four production-quality transaction managers that PyAgent's swarm architecture
depends on. `prj0000044` created minimal CI-unblocking stubs; this project replaces
them with real, fully-functional implementations housed in the new `src/transactions/`
package with a shared `BaseTransaction` ABC. The four managers cover in-memory data
(`MemoryTransaction`), encrypted file-system operations (`StorageTransaction`),
subprocess execution with SIGTERM rollback (`ProcessTransaction`), and UUID-based
context-lineage tracking (`ContextTransaction`).

## Goal & Scope
**Goal:** Implement four production-quality transaction managers aligned with the
`src/transactions/` Option-B architecture decided in `docs/agents/2think.memory.md`.

**In scope:**
- `src/transactions/` — new package with BaseTransaction ABC and all four managers
- `src/MemoryTransactionManager.py` — shim update (re-export from `src/transactions/`)
- `src/core/StorageTransactionManager.py` — shim update (re-export from `src/transactions/`)
- `src/core/ProcessTransactionManager.py` — shim update (re-export from `src/transactions/`)
- `src/core/ContextTransactionManager.py` — shim update (re-export from `src/transactions/`)
- `src/context_manager/ContextWindow.py` — NEW: token-budgeted LLM context surface (tiktoken-aware, eviction, OpenAI-compatible snapshot)
- `src/context_manager/__init__.py` — add ContextWindow re-export alongside ContextManager
- `tests/test_transaction_managers.py` — may add tests, must not remove existing 14
- `tests/test_StorageTransactionManager.py` — create (acceptance criteria)
- `tests/test_ProcessTransactionManager.py` — create (acceptance criteria)
- `tests/test_ContextTransactionManager.py` — create (acceptance criteria)
- `tests/test_ContextWindow.py` — create (acceptance criteria for ContextWindow)
- `docs/project/prj0000045/` — project docs

**Out of scope:** CI workflow changes, frontend, Rust core, agent behaviour.

## Scope Extension (2026-03-22)
`ContextWindow` is added to scope per updated @0master directive. Design already exists
in `docs/agents/2think.memory.md` §3.3. Plan task T15 must be added. Test file
`tests/test_ContextWindow.py` must be created. The ContextTransaction `.hand_to_llm()`
method depends on ContextWindow being present.

## Branch Plan
**Expected branch:** `prj0000045-transaction-managers-full`
**Scope boundary:** `src/transactions/`, `src/MemoryTransactionManager.py`,
  `src/core/StorageTransactionManager.py`, `src/core/ProcessTransactionManager.py`,
  `src/core/ContextTransactionManager.py`, `src/context_manager/ContextWindow.py`,
  `src/context_manager/__init__.py`, `tests/test_transaction_managers.py`,
  `tests/test_StorageTransactionManager.py`, `tests/test_ProcessTransactionManager.py`,
  `tests/test_ContextTransactionManager.py`, `tests/test_ContextWindow.py`,
  `docs/project/prj0000045/`, `requirements.txt`.
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the
  active branch is `prj0000045-transaction-managers-full` and changed files stay
  inside the scope boundary above.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting,
  or ambiguous, return the task to `@0master` before downstream handoff.

## Key Reference Files
- `docs/agents/2think.memory.md` §3.1, §4.1–4.7 — **binding interface contracts**
- `docs/E2E_ENCRYPTION.md` — encryption requirements for `StorageTransaction`
- `src/MemoryTransactionManager.py` — existing `MemoryTransaction` (threading.RLock)
- `src/core/StorageTransactionManager.py` — prj0000044 stub (stage/commit API)
- `src/core/UnifiedTransactionManager.py` — prj0000044 unified stub
- `tests/test_transaction_managers.py` — 14 existing tests that must keep passing

## Architecture Decision (@2think — BINDING)
**Selected: Option B** — `src/transactions/` package with one PascalCase file per
manager and a shared `BaseTransaction` ABC.

```
src/transactions/
├── __init__.py                   # re-exports all four types
├── BaseTransaction.py            # ABC: tid, __aenter__, __aexit__, commit, rollback
├── MemoryTransactionManager.py   # moved+upgraded from src/MemoryTransactionManager.py
├── StorageTransactionManager.py  # new: encrypted atomic file ops
├── ProcessTransactionManager.py  # new: async subprocess + SIGTERM rollback
└── ContextTransactionManager.py  # new: UUID lineage + contextvar stack
```

Backward-compat shims at:
- `src/MemoryTransactionManager.py` → re-exports from `src/transactions/`
- `src/core/StorageTransactionManager.py` → re-exports from `src/transactions/`
- `src/core/ProcessTransactionManager.py` → re-exports from `src/transactions/`
- `src/core/ContextTransactionManager.py` → re-exports from `src/transactions/`

## Binding Interface Contracts (from 2think.memory.md §4.1–4.4)

### BaseTransaction (ABC)
```python
class BaseTransaction(abc.ABC):
    def __init__(self, tid=None) -> None: self.tid = tid
    async def __aenter__(self) -> "BaseTransaction": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool: ...
    @abc.abstractmethod
    async def commit(self) -> None: ...
    @abc.abstractmethod
    async def rollback(self) -> None: ...
```

### StorageTransaction
```python
class StorageTransaction(BaseTransaction):
    async def write(self, path: Path, content: str | bytes, *, user_id=None) -> None: ...
    async def delete(self, path: Path) -> None: ...
    async def mkdir(self, path: Path) -> None: ...
    async def commit(self) -> None: ...   # applies all pending ops atomically
    async def rollback(self) -> None: ... # removes .tmp files, reverts deletes
    # BACKWARD COMPAT: preserves stage()/commit() sync API for test_transaction_managers.py
```

### ProcessTransaction
```python
class ProcessTransaction(BaseTransaction):
    async def run(self, cmd, *, cwd=None, timeout=30.0) -> tuple[int, str, str]: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...  # SIGTERM → SIGKILL
    # BACKWARD COMPAT: preserves start()/wait()/stdout sync API + RecursionGuardError
```

### ContextTransaction
```python
class ContextTransaction(BaseTransaction):
    transaction_id: uuid.UUID
    parent_id: uuid.UUID | None
    context_id: str
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    @classmethod
    def current(cls) -> "ContextTransaction | None": ...
    @classmethod
    def active_contexts(cls) -> set[str]: ...   # backward compat
    # BACKWARD COMPAT: preserves sync with/async with for context_id-based guard
```

### MemoryTransaction
```python
class MemoryTransaction(BaseTransaction):
    async def set(self, key, value, *, encrypt=False) -> None: ...
    async def get(self, key, *, decrypt=False) -> Any: ...
    async def delete(self, key) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def sync_remote(self, endpoint, *, encrypted=True) -> None: ...
    # BACKWARD COMPAT: preserves __enter__/__exit__ threading.RLock API
```

## Acceptance Criteria
1. `pytest tests/test_transaction_managers.py` — all 14 existing tests pass
2. `pytest tests/test_StorageTransactionManager.py tests/test_ProcessTransactionManager.py tests/test_ContextTransactionManager.py` — all pass
3. `pytest tests/test_ContextWindow.py` — all pass (NEW)
4. `python -c "from src.transactions import StorageTransaction, ProcessTransaction, ContextTransaction, MemoryTransaction"` — no import error
5. `python -c "from src.core.StorageTransactionManager import StorageTransaction"` — no import error (shim)
6. `python -c "from src.MemoryTransactionManager import MemoryTransaction"` — no import error (shim)
7. `python -c "from src.context_manager import ContextWindow"` — no import error (NEW)
8. All four managers have a `validate()` top-level function
9. `pytest -q` passes with no new failures vs. current main baseline

## Milestones
| # | Milestone | Agent | Status |
|---|---|---|---|
| M1 | Options explored | @2think | DONE (see 2think.memory.md §3.1 + §3.3) |
| M2 | Design confirmed | @3design | DONE |
| M3 | Plan finalized | @4plan | DONE (T00–T14); T15 ContextWindow must be added |
| M4 | Tests written | @5test | DONE for T03–T13; test_ContextWindow.py needed |
| M5 | Code implemented | @6code | NOT_STARTED |
| M6 | Integration validated | @7exec | NOT_STARTED |
| M7 | Security clean | @8ql | NOT_STARTED |
| M8 | Committed | @9git | NOT_STARTED |

## Status
_Last updated: 2026-03-22_
**Scope extended by @0master:** ContextWindow (`src/context_manager/ContextWindow.py`)
added to scope. Design already in `docs/agents/2think.memory.md` §3.3.
@4plan must add T15 (ContextWindow implementation + `src/context_manager/__init__.py` update).
@5test must add `tests/test_ContextWindow.py`.
@6code then implements T00–T15 on branch `prj0000045-transaction-managers-full`.
Handing off to @4plan for T15 addition (M1–M3 done for core scope, M3 needs T15 appended).
