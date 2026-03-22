# transaction-managers-full — Design

_Status: IN_PROGRESS_
_Designer: @3design | Updated: 2026-03-22_

> ⚠️ **Branch Gate Warning**
> Expected branch: `prj0000045-transaction-managers-full`
> Observed branch: `main`
> This design doc was authored on `main`. Per branch governance rules, @9git must
> refuse to stage, commit, push, or open a PR unless the working branch is
> `prj0000045-transaction-managers-full`. Create/switch to that branch before
> any commits that touch the scope files (see project.md § Branch Plan).

---

## Selected Option

**Option B — `src/transactions/` package** (binding decision from `docs/agents/2think.memory.md` §3.1)

Rationale: single canonical import surface, shared `BaseTransaction` ABC enforces
consistent `async with` contracts across all four managers, no circular-import risk,
PascalCase module names match project convention, and the path is clear for Rust FFI
acceleration (one location, one delegation point). Options A (single-file SRP
violation) and C (circular-import risk) were rejected.

---

## Architecture

### High-Level Layout

```
src/
├── transactions/                          NEW PACKAGE
│   ├── __init__.py                        re-exports all four public types + BaseTransaction
│   ├── BaseTransaction.py                 ABC: tid, __aenter__, __aexit__, commit, rollback
│   ├── MemoryTransactionManager.py        moved from src/MemoryTransactionManager.py + upgraded
│   ├── StorageTransactionManager.py       new: atomic multi-file ops + optional encryption
│   ├── ProcessTransactionManager.py       new: async subprocess + SIGTERM rollback
│   └── ContextTransactionManager.py       new: UUID lineage + contextvar stack + recursion guard
├── MemoryTransactionManager.py            SHIM → re-exports from src/transactions/
└── core/
    ├── StorageTransactionManager.py       SHIM → re-exports from src/transactions/   NEW
    ├── ProcessTransactionManager.py       SHIM → re-exports from src/transactions/   NEW
    └── ContextTransactionManager.py       SHIM → re-exports from src/transactions/   NEW

tests/
├── test_transaction_managers.py           EXISTING 14 tests — must keep passing
├── test_StorageTransactionManager.py      NEW acceptance tests
├── test_ProcessTransactionManager.py      NEW acceptance tests
└── test_ContextTransactionManager.py      NEW acceptance tests
```

### Dependency Graph

```
BaseTransaction (ABC)
    ↑ inherits
    ├── MemoryTransaction
    ├── StorageTransaction
    ├── ProcessTransaction
    └── ContextTransaction

src/transactions/__init__.py
    → re-exports all five symbols

src/MemoryTransactionManager.py (SHIM)
    → from src.transactions.MemoryTransactionManager import MemoryTransaction

src/core/StorageTransactionManager.py (SHIM)
    → from src.transactions.StorageTransactionManager import StorageTransaction, validate

src/core/ProcessTransactionManager.py (SHIM)
    → from src.transactions.ProcessTransactionManager import ProcessTransaction, validate

src/core/ContextTransactionManager.py (SHIM)
    → from src.transactions.ContextTransactionManager import (
          ContextTransaction, RecursionGuardError, validate
      )
```

---

## Dual-API Compatibility Strategy

The 14 existing tests in `tests/test_transaction_managers.py` use a **single-file SYNC API**:

| Manager | Existing sync API (tests must keep passing) |
|---|---|
| `StorageTransaction` | `StorageTransaction(path)`, `.stage(bytes)`, `.commit()`, sync/async `with` |
| `ProcessTransaction` | `ProcessTransaction(cmd)`, `.start()`, `.wait()`, `.start_async()`, `.wait_async(timeout)`, `._proc`, auto rollback on exception |
| `ContextTransaction` | `ContextTransaction(context_id: str)`, `.active_contexts()`, `RecursionGuardError`, sync/async `with`, recursion guard |

The new `@2think` binding contracts add a **multi-op ASYNC API**:

