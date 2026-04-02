# transaction-managers-full — Implementation Plan

_Status: COMPLETE_
_Planner: @4plan | Updated: 2026-03-22 | Completed: 2026-06-13_

> ⚠️ **Branch Gate Warning**
> Expected branch: `prj0000045-transaction-managers-full`
> Observed branch: `main`
> Per established project convention, documentation artifacts (plan, design, test, code
> docs) are authored on `main`. **@6code and @9git MUST switch to branch
> `prj0000045-transaction-managers-full` before creating or modifying ANY `.py` file.**
> No code commits are permitted on `main` for this project.

---

## Overview

Deliver four production-quality transaction managers inside a new `src/transactions/`
package, plus backward-compatible shims at the legacy import paths. The package
exposes `StorageTransaction`, `ProcessTransaction`, `ContextTransaction`, and
`MemoryTransaction` — each with a dual sync/async API so that the 14 existing
`test_transaction_managers.py` tests keep passing while new async-callers get a clean
`async with` interface.

**Current state (verified 2026-03-22):**
- `src/transactions/` — does NOT exist (all files are NEW)
- `src/core/StorageTransactionManager.py` — does NOT exist (NEW)
- `src/core/ProcessTransactionManager.py` — does NOT exist (NEW)
- `src/core/ContextTransactionManager.py` — does NOT exist (NEW)
- `tests/test_transaction_managers.py` — EXISTS, 14 tests, currently FAILING on import
  (missing `src.core.ProcessTransactionManager` and `src.core.ContextTransactionManager`)
- `src/MemoryTransactionManager.py` — EXISTS, needs body replaced with shim
- `tests/test_{Storage,Process,Context}TransactionManager.py` — do NOT exist (NEW)
- `cryptography` — installed (46.0.5) but not in `requirements.txt` (must be added)
- `httpx` — `httpx==0.28.1` already in `requirements.txt`; CI inherits via `-r requirements.txt`

---

## Open Questions — Resolved

### Q1: Asyncio compatibility under `asyncio_mode = auto`

**Resolution: Keep sync and async codepaths strictly separate — no `asyncio.run()` inside
`commit()`.**

- All four concrete managers define `commit()` as a **regular synchronous method** (NOT
  `async def`). This method contains the actual commit logic (file writes, process
  termination recording, context cleanup, memory flush).
- `__exit__` calls `commit()` directly (sync).
- `__aexit__` also calls the **sync** `commit()` directly — calling a sync function from
  an async context is legal in Python; it simply blocks the event loop briefly, which is
  acceptable for the I/O volumes involved (≤1 MB writes, per NFRs).
- There is **no** `asyncio.run()` call anywhere in `commit()`. No event-loop detection
  needed.
- The legacy `def test_*()` tests (not async) are outside any event loop, so there is
  no conflict.
- `async def acommit()` is available as a separate method for callers that want a true
  coroutine (calls `asyncio.to_thread(self.commit)` internally if needed).

### Q2: `_proc.poll()` vs asyncio Process.returncode

**Resolution: Separate attributes `_proc` and `_async_proc`.**

- `ProcessTransaction.start()` (sync) creates `subprocess.Popen` and stores it in
  `self._proc`. This Popen object has `.poll()` and must be used with
  `subprocess.PIPE` for stdout capture.
- `ProcessTransaction.start_async()` (async) creates `asyncio.subprocess.Process` and
  stores it in `self._async_proc`. It exposes `.returncode` (not `.poll()`).
- The two attributes coexist; legacy tests only access `_proc` and call `.poll()`.
- `rollback()` terminates whichever is active (checks both).

**Additional finding from tests:** `test_start_and_wait_success` asserts
`assert b"ok" in (tx.stdout or b"")`. Therefore:
- `ProcessTransaction.start()` MUST open the subprocess with
  `stdout=subprocess.PIPE, stderr=subprocess.PIPE`.
- `ProcessTransaction.wait()` MUST call `_proc.communicate()` (not `_proc.wait()`)
  and store stdout bytes in `self.stdout: Optional[bytes]`, return code in the
  return value.

### Q3: `validate()` in shims

**Resolution: Each shim re-imports and re-exports `validate`.**

- Every `src/transactions/*.py` implementation file exposes
  `def validate() -> bool: return True` at module level.
- Every `src/core/*.py` shim does:
  ```python
  from src.transactions.XxxTransactionManager import XxxTransaction, validate  # noqa: F401
  ```
