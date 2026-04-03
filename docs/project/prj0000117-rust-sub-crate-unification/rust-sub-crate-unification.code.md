# rust-sub-crate-unification - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-04-03_

## Implementation Summary
Implemented the minimal workspace-unification baseline required by the red contracts:
1. Added a root `[workspace]` in `rust_core/Cargo.toml` with members `crdt`, `p2p`, and `security` while preserving the existing root `[package]`, maturin metadata, and benchmark contract.
2. Moved `patch.crates-io` governance to `rust_core/Cargo.toml` and removed crate-local patch ownership from `rust_core/p2p/Cargo.toml`.
3. Converged lockfile ownership to root by generating `rust_core/Cargo.lock` and removing member lockfiles in `rust_core/crdt`, `rust_core/p2p`, and `rust_core/security`.
4. Left `.github/workflows/ci.yml` unchanged because the lightweight CI contract and benchmark smoke command already satisfied tests.

## Implementation Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-WS-001 | rust_core/Cargo.toml | tests/rust/test_workspace_unification_contracts.py::test_root_manifest_declares_workspace_members_for_target_subcrates | PASS |
| AC-WS-002 | rust_core/Cargo.lock, rust_core/crdt/Cargo.lock, rust_core/p2p/Cargo.lock, rust_core/security/Cargo.lock | tests/rust/test_workspace_unification_contracts.py::test_root_workspace_lockfile_is_single_authoritative_lockfile | PASS |
| AC-WS-003 | rust_core/Cargo.toml | tests/rust/test_workspace_unification_contracts.py::test_root_manifest_keeps_package_and_benchmark_contract | PASS |
| AC-WS-004 | rust_core/Cargo.toml, .github/workflows/ci.yml (no change required) | tests/ci/test_ci_workspace_unification_contracts.py::test_ci_contains_single_benchmark_smoke_command; tests/ci/test_ci_workspace_unification_contracts.py::test_ci_benchmark_smoke_command_keeps_rust_core_execution_context | PASS |
| AC-WS-006 | rust_core/Cargo.toml, rust_core/p2p/Cargo.toml | tests/rust/test_workspace_unification_contracts.py::test_patch_governance_is_root_owned_not_member_owned | PASS |
| AC-WS-007 | .github/workflows/ci.yml (no change required) | tests/ci/test_ci_workspace_unification_contracts.py::test_ci_quick_job_remains_lightweight_without_matrix_sharding; tests/ci/test_ci_workflow.py | PASS |

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| rust_core/Cargo.toml | add workspace members + root patch governance | +7/-0 |
| rust_core/p2p/Cargo.toml | remove crate-local patch block | +0/-6 |
| rust_core/Cargo.lock | generated authoritative root lockfile | regenerated |
| rust_core/crdt/Cargo.lock | removed member lockfile | deleted |
| rust_core/p2p/Cargo.lock | removed member lockfile | deleted |
| rust_core/security/Cargo.lock | removed member lockfile | deleted |

## Test Run Results
```
python -m pytest -q tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py
.......                                                                                     [100%]
7 passed in 4.96s

python -m pytest -q tests/ci/test_ci_workflow.py
........                                                                                    [100%]
8 passed in 4.03s

cargo metadata --manifest-path rust_core/Cargo.toml --no-deps
warning: please specify `--format-version` flag explicitly to avoid compatibility problems
# command completed successfully and reported workspace members including rust_core, crdt, p2p, security
```

## Deferred Items
none
