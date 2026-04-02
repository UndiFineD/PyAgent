# prj0000082 — agent-execution-sandbox — Design

_Status: IN_PROGRESS_
_Designer: @3design | Updated: 2026-03-26_

## Selected Option

**Option A — `SandboxedStorageTransaction` subclass + `SandboxMixin`**

Subclass `StorageTransaction` to intercept `write()`, `delete()`, `mkdir()`, and `commit()`
with symlink-resolved path allowlist checks before any op reaches the operation queue.
Exposes via `SandboxMixin.sandbox_tx()` factory.  Reuses the `_is_subpath()` / `validate_path()`
pattern already proven in `McpSandbox`.  Touches zero existing files — only new files are added.

**Rationale:** Options B (monkey-patch), C (OS-level), D (decorator), and E (`__init_subclass__`)
were all considered and rejected (see `think.md`).  Option A is the only choice that is:
Budget-S compatible (~120 LOC), zero-regression (new files only), type-annotation friendly,
and directly reuses existing path-validation prior art.

---

## Module Layout

```
src/core/sandbox/
    __init__.py                          — public exports
    SandboxConfig.py                     — SandboxConfig dataclass
    SandboxViolationError.py             — standalone exception (no src.mcp dependency)
    SandboxMixin.py                      — mixin: sandbox_tx() factory + _validate_host()
    SandboxedStorageTransaction.py       — StorageTransaction subclass with path guards
```

> **Deviation from `think.md`:** The think.md draft placed `SandboxMixin` in
> `src/core/base/mixins/` (a new directory).  This design consolidates all five sandbox
> modules into `src/core/sandbox/` to keep the feature self-contained, reduce the number
> of new directories to one, and mirror the `src/mcp/` module boundary convention.
> `src/core/base/mixins/` is deferred to a future prj that introduces multiple mixins.

---

## Interface Definitions

### `SandboxConfig`

```python
# src/core/sandbox/SandboxConfig.py
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SandboxConfig:
    """Immutable policy envelope passed to SandboxedStorageTransaction and SandboxMixin.

    Attributes:
        allowed_paths:   Allowlist of root directories; resolved at validation time.
        allowed_hosts:   Allowlist of exact-match hostnames / IP strings.
        allow_all_hosts: When True, _validate_host() is a no-op (bypass for trusted agents).
        agent_id:        UUID string identifying the agent instance owning this config.
    """

    allowed_paths: list[Path]
    allowed_hosts: list[str]
    allow_all_hosts: bool = False
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_strings(
        cls,
        paths: list[str],
        hosts: list[str],
        allow_all_hosts: bool = False,
        agent_id: str | None = None,
    ) -> "SandboxConfig":
        """Convenience constructor that converts string paths to pathlib.Path objects.

        Args:
            paths:           List of filesystem path strings for the allowlist.
            hosts:           List of exact-match hostname strings for the allowlist.
            allow_all_hosts: Pass True to skip host validation entirely.
            agent_id:        Optional UUID string; auto-generated when omitted.

        Returns:
            A fully constructed SandboxConfig instance.
        """
        return cls(
            allowed_paths=[Path(p) for p in paths],
            allowed_hosts=list(hosts),
            allow_all_hosts=allow_all_hosts,
            agent_id=agent_id or str(uuid.uuid4()),
        )
```

### `SandboxViolationError`

```python
# src/core/sandbox/SandboxViolationError.py
from __future__ import annotations


class SandboxViolationError(RuntimeError):
    """Raised when a sandboxed operation targets a forbidden path or host.

    Standalone RuntimeError subclass — deliberately avoids importing from
    src.mcp so that src.core.sandbox has no upward dependency on src.mcp.

    Attributes:
        resource: The forbidden path or hostname string.
        reason:   Human-readable explanation of the violation.
    """

    def __init__(self, resource: str, reason: str) -> None:
        super().__init__(f"Sandbox violation [{resource}]: {reason}")
        self.resource = resource
        self.reason = reason
```

### `SandboxedStorageTransaction`

