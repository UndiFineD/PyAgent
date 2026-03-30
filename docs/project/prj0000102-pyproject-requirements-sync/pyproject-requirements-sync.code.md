# pyproject-requirements-sync - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-30_

## Implementation Summary
Implemented T5/T6 by making `pyproject.toml` `[project.dependencies]` the canonical runtime dependency source,
adding deterministic `requirements.txt` generation, and wiring a blocking drift/policy gate into shared validation
checks.

Key decisions:
- Extended `src/tools/dependency_audit.py` to provide canonical read, deterministic emit, parity drift diff, and
	policy enforcement for duplicates/malformed specs and critical package operators.
- Added CLI modes (`--generate`, `--check`) and module entrypoint so local and CI invocation are deterministic.
- Wired parity/policy gate into both precommit and CI profiles in `scripts/ci/run_checks.py`.
- Replaced weak dependency tests with contract-level tests and added a structure selector test so
	`tests/structure -k "dependency and drift and ci"` is now meaningful.

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| src/tools/dependency_audit.py | Expanded from count-only audit to canonical reader + deterministic emitter + drift/policy gate CLI | +263/-22 |
| scripts/ci/run_checks.py | Added dependency sync gate execution in precommit/ci profiles | +6/-0 |
| tests/tools/test_dependency_audit.py | Replaced weak smoke test with contract tests for canonical/deterministic/drift/policy behavior | +116/-16 |
| tests/structure/test_dependency_drift_ci.py | Added structure-level CI wiring assertion for dependency drift selector | +25/-0 |
| requirements.txt | Regenerated deterministically from canonical `pyproject.toml` dependencies | rewritten |

## Test Run Results
```
python -m pytest -q tests -k "dependency and canonical and pyproject"
.                                                                                                                       [100%]
1 passed, 1313 deselected in 5.85s

python -m pytest -q tests -k "requirements and deterministic"
.                                                                                                                       [100%]
1 passed, 1313 deselected in 6.51s

python -m pytest -q tests/structure -k "dependency and drift and ci"
.                                                                                                                       [100%]
1 passed, 135 deselected in 1.58s

python -m pytest -q tests -k "dependency and policy"
..                                                                                                                      [100%]
2 passed, 1313 deselected in 8.36s

ruff check --fix src/tools/dependency_audit.py scripts/ci/run_checks.py tests/tools/test_dependency_audit.py
Found 9 errors (9 fixed, 0 remaining).

ruff check src/tools/dependency_audit.py scripts/ci/run_checks.py tests/tools/test_dependency_audit.py
All checks passed!

python -m mypy src/tools/dependency_audit.py scripts/ci/run_checks.py
Success: no issues found in 2 source files

rg placeholder scan on changed files
Command produced no output
```

## Deferred Items
none

## Post-Merge CI Hotfix (Shard 10)
- Added missing runtime dependencies for test import paths:
	- `python-json-logger` (for `from pythonjsonlogger.json import JsonFormatter`)
	- `PyJWT` (for `import jwt`)
- Regenerated `requirements.txt` using canonical sync mechanism:
	- `python -m src.tools.dependency_audit --generate --root .`
- Validation evidence:
	- `python -m pytest -q tests/test_structured_logging.py tests/test_watchdog.py` -> `11 passed`
	- `python -m pytest -q tests/tools/test_dependency_audit.py tests/structure/test_dependency_drift_ci.py` -> `7 passed`

## AC Evidence Mapping
| AC ID | Changed File(s) | Validating Test(s) | Status |
|---|---|---|---|
| AC-001 | src/tools/dependency_audit.py, requirements.txt | `pytest -q tests -k "dependency and canonical and pyproject"` | PASS |
| AC-002 | src/tools/dependency_audit.py, requirements.txt | `pytest -q tests -k "requirements and deterministic"` | PASS |
| AC-003 | src/tools/dependency_audit.py, scripts/ci/run_checks.py, tests/structure/test_dependency_drift_ci.py | `pytest -q tests/structure -k "dependency and drift and ci"` | PASS |
| AC-004 | src/tools/dependency_audit.py, tests/tools/test_dependency_audit.py | `pytest -q tests -k "dependency and policy"` | PASS |
| AC-005 | src/tools/dependency_audit.py, tests/tools/test_dependency_audit.py | `pytest -q tests -k "dependency and policy"` | PASS |