- Verified: `tests/test_core_quality.py` scans `src/core/` for a callable `validate`.
- The `src/transactions/__init__.py` also re-exports `validate` (aliased per module).

### Q4: Dual lock in MemoryTransaction

**Resolution: `threading.RLock` for sync path, `asyncio.Lock` for async path.**

- `self._rlock = threading.RLock()` — acquired in `__enter__`, released in `__exit__`.
- `self._alock = asyncio.Lock()` — acquired in `__aenter__`, released in `__aexit__`.
- Both are **instance** attributes created in `__init__`.
- Sync callers never touch `_alock`; async callers never touch `_rlock`.
- No `asyncio.run()` or blocking calls on either lock from the wrong context.

### Q5: `httpx` and `cryptography` version pinning

**Resolution: `cryptography` added to `requirements.txt`; `httpx` already correct.**

- `httpx==0.28.1` is already in `requirements.txt` (≥0.27.0 satisfied). No change
  to `httpx` line.
- `requirements-ci.txt` uses `-r requirements.txt` and inherits `httpx` and will
  inherit `cryptography` once added. No change to `requirements-ci.txt`.
- `cryptography>=42.0.0` must be added to `requirements.txt` (currently installed as
  transitive dep at 46.0.5, but not declared). This is required by
  `StorageTransaction._encrypt()`.

---

## Architecture Notes for @6code

### Class hierarchy choice

`StorageTransaction`, `ProcessTransaction`, and `ContextTransaction` do **NOT** inherit
from `BaseTransaction`. They provide a duck-typed compatible interface (same method
names, same context-manager protocol). This is necessary because Python cannot have
both `def commit(self)` and `async def commit(self)` in the same class — the sync
`commit()` must exist for legacy tests, so no ABC inheritance.

`MemoryTransaction` similarly does **not** inherit from `BaseTransaction`.
`BaseTransaction` is exported from `src/transactions/` for use by new async-only code
(future managers, swarm orchestration) and is not used by the four managers in this
project.

### File copyright header

Every new `.py` file MUST begin with the standard PyAgent copyright block:
```python
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# ...
```

---

## Task List

- [x] T00 | Add `cryptography>=42.0.0` to `requirements.txt` | Files: `requirements.txt` | Acceptance: `python -c "import cryptography"` works; line present in requirements.txt
- [x] T01 | Create `src/transactions/__init__.py` | Files: `src/transactions/__init__.py` | Acceptance: `from src.transactions import StorageTransaction, ProcessTransaction, ContextTransaction, MemoryTransaction, BaseTransaction` succeeds
- [x] T02 | Create `src/transactions/BaseTransaction.py` | Files: `src/transactions/BaseTransaction.py` | Acceptance: `BaseTransaction` is abstract; `StorageTransaction("x")` does NOT inherit it; direct instantiation raises TypeError
- [x] T03 | Create `src/transactions/StorageTransactionManager.py` | Files: `src/transactions/StorageTransactionManager.py` | Acceptance: `validate()` returns True; stage/commit/rollback/`__enter__`/`__exit__`/`__aenter__`/`__aexit__` all work; dual-mode constructor; encryption only when user_id supplied
- [x] T04 | Create `src/transactions/ProcessTransactionManager.py` | Files: `src/transactions/ProcessTransactionManager.py` | Acceptance: `validate()` returns True; `start()` sets `_proc` (Popen with PIPE); `wait()` sets `self.stdout`; `rollback()` terminates `_proc`; `start_async()`/`wait_async()` use asyncio subprocess
- [x] T05 | Create `src/transactions/ContextTransactionManager.py` | Files: `src/transactions/ContextTransactionManager.py` | Acceptance: `validate()` returns True; `RecursionGuardError` raised on re-entry; `active_contexts()` is accurate; `ValueError` on empty context_id; `UUID` assigned per transaction; `current()` classmethod works
- [x] T06 | Create `src/transactions/MemoryTransactionManager.py` | Files: `src/transactions/MemoryTransactionManager.py` | Acceptance: `validate()` returns True; sync `with` acquires `_rlock`; `async with` acquires `_alock`; `set/get/delete/commit/rollback` work; `sync_remote(dry_run=True)` returns payload dict without network
- [x] T07 | Create `src/core/StorageTransactionManager.py` (NEW shim) | Files: `src/core/StorageTransactionManager.py` | Acceptance: `from src.core.StorageTransactionManager import StorageTransaction, validate` succeeds; `validate()` returns True
- [x] T08 | Create `src/core/ProcessTransactionManager.py` (NEW shim) | Files: `src/core/ProcessTransactionManager.py` | Acceptance: `from src.core.ProcessTransactionManager import ProcessTransaction, validate` succeeds; `validate()` returns True
- [x] T09 | Create `src/core/ContextTransactionManager.py` (NEW shim) | Files: `src/core/ContextTransactionManager.py` | Acceptance: `from src.core.ContextTransactionManager import ContextTransaction, RecursionGuardError, validate` succeeds; `validate()` returns True
- [x] T10 | Update `src/MemoryTransactionManager.py` (replace body with shim) | Files: `src/MemoryTransactionManager.py` | Acceptance: `from src.MemoryTransactionManager import MemoryTransaction` succeeds; existing callers unaffected
- [x] T11 | Create `tests/test_StorageTransactionManager.py` | Files: `tests/test_StorageTransactionManager.py` | Acceptance: tests async multi-op write/delete/mkdir; encryption fixture via monkeypatch; `validate()` import check; all tests pass
- [x] T12 | Create `tests/test_ProcessTransactionManager.py` | Files: `tests/test_ProcessTransactionManager.py` | Acceptance: tests async `run()` returning (rc, stdout, stderr); rollback via SIGTERM; `validate()` import check; all tests pass
- [x] T13 | Create `tests/test_ContextTransactionManager.py` | Files: `tests/test_ContextTransactionManager.py` | Acceptance: tests UUID lineage (`transaction_id`, `parent_id`); `current()` classmethod; `validate()` import check; all tests pass
- [x] T14 | Full test validation run | — | `pytest tests/test_transaction_managers.py` — 14 passed; all shim import smoke-tests pass; `pytest tests/test_core_quality.py` passes

