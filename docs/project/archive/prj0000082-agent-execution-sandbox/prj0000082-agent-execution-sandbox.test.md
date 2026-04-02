# prj0000082 — agent-execution-sandbox — Test Artifacts

_Status: HANDED_OFF_
_Tester: @5test | Updated: 2026-03-26_

---

## Test Plan

**Scope:** `src.core.sandbox` package — `SandboxConfig`, `SandboxViolationError`,
`SandboxedStorageTransaction`, `SandboxMixin`.

**Framework:** pytest 9.x · pytest-asyncio (strict mode) · tmp_path for filesystem isolation.

**File:** `tests/test_sandbox.py`

**Approach:** TDD red-phase — all 19 tests import from `src.core.sandbox` (not yet created).
The entire file fails collection with `ModuleNotFoundError: No module named 'src.core.sandbox'`.
This is the expected and confirmed failure mode.

**Mock strategy:** No mocking required.  Unit tests (U3–U5) test the sync `_validate_path()`
method which performs zero I/O.  Integration tests (I1–I7) use `tmp_path` for real filesystem
operations against `acommit()`.  No `AsyncMock` / `MagicMock` needed.

---

## Test Cases

| ID | Test Name | Type | File | Status |
|----|-----------|------|------|--------|
| U1 | `test_sandbox_config_from_strings_valid` | unit | tests/test_sandbox.py | RED |
| U2 | `test_sandbox_config_from_strings_auto_uuid` | unit | tests/test_sandbox.py | RED |
| U3 | `test_validate_path_in_scope_passes` | unit | tests/test_sandbox.py | RED |
| U4 | `test_validate_path_out_of_scope_raises` | unit | tests/test_sandbox.py | RED |
| U5 | `test_validate_path_exact_boundary_passes` | unit | tests/test_sandbox.py | RED |
| U6 | `test_sandbox_violation_error_attributes` | unit | tests/test_sandbox.py | RED |
| U7 | `test_validate_host_allowed_passes` | unit | tests/test_sandbox.py | RED |
| U8 | `test_validate_host_forbidden_raises` | unit | tests/test_sandbox.py | RED |
| U9 | `test_validate_host_allow_all_hosts_bypasses` | unit | tests/test_sandbox.py | RED |
| I1 | `test_sandbox_tx_write_inside_allowed_path` | integration | tests/test_sandbox.py | RED |
| I2 | `test_sandbox_tx_write_outside_allowed_path_raises` | integration | tests/test_sandbox.py | RED |
| I3 | `test_sandbox_tx_delete_outside_allowed_path_raises` | integration | tests/test_sandbox.py | RED |
| I4 | `test_sandbox_tx_mkdir_outside_allowed_path_raises` | integration | tests/test_sandbox.py | RED |
| I5 | `test_sandbox_tx_commit_legacy_forbidden_target_raises` | integration | tests/test_sandbox.py | RED |
| I6 | `test_sandbox_mixin_agent_writes_to_allowed_dir` | integration | tests/test_sandbox.py | RED |
| I7 | `test_sandbox_tx_write_op_not_queued_on_violation` | integration | tests/test_sandbox.py | RED |
| N1 | `test_validate_path_symlink_escape_raises` | negative | tests/test_sandbox.py | RED |
| N2 | `test_validate_path_traversal_string_raises` | negative | tests/test_sandbox.py | RED |
| N3 | `test_sandbox_config_empty_allowed_paths_rejects_all` | negative | tests/test_sandbox.py | RED |

---

## Red-Phase Confirmation

**Command run:**
```powershell
python -m pytest tests/test_sandbox.py -v --tb=short 2>&1 | Select-Object -Last 30
```

**Observed output (exact):**
```
ERROR collecting tests/test_sandbox.py
ImportError while importing test module 'C:\Dev\PyAgent\tests\test_sandbox.py'.
tests\test_sandbox.py:36: in <module>
    from src.core.sandbox import (  # type: ignore[import]  # noqa: E402
E   ModuleNotFoundError: No module named 'src.core.sandbox'
1 error in 2.43s
```

**Failure reason:** `ModuleNotFoundError: No module named 'src.core.sandbox'`
**Assessment:** CORRECT — the import fails at module level because `src/core/sandbox/` does not
yet exist.  This confirms the red phase is valid; no test passed on a stub.

---

## Structure Test Regression Check

**Command run:**
```powershell
python -m pytest tests/structure/ -q --tb=short 2>&1 | Select-Object -Last 8
```

**Result:** `129 passed in 2.73s` — zero regressions.

---

## Validation Results

| ID | Result | Notes |
|----|--------|-------|
| U1–N3 | All RED (collection error) | ModuleNotFoundError at line 36 |

---

## Unresolved Failures

None — all failures are the expected pre-implementation collection error.

---

## Design Notes for @6code

1. **`StorageTransaction.write()` signature** —
   `async def write(self, path: Path, content: bytes, *, user_id: Optional[str] = None) -> None`.
   The sandbox override must pass `user_id=user_id` through to `super().write()`.

2. **`acommit()` for multi-op flush** — `await tx.acommit()` is the async multi-op commit.
   Sync `commit()` is legacy single-file mode only (validated in I5).

3. **`_validate_path` raises before any append** — the invariant that `tx._ops` stays empty
   on violation is validated by I2 and I7.

4. **Symlink test (N1) skips on Windows** — `os.symlink` requires elevated privileges on
   Windows; the test calls `pytest.skip(...)` on `OSError` rather than failing.

5. **Import path:** `src.transactions.StorageTransactionManager.StorageTransaction` is
   authoritative (not `src.core.StorageTransactionManager`).

---

## Run Command

```powershell
cd c:\Dev\PyAgent
& .venv\Scripts\Activate.ps1
python -m pytest tests/test_sandbox.py -v --tb=short
```

Expected (green phase): 19 passed.
Expected (current red): 1 collection error, 0 tests run.
