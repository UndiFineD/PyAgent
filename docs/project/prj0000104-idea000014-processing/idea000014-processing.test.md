# idea000014-processing - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-30_

## Test Plan
Red-phase preparation is defined for tasks T002-T005 from plan scope. This artifact defines:
- deterministic failing test targets by acceptance criterion,
- failure-reason quality gates (assertion-level failures, not import/placeholder failures),
- weak-test detection and rejection rules,
- deterministic rerun commands for @6code and @7exec.

Test framework and boundaries:
- Framework: `pytest`
- Test root: `tests/deps/`
- Isolation: fixture-based file inputs only; no repository-state mutation outside temporary paths.
- Scope: planning/doc/log/memory artifacts only in this step (no production implementation).

Red-phase objective:
- Each selector fails for a behavioral assertion tied to AC-002..AC-006.
- Failures caused by `ImportError`/`AttributeError`/placeholder assertions are treated as invalid red evidence.

Green-transition objective:
- The exact red selectors pass after @6code implementation.
- Weak-test gate remains PASS (tests cannot pass against stubs/placeholders).
- Deterministic workflow commands succeed with no diff drift.

## AC To Test Matrix
| AC ID | Planned test case IDs | Planned test file/selectors | Red expectation |
|---|---|---|---|
| AC-001 | TC-DOC-001 | `tests/docs/test_agent_workflow_policy_docs.py` (policy docs validation command only) | Not a red target for this phase; must stay green for artifact edits |
| AC-002 | TC-DET-001, TC-DET-002 | `tests/deps/test_generate_requirements_deterministic.py::test_generate_requirements_is_byte_stable`; `tests/deps/test_generate_requirements_deterministic.py::test_generate_requirements_is_noop_when_re_run` | Assertion mismatch until deterministic generation behavior exists |
| AC-003 | TC-PAR-001, TC-PAR-002 | `tests/deps/test_dependency_parity_gate.py::test_parity_check_returns_nonzero_on_mismatch`; `tests/deps/test_dependency_parity_gate.py::test_parity_check_returns_zero_on_match` | Exit-code/output assertions fail until parity checker is implemented |
| AC-004 | TC-PAR-003 | `tests/deps/test_dependency_parity_gate.py::test_parity_failure_includes_remediation_command` | Message contract assertion fails until actionable remediation output exists |
| AC-005 | TC-INS-001, TC-INS-002 | `tests/deps/test_install_compatibility_contract.py::test_requirements_install_contract_remains_supported`; `tests/deps/test_install_compatibility_contract.py::test_requirements_ci_chain_still_includes_requirements_txt` | Contract assertions fail until compatibility wiring is present |
| AC-006 | TC-MAL-001, TC-MAN-001, TC-DET-003 | `tests/deps/test_pyproject_parse_failure.py::test_malformed_pyproject_fails_with_structured_error`; `tests/deps/test_manual_requirements_edit_detected.py::test_manual_requirements_edit_is_detected`; `tests/deps/test_generate_requirements_deterministic.py::test_generation_normalizes_newline_and_order` | Behavioral assertions fail until malformed/manual-edit/nondeterminism guards exist |
| AC-007 | TC-DOC-002 | Design/plan artifact traceability checks (manual review + project docs policy test) | Documentation acceptance already defined; not a red code selector |

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-DET-001 | Deterministic generator produces byte-identical output on repeated runs. | tests/deps/test_generate_requirements_deterministic.py | RED_CONFIRMED |
| TC-DET-002 | Second generation run is no-op against committed generated artifact. | tests/deps/test_generate_requirements_deterministic.py | RED_CONFIRMED |
| TC-DET-003 | Output normalization enforces stable ordering/newline behavior. | tests/deps/test_generate_requirements_deterministic.py | RED_CONFIRMED |
| TC-PAR-001 | Parity checker exits non-zero when regenerated output differs from committed output. | tests/deps/test_dependency_parity_gate.py | RED_CONFIRMED |
| TC-PAR-002 | Parity checker exits zero when generated output matches committed output. | tests/deps/test_dependency_parity_gate.py | RED_CONFIRMED |
| TC-PAR-003 | Parity failure includes exact remediation command contract. | tests/deps/test_dependency_parity_gate.py | RED_CONFIRMED |
| TC-MAL-001 | Malformed `pyproject.toml` returns structured parse error contract. | tests/deps/test_pyproject_parse_failure.py | RED_CONFIRMED |
| TC-MAN-001 | Manual edits to generated requirements are detected and rejected. | tests/deps/test_manual_requirements_edit_detected.py | RED_CONFIRMED |
| TC-INS-001 | Requirements-based install path remains supported. | tests/deps/test_install_compatibility_contract.py | RED_CONFIRMED |
| TC-INS-002 | CI include-chain compatibility for requirements artifacts remains valid. | tests/deps/test_install_compatibility_contract.py | RED_CONFIRMED |
| TC-DOC-001 | Project docs governance policy remains green after artifact edits. | tests/docs/test_agent_workflow_policy_docs.py | PASS |