```python
# src/core/sandbox/SandboxedStorageTransaction.py
from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxViolationError import SandboxViolationError
from src.transactions.StorageTransactionManager import StorageTransaction


def _is_subpath(child: Path, parent: Path) -> bool:
    """Return True if child is at or under parent (mirrors McpSandbox._is_subpath)."""
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


class SandboxedStorageTransaction(StorageTransaction):
    """StorageTransaction subclass that enforces an allowed-path policy.

    Overrides write(), delete(), mkdir(), and commit() to call _validate_path()
    before any operation is queued or executed.  Raises SandboxViolationError
    immediately, so the op is never appended to self._ops — rollback is implicit.
    """

    def __init__(self, sandbox: SandboxConfig, target: Optional[Path] = None) -> None:
        super().__init__(target)
        self._sandbox = sandbox

    def _validate_path(self, path: Path) -> None:
        """Resolve symlinks then verify path is under an allowed prefix.

        Args:
            path: The path to validate (may be relative or contain symlinks).

        Raises:
            SandboxViolationError: If the resolved path escapes every allowed prefix.
        """
        resolved = Path(path).resolve()
        if not any(
            _is_subpath(resolved, ap.resolve()) for ap in self._sandbox.allowed_paths
        ):
            raise SandboxViolationError(
                resource=str(resolved),
                reason=(
                    f"not under any allowed prefix: "
                    f"{[str(p) for p in self._sandbox.allowed_paths]!r}"
                ),
            )

    # ------------------------------------------------------------------
    # Multi-op async overrides
    # ------------------------------------------------------------------

    async def write(
        self, path: Path, content: bytes, *, user_id: Optional[str] = None
    ) -> None:
        """Validate path then delegate to super().write()."""
        self._validate_path(path)
        await super().write(path, content, user_id=user_id)

    async def delete(self, path: Path) -> None:
        """Validate path then delegate to super().delete()."""
        self._validate_path(path)
        await super().delete(path)

    async def mkdir(self, path: Path) -> None:
        """Validate path then delegate to super().mkdir()."""
        self._validate_path(path)
        await super().mkdir(path)

    # ------------------------------------------------------------------
    # Legacy single-file override
    # ------------------------------------------------------------------

    def commit(self) -> None:
        """Validate self._target before the atomic tmp-file write.

        Raises:
            SandboxViolationError: If self._target is set and escapes all allowed prefixes.
        """
        if self._target is not None:
            self._validate_path(self._target)
        super().commit()
```

### `SandboxMixin`

```python
# src/core/sandbox/SandboxMixin.py
from __future__ import annotations

from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxViolationError import SandboxViolationError
from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction


class SandboxMixin:
    """Mixin that exposes sandbox_tx() and _validate_host() on a BaseAgent subclass.

    The consuming class must provide a _sandbox_config attribute of type SandboxConfig.
    Follows the CortMixin convention: the mixin references self._sandbox_config;
    the concrete agent class initialises it (typically in __init__).

    Example usage:
        class MyAgent(BaseAgent, SandboxMixin):
            def __init__(self, ...):
                super().__init__(...)
                self._sandbox_config = SandboxConfig.from_strings(
                    paths=["/workspace/output"],
                    hosts=["api.example.com"],
                )
    """

    _sandbox_config: SandboxConfig  # provided by the concrete class

    def sandbox_tx(self, target=None) -> SandboxedStorageTransaction:
        """Factory: return a SandboxedStorageTransaction bound to this agent's config.

        Args:
            target: Optional Path for legacy single-file mode.

        Returns:
            A SandboxedStorageTransaction instance ready for use as a context manager.
        """
        return SandboxedStorageTransaction(self._sandbox_config, target=target)

    def _validate_host(self, host: str) -> None:
        """Validate a hostname against the sandbox allowlist.

        When allow_all_hosts is True the check is bypassed entirely (useful for
        trusted internal agents that must reach arbitrary endpoints).
        Performs simple exact-match comparison against allowed_hosts — no DNS
        resolution (Budget S; DNS canonicalisation deferred to a future prj).

        Args:
            host: Hostname or IP string to check.

        Raises:
            SandboxViolationError: If host is not in the allowlist and
                allow_all_hosts is False.
        """
        config = self._sandbox_config
        if config.allow_all_hosts:
            return
        if host not in config.allowed_hosts:
            raise SandboxViolationError(
                resource=host,
                reason=(
                    f"host not in allowed_hosts: {config.allowed_hosts!r}"
                ),
            )
```

### `__init__.py` (public exports)

```python
# src/core/sandbox/__init__.py
from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxMixin import SandboxMixin
from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction
from src.core.sandbox.SandboxViolationError import SandboxViolationError

__all__ = [
    "SandboxConfig",
    "SandboxMixin",
    "SandboxedStorageTransaction",
    "SandboxViolationError",
]
```

---

## Integration into BaseAgent

