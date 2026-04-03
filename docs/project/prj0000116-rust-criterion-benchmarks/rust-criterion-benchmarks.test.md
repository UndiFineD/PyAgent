# rust-criterion-benchmarks - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-03_

## Test Plan
Scope and approach:
1. Add deterministic, structure-only red-phase contract tests for Rust Criterion baseline wiring and CI smoke integration.
2. Avoid runtime benchmark execution in tests; validate file presence and static contract markers only.
3. Keep assertions bound to design contracts IFACE-BENCH-001, IFACE-BENCH-003, and IFACE-BENCH-005.

Framework and selectors:
1. `pytest` contract tests in `tests/rust/test_rust_criterion_baseline.py`.
2. CI workflow contract selector added to `tests/ci/test_ci_workflow.py`.

## AC-to-Test Matrix
| AC ID | Contract | Test Case ID(s) |
|---|---|---|
| AC-BENCH-001 | Criterion configuration in `rust_core/Cargo.toml` | TC-BENCH-001 |
| AC-BENCH-002 | Benchmark harness file and naming contract patterns | TC-BENCH-002, TC-BENCH-003 |
| AC-BENCH-005 | CI contains smoke benchmark command | TC-BENCH-004 |
| AC-BENCH-006 | CI smoke remains non-threshold and non-matrix-heavy | TC-BENCH-004 |

## Weak-Test Detection Gate
Gate checks:
1. No test that only asserts importability, existence-only, or `assert True`.
2. Every selector validates concrete behavior contract text (Cargo TOML keys, Criterion macros, workflow command/path semantics).
3. Red failures must be assertion-based contract misses, not `ImportError` or `AttributeError`.

Gate status:
1. PASS - red-run produced only assertion-based failures tied to missing contract behavior.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-BENCH-001 | Assert Cargo TOML has Criterion dev-dependency and `stats_baseline` bench target with harness disabled | tests/rust/test_rust_criterion_baseline.py | RED_EXPECTED |
| TC-BENCH-002 | Assert `rust_core/benches/stats_baseline.rs` exists and includes Criterion harness macros | tests/rust/test_rust_criterion_baseline.py | RED_EXPECTED |
| TC-BENCH-003 | Assert benchmark naming contract (`stats/<domain>` + `<function>/<dataset>`) is encoded in source | tests/rust/test_rust_criterion_baseline.py | RED_EXPECTED |
| TC-BENCH-004 | Assert CI contains exactly one benchmark smoke command and artifact check without threshold/matrix expansion | tests/ci/test_ci_workflow.py | RED_EXPECTED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-BENCH-001 | RED_EXPECTED | `AssertionError: rust_core/Cargo.toml must add criterion under [dev-dependencies] for stats baseline bench` |
| TC-BENCH-002 | RED_EXPECTED | `AssertionError: rust_core/benches/stats_baseline.rs must exist` |
| TC-BENCH-003 | RED_EXPECTED | `AssertionError: rust_core/benches/stats_baseline.rs must exist` |
| TC-BENCH-004 | RED_EXPECTED | `AssertionError: ci.yml must contain exactly one benchmark smoke command: 'cargo bench --bench stats_baseline -- --noplot'` |

Command evidence:
1. `.venv\Scripts\ruff.exe check --fix tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py` -> `Found 1 error (1 fixed, 0 remaining).`
2. `.venv\Scripts\ruff.exe check tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py` -> `All checks passed!`
3. `.venv\Scripts\ruff.exe check --select D tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py` -> `All checks passed!`
4. `python -m pytest -q tests/rust/test_rust_criterion_baseline.py tests/ci/test_ci_workflow.py::test_ci_workflow_has_single_rust_benchmark_smoke_step_without_threshold_gate` -> `4 failed in 4.74s`.

## Unresolved Failures
1. Criterion dev-dependency and `[[bench]]` target are not configured in `rust_core/Cargo.toml`.
2. `rust_core/benches/stats_baseline.rs` does not exist.
3. CI workflow does not include benchmark smoke command and artifact check.

Handoff:
1. Target agent: `@6code`.
2. Readiness: READY_FOR_IMPLEMENTATION.