---

## Task Details

### T00 — Add `cryptography>=42.0.0` to `requirements.txt`

**File:** `requirements.txt`
**Change:** Add one line `cryptography>=42.0.0` in the direct-dependencies section
(after `httpx...`).
**Why:** `StorageTransaction._encrypt()` uses `cryptography.fernet.Fernet` and
`cryptography.hazmat.primitives.kdf.hkdf.HKDF`. Currently installed transitively
(46.0.5) but not declared — declaring it enforces a floor version and prevents
silent breakage if the transitive dep is removed.
**Acceptance:** `Select-String -Path requirements.txt -Pattern "cryptography"` returns
a match; `python -c "import cryptography; print(cryptography.__version__)"` prints
`46.*` or similar.

---

### T01 — `src/transactions/__init__.py`

**File:** `src/transactions/__init__.py` (NEW)
**Content:** Re-export all public symbols:
```python
from src.transactions.BaseTransaction import BaseTransaction
from src.transactions.MemoryTransactionManager import MemoryTransaction, validate as validate_memory
from src.transactions.StorageTransactionManager import StorageTransaction, validate as validate_storage
from src.transactions.ProcessTransactionManager import ProcessTransaction, validate as validate_process
from src.transactions.ContextTransactionManager import ContextTransaction, RecursionGuardError, validate as validate_context

__all__ = [
    "BaseTransaction",
    "MemoryTransaction",
    "StorageTransaction",
    "ProcessTransaction",
    "ContextTransaction",
    "RecursionGuardError",
]
```
**Acceptance:** `from src.transactions import StorageTransaction, ProcessTransaction, ContextTransaction, MemoryTransaction` — all four importable.

---

### T02 — `src/transactions/BaseTransaction.py`

**File:** `src/transactions/BaseTransaction.py` (NEW)
**Design contract (from design.md):**
```python
class BaseTransaction(abc.ABC):
    def __init__(self, tid=None): self.tid = tid
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type: await self.rollback()
        else: await self.commit()
        return False
    @abc.abstractmethod
    async def commit(self) -> None: ...
    @abc.abstractmethod
    async def rollback(self) -> None: ...

def validate() -> bool: return True
```
**Note for @6code:** None of the four concrete managers in this project inherit
`BaseTransaction`. It is exported for future async-only code. Do NOT change the
concrete manager classes to inherit it.
**Acceptance:** `from src.transactions.BaseTransaction import BaseTransaction, validate`;
`BaseTransaction()` raises `TypeError` (abstract).

---

### T03 — `src/transactions/StorageTransactionManager.py`

