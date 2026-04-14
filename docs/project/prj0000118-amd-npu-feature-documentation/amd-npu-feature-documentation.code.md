# amd-npu-feature-documentation - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-04-03_

## Implementation Summary

Implemented minimal canonical AMD NPU runtime guidance documentation in `docs/performance/HARDWARE_ACCELERATION.md`. Added a new section "## Canonical AMD NPU Runtime Guidance" with:

- **AC-AMD-001**: Explicit canonical guidance marker and location statement
- **AC-AMD-002**: Feature activation commands (both feature-off and feature-on `cargo run` forms)
- **AC-AMD-003**: Fallback semantics with exit code `-1` (AMD_NPU_STATUS_UNAVAILABLE) and safe interpretation guidance
- **AC-AMD-004**: Supported environment boundary (Windows x86_64, AMD Ryzen AI SDK) with explicit unsupported paths list
- **AC-AMD-005**: Mandatory evidence schema table (Command, Exit Status, Observed Outcome, Runner Context)
- **AC-AMD-006**: Explicit non-goals section and CI defer contract with rationale

All 6 test selectors pass (AC-AMD-001..006).

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| docs/performance/HARDWARE_ACCELERATION.md | Added canonical AMD NPU runtime guidance section (AC-AMD-001..006) | +130 |

## Test Run Results
```
tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_001_requires_canonical_runtime_guidance_marker PASSED
tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_002_requires_feature_off_and_feature_on_command_examples PASSED
tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_003_requires_unavailable_status_minus_one_semantics PASSED
tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_004_requires_supported_environment_boundary_and_unsupported_paths PASSED
tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_005_requires_mandatory_evidence_schema_fields PASSED
tests/docs/test_prj0000118_amd_npu_feature_documentation_contracts.py::test_ac_amd_006_requires_non_goals_and_ci_defer_contract PASSED

6 passed in 4.41s
```

## Deferred Items

CI automation, Rust feature-gating in `rust_core`, and SDK detection remain deferred by explicit AC-AMD-006 contract (CI Defer Contract).