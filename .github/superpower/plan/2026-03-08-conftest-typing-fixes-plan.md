# Conftest Typing Fixes Implementation Plan

**Goal:** Fix the reported typing issues in `conftest.py` (missing annotations, typed monkey-patch signatures, and typed-safe `session.exitstatus` assignment) without changing runtime behavior.

**Architecture:** Type-only refactor with lightweight internal `Protocol` interfaces, strict return types for monkey-patched importlib wrappers, and pragmatic nested-function annotations.

**Tech Stack:** Python 3.14, `typing`/`types` stdlib, pytest.

---

## 1) Scope and Acceptance Criteria

### In Scope
- Add/adjust typing in `conftest.py` for the user-reported lines:
  - monkey-patch target methods (`_patched_spec`, `_patched_module`)
  - missing annotations for `__enter__`, nested `logged_open`, `__exit__`, `_debug_log`
  - typed-safe `session.exitstatus = 1`
- Keep behavior and control flow unchanged.

### Out of Scope
- Refactoring unrelated hook logic.
- Functional changes to write tracking or import patching behavior.

### Definition of Done
- All targeted tests pass.
- No new diagnostics for the touched symbols in `conftest.py`.
- Existing guard tests still pass.

---

## 2) File Map

### Files to Modify
- `conftest.py`

### Files to Create
- `tests/test_conftest_typing_contract.py`

---

## 3) Implementation Phases (TDD-first)

## Phase 1 — Add failing tests for typing-sensitive behavior

**Objective:** Lock behavior before making type changes.

### Step 1.1: Write failing tests for session exitstatus behavior and protocol-affected call paths
- File: `tests/test_conftest_typing_contract.py`
- Add tests:
  1. `session_finish` sets `exitstatus=1` when git status reports modified files.
  2. `session_finish` does not raise when session object is minimal but compatible.
  3. `_resolve_import_fixer` still prefers `scripts/` then `scripts-old/` (sanity guard).

### Step 1.2: Run tests and confirm baseline
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_conftest_typing_contract.py -v`
- Expected output:
  - Failing or incomplete coverage if tests reference not-yet-typed helpers directly.

---

## Phase 2 — Introduce lightweight Protocols and import typing primitives

**Objective:** Provide explicit structural typing for objects used in hooks.

### Step 2.1: Implement minimal Protocol definitions
- File: `conftest.py`
- Add near imports:
  - `Protocol`, `Any`, `IO`, `ModuleType` and importlib `ModuleSpec` typing references.
- Add internal protocols:
  - `_SessionWithExitStatus` with `exitstatus: int`
  - `_PytestItemLike` with attributes consumed in `inject_globals`/`_debug_log`

### Step 2.2: Re-run targeted tests
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_conftest_typing_contract.py -v`
- Expected output:
  - Tests remain green/near-green, proving no behavior drift from introducing Protocols.

---

## Phase 3 — Annotate monkey-patch wrappers with strict returns and flexible inputs

**Objective:** Fix missing/weak typing for importlib patch methods while preserving compatibility.

### Step 3.1: Update `_patched_spec` signature
- File: `conftest.py`
- Change signature to:
  - flexible incoming args (`name`, `location`, `*args`, `**kwargs`) for monkey-patch parity
  - strict return: `ModuleSpec | None`

### Step 3.2: Update `_patched_module` signature
- File: `conftest.py`
- Change signature to:
  - parameter typed as `ModuleSpec`
  - return typed as `ModuleType`

### Step 3.3: Run targeted tests
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_conftest_typing_contract.py -v`
- Expected output:
  - Pass; no functional change.

---

## Phase 4 — Annotate context manager and nested wrappers

**Objective:** Resolve missing annotations in `WriteTracker` methods and nested helpers.

### Step 4.1: Annotate `__enter__`
- File: `conftest.py`
- Signature: `def __enter__(self) -> None:`

### Step 4.2: Annotate nested `logged_write` and `logged_open` with balanced typing
- File: `conftest.py`
- `logged_write`: pragmatic parameter typing and explicit return consistent with `Path.write_text` usage.
- `logged_open`: balanced typing for `file`, `mode`, variadics; explicit `IO[Any]`-style return.

### Step 4.3: Annotate `__exit__`
- File: `conftest.py`
- Signature with exception params typed and `-> None`.

### Step 4.4: Run targeted tests
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_conftest_typing_contract.py -v`
- Expected output:
  - Pass.

---

## Phase 5 — Annotate `_debug_log` and typed-safe exitstatus assignment

**Objective:** Fix remaining user-listed typing issues.

### Step 5.1: Annotate `_debug_log`
- File: `conftest.py`
- Type annotate:
  - `item` as `_PytestItemLike`
  - `module_name` as `str`
  - `target_globals` as `dict[str, object] | None`
  - return `None`

### Step 5.2: Keep behavior, add safe cast for `session.exitstatus = 1`
- File: `conftest.py`
- In `session_finish`:
  - cast `session` to `_SessionWithExitStatus` before assignment
  - preserve assignment semantics and try/except envelope

### Step 5.3: Run targeted tests
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_conftest_typing_contract.py -v`
- Expected output:
  - Pass.

---

## Phase 6 — Regression validation

**Objective:** Ensure no regressions in existing relevant tests.

### Step 6.1: Run existing conftest-adjacent tests
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_conftest_import_fixer_resolution.py -v`
- Expected output:
  - Pass.

### Step 6.2: Run guard tests already used in session
- Command:
  - `.venv\Scripts\python.exe -m pytest tests/test_repo_layout_scaffold.py tests/test_dryrun_lists_moves.py -v`
- Expected output:
  - Pass.

---

## 4) Command Summary

1. `.venv\Scripts\python.exe -m pytest tests/test_conftest_typing_contract.py -v`
2. `.venv\Scripts\python.exe -m pytest tests/test_conftest_import_fixer_resolution.py -v`
3. `.venv\Scripts\python.exe -m pytest tests/test_repo_layout_scaffold.py tests/test_dryrun_lists_moves.py -v`

---

## 5) Risks and Mitigations

- **Risk:** Over-constraining monkey-patched call signatures.
  - **Mitigation:** Use flexible input params and strict returns only.
- **Risk:** Type-only edits accidentally alter behavior.
  - **Mitigation:** No control-flow changes; verify after each phase.
- **Risk:** Nested function annotations become noisy/fragile.
  - **Mitigation:** Balanced typing approach for wrappers.

---

## 6) Handoff

Implementation should proceed in execution mode with strict TDD sequencing (test -> fail/confirm -> minimal code change -> test -> pass) and no unrelated refactors.