**File:** `src/transactions/StorageTransactionManager.py` (NEW)
**Key implementation constraints:**

1. **Dual-mode constructor:**
   - `StorageTransaction(target: Path)` — legacy mode (single-file, stage/commit API)
   - `StorageTransaction()` or `StorageTransaction(tid=uuid)` — new multi-op async mode
   - Detect mode by checking `isinstance(target, Path)` in `__init__`.

2. **Sync commit (no asyncio):**
   ```python
   def commit(self) -> None:
       if self._committed or self._rolled_back: return
       if self._staged is None: return
       # tmp-file + os.replace (same as prj0000044 stub)
       ...
       self._committed = True
   ```

3. **`__exit__` and `__aexit__`** both call `self.commit()` (sync) on clean exit.

4. **Async multi-op methods:** `async def write(path, content, *, user_id=None)`,
   `async def delete(path)`, `async def mkdir(path)` — queue operations to
   `self._ops: list`; `async def commit()` (different name from sync `commit()` —
   name it `acommit()` and document relation) or run them via `asyncio.to_thread`.

   > **Note for @6code:** Python cannot have BOTH `def commit(self)` and
   > `async def commit(self)`. Use `async def acommit(self)` for the async multi-op
   > path. The `__aexit__` calls `self.commit()` (sync) for `async with target_path`
   > usage. For multi-op async usage, callers use `await tx.acommit()` explicitly or
   > `async def __aexit__` can detect mode (via `self._ops`) and call the appropriate
   > commit path.

5. **Encryption (`user_id != None`):**
   - Key derivation: `HKDF-SHA256(master_key, salt=user_id.encode(), info=b"storage-tx")`
   - Master key from env `PYAGENT_STORAGE_MASTER_KEY` (base64-encoded 32 bytes)
   - If key absent and `user_id` is set: raise `EncryptionConfigError` at `write()` time
   - If `user_id=None`: plaintext (tests use `user_id=None`)

6. **`validate()` at module level.**

**Acceptance:**
- All 5 `TestStorageTransaction` tests in `test_transaction_managers.py` pass.
- `from src.transactions.StorageTransactionManager import StorageTransaction, validate`
- `validate()` returns `True`.
- `StorageTransaction(tmp_path / "f.bin")` in sync `with` — commit writes file atomically.

---

### T04 — `src/transactions/ProcessTransactionManager.py`

**File:** `src/transactions/ProcessTransactionManager.py` (NEW)
**Key implementation constraints:**

1. **Dual-mode constructor:**
   - `ProcessTransaction(cmd: list[str])` — legacy mode
   - `ProcessTransaction()` — new multi-run mode

2. **Sync attributes (required by legacy tests):**
   ```python
   self._proc: Optional[subprocess.Popen] = None
   self.stdout: Optional[bytes] = None
   self.stderr: Optional[bytes] = None
   ```

3. **`start()` implementation (sync):**
   ```python
   def start(self) -> None:
       self._proc = subprocess.Popen(
           self._cmd,
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE,
       )
   ```

4. **`wait()` implementation (sync) — must capture stdout:**
   ```python
   def wait(self) -> int:
       stdout, stderr = self._proc.communicate()
       self.stdout = stdout
       self.stderr = stderr
       return self._proc.returncode
   ```
   > **Critical:** `test_start_and_wait_success` asserts `b"ok" in (tx.stdout or b"")`.
   > Must use `.communicate()`, not `.wait()`.

5. **`rollback()` (sync) — SIGTERM + SIGKILL fallback:**
   ```python
   def rollback(self) -> None:
       for proc in [self._proc, self._async_proc]:
           if proc and proc.poll() is None:  # only for Popen
               proc.terminate()
               ...
   ```

6. **`__exit__` triggers rollback if `exc_type is not None`.**

7. **Async support:**
   - `async def start_async()` — uses `asyncio.create_subprocess_exec`, stores in
     `self._async_proc`
   - `async def wait_async(timeout=30.0)` — uses `asyncio.wait_for`
   - `async def __aenter__` / `async def __aexit__`
   - `async def run(cmd, *, cwd, timeout)` — new multi-op API, returns
     `(rc, stdout, stderr)` as strings

8. **`validate()` at module level.**

**Acceptance:**
- All 4 `TestProcessTransaction` tests in `test_transaction_managers.py` pass
  (including `test_rollback_terminates_process` which checks `_proc.poll() is not None`
  after rollback).
