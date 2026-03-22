# transaction-managers-full — Test Artifacts

_Status: HANDED_OFF_
_Tester: @5test | Updated: 2026-03-22_

## Test Plan

Four new test files created on branch `prj0000045-transaction-managers-full`.
Coverage: all four transaction managers (Storage, Process, Context, Memory).
Framework: pytest with `asyncio_mode = strict` — async tests marked `@pytest.mark.asyncio`.
Import guards: `pytest.skip()` used for all modules that don't exist yet; ensures
graceful SKIP (not crash) at collection time. No `xfail` markers needed — skips
communicate pending task ID directly.

**Branch gate:** PASSED — confirmed on `prj0000045-transaction-managers-full`.

**Red-phase run (2026-03-22):**
```
48 collected | 4 passed | 1 failed | 43 skipped
```
- `test_module_level_validate_exists_and_returns_true` → FAIL (AssertionError, not ImportError) ✓ correct red
- All other non-passing tests → SKIP (missing modules, not test logic errors)

## Test Cases

### tests/test_MemoryTransactionManager.py (10 tests)

| ID | Description | File | Status |
|---|---|---|---|
| TC-M1 | import MemoryTransaction from shim | test_MemoryTransactionManager.py | PASS |
| TC-M2 | sync CM reentrant (RLock does not deadlock same thread) | test_MemoryTransactionManager.py | PASS |
| TC-M3 | sync CM releases lock on exit | test_MemoryTransactionManager.py | PASS |
| TC-M4 | async CM __aenter__/__aexit__ complete cleanly | test_MemoryTransactionManager.py | PASS |
| TC-M5 | module-level validate() exists and returns True | test_MemoryTransactionManager.py | FAIL (AssertionError — T10 pending) |
| TC-M6 | transactions pkg import + validate() → True | test_MemoryTransactionManager.py | SKIP (T06 pending) |
| TC-M7 | set/get/delete KV operations | test_MemoryTransactionManager.py | SKIP (T06 pending) |
| TC-M8 | commit() flushes _pending into _store | test_MemoryTransactionManager.py | SKIP (T06 pending) |
| TC-M9 | rollback() discards _pending without touching _store | test_MemoryTransactionManager.py | SKIP (T06 pending) |
| TC-M10 | sync_remote(dry_run=True) returns dict payload | test_MemoryTransactionManager.py | SKIP (T06 pending) |

### tests/test_StorageTransactionManager.py (13 tests)

| ID | Description | File | Status |
|---|---|---|---|
| TC-S1 | shim import: StorageTransaction importable | test_StorageTransactionManager.py | SKIP (T07 pending) |
| TC-S2 | shim validate() → True | test_StorageTransactionManager.py | SKIP (T07 pending) |
| TC-S3 | stage() + commit() writes exact bytes to target | test_StorageTransactionManager.py | SKIP (T07 pending) |
| TC-S4 | rollback on exception preserves original file | test_StorageTransactionManager.py | SKIP (T07 pending) |
| TC-S5 | double-commit raises exception | test_StorageTransactionManager.py | SKIP (T07 pending) |
| TC-S6 | commit with no stage is safe no-op | test_StorageTransactionManager.py | SKIP (T07 pending) |
| TC-S7 | async with StorageTransaction commits | test_StorageTransactionManager.py | SKIP (T07 pending) |
| TC-S8 | transactions pkg import + validate() → True | test_StorageTransactionManager.py | SKIP (T03 pending) |
| TC-S9 | async write() + acommit() creates file | test_StorageTransactionManager.py | SKIP (T03 pending) |
| TC-S10 | async rollback() removes tmp, target absent | test_StorageTransactionManager.py | SKIP (T03 pending) |
| TC-S11 | async delete() removes existing file | test_StorageTransactionManager.py | SKIP (T03 pending) |
| TC-S12 | async mkdir() creates directory | test_StorageTransactionManager.py | SKIP (T03 pending) |
| TC-S13 | encryption raises EncryptionConfigError without master key env | test_StorageTransactionManager.py | SKIP (T03 pending) |

### tests/test_ProcessTransactionManager.py (12 tests)

| ID | Description | File | Status |
|---|---|---|---|
| TC-P1 | shim import: ProcessTransaction importable | test_ProcessTransactionManager.py | SKIP (T08 pending) |
| TC-P2 | shim validate() → True | test_ProcessTransactionManager.py | SKIP (T08 pending) |
| TC-P3 | start() creates _proc (Popen) with stdout=PIPE | test_ProcessTransactionManager.py | SKIP (T08 pending) |
| TC-P4 | wait() returns int rc, sets tx.stdout bytes | test_ProcessTransactionManager.py | SKIP (T08 pending) |
| TC-P5 | rollback() terminates running _proc | test_ProcessTransactionManager.py | SKIP (T08 pending) |
| TC-P6 | exception in context triggers rollback | test_ProcessTransactionManager.py | SKIP (T08 pending) |
| TC-P7 | async start_async() + wait_async() → rc==0 | test_ProcessTransactionManager.py | SKIP (T08 pending) |
| TC-P8 | transactions pkg import + validate() → True | test_ProcessTransactionManager.py | SKIP (T04 pending) |
| TC-P9 | async run() returns (int, str, str) 3-tuple | test_ProcessTransactionManager.py | SKIP (T04 pending) |
| TC-P10 | async run() returncode matches process exit status | test_ProcessTransactionManager.py | SKIP (T04 pending) |
| TC-P11 | async run() stdout captures printed output | test_ProcessTransactionManager.py | SKIP (T04 pending) |
| TC-P12 | async rollback terminates _async_proc | test_ProcessTransactionManager.py | SKIP (T04 pending) |

