# prj0000082 — agent-execution-sandbox — Exec

_Status: DONE — PASSED → @8ql_
_Executor: @7exec | Updated: 2026-03-26_

## Execution Plan
1. Run sandbox tests (all 5 sandbox test files)
2. Run structure tests (tests/structure/)
3. Run full test suite (tests/ excluding pre-existing test_core_memory.py)
4. Import smoke test
5. mypy type check
6. ruff lint
7. Coverage check (src/core/sandbox — all 5 test files combined)
6.5. Placeholder scan + pre-commit lint gate

## Run Log — Re-run 3 (post @6code coverage fix — validate() tests + unused import cleanup)

### Step 1 — Sandbox tests
```
32 passed, 1 skipped in 3.44s
Skipped: test_validate_path_symlink_escape_raises (Windows symlink — expected)
New tests present: test_SandboxConfig.py (3), test_SandboxMixin.py (3),
  test_SandboxViolationError.py (3), test_SandboxedStorageTransaction.py (5)
```

### Step 2 — Structure tests
```
129 passed in 2.57s — all 129/129 green
```

### Step 3 — Full test suite (excl. test_core_memory.py — pre-existing prj0000079 issue)
```
4 failed, 967 passed, 9 skipped in 233.51s
(was: 4 failed, 964 passed in run 2 — +3 new tests from validate() coverage)
All 4 failures are pre-existing (unchanged from run 2)
```

### Step 4 — Import smoke test
```
from src.core.sandbox import SandboxConfig, SandboxViolationError, SandboxMixin, SandboxedStorageTransaction
Import OK
```

### Step 5 — mypy
```
Success: no issues found in 5 source files
```

### Step 6 — ruff (src/core/sandbox/ + new test files)
```
All checks passed! (both src/core/sandbox/ and 4 new test files)
```

### Step 6.5 — Placeholder scan
```
rg found no matches in src/core/sandbox/ or test files — CLEAN
```

### Step 6.5b — Pre-commit lint gate
```
All hooks: Skipped (no Python files in diff — test files already committed by @6code)
ruff direct check on 4 new test files: All checks passed!
```

### Step 7 — Coverage (all 5 test files --cov=src/core/sandbox)
```
SandboxConfig.py                     100%
SandboxMixin.py                      100%
SandboxViolationError.py             100%
SandboxedStorageTransaction.py       100%
__init__.py                         100%
TOTAL                               100%
(was: 86.67% in run 2 — FIXED; was 95% in run 1)
```

## Pass/Fail Summary
| Check | Status | Notes |
|---|---|---|
| Sandbox tests (all 5 files) | PASS | 32 passed, 1 skipped (symlink/Windows — expected) |
| Structure tests (tests/structure/) | PASS | 129/129 passed |
| Full test suite | PASS† | 967 passed (+3 vs run 2), 4 failed — all pre-existing |
| Import smoke | PASS | Import OK |
| mypy | PASS | Success: no issues found in 5 source files |
| ruff (sandbox + test files) | PASS | All checks passed |
| Placeholder scan | PASS | No matches in src/core/sandbox/ |
| Pre-commit lint gate | PASS | No Python files in diff; new test files ruff-clean |
| Coverage (src/core/sandbox/) | PASS | **100%** — all 5 modules (up from 86.67% in run 2) |

† Full suite: the 4 failures are all pre-existing, documented below.

## Blockers

**None — all gates passed. Ready for @8ql.**

---

### PRE-EXISTING failures (not caused by this PR — unchanged from runs 1 & 2)

| Test | Root cause | Project |
|---|---|---|
| `test_project_overviews_use_modern_template_or_carry_legacy_exception` | prj0000079.project.md missing `## Project Identity` | prj0000079 automem |
| `test_memory_validate` | `src.core.memory` missing `validate` attribute | prj0000079 automem |
| `test_flake8_repo_config_has_no_repo_issues` | AutoMemCore.py E221/F401, BenchmarkRunner.py E302, CortCore.py F401, ql.py E501 | prj0000079, CortCore |
| `test_all_sarif_files_are_fresh` | SARIF files 33h+ old (time-based, environmental) | environmental |

### Step 1 — Sandbox tests
```
19 collected — 18 passed, 1 skipped in 1.70s
Skipped: test_validate_path_symlink_escape_raises (Windows symlink — expected)
```

### Step 2 — Structure tests
```
129 passed in 2.95s — all 129/129 green
```