| Manager | New async API (new tests and swarm callers) |
|---|---|
| `StorageTransaction` | `async write(path, content)`, `async delete(path)`, `async mkdir(path)`, `async commit()`, `async rollback()` |
| `ProcessTransaction` | `async run(cmd, cwd, timeout)` → `(rc, stdout, stderr)`, `async commit()`, `async rollback()` |
| `ContextTransaction` | `transaction_id: UUID`, `parent_id: UUID|None`, `current()` classmethod, `async commit()`, `async rollback()` |

### Coexistence Strategy: Single Class, Two Initializers

Both APIs live in the **same class**. The constructor accepts both forms via overloaded
behaviour:

#### `StorageTransaction` — Constructor modes

```
Mode A (legacy single-file):  StorageTransaction(target: Path)
Mode B (new multi-op):        StorageTransaction()  [no arg or tid=<uuid>]
```

- When instantiated with a positional `Path`, the constructor sets `self._legacy_target`
  and enables the `.stage()` / `.commit()` sync path.
- When instantiated without arguments (or with only `tid=`), the full multi-op async
  API is active.
- Both modes share `__enter__`, `__exit__`, `__aenter__`, `__aexit__`.
- `commit()` is **synchronous** in legacy mode (called from sync `with`).
  `async commit()` runs via `asyncio.run()` if no event loop is detected, or native
  async if inside an event loop. A single `_commit_impl()` coroutine does the actual
  work; the sync `commit()` calls `asyncio.run()` when no running loop is present.

> NOTE: `commit()` sync bridge only needed for tests; internal swarm code must always
> use `async with`.

#### `ProcessTransaction` — Constructor modes

```
Mode A (legacy single-cmd):   ProcessTransaction(cmd: list[str])
Mode B (new multi-cmd):        ProcessTransaction()
```

- Legacy mode: `.start()` (sync `subprocess.Popen`), `.wait()` (sync), `.start_async()`
  (`asyncio.create_subprocess_exec`), `.wait_async(timeout)`, `._proc` attribute.
- New mode: `.run(cmd, cwd, timeout)` → `async tuple[int, str, str]`.
- Rollback in both modes sends SIGTERM then SIGKILL after a 3 s grace period.
- `.__exit__` triggers rollback on non-None `exc_type`.
- `._proc` attribute is preserved in both modes (last started subprocess).

#### `ContextTransaction` — Constructor modes

```
Mode A (legacy context_id):   ContextTransaction(context_id: str)
Mode B (new UUID lineage):     ContextTransaction(context_id: str, *, parent_id=None, tid=None)
```

- Both modes use the same class; `transaction_id` (UUID4) is always auto-assigned.
- `parent_id` defaults to the current contextvar stack head, enabling transparent
  lineage without callers changing their code.
- `active_contexts()` returns the set of active `context_id` strings — backward compat.
- `RecursionGuardError` is raised if the same `context_id` is entered while already
  active in the same thread/task.
- `current()` classmethod returns the innermost `ContextTransaction` from the
  contextvar stack — new swarm API.

---

## Interfaces & Contracts

### BaseTransaction (ABC)

```python
# src/transactions/BaseTransaction.py
from __future__ import annotations
import abc
from typing import Any, Optional

class BaseTransaction(abc.ABC):
    def __init__(self, tid: Optional[Any] = None) -> None:
        self.tid = tid

    async def __aenter__(self) -> "BaseTransaction":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        return False  # do not suppress exceptions

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...

def validate() -> bool:
    return True
```

### StorageTransaction

