# rust-sub-crate-unification - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-03_

## Test Plan
Objective: Create red-phase contract tests for minimal workspace unification slice covering workspace membership, lockfile governance, command compatibility, and CI benchmark-smoke continuity.

Scope (this wave):
1. `tests/rust/test_workspace_unification_contracts.py`
2. `tests/ci/test_ci_workspace_unification_contracts.py`

Out of scope (this wave):
1. Running heavy Rust builds/benches as part of test assertions.
2. Implementing production manifest/workflow changes.

Branch gate:
1. Expected: `prj0000117-rust-sub-crate-unification`
2. Observed: `prj0000117-rust-sub-crate-unification`
3. Result: PASS

## AC-to-Test Matrix
| AC ID | Contract requirement | Test case IDs |
|---|---|---|
| AC-WS-001 | Root `rust_core/Cargo.toml` defines workspace members (`crdt`, `p2p`, `security`) while preserving root package metadata. | TC-WS-001, TC-WS-003 |
| AC-WS-002 | Canonical lockfile strategy uses only `rust_core/Cargo.lock`; member lockfiles are not authoritative. | TC-WS-002 |
| AC-WS-003 | Existing root package/extension command compatibility remains intact at structure level. | TC-WS-003 |
| AC-WS-004 | Benchmark smoke command compatibility remains present in CI at contract level. | TC-CI-002, TC-CI-003 |
| AC-WS-006 | Workspace patch governance is root-owned. | TC-WS-004 |
| AC-WS-007 | CI command context stays explicit and lightweight post-unification. | TC-CI-001, TC-CI-002, TC-CI-003 |

## Weak-Test Detection Gate
Gate checklist:
1. No tests assert only import/existence or non-None placeholders.
2. No unconditional `assert True` or TODO placeholder tests.
3. Red failures must be assertion-level behavior mismatches, not ImportError/AttributeError.
4. Every AC in this slice maps to at least one concrete test case ID.

Gate status: PASS.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-WS-001 | Root manifest includes `[workspace]` members for `crdt`, `p2p`, `security`. | `tests/rust/test_workspace_unification_contracts.py` | RED_EXPECTED |
| TC-WS-002 | Root lockfile is authoritative and member lockfiles are absent. | `tests/rust/test_workspace_unification_contracts.py` | RED_EXPECTED |
| TC-WS-003 | Root package + benchmark contract markers remain in root Cargo manifest. | `tests/rust/test_workspace_unification_contracts.py` | EXPECT_PASS |
| TC-WS-004 | Patch governance is root-owned and not crate-local. | `tests/rust/test_workspace_unification_contracts.py` | RED_EXPECTED |
| TC-CI-001 | CI quick job remains lightweight (no matrix strategy). | `tests/ci/test_ci_workspace_unification_contracts.py` | EXPECT_PASS |
| TC-CI-002 | CI keeps exactly one benchmark smoke command. | `tests/ci/test_ci_workspace_unification_contracts.py` | EXPECT_PASS |
| TC-CI-003 | Benchmark smoke command executes with `rust_core` context. | `tests/ci/test_ci_workspace_unification_contracts.py` | EXPECT_PASS |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-WS-001 | FAIL (RED_EXPECTED) | AssertionError: `rust_core/Cargo.toml [workspace].members must include 'crdt', 'p2p', and 'security'` |
| TC-WS-002 | FAIL (RED_EXPECTED) | AssertionError: member `Cargo.lock` files still exist under `rust_core/crdt`, `rust_core/p2p`, `rust_core/security` |
| TC-WS-003 | PASS | Root `package.name=rust_core` and `[[bench]] stats_baseline harness=false` contract markers present |
| TC-WS-004 | FAIL (RED_EXPECTED) | AssertionError: root `rust_core/Cargo.toml` missing `[patch.crates-io]` ownership |
| TC-CI-001 | PASS | `jobs.quick` has no `strategy` matrix |
| TC-CI-002 | PASS | Exactly one `cargo bench --bench stats_baseline -- --noplot` command found |
| TC-CI-003 | PASS | Benchmark smoke step includes `pushd rust_core` context |

Validation command evidence:
1. `python -m pytest -q tests/rust/test_workspace_unification_contracts.py tests/ci/test_ci_workspace_unification_contracts.py`
	- Result: `3 failed, 4 passed`
	- Failing selectors: `TC-WS-001`, `TC-WS-002`, `TC-WS-004`
	- Failure mode quality: assertion failures only (no ImportError/AttributeError)
2. `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
	- Result: `1 failed, 16 passed`
	- Failure is known baseline unrelated to this project scope (missing historical legacy file).

## Unresolved Failures
1. RED blockers for implementation handoff (@6code):
	- Add root `[workspace]` with members `crdt`, `p2p`, `security` to `rust_core/Cargo.toml`.
	- Enforce root lockfile singleton by removing member lockfiles.
	- Move `[patch.crates-io]` governance from member manifests to root `rust_core/Cargo.toml`.
2. Baseline non-project blocker:
	- `tests/docs/test_agent_workflow_policy_docs.py` fails due to pre-existing missing legacy file `docs/project/prj0000005/prj005-llm-swarm-architecture.git.md`.
