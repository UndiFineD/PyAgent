# amd-npu-feature-documentation - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-03_

## Test Plan
Run docs-only red-phase contract tests that assert mandatory AMD NPU documentation behavior is present in
`docs/performance/HARDWARE_ACCELERATION.md`. Tests must fail via assertion-level behavior checks for AC-AMD-001..006
before @6code implementation changes are applied.

## Branch and Scope Preconditions
- Expected branch: prj0000118-amd-npu-feature-documentation
- Observed branch: prj0000118-amd-npu-feature-documentation
- Project match: PASS
- Scope-bounded files reviewed:
	- `docs/project/prj0000118-amd-npu-feature-documentation/amd-npu-feature-documentation.test.md`
	- `tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py`
	- `.github/agents/data/current.5test.memory.md`
	- `.github/agents/data/2026-04-03.5test.log.md`
- Required evidence:
	- `git branch --show-current`

## AC-to-Test Matrix
| AC ID | Requirement Summary | Test Case ID | Selector(s) |
|---|---|---|---|
| AC-AMD-001 | Canonical runtime guidance location is explicit and references amd_npu behavior. | TC-AMD-001 | `tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_001_requires_canonical_runtime_guidance_marker` |
| AC-AMD-002 | Feature activation includes both feature-off and feature-on command forms aligned with Cargo feature wiring. | TC-AMD-002 | `tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_002_requires_feature_off_and_feature_on_command_examples` |
| AC-AMD-003 | Unsupported/fallback behavior explicitly documents `-1` unavailable semantics. | TC-AMD-003 | `tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_003_requires_unavailable_status_minus_one_semantics` |
| AC-AMD-004 | Supported environment boundaries and unsupported paths are explicit. | TC-AMD-004 | `tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_004_requires_supported_environment_boundary_and_unsupported_paths` |
| AC-AMD-005 | Validation checklist/evidence schema fields are mandatory. | TC-AMD-005 | `tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_005_requires_mandatory_evidence_schema_fields` |
| AC-AMD-006 | Non-goals and CI defer contract are explicit. | TC-AMD-006 | `tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_006_requires_non_goals_and_ci_defer_contract` |

## Weak-Test Detection Gate
- Block handoff to @6code if any test can pass while documentation is placeholder-only, stub-like, or lacks behavioral assertions.
- Reject tests that only assert import/existence checks without contract semantics.
- Reject tests that use `assert True`, placeholder TODOs, or no-op execution checks.
- Red-phase failures must be assertion-level contract failures, not `ImportError` or `AttributeError`.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-AMD-001 | Canonical marker for AMD NPU runtime guidance exists and references `amd_npu` behavior. | tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py | RED_CONFIRMED |
| TC-AMD-002 | Docs contain both feature-off and feature-on command examples tied to `--features amd_npu`. | tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py | RED_CONFIRMED |
| TC-AMD-003 | Docs define explicit fallback semantics for unavailable status `-1`. | tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py | RED_CONFIRMED |
| TC-AMD-004 | Docs declare supported environment boundary and unsupported paths. | tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py | RED_CONFIRMED |
| TC-AMD-005 | Docs include mandatory evidence schema fields for validation records. | tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py | RED_CONFIRMED |
| TC-AMD-006 | Docs include explicit non-goals and CI defer contract language. | tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py | RED_CONFIRMED |

## Red-Phase Selector Order
| Selector ID | Command | Purpose |
|---|---|---|
| S1 | `python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_001_requires_canonical_runtime_guidance_marker` | AC-AMD-001 canonical marker contract |
| S2 | `python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_002_requires_feature_off_and_feature_on_command_examples` | AC-AMD-002 activation command contract |
| S3 | `python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_003_requires_unavailable_status_minus_one_semantics` | AC-AMD-003 fallback semantics contract |
| S4 | `python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_004_requires_supported_environment_boundary_and_unsupported_paths` | AC-AMD-004 environment boundary contract |
| S5 | `python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_005_requires_mandatory_evidence_schema_fields` | AC-AMD-005 evidence schema contract |
| S6 | `python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_006_requires_non_goals_and_ci_defer_contract` | AC-AMD-006 defer/non-goals contract |
| S7 | `python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py` | Aggregate red-phase contract evidence |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-AMD-001 | FAIL (RED_EXPECTED) | `assert "## canonical amd npu runtime guidance" in normalized` failed. |
| TC-AMD-002 | FAIL (RED_EXPECTED) | `assert "cargo run --bin pyagent_cli -- amd-npu-status" in raw` failed. |
| TC-AMD-003 | FAIL (RED_EXPECTED) | `assert "amd_npu_status_unavailable" in normalized` failed. |
| TC-AMD-004 | FAIL (RED_EXPECTED) | `assert "windows x86_64" in normalized` failed. |
| TC-AMD-005 | FAIL (RED_EXPECTED) | Missing evidence schema phrase assertion failed (`evidence schema`). |
| TC-AMD-006 | FAIL (RED_EXPECTED) | `assert "non-goals" in normalized` failed. |

## Unresolved Failures
- Aggregate selector `python -m pytest -q tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py` returns `6 failed in 6.68s`.
- Failure mode is assertion-level only; no `ImportError` or `AttributeError` observed.
- @6code must satisfy the six failing selectors listed in the AC-to-Test matrix and test summary.