### Step 3 — Full test suite (excl. test_core_memory.py — pre-existing prj0000079 issue)
```
4 failed, 964 passed, 9 skipped in 215.25s
(was: 8 failed, 816 passed — @6code fixed 4 blockers, added 148 new passing tests)
```

### Step 4 — Import smoke test
```
from src.core.sandbox import SandboxConfig, SandboxViolationError, SandboxMixin, SandboxedStorageTransaction
Import OK
```

### Step 5 — mypy
```
Success: no issues found in 5 source files
```

### Step 6 — ruff (src/core/sandbox/)
```
All checks passed!
```

### Step 6.5 — Placeholder scan
```
rg found no matches in src/core/sandbox/ — CLEAN
```

### Step 7 — Coverage (tests/test_sandbox.py --cov=src/core/sandbox)
```
SandboxConfig.py                     88%  missing: 76-77
SandboxMixin.py                      90%  missing: 73-74
SandboxViolationError.py             78%  missing: 52-53
SandboxedStorageTransaction.py       85%  missing: 124, 137, 155, 165-166
__init__.py                         100%
TOTAL                               86.67%
PREVIOUS (run 1): 95%  — REGRESSION of 8.3 pp
```

## Pass/Fail Summary
| Check | Status | Notes |
|---|---|---|
| Sandbox tests (test_sandbox.py) | PASS | 18 passed, 1 skipped (symlink/Windows — expected) |
| Structure tests (tests/structure/) | PASS | 129/129 passed |
| Full test suite | PASS† | 964 passed, 4 failed — all 4 are pre-existing (see below) |
| Import smoke | PASS | Import OK |
| mypy | PASS | Success: no issues found in 5 source files |
| ruff (sandbox) | PASS | All checks passed |
| Coverage | **FAIL** | 86.67% — below 90% threshold; was 95% in run 1 — REGRESSION |

† Full suite: the 4 failures are all pre-existing, documented below.

## Blockers

### BLOCKING FAILURE — Caused by this PR (return to @6code)

#### 1. Coverage regression — BLOCKING
- **Check**: `python -m pytest tests/test_sandbox.py --cov=src/core/sandbox`
- **Previous coverage (run 1)**: 95% — PASS
- **Current coverage (run 2)**: 86.67% — FAIL (threshold: ≥ 90%)
- **Root cause**: `@6code` added `validate()` functions to all 4 sandbox modules to fix blocker #3
  from run 1, but `tests/test_sandbox.py` does not exercise the new `validate()` code paths.
- **Uncovered lines**:
  - `src/core/sandbox/SandboxConfig.py`: lines 76–77 (validate function body)
  - `src/core/sandbox/SandboxMixin.py`: lines 73–74 (validate function body)
  - `src/core/sandbox/SandboxViolationError.py`: lines 52–53 (validate function body)
  - `src/core/sandbox/SandboxedStorageTransaction.py`: lines 124, 137, 155, 165–166
- **Fix required**: Add test cases calling `validate()` on each module to the per-module
  test files (`test_SandboxConfig.py`, `test_SandboxMixin.py`, `test_SandboxViolationError.py`,
  `test_SandboxedStorageTransaction.py`).

---

### Advisory (pre-existing test worsened — not a new test failure, but cleanup recommended)

The test `test_flake8_repo_config_has_no_repo_issues` was already pre-existing FAIL before this PR.
The new test files created by @6code added more flake8 warnings to this already-failing gate:
- `tests/test_SandboxMixin.py:23`: F401 `pathlib.Path` imported but unused
- `tests/test_SandboxMixin.py:37`: F401 `pytest` imported but unused
- `tests/test_SandboxViolationError.py:23`: F401 `pytest` imported but unused
These can be removed while @6code adds coverage tests for the validate() functions.

---

### PRE-EXISTING failures (not caused by this PR — unchanged from run 1)

| Test | Root cause | Project |
|---|---|---|
| `test_project_overviews_use_modern_template_or_carry_legacy_exception` | prj0000079.project.md missing `## Project Identity` | prj0000079 automem |
| `test_memory_validate` | `src.core.memory` missing `validate` attribute | prj0000079 automem |
| `test_flake8_repo_config_has_no_repo_issues` | AutoMemCore.py E221/F401, BenchmarkRunner.py E302, CortCore.py F401, ql.py E501, test files F401 | prj0000079, CortCore |
| `test_all_sarif_files_are_fresh` | SARIF files 33h+ old (time-based, environmental) | environmental |