A concrete agent opts in by:

1. Adding `SandboxMixin` to its MRO alongside `BaseAgent`.
2. Initialising `self._sandbox_config` in `__init__`.
3. Replacing `StorageTransaction()` calls with `self.sandbox_tx()`.

```python
from src.agents.BaseAgent import BaseAgent
from src.core.sandbox import SandboxConfig, SandboxMixin


class CoderAgent(BaseAgent, SandboxMixin):

    def __init__(self, manifest, workspace_dir: str, **kwargs):
        super().__init__(manifest, **kwargs)
        self._sandbox_config = SandboxConfig.from_strings(
            paths=[workspace_dir],
            hosts=[],          # no outbound HTTP in this agent
        )

    async def run(self, task):
        async with self.sandbox_tx() as tx:
            await tx.write(task.output_path, task.content.encode())
            await tx.acommit()
```

Agents that do not compose `SandboxMixin` are completely unaffected — no changes to `BaseAgent`
or to any existing agent class.

---

## Validation / Symlink Handling

The `_validate_path()` algorithm:

1. `resolved = Path(path).resolve()` — follows all symlinks using the OS kernel's `realpath()`
   equivalent; every intermediate directory is resolved before the prefix check.
2. For each `ap` in `self._sandbox.allowed_paths`: compute `ap.resolve()` and test
   `resolved.relative_to(ap_resolved)`.  At least one must succeed.
3. If none match, raise `SandboxViolationError(resource=str(resolved), reason=...)`.

This means a symlink `/workspace/link → /etc/passwd` will be resolved to `/etc/passwd` before
the check, which will fail unless `/etc` is in `allowed_paths`.  The escape is caught.

`allowed_paths` are also resolved at check time (not pre-cached) so the allowlist remains
correct even when the workspace directory itself is a symlink.

---

## Error Contract

| Situation | Outcome |
|---|---|
| Path escapes every allowed prefix | `SandboxViolationError` raised immediately; op is never queued |
| Host not in allowlist (and `allow_all_hosts=False`) | `SandboxViolationError` raised by `_validate_host()` |
| `allow_all_hosts=True` | `_validate_host()` is a no-op; path checks still apply |
| `StorageTransaction` base class error (e.g. I/O failure) | Propagated unchanged after sandbox check passes |
| `commit()` called twice | `CommitError` from base class (unaffected by sandbox) |

`SandboxViolationError` carries:
- `resource` — the offending path/host string (resolved form for paths).
- `reason` — the human-readable explanation including the allowlist.
- `str(error)` — `"Sandbox violation [<resource>]: <reason>"`.

The error is raised synchronously (before any `await`), so callers can catch it without
needing `try/except` inside a coroutine.  It should be **logged at WARNING** by the agent
and re-raised or converted to a task failure result — not swallowed.

---

## Test Strategy (for @5test)

### Unit tests

| Test | Description |
|---|---|
| `SandboxConfig.from_strings()` | Converts strings to `Path`; propagates `agent_id`; auto-generates UUID |
| `_validate_path()` — in-scope | Path inside `allowed_paths` passes without error |
| `_validate_path()` — out-of-scope | Path outside all prefixes raises `SandboxViolationError` |
| `_validate_path()` — symlink escape | Symlink pointing outside allowed root is rejected |
| `_validate_path()` — exact boundary | `allowed_paths[0]` itself is a valid target |
| `SandboxViolationError` attributes | `resource` and `reason` fields are set; `str()` format matches |
| `_validate_host()` — allowed | Exact-match host passes |
| `_validate_host()` — forbidden | Unknown host raises `SandboxViolationError` |
| `_validate_host()` — allow_all_hosts | Any host passes when flag is True; path checks still run |

### Integration tests

| Test | Description |
|---|---|
| `sandbox_tx()` write inside allowed path | `await tx.write(allowed_path, b"x")` succeeds; `acommit()` writes file |
| `sandbox_tx()` write outside allowed path | `await tx.write(outside_path, b"x")` raises before queueing op |
| `sandbox_tx()` delete outside allowed path | `await tx.delete(outside_path)` raises |
| `sandbox_tx()` mkdir outside allowed path | `await tx.mkdir(outside_path)` raises |
| Legacy `commit()` with forbidden target | `SandboxedStorageTransaction(config, target=forbidden)` → `commit()` raises |
| Agent with `SandboxMixin` end-to-end | Concrete agent writes to allowed dir; operation succeeds |

### Negative / escape tests