- `tx.stdout` contains process output after `wait()`.

---

### T05 — `src/transactions/ContextTransactionManager.py`

**File:** `src/transactions/ContextTransactionManager.py` (NEW)
**Key implementation constraints:**

1. **Module-level contextvar (required for class-method access):**
   ```python
   _active_contexts: ContextVar[set] = ContextVar("_active_contexts", default=None)
   _context_stack: ContextVar[list] = ContextVar("_context_stack", default=None)
   ```
   > Use `default=None` and handle in methods (avoid sharing mutable default).

2. **`RecursionGuardError(RuntimeError)` — raised when same `context_id` entered twice.**

3. **Constructor:**
   ```python
   def __init__(self, context_id: str, *, parent_id=None, tid=None):
       if not context_id:
           raise ValueError("context_id must be a non-empty string")
       self.context_id = context_id
       self.transaction_id = tid or uuid.uuid4()
       # parent_id: auto-derives from _context_stack head
   ```

4. **`__enter__`:** checks `active_contexts()` for `context_id`; raises
   `RecursionGuardError` if already active; adds to active set; pushes self onto stack.

5. **`__exit__`:** removes `context_id` from active set; pops self from stack.

6. **`active_contexts()` classmethod** — returns `set` of `context_id` strings.

7. **`current()` classmethod** — returns innermost `ContextTransaction` from stack.

8. **`async __aenter__` / `async __aexit__`** — same logic as sync but async protocol.

9. **`async def commit()` / `async def rollback()`** — no-ops (context cleanup happens
   in `__exit__`); present for interface compatibility.

10. **`validate()` at module level.**

**Acceptance:**
- All 5 `TestContextTransaction` tests in `test_transaction_managers.py` pass.
- `RecursionGuardError` importable from both `src.transactions.ContextTransactionManager`
  and the `src.core.ContextTransactionManager` shim.
- `ContextTransaction("")` raises `ValueError`.

---

### T06 — `src/transactions/MemoryTransactionManager.py`

**File:** `src/transactions/MemoryTransactionManager.py` (NEW)
**Key implementation constraints:**

1. **Dual lock (resolved from Q4):**
   ```python
   self._rlock = threading.RLock()   # sync path
   self._alock: Optional[asyncio.Lock] = None  # lazy-init async path
   ```
   > `asyncio.Lock()` must be created in an async context (can't create at
   > `__init__` time if no event loop is running). Lazy-init: create in `__aenter__`
   > on first call.

2. **Sync CM:** `__enter__` acquires `_rlock`, `__exit__` releases `_rlock`.
3. **Async CM:** `__aenter__` acquires `_alock` (lazy-init), `__aexit__` releases.
4. **Key-value store (new async API):**
   ```python
   self._store: dict = {}    # committed data
   self._pending: dict = {}  # staged changes
   ```
   - `async def set(key, value, *, encrypt=False)` — adds to `_pending`
   - `async def get(key, *, decrypt=False)` — reads from `_store` (committed)
   - `async def delete(key)` — marks key for deletion in `_pending`
   - `async def commit()` — merges `_pending` into `_store`; clears `_pending`
   - `async def rollback()` — clears `_pending`

5. **`sync_remote(endpoint, *, encrypted=True, dry_run=False)`:**
   - If `dry_run=True`: builds payload dict `{"tid": str(tid), "encrypted": bool, "payload": {...}}` and returns it without any network I/O.
   - If `endpoint` is falsy: no-op, return `None`.
   - If `httpx` unavailable: log warning, return `None`.
   - Encryption: `Fernet` key from env `PYAGENT_MEMORY_SYNC_TOKEN` (not
     `PYAGENT_STORAGE_MASTER_KEY` — separate key).
   - Transport errors: raise `RemoteSyncError(endpoint, cause)`.

6. **`validate()` at module level.**

**Acceptance:**
- `from src.transactions.MemoryTransactionManager import MemoryTransaction, validate`
- `validate()` returns `True`.
- Sync `with MemoryTransaction() as tx: pass` — no error.
- `sync_remote(endpoint="https://x.com", dry_run=True)` returns a `dict` with
  `"payload"` key.

---

### T07 — `src/core/StorageTransactionManager.py` (NEW shim)