```python
# src/transactions/StorageTransactionManager.py
import asyncio, os, tempfile, uuid
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet

class StorageTransaction(BaseTransaction):
    """Atomic multi-file or single-file write transaction."""

    # ---- Initialiser (dual-mode) ----
    def __init__(
        self,
        target: Optional[Path] = None,   # legacy mode: single-file target
        *,
        tid: Optional[uuid.UUID] = None,
        user_id: Optional[str] = None,   # encryption key derivation (None = no encrypt)
    ) -> None: ...

    # ---- Legacy sync API (test_transaction_managers.py) ----
    def stage(self, content: bytes) -> None: ...
    def commit(self) -> None: ...          # sync bridge → _commit_impl()
    def rollback(self) -> None: ...

    def __enter__(self) -> "StorageTransaction": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

    # ---- New async multi-op API ----
    async def write(self, path: Path, content: str | bytes,
                    *, user_id: Optional[str] = None) -> None: ...
    async def delete(self, path: Path) -> None: ...
    async def mkdir(self, path: Path) -> None: ...
    async def commit(self) -> None: ...    # overloaded: async version
    async def rollback(self) -> None: ...

    # ---- Internal ----
    async def _commit_impl(self) -> None: ...
    def _encrypt(self, content: bytes, user_id: str) -> bytes: ...
    def _decrypt(self, content: bytes, user_id: str) -> bytes: ...

def validate() -> bool:
    return True
```

### ProcessTransaction

```python
# src/transactions/ProcessTransactionManager.py
import asyncio, subprocess, uuid
from pathlib import Path
from typing import Optional

class ProcessTransaction(BaseTransaction):
    """Subprocess guard with SIGTERM rollback."""

    # ---- Initialiser (dual-mode) ----
    def __init__(
        self,
        cmd: Optional[list[str]] = None,  # legacy mode: single command
        *,
        tid: Optional[uuid.UUID] = None,
    ) -> None:
        self._cmd = cmd
        self._proc: Optional[subprocess.Popen] = None   # legacy ._proc attribute
        self._async_proc = None                          # asyncio.Process
        self._procs: list = []                           # new multi-run registry

    # ---- Legacy sync API ----
    def start(self) -> None: ...
    def wait(self) -> int: ...
    def rollback(self) -> None: ...  # SIGTERM → SIGKILL after 3 s
    def __enter__(self) -> "ProcessTransaction": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

    # ---- Legacy async API ----
    async def start_async(self) -> None: ...
    async def wait_async(self, timeout: float = 30.0) -> int: ...
    async def __aenter__(self) -> "ProcessTransaction": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    # ---- New multi-op async API ----
    async def run(
        self,
        cmd: list[str],
        *,
        cwd: Optional[Path] = None,
        timeout: float = 30.0,
    ) -> tuple[int, str, str]: ...   # (returncode, stdout, stderr)
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

def validate() -> bool:
    return True
```

### ContextTransaction

```python
# src/transactions/ContextTransactionManager.py
import uuid
from contextvars import ContextVar
from typing import Optional, Set

_active_contexts: ContextVar[set] = ContextVar("_active_contexts", default=set())
_context_stack: ContextVar[list] = ContextVar("_context_stack", default=[])

class RecursionGuardError(RuntimeError):
    """Raised when the same context_id is entered recursively."""

class ContextTransaction(BaseTransaction):
    """UUID lineage tracking with recursion guard."""

    def __init__(
        self,
        context_id: str,
        *,
        parent_id: Optional[uuid.UUID] = None,
        tid: Optional[uuid.UUID] = None,
    ) -> None:
        if not context_id:
            raise ValueError("context_id must be a non-empty string")
        self.context_id = context_id
        self.transaction_id: uuid.UUID = tid or uuid.uuid4()
        # parent_id auto-set from stack head if not supplied
        stack = _context_stack.get([])
        self.parent_id: Optional[uuid.UUID] = parent_id or (
            stack[-1].transaction_id if stack else None
        )

    # ---- Sync context manager (legacy) ----
    def __enter__(self) -> "ContextTransaction": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

    # ---- Async context manager ----
    async def __aenter__(self) -> "ContextTransaction": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    # ---- Base async API ----
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

    # ---- Class-level accessors ----
    @classmethod
    def active_contexts(cls) -> Set[str]: ...    # legacy: set of context_id strings
    @classmethod
    def current(cls) -> Optional["ContextTransaction"]: ...  # new: innermost from stack

def validate() -> bool:
    return True
```

