# prj0000088-ai-fuzzing-security - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-27_

## Test Plan
Red-phase contract tests were authored for fuzzing core behavior in seven module-focused test files plus one
umbrella contract file:
- `tests/test_fuzzing_core.py` contains TEST-01..TEST-18 mapped from plan AC requirements.
- `tests/test_FuzzCase.py`, `tests/test_FuzzMutator.py`, `tests/test_FuzzCorpus.py`,
	`tests/test_FuzzEngineCore.py`, `tests/test_FuzzSafetyPolicy.py`, and `tests/test_FuzzResult.py`
	provide per-module contract checks.

Red-phase failure strategy:
- Avoid import-time collection errors by using runtime symbol loading.
- Fail with explicit `pytest.fail(...)` behavior messages when `src.core.fuzzing.*` modules are missing.
- Ensure failures indicate missing fuzzing behavior contracts rather than unresolved Python imports in test discovery.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TEST-01 | Policy violation exception typing | tests/test_fuzzing_core.py | RED |
| TEST-02 | Execution/config exception typing | tests/test_fuzzing_core.py | RED |
| TEST-03 | FuzzCase immutability contract | tests/test_fuzzing_core.py | RED |
| TEST-04 | Deterministic replay key generation | tests/test_fuzzing_core.py | RED |
| TEST-05 | Per-case result typing and state | tests/test_fuzzing_core.py | RED |
| TEST-06 | Deterministic campaign summary counts | tests/test_fuzzing_core.py | RED |
| TEST-07 | Reject non-local target | tests/test_fuzzing_core.py | RED |
| TEST-08 | Reject disallowed operator | tests/test_fuzzing_core.py | RED |
| TEST-09 | Enforce budget limits | tests/test_fuzzing_core.py | RED |
| TEST-10 | Normalize corpus entries to bytes | tests/test_fuzzing_core.py | RED |
| TEST-11 | Deduplicate repeated payloads | tests/test_fuzzing_core.py | RED |
| TEST-12 | Deterministic indexed selection | tests/test_fuzzing_core.py | RED |
| TEST-13 | Registry exposes allowed operators | tests/test_fuzzing_core.py | RED |
| TEST-14 | Seeded deterministic mutation equality | tests/test_fuzzing_core.py | RED |
| TEST-15 | Mutation output remains bytes and bounded | tests/test_fuzzing_core.py | RED |
| TEST-16 | Engine schedules bounded case count | tests/test_fuzzing_core.py | RED |
| TEST-17 | Engine applies policy before execution | tests/test_fuzzing_core.py | RED |
| TEST-18 | Replay-stable ordering and case IDs | tests/test_fuzzing_core.py | RED |
| MOD-01 | FuzzCase module contract exposure | tests/test_FuzzCase.py | RED |
| MOD-02 | FuzzMutator module contract exposure | tests/test_FuzzMutator.py | RED |
| MOD-03 | FuzzCorpus module contract exposure | tests/test_FuzzCorpus.py | RED |
| MOD-04 | FuzzEngineCore module contract exposure | tests/test_FuzzEngineCore.py | RED |
| MOD-05 | FuzzSafetyPolicy module contract exposure | tests/test_FuzzSafetyPolicy.py | RED |
| MOD-06 | FuzzResult module contract exposure | tests/test_FuzzResult.py | RED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| RED-TARGET | FAIL (expected red) | `python -m pytest -q tests/test_fuzzing_core.py tests/test_FuzzCase.py tests/test_FuzzMutator.py tests/test_FuzzCorpus.py tests/test_FuzzEngineCore.py tests/test_FuzzSafetyPolicy.py tests/test_FuzzResult.py --tb=short` -> 24 failed in 3.37s |
| STRUCTURE | FAIL (pre-existing project governance mismatch) | `python -m pytest -q tests/structure --tb=short` -> 1 failed, 128 passed in 2.47s |
| LINT-FIX | PASS | `.venv\Scripts\ruff.exe check --fix` on all seven new test files |
| LINT-CHECK | PASS | `.venv\Scripts\ruff.exe check` on all seven new test files |

## Unresolved Failures
- Red target failures are intentional and map to missing implementation modules:
	- `src.core.fuzzing.exceptions`
	- `src.core.fuzzing.FuzzCase`
	- `src.core.fuzzing.FuzzResult`
	- `src.core.fuzzing.FuzzSafetyPolicy`
	- `src.core.fuzzing.FuzzCorpus`
	- `src.core.fuzzing.FuzzMutator`
	- `src.core.fuzzing.FuzzEngineCore`
- Structure suite failure (not introduced by these tests):
	- `tests/structure/test_kanban.py::test_kanban_total_rows`
	- Assertion: expected 88 project rows in `docs/project/kanban.md`, found 90.
