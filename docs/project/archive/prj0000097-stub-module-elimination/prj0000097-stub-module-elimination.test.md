# prj0000097-stub-module-elimination - Test Artifacts

_Status: HANDED_OFF_
_Tester: @5test | Updated: 2026-03-29_

## Test Plan
Slice 1 red-phase contract testing for `rl` and `speculation`.

Scope:
- Author deterministic behavior/deprecation/guard tests for AC-001..AC-006.
- Keep failures assertion-driven (no ImportError/AttributeError blockers).
- Capture targeted pytest evidence for handoff to @6code.

Out of scope:
- Any production code implementation in `src/`.
- Any runtime/memory/cort implementation changes.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-RL-001 | Discounted return computes deterministic discounted sum and empty input behavior. | tests/rl/test_discounted_return.py | RED |
| TC-RL-002 | Discounted return rejects invalid `gamma` and non-finite rewards. | tests/rl/test_discounted_return.py | RED |
| TC-SPC-001 | `select_candidate` enforces threshold and highest-score selection. | tests/speculation/test_select_candidate.py | RED |
| TC-SPC-002 | `select_candidate` applies deterministic lexicographic tie-break. | tests/speculation/test_select_candidate.py | RED |
| TC-DEP-001 | `rl.validate()` emits required deprecation warning and remains callable. | tests/rl/test_rl_deprecation.py | RED |
| TC-DEP-002 | `speculation.validate()` emits required deprecation warning and remains callable. | tests/speculation/test_speculation_deprecation.py | RED |
| TC-IMP-001 | Import-scope guard rejects non-allowlisted `rl`/`speculation` imports. | tests/guards/test_rl_speculation_import_scope.py | RED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-RL-001, TC-RL-002 | FAIL (expected red) | `python -m pytest -q tests/rl/test_discounted_return.py --tb=short` -> 7 failed in 1.76s; assertion failure: `Expected rl.discounted_return() to exist and be callable.` |
| TC-SPC-001, TC-SPC-002 | FAIL (expected red) | `python -m pytest -q tests/speculation/test_select_candidate.py --tb=short` -> 7 failed in 1.55s; assertion failure: `Expected speculation.select_candidate() to exist and be callable.` |
| TC-DEP-001, TC-DEP-002 | FAIL (expected red) | `python -m pytest -q tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py --tb=short` -> 2 failed in 0.82s; `DID NOT WARN` for `DeprecationWarning`. |
| TC-IMP-001 | FAIL (expected red) | `python -m pytest -q tests/guards/test_rl_speculation_import_scope.py --tb=short` -> 1 failed, 1 passed in 1.40s; disallowed imports found in `tests/test_rl_package.py` and `tests/test_speculation_package.py`. |

## AC-to-Test Matrix
| AC ID | Requirement | Test Case IDs | File(s) |
|---|---|---|---|
| AC-001 | RL discounted return correctness, including empty input. | TC-RL-001 | tests/rl/test_discounted_return.py |
| AC-002 | RL rejects invalid `gamma` and non-finite rewards. | TC-RL-002 | tests/rl/test_discounted_return.py |
| AC-003 | Speculation threshold and top candidate selection are correct. | TC-SPC-001 | tests/speculation/test_select_candidate.py |
| AC-004 | Speculation tie-break is deterministic and lexicographic. | TC-SPC-002 | tests/speculation/test_select_candidate.py |
| AC-005 | Legacy `validate()` shims emit warnings and remain callable. | TC-DEP-001, TC-DEP-002 | tests/rl/test_rl_deprecation.py; tests/speculation/test_speculation_deprecation.py |
| AC-006 | Import guard blocks unauthorized new imports of `rl` and `speculation`. | TC-IMP-001 | tests/guards/test_rl_speculation_import_scope.py |
| AC-007 | Import-smoke focus replaced by behavior/deprecation coverage. | TC-IMP-001 + new behavior/deprecation suites | tests/guards/test_rl_speculation_import_scope.py; tests/rl/*; tests/speculation/* |
| AC-008 | No out-of-scope implementation edits in runtime/memory/cort lanes. | Diff-scope check for @6code/@8ql | n/a (@5test performed test-only edits) |

## Weak-Test Detection Gate
Gate outcome: PASS

Checks:
- No placeholder assertions (`assert True`, existence-only imports) in new Slice 1 tests.
- Red failures are assertion-contract failures, not ImportError/AttributeError collection errors.
- Deprecation tests fail on missing warning semantics (`DID NOT WARN`), confirming real behavior checks.
- Guard test fails on concrete unauthorized import sites with file:line evidence.

Lint/docstring gates executed:
- `.venv\Scripts\ruff.exe check --fix tests/rl/test_discounted_return.py tests/speculation/test_select_candidate.py tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py tests/guards/test_rl_speculation_import_scope.py` -> PASS (11 fixed)
- `.venv\Scripts\ruff.exe check tests/rl/test_discounted_return.py tests/speculation/test_select_candidate.py tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py tests/guards/test_rl_speculation_import_scope.py` -> PASS
- `.venv\Scripts\ruff.exe check --select D tests/rl/test_discounted_return.py tests/speculation/test_select_candidate.py tests/rl/test_rl_deprecation.py tests/speculation/test_speculation_deprecation.py tests/guards/test_rl_speculation_import_scope.py` -> PASS

## Unresolved Failures
- `rl.discounted_return` is absent, causing contract assertion failures in RL behavior tests.
- `speculation.select_candidate` is absent, causing contract assertion failures in speculation behavior tests.
- `rl.validate` and `speculation.validate` do not emit required `DeprecationWarning` messages.
- Import-scope guard reports legacy import-smoke tests as disallowed import sites.

## Handoff
- Target: @6code
- Readiness: READY
- Required implementation scope:
	- Implement `discounted_return(rewards: list[float], gamma: float = 0.99) -> float` in `src/rl/__init__.py` per design contract.
	- Implement `select_candidate(scores: dict[str, float], threshold: float = 0.0) -> str | None` in `src/speculation/__init__.py` per design contract.
	- Update `rl.validate` and `speculation.validate` to emit required deprecation warnings while returning `True`.
	- Resolve import-guard failure by replacing/removing legacy import-smoke tests (`tests/test_rl_package.py`, `tests/test_speculation_package.py`) according to AC-007.