## Validation Results
| ID | Result | Output |
|---|---|---|
| RED-GATE-01 | FAIL_AS_EXPECTED | `python -m pytest -q tests/deps/test_generate_requirements_deterministic.py` => 0 passed, 3 failed |
| RED-GATE-02 | FAIL_AS_EXPECTED | `python -m pytest -q tests/deps/test_dependency_parity_gate.py` => 0 passed, 3 failed |
| RED-GATE-03 | FAIL_AS_EXPECTED | `python -m pytest -q tests/deps/test_pyproject_parse_failure.py tests/deps/test_manual_requirements_edit_detected.py` => 0 passed, 2 failed |
| RED-GATE-04 | FAIL_AS_EXPECTED | `python -m pytest -q tests/deps/test_install_compatibility_contract.py` => 0 passed, 2 failed |
| RED-GATE-05 | FAIL_AS_EXPECTED | `python -m pytest -q tests/deps` => 0 passed, 10 failed |
| RED-GATE-06 | PASS | Failure signatures are assertion mismatches on exit-code/message contracts; no `ImportError`/`AttributeError` in selector output |
| RED-GATE-07 | PASS | Weak-test heuristic gate: `rg -n "assert True|TODO|is not None|isinstance\(" tests/deps` => no matches |
| DOC-GATE-01 | PASS | `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py` |

## Red-Phase Selectors
Run in this order to localize failures and capture deterministic evidence:

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

python -m pytest -q tests/deps/test_generate_requirements_deterministic.py
python -m pytest -q tests/deps/test_dependency_parity_gate.py
python -m pytest -q tests/deps/test_pyproject_parse_failure.py tests/deps/test_manual_requirements_edit_detected.py
python -m pytest -q tests/deps/test_install_compatibility_contract.py
python -m pytest -q tests/deps
```

Expected red result profile:
- Non-zero exit for targeted red suites.
- Failure messages reference unmet behavioral assertions (determinism/parity/contracts).
- If failures are import/symbol-missing only, red evidence is rejected and tests must be hardened.

## Weak-Test Detection Gate (Blocking)
Weak tests are rejected if any planned tests:
- only assert import/existence/type without behavior,
- pass against `pass`/stub/`return None` implementations,
- assert only "no exception",
- contain placeholder assertions (`assert True`, TODO-only tests).

Gate checks:
```powershell
# Heuristic guard against obvious weak patterns in new deps tests
rg -n "assert True|TODO|is not None|isinstance\(" tests/deps

# Mandatory semantic gate: red failures must be assertion/behavior related
python -m pytest -q tests/deps
```

Gate rule:
- Any unresolved weak-test finding blocks handoff to @6code.

Observed gate evidence:
- Heuristic scan PASS: no matches for `assert True`, `TODO`, `is not None`, `isinstance(` in `tests/deps`.
- Semantic red evidence PASS: all failures are assertion-level contract mismatches in command exit-code/message expectations and install/parity text contracts.
- No unresolved weak-test findings.

## Deterministic Command Set For @6code And @7exec
These commands must be used unchanged for reproducibility:

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# @6code green validation target
python -m pytest -q tests/deps

# @7exec runtime determinism/parity validation
python scripts/deps/generate_requirements.py --output requirements.txt
python scripts/deps/check_dependency_parity.py --check
git diff --exit-code -- requirements.txt
```

## Green Transition Criteria
Transition from red to green is allowed only when all are true:
1. All red selectors are present and reproducibly failing for behavioral reasons.
2. AC-to-test matrix remains fully mapped (AC-002..AC-006 each has concrete case IDs).
3. Weak-test detection gate is PASS.
4. @6code receives deterministic command set and failure evidence references.

Promotion to @7exec validation is allowed only when all are true:
1. `python -m pytest -q tests/deps` exits 0.
2. Generation/parity commands exit 0.
3. `git diff --exit-code -- requirements.txt` exits 0 after regeneration.

## Handoff Readiness To @6code
- Current readiness: READY
- BLOCKED state removed: YES
- Justification:
	- Planned red files/selectors are authored and executed.
	- Red suite fails deterministically with assertion-level evidence (`0 passed, 10 failed`).
	- Failure output contains no `ImportError` or `AttributeError` signatures.
	- Weak-test gate checks are PASS.

## Unresolved Failures
Expected red failures pending @6code implementation of parity/generator/install-contract behavior:
- Generator command contract unmet (`scripts/deps/generate_requirements.py` missing; exit code assertions fail).
- Parity command contract unmet (`scripts/deps/check_dependency_parity.py` missing; exit code/message assertions fail).
- Install contract parity-preflight/documentation assertions unmet in `install.ps1` and `requirements-ci.txt`.