**File:** `src/core/StorageTransactionManager.py` (CREATE — file does NOT currently exist)
**Content:**
```python
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0
# ... (full header)

"""Shim: re-exports StorageTransaction from src.transactions package."""

from src.transactions.StorageTransactionManager import StorageTransaction, validate  # noqa: F401

__all__ = ["StorageTransaction", "validate"]
```
**Acceptance:** `from src.core.StorageTransactionManager import StorageTransaction, validate` — both importable; `validate()` returns `True`.

---

### T08 — `src/core/ProcessTransactionManager.py` (NEW shim)

**File:** `src/core/ProcessTransactionManager.py` (CREATE — file does NOT exist)
**Content:**
```python
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0
# ... (full header)

"""Shim: re-exports ProcessTransaction from src.transactions package."""

from src.transactions.ProcessTransactionManager import ProcessTransaction, validate  # noqa: F401

__all__ = ["ProcessTransaction", "validate"]
```
**Acceptance:** `from src.core.ProcessTransactionManager import ProcessTransaction, validate` — both importable.

---

### T09 — `src/core/ContextTransactionManager.py` (NEW shim)

**File:** `src/core/ContextTransactionManager.py` (CREATE — file does NOT exist)
**Content:**
```python
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0
# ... (full header)

"""Shim: re-exports ContextTransaction from src.transactions package."""

from src.transactions.ContextTransactionManager import (  # noqa: F401
    ContextTransaction,
    RecursionGuardError,
    validate,
)

__all__ = ["ContextTransaction", "RecursionGuardError", "validate"]
```
**Acceptance:** `from src.core.ContextTransactionManager import ContextTransaction, RecursionGuardError, validate` — all importable; `RecursionGuardError` is a subclass of `RuntimeError`.

---

### T10 — `src/MemoryTransactionManager.py` (replace body with shim)

**File:** `src/MemoryTransactionManager.py` (EDIT existing — keep Python header, replace body)
**New content after header:**
```python
"""Shim: re-exports MemoryTransaction from src.transactions package.

Previous in-process implementation moved to src/transactions/MemoryTransactionManager.py.
"""

from src.transactions.MemoryTransactionManager import MemoryTransaction, validate  # noqa: F401

__all__ = ["MemoryTransaction", "validate"]
```
**Acceptance:** `from src.MemoryTransactionManager import MemoryTransaction` — works;
existing callers that use `with MemoryTransaction() as tx:` still function.

---

### T11 — `tests/test_StorageTransactionManager.py`

**File:** `tests/test_StorageTransactionManager.py` (CREATE — written by @5test)
**Required tests (minimum):**
1. `test_validate_returns_true` — `from src.transactions.StorageTransactionManager import validate; assert validate() is True`
2. `test_shim_validate` — `from src.core.StorageTransactionManager import validate; assert validate() is True`
3. `test_async_write_creates_file(tmp_path)` — `async with StorageTransaction() as tx: await tx.write(path, b"data"); assert path.read_bytes() == b"data"`
4. `test_async_write_rollback(tmp_path)` — raises inside `async with`; file not created
5. `test_async_delete(tmp_path)` — write a file, then `async with StorageTransaction() as tx: await tx.delete(path); await tx.acommit()` — file gone
6. `test_async_mkdir(tmp_path)` — `await tx.mkdir(new_dir)` — directory created
7. `test_encryption_requires_key(tmp_path, monkeypatch)` — `write(path, b"x", user_id="u1")` with no env key raises `EncryptionConfigError`
8. `test_encrypted_write(tmp_path, storage_key)` — ciphertext on disk ≠ plaintext

**Acceptance:** All tests pass; `validate()` importable from both canonical and shim paths.

---

### T12 — `tests/test_ProcessTransactionManager.py`

**File:** `tests/test_ProcessTransactionManager.py` (CREATE — written by @5test)
**Required tests (minimum):**
1. `test_validate_returns_true` — canonical + shim validate check
2. `test_async_run_success` — `async with ProcessTransaction() as tx: rc, out, err = await tx.run([sys.executable, "-c", "print('hi')"]); assert rc == 0; assert "hi" in out`
3. `test_async_run_rollback_on_exception` — raises inside `async with`; any running procs terminated
4. `test_async_run_timeout` — long-running cmd with short timeout → `asyncio.TimeoutError` or equivalent
5. `test_shim_importable` — `from src.core.ProcessTransactionManager import ProcessTransaction, validate`

**Acceptance:** All tests pass.

---

### T13 — `tests/test_ContextTransactionManager.py`

