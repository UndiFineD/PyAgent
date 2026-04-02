# prj0000082 — agent-execution-sandbox — Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-26_

---

## Overview

Implement a sandboxed path-enforcement layer for PyAgent storage operations.  The feature
adds five new Python modules under `src/core/sandbox/` and one test file at
`tests/core/sandbox/test_sandbox.py`.  Zero existing source files are modified.

`SandboxedStorageTransaction` subclasses `StorageTransaction` and intercepts `write()`,
`delete()`, `mkdir()`, and `commit()` with symlink-resolved allowlist checks before any
operation is queued.  `SandboxMixin` exposes a `sandbox_tx()` factory and a `_validate_host()`
method for `BaseAgent` subclasses that opt in by adding `SandboxMixin` to their MRO.

**Budget:** ~120 LOC implementation · 19 test cases · single sprint.

---

## Sprint Overview

| Metric | Value |
|---|---|
| New production files | 5 |
| New test files | 1 |
| Total test cases | 19 |
| Target module | `src/core/sandbox/` |
| Base class | `src.transactions.StorageTransactionManager.StorageTransaction` |
| Regression baseline | 129 structure tests (must remain green) |

---

## Implementation Order (TDD — tests first)

### Phase 1 — Test stubs (failing — red phase)

**File:** `tests/core/sandbox/test_sandbox.py`

Write all 19 test functions as stubs that `import` the not-yet-existing modules and
`pytest.fail("not implemented")`.  Each stub pins the exact assertion contract used in
Phase 2–5 so that green completion is unambiguous.

**Test list (complete — all 19):**

Unit tests (9):
- `test_sandbox_config_from_strings_valid`
- `test_sandbox_config_from_strings_auto_uuid`
- `test_validate_path_in_scope_passes`
- `test_validate_path_out_of_scope_raises`
- `test_validate_path_exact_boundary_passes`
- `test_sandbox_violation_error_attributes`
- `test_validate_host_allowed_passes`
- `test_validate_host_forbidden_raises`
- `test_validate_host_allow_all_hosts_bypasses`

Integration tests (7):
- `test_sandbox_tx_write_inside_allowed_path`
- `test_sandbox_tx_write_outside_allowed_path_raises`
- `test_sandbox_tx_delete_outside_allowed_path_raises`
- `test_sandbox_tx_mkdir_outside_allowed_path_raises`
- `test_sandbox_tx_commit_legacy_forbidden_target_raises`
- `test_sandbox_mixin_agent_writes_to_allowed_dir`
- `test_sandbox_tx_write_op_not_queued_on_violation`

Negative / escape tests (3):
- `test_validate_path_symlink_escape_raises`
- `test_validate_path_traversal_string_raises`
- `test_sandbox_config_empty_allowed_paths_rejects_all`

**Acceptance:** `pytest tests/core/sandbox/test_sandbox.py` collects 19 tests, all FAIL with
`ImportError` or explicit `pytest.fail` — red phase confirmed.

---

### Phase 2 — `SandboxViolationError`

**File:** `src/core/sandbox/SandboxViolationError.py`

| Item | Detail |
|---|---|
| Base class | `RuntimeError` |
| `__init__` signature | `(self, resource: str, reason: str) -> None` |
| `super().__init__` message | `f"Sandbox violation [{resource}]: {reason}"` |
| Instance attributes | `self.resource: str`, `self.reason: str` |
| Dependencies | None — standalone (deliberately no `src.mcp` import) |

**Turns green:** `test_sandbox_violation_error_attributes`

---

### Phase 3 — `SandboxConfig`

**File:** `src/core/sandbox/SandboxConfig.py`

| Item | Detail |
|---|---|
| Decorator | `@dataclass` |
| `allowed_paths` | `list[Path]` — allowlist of allowed root directories |
| `allowed_hosts` | `list[str]` — allowlist of exact-match hostnames / IPs |
| `allow_all_hosts` | `bool = False` — bypass flag for `_validate_host()` |
| `agent_id` | `str = field(default_factory=lambda: str(uuid.uuid4()))` |
| `from_strings()` classmethod | `(paths: list[str], hosts: list[str], *, allow_all_hosts: bool = False, agent_id: str \| None = None) -> SandboxConfig` |
| `from_strings()` behaviour | Converts each path string to `Path`; copies hosts list; auto-generates UUID when `agent_id` is `None` |

