# rust-sub-crate-unification - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-03_

## Overview
Minimal-first TDD plan for `prj0000117` to unify existing Rust sub-crates under the root `rust_core/Cargo.toml` workspace boundary with deterministic command behavior.

In scope for this slice:
1. Root mixed package+workspace manifest update.
2. Root-owned patch and lockfile governance.
3. Deterministic package-scoped cargo build/test command usage.
4. Targeted CI command-context updates only when required by workspace behavior.

Out of scope for this slice:
1. Broad Rust API refactors.
2. Broad dependency harmonization beyond workspace convergence.
3. CI redesign outside workspace command compatibility.

## Branch and Scope Gates
1. Expected branch: `prj0000117-rust-sub-crate-unification`.
2. Allowed file ownership (this plan):
	 - `rust_core/Cargo.toml`
	 - `rust_core/Cargo.lock`
	 - `rust_core/crdt/Cargo.toml`
	 - `rust_core/p2p/Cargo.toml`
	 - `rust_core/security/Cargo.toml`
	 - `rust_core/crdt/Cargo.lock`
	 - `rust_core/p2p/Cargo.lock`
	 - `rust_core/security/Cargo.lock`
	 - `.github/workflows/ci.yml`
	 - `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md`
	 - `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.code.md`
	 - `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.exec.md`
	 - `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.ql.md`
	 - `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.git.md`
3. Branch mismatch or out-of-scope edits are BLOCKED and must return to `@0master`.

## Task List

### Milestone M1 - Contract and Red Tests
- [ ] T-WS-001 (sequential-only)
	- Objective: Define workspace unification contracts and red selectors for AC-WS-001..AC-WS-007 before implementation.
	- Target files: `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md`
	- Dependencies: none
	- Acceptance criteria: Contract section maps IFACE-WS-001..IFACE-WS-005 to deterministic command checks.
	- Validation command: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
	- Owner: `@5test`

- [ ] T-WS-002 (sequential-only)
	- Objective: Add failing selectors for missing workspace membership, lockfile singleton, and root patch ownership.
	- Target files: `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md`
	- Dependencies: T-WS-001
	- Acceptance criteria: Red-state checks fail on pre-implementation state and explicitly reference root manifest and member lockfile presence.
	- Validation command: `cargo metadata --manifest-path rust_core/Cargo.toml`
	- Owner: `@5test`

### Milestone M2 - Minimal Workspace Convergence
- [ ] T-WS-003 (parallel-safe)
	- Objective: Add root workspace membership and root-owned patch governance while preserving root package metadata for `maturin`.
	- Target files: `rust_core/Cargo.toml`
	- Dependencies: T-WS-002
	- Acceptance criteria: AC-WS-001 and AC-WS-006 satisfied with workspace members declared and root patch override present.
	- Validation command: `cargo metadata --manifest-path rust_core/Cargo.toml`
	- Owner: `@6code`

- [ ] T-WS-004 (parallel-safe)
	- Objective: Align sub-crate manifests to workspace governance with only required local constraints retained.
	- Target files: `rust_core/crdt/Cargo.toml`, `rust_core/p2p/Cargo.toml`, `rust_core/security/Cargo.toml`
	- Dependencies: T-WS-002
	- Acceptance criteria: Sub-crate manifests no longer own workspace-global patch/lock policy; package-local constraints remain valid.
	- Validation command: `cargo build -p rust_core_crdt --manifest-path rust_core/Cargo.toml`
	- Owner: `@6code`

- [ ] T-WS-005 (sequential-only)
	- Objective: Converge lockfiles to root singleton and remove member lockfiles in one atomic migration.
	- Target files: `rust_core/Cargo.lock`, `rust_core/crdt/Cargo.lock`, `rust_core/p2p/Cargo.lock`, `rust_core/security/Cargo.lock`, `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.code.md`
	- Dependencies: T-WS-003, T-WS-004
	- Acceptance criteria: AC-WS-002 satisfied; only `rust_core/Cargo.lock` remains.
	- Validation command: `rg --files rust_core | rg "Cargo.lock$"`
	- Owner: `@6code`

### Milestone M3 - Command Compatibility and CI Context
- [ ] T-WS-006 (sequential-only)
	- Objective: Apply minimal CI command-context adjustments to keep build/test/bench deterministic under workspace mode.
	- Target files: `.github/workflows/ci.yml`
	- Dependencies: T-WS-005
	- Acceptance criteria: AC-WS-004, AC-WS-005, and AC-WS-007 command contracts are explicit and stable.
	- Validation command: `rg -n "manifest-path rust_core/Cargo.toml|cargo bench --bench stats_baseline|cargo (build|test) -p rust_core_(crdt|p2p|security)" .github/workflows/ci.yml`
	- Owner: `@6code`