**File:** `tests/test_ContextTransactionManager.py` (CREATE — written by @5test)
**Required tests (minimum):**
1. `test_validate_returns_true` — canonical + shim validate check
2. `test_transaction_id_is_uuid` — `ContextTransaction("t").transaction_id` is `uuid.UUID`
3. `test_parent_id_set_from_stack` — nested context: inner `parent_id == outer.transaction_id`
4. `test_current_classmethod` — `ContextTransaction.current()` returns innermost inside `with`; `None` outside
5. `test_shim_imports_recursion_guard` — `from src.core.ContextTransactionManager import RecursionGuardError; assert issubclass(RecursionGuardError, RuntimeError)`

**Acceptance:** All tests pass.

---

### T14 — Full Validation Run

No code changes; @7exec runs all validation commands and confirms:
- 14 tests in `test_transaction_managers.py` pass
- All new acceptance tests pass
- All shim smoke-test imports succeed
- `test_core_quality.py` passes

---

## Dependency Order

```
T00 (requirements.txt)
  └─ T02 (BaseTransaction)               [no transitive deps]
  └─ T03 (StorageTransaction impl)       [needs cryptography, BaseTransaction exists]
  └─ T04 (ProcessTransaction impl)       [no crypto dep]
  └─ T05 (ContextTransaction impl)       [no crypto dep]
  └─ T06 (MemoryTransaction impl)        [needs httpx + cryptography]
  └─ T01 (transactions/__init__.py)      [needs T02–T06 complete]
       └─ T07 (core shim Storage)        [needs T01 or T03]
       └─ T08 (core shim Process)        [needs T01 or T04]
       └─ T09 (core shim Context)        [needs T01 or T05]
       └─ T10 (root shim Memory)         [needs T01 or T06]
            └─ T11–T13 (@5test writes)  [needs T07–T10 importable]
                 └─ T14 (full run)       [all above done]
```

**Minimum path to unblock `test_transaction_managers.py` (14 tests):**
`T03 → T04 → T05 → T07 → T08 → T09` (shims importable → tests collect → tests pass)

---

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M0 | Pre-conditions met | T00 | DONE |
| M1 | Base ABC + package skeleton | T01, T02 | DONE |
| M2 | All four managers implemented | T03, T04, T05, T06 | DONE |
| M3 | Shims in place — 14 existing tests pass | T07, T08, T09, T10 | DONE |
| M4 | New acceptance tests written by @5test | T11, T12, T13 | DONE |
| M5 | Full validation passes | T14 | DONE |

---

## Validation Commands

@7exec will run these **in order**, on branch `prj0000045-transaction-managers-full`:

```powershell
# 1. Confirm cryptography declared
Select-String -Path requirements.txt -Pattern "cryptography"

# 2. Confirm shim imports
& c:\Dev\PyAgent\.venv\Scripts\python.exe -c "from src.core.StorageTransactionManager import StorageTransaction; from src.core.ProcessTransactionManager import ProcessTransaction; from src.core.ContextTransactionManager import ContextTransaction, RecursionGuardError; print('shims OK')"

# 3. Confirm root shim
& c:\Dev\PyAgent\.venv\Scripts\python.exe -c "from src.MemoryTransactionManager import MemoryTransaction; print('root shim OK')"

# 4. Confirm canonical package
& c:\Dev\PyAgent\.venv\Scripts\python.exe -c "from src.transactions import StorageTransaction, ProcessTransaction, ContextTransaction, MemoryTransaction; print('OK')"

# 5. Run the 14 existing tests
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest tests/test_transaction_managers.py -v

# 6. Run new acceptance tests
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest tests/test_StorageTransactionManager.py tests/test_ProcessTransactionManager.py tests/test_ContextTransactionManager.py -v

# 7. Run quality check (validate() scan)
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest tests/test_core_quality.py -v

# 8. Full test suite
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1; python -m pytest -q
```
| M4 | Tests pass | T11–T14 | |

## Validation Commands
```powershell
# Acceptance criteria
python -c "from src.transactions import StorageTransaction, ProcessTransaction, ContextTransaction, MemoryTransaction"
python -c "from src.core.StorageTransactionManager import StorageTransaction"
python -c "from src.MemoryTransactionManager import MemoryTransaction"
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest tests/test_transaction_managers.py -v
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest tests/test_StorageTransactionManager.py tests/test_ProcessTransactionManager.py tests/test_ContextTransactionManager.py -v
c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q
```