**Turns green:** `test_sandbox_config_from_strings_valid`, `test_sandbox_config_from_strings_auto_uuid`

---

### Phase 4 — `SandboxedStorageTransaction`

**File:** `src/core/sandbox/SandboxedStorageTransaction.py`

**Imports (no external deps beyond stdlib + existing project modules):**
```python
from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxViolationError import SandboxViolationError
from src.transactions.StorageTransactionManager import StorageTransaction
```

**Module-level helper (copied locally — do NOT import from `src.mcp`):**
```python
def _is_subpath(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False
```

**Class:** `SandboxedStorageTransaction(StorageTransaction)`

| Method | Signature | Behaviour |
|---|---|---|
| `__init__` | `(self, sandbox: SandboxConfig, target: Optional[Path] = None)` | Calls `super().__init__(target)`; stores `self._sandbox = sandbox` |
| `_validate_path` | `(self, path: Path) -> None` | `resolved = Path(path).resolve()`; raises `SandboxViolationError` if no `ap.resolve()` covers it |
| `write` | `async (self, path: Path, content: bytes, *, user_id: Optional[str] = None) -> None` | `_validate_path(path)` then `await super().write(path, content, user_id=user_id)` |
| `delete` | `async (self, path: Path) -> None` | `_validate_path(path)` then `await super().delete(path)` |
| `mkdir` | `async (self, path: Path) -> None` | `_validate_path(path)` then `await super().mkdir(path)` |
| `commit` | `(self) -> None` | Validates `self._target` if set, then `super().commit()` |

**Key invariant:** `_validate_path` raises *before* any `await`, so a violation never appends
to `self._ops` — rollback is implicit (queue stays empty).

**Turns green:** `test_validate_path_in_scope_passes`, `test_validate_path_out_of_scope_raises`,
`test_validate_path_exact_boundary_passes`, `test_validate_path_symlink_escape_raises`,
`test_validate_path_traversal_string_raises`, `test_sandbox_config_empty_allowed_paths_rejects_all`,
`test_sandbox_tx_write_inside_allowed_path`, `test_sandbox_tx_write_outside_allowed_path_raises`,
`test_sandbox_tx_delete_outside_allowed_path_raises`, `test_sandbox_tx_mkdir_outside_allowed_path_raises`,
`test_sandbox_tx_commit_legacy_forbidden_target_raises`, `test_sandbox_tx_write_op_not_queued_on_violation`

---

### Phase 5 — `SandboxMixin`

**File:** `src/core/sandbox/SandboxMixin.py`

| Item | Detail |
|---|---|
| Class | `SandboxMixin` (no base class — plain mixin) |
| Class-level annotation | `_sandbox_config: SandboxConfig` — provided by the concrete agent `__init__` |
| `sandbox_tx` | `(self, target=None) -> SandboxedStorageTransaction` — returns `SandboxedStorageTransaction(self._sandbox_config, target=target)` |
| `_validate_host` | `(self, host: str) -> None` — exact-match check; no-op when `allow_all_hosts=True` |

`_validate_host` algorithm:
1. If `self._sandbox_config.allow_all_hosts` → return immediately.
2. If `host not in self._sandbox_config.allowed_hosts` → raise `SandboxViolationError(resource=host, reason=...)`.

**Turns green:** `test_validate_host_allowed_passes`, `test_validate_host_forbidden_raises`,
`test_validate_host_allow_all_hosts_bypasses`, `test_sandbox_mixin_agent_writes_to_allowed_dir`

---

### Phase 6 — `__init__.py`

**File:** `src/core/sandbox/__init__.py`

Public re-exports only:
```python
from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxMixin import SandboxMixin
from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction
from src.core.sandbox.SandboxViolationError import SandboxViolationError

__all__ = ["SandboxConfig", "SandboxMixin", "SandboxedStorageTransaction", "SandboxViolationError"]
```

---

## Test File Specification

**File:** `tests/core/sandbox/test_sandbox.py`

Every test must carry the project's standard Apache 2.0 header and use `pytest` + `tmp_path`
fixture for filesystem operations.  Async integration tests use `pytest.mark.asyncio`.