### tests/test_ContextTransactionManager.py (13 tests)

| ID | Description | File | Status |
|---|---|---|---|
| TC-C1 | shim exports ContextTransaction + RecursionGuardError | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C2 | shim validate() → True | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C3 | transaction_id is uuid.UUID auto-assigned | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C4 | inner.parent_id == outer.transaction_id when nested | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C5 | active_contexts() reflects enter and exit | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C6 | RecursionGuardError on re-entrant same context_id | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C7 | ValueError on empty context_id | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C8 | current() returns innermost from stack | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C9 | async with ContextTransaction enters/exits cleanly | test_ContextTransactionManager.py | SKIP (T09 pending) |
| TC-C10 | transactions pkg import + validate() → True | test_ContextTransactionManager.py | SKIP (T05 pending) |
| TC-C11 | UUID lineage: outer parent_id=None, inner linked | test_ContextTransactionManager.py | SKIP (T05 pending) |
| TC-C12 | current() → None when no context active | test_ContextTransactionManager.py | SKIP (T05 pending) |
| TC-C13 | RecursionGuardError leaves no state leak | test_ContextTransactionManager.py | SKIP (T05 pending) |

### tests/test_transaction_managers.py (14 existing — DO NOT MODIFY)

| ID | Description | Status |
|---|---|---|
| TC-COMPAT-01..14 | All 14 existing tests | FAIL (ImportError — T07+T08+T09 pending) |

## Validation Results (red phase, 2026-03-22)

| ID | Result | Output |
|---|---|---|
| TC-M1 | PASS | imports without error |
| TC-M2 | PASS | nested `with MemoryTransaction()` does not deadlock |
| TC-M3 | PASS | second `with` block enters after first exits |
| TC-M4 | PASS | async CM completes without error |
| TC-M5 | FAIL | `AssertionError: Module-level validate() not yet implemented (T10 pending)` |
| TC-M6..M10 | SKIP | `T06 pending: src.transactions.MemoryTransactionManager not yet created` |
| TC-S1..S13 | SKIP | T07/T03 pending |
| TC-P1..P12 | SKIP | T08/T04 pending |
| TC-C1..C13 | SKIP | T09/T05 pending |
| TC-COMPAT-01..14 | ERROR | `ModuleNotFoundError: No module named 'src.core.StorageTransactionManager'` |

## Unresolved Failures

**TC-M5** — `test_module_level_validate_exists_and_returns_true`
- Expected failure: `src.MemoryTransactionManager` has no `validate()` function (T10 pending).
- Correct red-phase evidence: `AssertionError: Module-level validate() not yet implemented`
- Resolved by: T10 (replace MemoryTransactionManager.py body with shim)

**TC-COMPAT-01..14** (test_transaction_managers.py)
- Collection error: `ModuleNotFoundError: No module named 'src.core.StorageTransactionManager'`
- Resolved by: T07 + T08 + T09 (create the three shim files in src/core/)

## @6code Handoff

To turn all SKIP/FAIL tests GREEN, @6code must implement in order:

| Task | File | Unblocks |
|---|---|---|
| T00 | `requirements.txt` — add `cryptography>=42.0.0` | TC-S13 encryption fixture |
| T01 | `src/transactions/__init__.py` | all transactions-pkg imports |
| T02 | `src/transactions/BaseTransaction.py` | T03–T06 ABC |
| T03 | `src/transactions/StorageTransactionManager.py` | TC-S8..S13 |
| T04 | `src/transactions/ProcessTransactionManager.py` | TC-P8..P12 |
| T05 | `src/transactions/ContextTransactionManager.py` | TC-C10..C13 |
| T06 | `src/transactions/MemoryTransactionManager.py` | TC-M6..M10 |
| T07 | `src/core/StorageTransactionManager.py` (shim) | TC-S1..S7 + COMPAT-01..05 |
| T08 | `src/core/ProcessTransactionManager.py` (shim) | TC-P1..P7 + COMPAT-06..09 |
| T09 | `src/core/ContextTransactionManager.py` (shim) | TC-C1..C9 + COMPAT-10..14 |
| T10 | `src/MemoryTransactionManager.py` (shim body) | TC-M5 |