### MemoryTransaction (upgraded)

```python
# src/transactions/MemoryTransactionManager.py
import threading, uuid
from typing import Any, Optional

class MemoryTransaction(BaseTransaction):
    """In-memory key-value store with RLock + optional remote sync."""

    def __init__(self, tid: Optional[Any] = None) -> None:
        self.tid = tid
        self._store: dict = {}
        self._pending: dict = {}
        self._lock = threading.RLock()

    # ---- Backward-compat sync API (existing callers) ----
    def __enter__(self) -> "MemoryTransaction": ...
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...
    async def __aenter__(self) -> "MemoryTransaction": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    # ---- New async key-value API ----
    async def set(self, key: str, value: Any, *, encrypt: bool = False) -> None: ...
    async def get(self, key: str, *, decrypt: bool = False) -> Any: ...
    async def delete(self, key: str) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

    # ---- Remote sync ----
    async def sync_remote(
        self,
        endpoint: str,
        *,
        encrypted: bool = True,
        dry_run: bool = False,
    ) -> None: ...

def validate() -> bool:
    return True
```

---

## Encryption Approach (StorageTransaction)

### Library

**`cryptography` package** (PyPI: `cryptography`) — already a transitive dependency
through `src/core/base/logic/security/e2e_encryption_core.py`. Uses Fernet
(AES-128-CBC + HMAC-SHA256) for symmetric file encryption at rest. The Signal/X25519
layer in `docs/E2E_ENCRYPTION.md` applies to peer-to-peer messaging, not to
file-at-rest storage — these are separate encryption planes.

### Key Derivation

```
master_key  (env: PYAGENT_STORAGE_MASTER_KEY, 32 random bytes, base64-encoded)
    ↓  HKDF-SHA256(salt=user_id.encode(), info=b"storage-tx")
user_key    (32 bytes → Fernet key via base64.urlsafe_b64encode)
    ↓  Fernet.encrypt(plaintext)
ciphertext  (stored in tmp file, committed atomically)
```

- `user_id=None` → no encryption; plaintext written as-is. Tests use `user_id=None`
  by default — no key infrastructure required.
- `user_id` is a string (e.g., OAuth `sub` claim); actual master key sourced from env.
- If `PYAGENT_STORAGE_MASTER_KEY` is absent and encryption is requested, raises
  `EncryptionConfigError` at `write()` time (not at import time) — tests that don't
  set `user_id` are unaffected.
- `_encrypt()` and `_decrypt()` are internal helpers on `StorageTransaction`. They are
  unit-testable with a fixture that injects a dummy master key via `monkeypatch`.

### Test Pattern

```python
@pytest.fixture
def storage_key(monkeypatch):
    import base64, os
    monkeypatch.setenv(
        "PYAGENT_STORAGE_MASTER_KEY",
        base64.b64encode(os.urandom(32)).decode()
    )

async def test_encrypted_write(tmp_path, storage_key):
    async with StorageTransaction() as tx:
        await tx.write(tmp_path / "secret.bin", b"data", user_id="u1")
    assert (tmp_path / "secret.bin").read_bytes() != b"data"
```

---

## Remote Memory Sync (MemoryTransaction)

### Design

`sync_remote(endpoint, *, encrypted=True, dry_run=False)` sends the committed
in-memory store as a JSON payload to `endpoint` via `httpx.AsyncClient.post()`.

```
POST {endpoint}
Content-Type: application/json
Authorization: Bearer {PYAGENT_MEMORY_SYNC_TOKEN}

{
  "tid": "<uuid>",
  "encrypted": true,
  "payload": {"key": "<fernet-encrypted-base64>", ...}
}
```

- If `dry_run=True`: builds the request payload but does not send; returns the payload
  dict. Tests use `dry_run=True` — no live server required.
