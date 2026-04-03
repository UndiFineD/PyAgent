# rust-criterion-benchmarks - Code Artifacts

_Status: IN_PROGRESS_
_Coder: @6code | Updated: 2026-04-03_

## Implementation Summary
Implemented the minimal benchmark baseline required by red contracts:
1. Added Criterion under `rust_core` dev dependencies and registered `stats_baseline` with `harness = false`.
2. Added `rust_core/benches/stats_baseline.rs` Criterion harness with naming contract markers:
	- group: `stats/core`
	- benchmark id: `sum/1k`
3. Added exactly one CI smoke benchmark command and artifact path check in `.github/workflows/ci.yml` without threshold gates or matrix expansion.

## AC Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-BENCH-001 | `rust_core/Cargo.toml` | `tests/rust/test_rust_criterion_baseline.py::test_rust_core_cargo_declares_criterion_baseline_bench_contract` | PASS |
| AC-BENCH-002 | `rust_core/benches/stats_baseline.rs` | `tests/rust/test_rust_criterion_baseline.py::test_stats_baseline_benchmark_file_uses_criterion_harness_patterns`; `tests/rust/test_rust_criterion_baseline.py::test_stats_baseline_benchmark_contains_design_naming_contract_markers` | PASS |
| AC-BENCH-005 | `.github/workflows/ci.yml` | `tests/ci/test_ci_workflow.py::test_ci_workflow_has_single_rust_benchmark_smoke_step_without_threshold_gate` | PASS |
| AC-BENCH-006 | `.github/workflows/ci.yml` | `tests/ci/test_ci_workflow.py::test_ci_workflow_has_single_rust_benchmark_smoke_step_without_threshold_gate` | PASS |
| AC-BENCH-007 | `rust_core/Cargo.toml`; `rust_core/benches/stats_baseline.rs`; `.github/workflows/ci.yml` | `git status --short` scope check | PASS |

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `.github/workflows/ci.yml` | Add single rust benchmark smoke step and criterion artifact check | +7/-1 |
| `rust_core/Cargo.toml` | Add Criterion dev dependency and `[[bench]]` target config | +5/-0 |
| `rust_core/benches/stats_baseline.rs` | Add new minimal Criterion benchmark harness | +14/-0 |

## Test Run Results
```
python -m pytest -q tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py::test_ci_workflow_has_single_rust_benchmark_smoke_step_without_threshold_gate
....                                                                                        [100%]
4 passed in 4.52s

python -m pytest -q tests/ci/test_ci_workflow.py
........                                                                                    [100%]
8 passed in 4.79s
```

## Deferred Items
None.
