# prj0000097-stub-module-elimination - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-29_

## Implementation Summary
Implemented Slice 1 production behavior for `rl` and `speculation` with deterministic,
typed APIs and deprecated compatibility shims.

Delivered changes:
- Added `rl.discounted_return(rewards, gamma)` with range validation and finite-value checks.
- Added `speculation.select_candidate(scores, threshold)` with deterministic score selection
	and lexicographic tie-break.
- Updated `rl.validate()` and `speculation.validate()` to emit required
	`DeprecationWarning` messages while returning `True` for compatibility.
- Replaced conflicting legacy import-smoke tests with package API-surface tests using
	`importlib.import_module(...)` so import-scope guard policy remains enforced.
- Updated this project's git summary template to modern Branch Plan format so broader
	policy tests stay green.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| src/rl/__init__.py | Added `discounted_return`, deprecating `validate` shim, exports update | +49/-5 |
| src/speculation/__init__.py | Added `select_candidate`, deprecating `validate` shim, exports update | +52/-3 |
| tests/test_rl_package.py | Replaced direct import-smoke with API surface check | +12/-5 |
| tests/test_speculation_package.py | Replaced direct import-smoke with API surface check | +12/-5 |
| docs/project/prj0000097-stub-module-elimination/prj0000097-stub-module-elimination.git.md | Added required modern Branch Plan sections | +20/-2 |

## AC Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-001 | `src/rl/__init__.py` | `tests/rl/test_discounted_return.py` | PASS |
| AC-002 | `src/rl/__init__.py` | `tests/rl/test_discounted_return.py` | PASS |
| AC-003 | `src/speculation/__init__.py` | `tests/speculation/test_select_candidate.py` | PASS |
| AC-004 | `src/speculation/__init__.py` | `tests/speculation/test_select_candidate.py` | PASS |
| AC-005 | `src/rl/__init__.py`, `src/speculation/__init__.py` | `tests/rl/test_rl_deprecation.py`, `tests/speculation/test_speculation_deprecation.py` | PASS |
| AC-006 | `tests/test_rl_package.py`, `tests/test_speculation_package.py` | `tests/guards/test_rl_speculation_import_scope.py` | PASS |
| AC-007 | `tests/test_rl_package.py`, `tests/test_speculation_package.py` | `tests/test_rl_package.py`, `tests/test_speculation_package.py`, `tests/rl/*`, `tests/speculation/*` | PASS |
| AC-008 | Scoped diff review (no runtime/memory/cort implementation edits) | N/A (diff-scope verification) | PASS |

## Test Run Results
```
# Lint/docstring checks on changed Python files
.venv\Scripts\ruff.exe check --fix src/rl/__init__.py src/speculation/__init__.py tests/test_rl_package.py tests/test_speculation_package.py
All checks passed!

.venv\Scripts\ruff.exe check src/rl/__init__.py src/speculation/__init__.py tests/test_rl_package.py tests/test_speculation_package.py
All checks passed!

.venv\Scripts\ruff.exe check --select D src/rl/__init__.py src/speculation/__init__.py tests/test_rl_package.py tests/test_speculation_package.py
All checks passed!

# Targeted validations
python -m pytest -q tests/rl/test_discounted_return.py
7 passed in 0.89s

python -m pytest -q tests/speculation/test_select_candidate.py
7 passed in 1.22s

python -m pytest -q tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py
2 passed in 0.62s

python -m pytest -q tests/guards/test_rl_speculation_import_scope.py
2 passed in 1.23s

python -m pytest -q tests/test_rl_package.py tests/test_speculation_package.py
2 passed in 0.66s

# Broader slice validation
python -m pytest -q tests/rl tests/speculation tests/guards/test_rl_speculation_import_scope.py
18 passed in 2.12s

# Full suite
python -m pytest -q
1272 passed, 10 skipped, 3 warnings in 182.19s
```

## Deferred Items
none