- If `endpoint` is `None` or empty string: `sync_remote()` is a no-op (do not raise).
- If `httpx` is unavailable: logs a warning and returns silently.
- Encryption uses the same Fernet per-user key as `StorageTransaction`. If
  `encrypted=True` and no key configured: raises `EncryptionConfigError`.
- Transport errors (network timeouts, 4xx/5xx) are logged at WARNING level and
  re-raised as `RemoteSyncError(endpoint, cause)` so callers can control retry strategy.

### Test Pattern

```python
async def test_sync_remote_dry_run():
    async with MemoryTransaction() as tx:
        await tx.set("foo", "bar")
        payload = await tx.sync_remote(
            "https://example.com/mem", encrypted=False, dry_run=True
        )
    assert payload["payload"]["foo"] == "bar"
```

---

## ContextTransaction → LLM Handoff Design

**OUT OF SCOPE** for prj0000045 per `transaction-managers-full.project.md`
("Out of scope: ContextWindow"). Documented here for @4plan to include as a
follow-on task in a separate project.

### Intent (for completeness)

- `ContextTransaction.commit()` checks `self._context_window` attribute.
- If set (a `ContextWindow` instance), it calls
  `await context_window.push("system", str(self.transaction_id))` to append a
  lineage breadcrumb.
- The LLM adapter call is a hook/stub; tests inject a `MockContextWindow` via DI.
- No live LLM invocation required for tests.

### Deferred Implementation

```python
class ContextTransaction(BaseTransaction):
    def attach_context_window(self, window: "ContextWindow") -> None:
        self._context_window = window

    async def commit(self) -> None:
        # ... pop from stack ...
        if getattr(self, "_context_window", None) is not None:
            await self._context_window.push(
                "system",
                f"[ctx-lineage] tid={self.transaction_id} parent={self.parent_id}"
            )
```

---

## Non-Functional Requirements

- **Performance:** `StorageTransaction.commit()` ≤ 50 ms for ≤ 1 MB payloads on local
  disk (tmp-write + `os.replace` is a single rename, O(1) on same filesystem).
  `ProcessTransaction.rollback()` sends SIGTERM within 100 ms of `__exit__` with
  exception. `ContextTransaction` contextvar reads/writes are O(1); no locking.
  `MemoryTransaction` uses `threading.RLock` for sync callers; async callers use a
  dedicated `asyncio.Lock` to avoid blocking the event loop.

- **Security:** Encryption key never logged or included in exceptions.
  `PYAGENT_STORAGE_MASTER_KEY` sourced from environment only. HKDF salt is
  `user_id.encode()` — treat as sensitive. SIGTERM on rollback prevents orphaned
  subprocesses. `RecursionGuardError` prevents context poisoning via re-entrant abuse.
  `sync_remote` payload is Fernet-encrypted on the wire; Bearer token from env
  `PYAGENT_MEMORY_SYNC_TOKEN`.

- **Testability:** All four managers expose a `validate() -> bool` top-level function
  (required by `tests/test_core_quality.py`). Encryption is opt-in (`user_id=None`
  skips it). `sync_remote` is testable via `dry_run=True` with no network dependency.
  ContextWindow LLM handoff testable via `MockContextWindow` stub. Shim import
  smoke-tests run in acceptance tests (no implementation logic in shims).

---

## Migration Path: Shims

The four `src/core/` shim files do not exist yet and must be created as new files.
Their content is 3–4 lines each:

```python
# src/core/StorageTransactionManager.py  (NEW FILE — shim only)
from src.transactions.StorageTransactionManager import StorageTransaction, validate  # noqa: F401
__all__ = ["StorageTransaction", "validate"]
```

```python
# src/core/ProcessTransactionManager.py  (NEW FILE — shim only)
from src.transactions.ProcessTransactionManager import ProcessTransaction, validate  # noqa: F401
__all__ = ["ProcessTransaction", "validate"]
```

```python
# src/core/ContextTransactionManager.py  (NEW FILE — shim only)
from src.transactions.ContextTransactionManager import (  # noqa: F401
    ContextTransaction, RecursionGuardError, validate
)
__all__ = ["ContextTransaction", "RecursionGuardError", "validate"]
```