### Milestone M4 - Execution and Quality Closure
- [ ] T-WS-007 (sequential-only)
	- Objective: Execute runtime validation for workspace metadata, package build/test, benchmark smoke, and maturin continuity.
	- Target files: `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.exec.md`
	- Dependencies: T-WS-006
	- Acceptance criteria: AC-WS-001..AC-WS-005 evidenced with exit code `0` outputs.
	- Validation command: `maturin develop --manifest-path rust_core/Cargo.toml`
	- Owner: `@7exec`

- [ ] T-WS-008 (sequential-only)
	- Objective: Validate security/quality closure with root patch effectiveness and no member lockfile regression.
	- Target files: `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.ql.md`
	- Dependencies: T-WS-007
	- Acceptance criteria: AC-WS-006 and AC-WS-007 verified; any blocker has remediation evidence and rerun proof.
	- Validation command: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
	- Owner: `@8ql`

### Milestone M5 - Git Closure Handoff
- [ ] T-WS-009 (sequential-only)
	- Objective: Complete branch/scope validation, narrow staging proof, and handoff package for commit/PR.
	- Target files: `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.git.md`
	- Dependencies: T-WS-008
	- Acceptance criteria: Active branch remains expected; staged set stays inside approved ownership map.
	- Validation command: `git branch --show-current`
	- Owner: `@9git`

## Parallel Ownership Map
| Task ID | Parallel mode | File ownership | Lock rule |
|---|---|---|---|
| T-WS-001 | sequential-only | `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md` | Exclusive |
| T-WS-002 | sequential-only | `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.test.md` | Exclusive |
| T-WS-003 | parallel-safe | `rust_core/Cargo.toml` | Disjoint from T-WS-004 |
| T-WS-004 | parallel-safe | `rust_core/crdt/Cargo.toml`, `rust_core/p2p/Cargo.toml`, `rust_core/security/Cargo.toml` | Disjoint from T-WS-003 |
| T-WS-005 | sequential-only | `rust_core/Cargo.lock`, `rust_core/crdt/Cargo.lock`, `rust_core/p2p/Cargo.lock`, `rust_core/security/Cargo.lock`, `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.code.md` | Convergence owner `@6code` |
| T-WS-006 | sequential-only | `.github/workflows/ci.yml` | Exclusive |
| T-WS-007 | sequential-only | `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.exec.md` | Exclusive |
| T-WS-008 | sequential-only | `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.ql.md` | Exclusive |
| T-WS-009 | sequential-only | `docs/project/prj0000117-rust-sub-crate-unification/rust-sub-crate-unification.git.md` | Exclusive |

Convergence step:
1. T-WS-003 and T-WS-004 may execute in parallel only after T-WS-002 completes.
2. T-WS-005 is the mandatory sync barrier and merge-decision step, owned by `@6code`, before CI edits in T-WS-006.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Contract and red tests | T-WS-001, T-WS-002 | PLANNED |
| M2 | Workspace and lockfile convergence | T-WS-003, T-WS-004, T-WS-005 | PLANNED |
| M3 | Command compatibility and CI context | T-WS-006 | PLANNED |
| M4 | Runtime and quality closure | T-WS-007, T-WS-008 | PLANNED |
| M5 | Git closure handoff | T-WS-009 | PLANNED |

## Validation Commands by Milestone
### M1
```powershell
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
cargo metadata --manifest-path rust_core/Cargo.toml
```

### M2
```powershell
cargo metadata --manifest-path rust_core/Cargo.toml
cargo build -p rust_core_crdt --manifest-path rust_core/Cargo.toml
cargo build -p rust_core_p2p --manifest-path rust_core/Cargo.toml
cargo build -p rust_core_security --manifest-path rust_core/Cargo.toml
rg --files rust_core | rg "Cargo.lock$"
```

### M3
```powershell
rg -n "manifest-path rust_core/Cargo.toml|cargo bench --bench stats_baseline|cargo (build|test) -p rust_core_(crdt|p2p|security)" .github/workflows/ci.yml
```

### M4
```powershell
cargo test -p rust_core_crdt --manifest-path rust_core/Cargo.toml
cargo test -p rust_core_p2p --manifest-path rust_core/Cargo.toml
cargo test -p rust_core_security --manifest-path rust_core/Cargo.toml
cd rust_core; cargo bench --bench stats_baseline -- --noplot
maturin develop --manifest-path rust_core/Cargo.toml
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```

### M5
```powershell
git branch --show-current
git status --short
```

## Dependencies and Sequence
1. T-WS-001 -> T-WS-002.
2. T-WS-002 -> parallel wave (T-WS-003 + T-WS-004).
3. Parallel wave -> T-WS-005 convergence.
4. T-WS-005 -> T-WS-006 -> T-WS-007 -> T-WS-008 -> T-WS-009.

## Handoff Package to @5test
1. Start with T-WS-001 and T-WS-002 only.
2. Keep red tests scoped to workspace membership, lockfile singleton, root patch ownership, and command determinism.
3. Do not introduce broad crate refactor assertions in this slice.
