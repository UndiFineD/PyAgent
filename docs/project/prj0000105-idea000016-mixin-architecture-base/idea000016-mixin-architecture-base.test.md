# idea000016-mixin-architecture-base - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-30_

## Branch Plan
Expected branch: prj0000105-idea000016-mixin-architecture-base.

## Branch Validation
- PASS: Branch validated during initialization.

## Scope Validation
- PASS: Changes limited to `tests/core/base/mixins/*` and project @5test artifacts/memory/log.

## Failure Disposition
None. Branch gate and scope gate remained valid through red execution.

## Test Plan
Chunk A red-phase execution for T001-T006 (AC-MX-001/002/003).

Approach:
1. Write failing contract tests that encode target canonical namespace, host contract behavior, and shim policy behavior.
2. Ensure failures are deterministic and attributable to missing behavior/contract drift.
3. Gate weak tests before handoff.

Red selectors:
- `python -m pytest -q tests/core/base/mixins/test_export_contract.py`
- `python -m pytest -q tests/core/base/mixins/test_host_contract.py`
- `python -m pytest -q tests/core/base/mixins/test_host_validation_in_mixins.py`
- `python -m pytest -q tests/core/base/mixins/test_legacy_shim_imports.py`
- `python -m pytest -q tests/core/base/mixins/test_shim_deprecation_policy.py`
- `python -m pytest -q tests/core/base/mixins`

## AC-To-Test Matrix
| AC ID | Task IDs | Test Case IDs | File |
|---|---|---|---|
| AC-MX-001 | T001, T002 | TC-MX-001, TC-MX-002 | tests/core/base/mixins/test_export_contract.py |
| AC-MX-002 | T003, T004 | TC-MX-003, TC-MX-004, TC-MX-005, TC-MX-006 | tests/core/base/mixins/test_host_contract.py; tests/core/base/mixins/test_host_validation_in_mixins.py |
| AC-MX-003 | T005, T006 | TC-MX-007, TC-MX-008, TC-MX-009, TC-MX-010, TC-MX-011, TC-MX-012 | tests/core/base/mixins/test_legacy_shim_imports.py; tests/core/base/mixins/test_shim_deprecation_policy.py |

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-MX-001 | Canonical mixin namespace resolves as `src.core.base.mixins` | tests/core/base/mixins/test_export_contract.py | RED |
| TC-MX-002 | Canonical `__all__` export order is deterministic | tests/core/base/mixins/test_export_contract.py | RED |
| TC-MX-003 | Host contract validation rejects missing required host capabilities | tests/core/base/mixins/test_host_contract.py | RED |
| TC-MX-004 | Host contract validation accepts fully compliant host | tests/core/base/mixins/test_host_contract.py | RED |
| TC-MX-005 | Audit mixin emits host-contract validation migration event | tests/core/base/mixins/test_host_validation_in_mixins.py | RED |
| TC-MX-006 | Sandbox mixin emits host-contract error event before rejection | tests/core/base/mixins/test_host_validation_in_mixins.py | RED |
| TC-MX-007 | Legacy audit shim keeps behavior and declares canonical target metadata | tests/core/base/mixins/test_legacy_shim_imports.py | RED |
| TC-MX-008 | Legacy sandbox shim keeps behavior and declares canonical target metadata | tests/core/base/mixins/test_legacy_shim_imports.py | RED |
| TC-MX-009 | Legacy replay shim keeps behavior and declares canonical target metadata | tests/core/base/mixins/test_legacy_shim_imports.py | RED |
| TC-MX-010 | Legacy audit shim declares deterministic removal-wave metadata | tests/core/base/mixins/test_shim_deprecation_policy.py | RED |
| TC-MX-011 | Legacy sandbox shim declares deterministic removal-wave metadata | tests/core/base/mixins/test_shim_deprecation_policy.py | RED |
| TC-MX-012 | Legacy replay shim declares deterministic removal-wave metadata | tests/core/base/mixins/test_shim_deprecation_policy.py | RED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| CMD-RED-001 | FAIL (expected red) | `test_export_contract.py`: 2 failed (namespace resolves to `<missing>` and canonical `__all__` expected list vs `[]`) |
| CMD-RED-002 | FAIL (expected red) | `test_host_contract.py`: 2 failed (`validate_host_contract` missing on host classes) |
| CMD-RED-003 | FAIL (expected red) | `test_host_validation_in_mixins.py`: 2 failed (expected migration events not emitted) |
| CMD-RED-004 | FAIL (expected red) | `test_legacy_shim_imports.py`: 3 failed (missing `__shim_target__` metadata, behavior branch executed) |
| CMD-RED-005 | FAIL (expected red) | `test_shim_deprecation_policy.py`: 3 failed (`__shim_removal_wave__` absent) |
| CMD-RED-006 | FAIL (expected red) | `tests/core/base/mixins`: 12 failed aggregate |
| CMD-QA-001 | PASS | `ruff check --fix` on all new files |
| CMD-QA-002 | PASS | `ruff check` on all new files |
| CMD-QA-003 | PASS | `ruff check --select D` on all new files |
| CMD-QA-004 | PASS | Weak-test pattern gate: `rg -n "assert\s+True|TODO: implement|is\s+not\s+None|isinstance\(" tests/core/base/mixins` produced no matches |

## Weak-Test Detection Gate
- Gate status: PASS
- Rule checks applied:
	- No placeholder assertions (`assert True`), TODO placeholders, or simple `isinstance` shape checks.
	- No tests that only assert import success without behavioral assertions.
- Evidence:
	- `rg -n "assert\s+True|TODO: implement|is\s+not\s+None|isinstance\(" tests/core/base/mixins` -> no output.
	- Red failures are assertion mismatches on contract behavior/metadata, plus explicit missing canonical namespace contract.

## Unresolved Failures
Expected red failures remain unresolved pending @6code implementation for T001-T006.

## Handoff
- Target: @6code
- Status: READY
- Entry condition satisfied: deterministic red suite exists and fails for expected contract/behavior gaps.