### Unit tests

| # | Test name | Exercises | Key assertion |
|---|---|---|---|
| U1 | `test_sandbox_config_from_strings_valid` | `SandboxConfig.from_strings()` path conversion + explicit `agent_id` | `config.allowed_paths == [Path("/tmp/a")]`; `config.agent_id == "my-id"` |
| U2 | `test_sandbox_config_from_strings_auto_uuid` | Auto-generated `agent_id` | `uuid.UUID(config.agent_id)` parses without error; field is non-empty |
| U3 | `test_validate_path_in_scope_passes` | `_validate_path()` on a path inside `allowed_paths` | No exception raised |
| U4 | `test_validate_path_out_of_scope_raises` | `_validate_path()` on a path outside all `allowed_paths` | Raises `SandboxViolationError`; `err.resource` contains the resolved path string |
| U5 | `test_validate_path_exact_boundary_passes` | `_validate_path()` where `path == allowed_paths[0]` | No exception raised |
| U6 | `test_sandbox_violation_error_attributes` | `SandboxViolationError` construction | `err.resource == "/bad/path"`; `err.reason == "test reason"`; `"Sandbox violation [/bad/path]"` in `str(err)` |
| U7 | `test_validate_host_allowed_passes` | `SandboxMixin._validate_host()` with whitelisted host | No exception raised |
| U8 | `test_validate_host_forbidden_raises` | `SandboxMixin._validate_host()` with unlisted host | Raises `SandboxViolationError`; `err.resource == "evil.com"` |
| U9 | `test_validate_host_allow_all_hosts_bypasses` | `allow_all_hosts=True` short-circuits `_validate_host()` | No exception raised for any host value |

### Integration tests

| # | Test name | Exercises | Key assertion |
|---|---|---|---|
| I1 | `test_sandbox_tx_write_inside_allowed_path` | Full write + `acommit()` to allowed dir | File exists on disk and contains `b"hello"` after `acommit()` |
| I2 | `test_sandbox_tx_write_outside_allowed_path_raises` | `write()` to path outside allowed dir | Raises `SandboxViolationError` before returning; `tx._ops` is empty |
| I3 | `test_sandbox_tx_delete_outside_allowed_path_raises` | `delete()` on path outside allowed dir | Raises `SandboxViolationError` |
| I4 | `test_sandbox_tx_mkdir_outside_allowed_path_raises` | `mkdir()` on path outside allowed dir | Raises `SandboxViolationError` |
| I5 | `test_sandbox_tx_commit_legacy_forbidden_target_raises` | Legacy `commit()` with `target` outside allowed dir | `SandboxViolationError` raised; no file written to disk |
| I6 | `test_sandbox_mixin_agent_writes_to_allowed_dir` | Minimal concrete class mixing `SandboxMixin`; calls `sandbox_tx().write()` + `acommit()` | File written successfully; no exception |
| I7 | `test_sandbox_tx_write_op_not_queued_on_violation` | Verify `_ops` stays empty after a failed `write()` | `len(tx._ops) == 0` after `SandboxViolationError` is raised |

### Negative / escape tests

| # | Test name | Exercises | Key assertion |
|---|---|---|---|
| N1 | `test_validate_path_symlink_escape_raises` | Symlink inside `allowed_paths[0]` pointing outside | `SandboxViolationError` raised (symlink is resolved first via `Path.resolve()`) |
| N2 | `test_validate_path_traversal_string_raises` | `allowed_root / "../etc/passwd"` style path | Resolved path escapes allowed dir → `SandboxViolationError` |
| N3 | `test_sandbox_config_empty_allowed_paths_rejects_all` | `SandboxConfig(allowed_paths=[], ...)` used in transaction | Any `write()` call raises `SandboxViolationError` |

---

## Task Checklist

- [ ] **T1** — Write `tests/core/sandbox/test_sandbox.py` (19 stubs, red phase)
        Files: `tests/core/sandbox/__init__.py`, `tests/core/sandbox/test_sandbox.py`
        Acceptance: 19 tests collected, all fail with `ImportError` or `pytest.fail`