| Test | Description |
|---|---|
| Symlink traversal | Create symlink in allowed dir pointing outside; write via symlink raises |
| Path traversal string | `allowed_root + "/../etc/passwd"` resolves out of scope; raises |
| Empty `allowed_paths` | Every path is rejected (no whitelist entry can match) |

---

## Open Questions Resolved

| # | Question | Resolution |
|---|---|---|
| 1 | `allowed_paths: list[str]` vs `list[Path]` | `list[Path]` with `from_strings()` classmethod for string callers |
| 2 | `SandboxViolationError` hierarchy | Standalone `SandboxViolationError(RuntimeError)` — no `src.mcp` import in `src.core.sandbox` |
| 3 | Legacy `commit()` validation scope | Included — `self._target` is validated before the atomic write |
| 4 | Host wildcard API | `allow_all_hosts: bool` flag (explicit; avoids `"*"` string sentinel confusion) |
| 5 | DNS resolution in `_validate_host()` | Simple exact-match only for Budget S; DNS canonicalisation deferred |

---

## Non-Goals (Budget S)

- Network-level firewalling (kernel `seccomp`, iptables, or Windows Filtering Platform).
- Rust FFI acceleration (no hot path requiring native performance at this scale).
- Integration with `ProcessTransaction` or `ContextTransaction` (future prj).
- DNS-based host canonicalisation in `_validate_host()`.
- Automatic injection of `SandboxMixin` into existing agents (opt-in only).
- Enforcement of raw `open()` / `pathlib.write_bytes()` calls that bypass `StorageTransaction`.

---

## Architecture

```
src/core/sandbox/
    __init__.py ─────────────────── re-exports all public symbols
    SandboxConfig.py ────────────── @dataclass, from_strings() classmethod
    SandboxViolationError.py ────── RuntimeError subclass; carries resource + reason
    SandboxedStorageTransaction.py ─ subclasses StorageTransaction; adds _validate_path()
    SandboxMixin.py ─────────────── mixin for BaseAgent subclasses; sandbox_tx() factory

src/transactions/StorageTransactionManager.py  (UNCHANGED)
    StorageTransaction ──────────── base class (write/delete/mkdir/commit/acommit)

src/mcp/McpSandbox.py  (UNCHANGED — read-only reference)
    _is_subpath() ───────────────── copied (not imported) into SandboxedStorageTransaction

tests/core/sandbox/
    test_SandboxConfig.py
    test_SandboxViolationError.py
    test_SandboxedStorageTransaction.py
    test_SandboxMixin.py
```

Dependency arrows (all new, no existing module modified):

```
SandboxedStorageTransaction  →  StorageTransactionManager
SandboxedStorageTransaction  →  SandboxConfig
SandboxedStorageTransaction  →  SandboxViolationError
SandboxMixin                 →  SandboxedStorageTransaction
SandboxMixin                 →  SandboxConfig
SandboxMixin                 →  SandboxViolationError
__init__                     →  all four above
```

No existing module in `src/` is modified.

---

## Non-Functional Requirements

- **Performance:** `_validate_path()` calls `Path.resolve()` (one `os.stat` chain per component).
  For Budget S workloads (<10 ops/sec per agent) this is negligible. Hot-path caching deferred.
- **Security:** Symlink-resolved check prevents `../` escape sequences and symlink traversal.
  Documented limitation: raw `open()` calls bypass enforcement.
- **Testability:** All classes are pure Python with no global state, fully unit-testable without
  filesystem setup except for symlink tests (which use `tmp_path` pytest fixture).

---

## Key Inputs for @4plan

1. Create `src/core/sandbox/__init__.py` with public exports.
2. Create `src/core/sandbox/SandboxConfig.py` — `@dataclass` with `from_strings()`.
3. Create `src/core/sandbox/SandboxViolationError.py` — `RuntimeError` subclass.
4. Create `src/core/sandbox/SandboxedStorageTransaction.py` — subclass of `StorageTransaction`;
   copy `_is_subpath()` locally (do not import from `src.mcp`).
5. Create `src/core/sandbox/SandboxMixin.py` — accesses `self._sandbox_config`.
6. Create `tests/core/sandbox/` with unit + integration + negative tests as specified above.
7. `write()` content parameter is `bytes` (matches actual `StorageTransaction.write` signature —
   the design doc template used `str`; `bytes` is correct).
8. All new `.py` files must carry the standard Apache 2.0 header per project conventions.

_Status: DONE_