```python
# src/MemoryTransactionManager.py  (EXISTING FILE — body replaced with shim)
from src.transactions.MemoryTransactionManager import MemoryTransaction, validate  # noqa: F401
__all__ = ["MemoryTransaction", "validate"]
```

The existing tests import from `src.core.{Storage,Process,Context}TransactionManager`
and those shim files do **not** yet exist. Creating the shims is a Day-1 task for
@6code (before any implementation work begins).

---

## What Files Change / What Files Are New

### New files

| File | Purpose |
|---|---|
| `src/transactions/__init__.py` | Package re-export |
| `src/transactions/BaseTransaction.py` | ABC |
| `src/transactions/MemoryTransactionManager.py` | Upgraded MemoryTransaction |
| `src/transactions/StorageTransactionManager.py` | New StorageTransaction (dual-mode) |
| `src/transactions/ProcessTransactionManager.py` | New ProcessTransaction (dual-mode) |
| `src/transactions/ContextTransactionManager.py` | New ContextTransaction (dual-mode) |
| `src/core/StorageTransactionManager.py` | Shim (3 lines) |
| `src/core/ProcessTransactionManager.py` | Shim (3 lines) |
| `src/core/ContextTransactionManager.py` | Shim (3 lines) |
| `tests/test_StorageTransactionManager.py` | Acceptance tests |
| `tests/test_ProcessTransactionManager.py` | Acceptance tests |
| `tests/test_ContextTransactionManager.py` | Acceptance tests |

### Modified files

| File | Change |
|---|---|
| `src/MemoryTransactionManager.py` | Replace body with 3-line shim |

### Unchanged files

| File | Reason |
|---|---|
| `tests/test_transaction_managers.py` | 14 legacy tests must keep passing — no touches |
| `src/core/UnifiedTransactionManager.py` | Out of scope for this project |

---

## Open Questions for @4plan

1. **Sync commit bridge**: `StorageTransaction.commit()` (sync) must work in legacy
   tests that don't use `asyncio.run()`. Recommended impl:
   ```python
   def commit(self) -> None:
       try:
           asyncio.get_running_loop()
           raise RuntimeError("commit() called from async; use 'await tx.commit()'")
       except RuntimeError:
           asyncio.run(self._commit_impl())
   ```
   `pytest-asyncio`'s `asyncio_mode = auto` setting means test functions ARE inside an
   event loop. @4plan must verify: the legacy sync tests are `def test_*()` (not async),
   so `asyncio.get_running_loop()` raises `RuntimeError` → `asyncio.run()` path is safe.

2. **ProcessTransaction._proc compatibility**: Legacy tests assert `tx._proc is not None`
   and `tx._proc.poll() is not None`. The new async API uses `asyncio.subprocess.Process`
   which has no `.poll()`. The implementation must keep `_proc` pointing at a
   `subprocess.Popen` object when instantiated in legacy mode (sync `.start()`). The
   `start_async()` method sets `_async_proc` separately.

3. **`validate()` placement**: `tests/test_core_quality.py` scans `src/core/` for
   `validate()`. The shim files in `src/core/` must re-export `validate()` explicitly
   (included in the shim designs above). @4plan should add an acceptance test that
   imports each shim and calls `validate()`.

4. **Dual asyncio.Lock in MemoryTransaction**: The current `threading.RLock` blocks the
   event loop if called from async context. The upgrade should add `asyncio.Lock` for
   the new async API while keeping `threading.RLock` for the legacy sync `with`.
   @4plan should specify this dual-lock design explicitly in the task for @6code.

5. **`httpx` version pinning for sync_remote**: `requirements.txt` lists `httpx` but
   the version should be pinned to ≥ 0.27.0 for `AsyncClient` stability. @4plan should
   verify and update the pin.

---

_Status: DONE_
_Designer: @3design | Updated: 2026-03-22_