- [ ] **T2** — Implement `src/core/sandbox/SandboxViolationError.py`
        Files: `src/core/sandbox/__init__.py` (dir init), `src/core/sandbox/SandboxViolationError.py`
        Acceptance: `test_sandbox_violation_error_attributes` passes
- [ ] **T3** — Implement `src/core/sandbox/SandboxConfig.py`
        Files: `src/core/sandbox/SandboxConfig.py`
        Acceptance: `test_sandbox_config_from_strings_valid`, `test_sandbox_config_from_strings_auto_uuid` pass
- [ ] **T4** — Implement `src/core/sandbox/SandboxedStorageTransaction.py`
        Files: `src/core/sandbox/SandboxedStorageTransaction.py`
        Acceptance: 12 tests covering path validation and async operations pass
- [ ] **T5** — Implement `src/core/sandbox/SandboxMixin.py`
        Files: `src/core/sandbox/SandboxMixin.py`
        Acceptance: `test_validate_host_*` (3) + `test_sandbox_mixin_agent_writes_to_allowed_dir` pass
- [ ] **T6** — Populate `src/core/sandbox/__init__.py` with public exports
        Files: `src/core/sandbox/__init__.py`
        Acceptance: `from src.core.sandbox import SandboxConfig, SandboxMixin, ...` works
- [ ] **T7** — Full validation run (all 19 green, 129 structure tests clean, mypy, ruff, coverage ≥ 90%)

---

## Dependency Order

```
T1 (test stubs)
    └── T2 (SandboxViolationError)
            └── T3 (SandboxConfig)
                    └── T4 (SandboxedStorageTransaction)   ← imports Config + Error
                            └── T5 (SandboxMixin)          ← imports all three
                                    └── T6 (__init__.py)
                                            └── T7 (validation)
```

Each task depends on the one above it; no parallelism within a sprint this size.

---

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Red phase complete | T1 | Not started |
| M2 | Error + config layer | T2, T3 | Not started |
| M3 | Transaction layer | T4 | Not started |
| M4 | Mixin + public API | T5, T6 | Not started |
| M5 | All green + quality gates | T7 | Not started |

---

## Acceptance Criteria

- [ ] All 19 tests in `tests/core/sandbox/test_sandbox.py` pass
- [ ] 129 structure tests pass (zero regressions)
- [ ] `mypy src/core/sandbox/ --strict` exits 0
- [ ] `ruff check src/core/sandbox/` exits 0
- [ ] Coverage ≥ 90% on `src/core/sandbox/`

---

## Design Notes / Adjustments

The following observations were made while reading the actual `StorageTransaction` source
(`src/transactions/StorageTransactionManager.py`) that confirm or refine the design:

1. **`write()` signature** — `async def write(self, path: Path, content: bytes, *, user_id: Optional[str] = None) -> None`.
   The design doc already corrected the `content: bytes` type.  The sandbox override must pass
   `user_id=user_id` through to `super().write()` to preserve optional per-user encryption.

2. **`acommit()` exists** — the multi-op flush method is `acommit()` (not `commit()`).
   Integration tests that test a full write+flush cycle must call `await tx.acommit()`.
   The sync `commit()` is the legacy single-file mode only.

3. **`__init__` parameter order** — `StorageTransaction.__init__(self, target: Optional[Path] = None)`.
   `SandboxedStorageTransaction.__init__` must call `super().__init__(target)`.

4. **Import path** — canonical location is `src.transactions.StorageTransactionManager.StorageTransaction`
   (a second copy exists at `src.core.StorageTransactionManager` but `src.transactions.*` is authoritative).

5. **`commit()` no-op guard** — `StorageTransaction.commit()` is already a no-op when `_staged is None`.
   The sandbox override only needs to call `_validate_path(self._target)` when `self._target is not None`;
   the base class handles the rest.

---

## Validation Commands

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1
python -m pytest tests/core/sandbox/test_sandbox.py -v --tb=short
python -m pytest tests/structure/ -q --tb=short
python -m mypy src/core/sandbox/ --strict
python -m ruff check src/core/sandbox/
python -m pytest tests/core/sandbox/test_sandbox.py --cov=src/core/sandbox --cov-report=term-missing
```

## Notes
<!-- @4plan will populate this file -->
