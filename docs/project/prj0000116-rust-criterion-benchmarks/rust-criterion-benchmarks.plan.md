# rust-criterion-benchmarks - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-04-03_

## Overview
Minimal-first TDD plan for `prj0000116` to deliver only two outcomes:
1. Rust Criterion baseline benchmark harness for `rust_core` stats targets.
2. A single CI smoke step that executes the benchmark and checks artifact presence.

Out of scope for this plan:
1. Performance threshold enforcement.
2. Multi-OS benchmark matrices.
3. Broad `rust_core` refactors.

## Branch and Scope Gates
1. Expected branch: `prj0000116-rust-criterion-benchmarks`.
2. Allowed file ownership (this plan):
	 - `rust_core/Cargo.toml`
	 - `rust_core/benches/stats_baseline.rs`
	 - `.github/workflows/ci.yml`
	 - `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.test.md`
	 - `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.code.md`
	 - `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.exec.md`
	 - `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.ql.md`
	 - `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.git.md`
3. Branch mismatch or out-of-scope edits are BLOCKED and must return to `@0master`.

## Task List

### Milestone M1 - Benchmark Contract and Red Tests
- [ ] T-BENCH-001 (sequential-only)
	- Objective: Define benchmark naming and smoke contracts in test artifact before implementation.
	- Target files: `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.test.md`
	- Dependencies: none
	- Acceptance criteria: AC-BENCH-001, AC-BENCH-002, AC-BENCH-003 contract selectors documented and tied to deterministic commands.
	- Validation command: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
	- Owner: `@5test`

- [ ] T-BENCH-002 (sequential-only)
	- Objective: Create failing checks for missing Criterion wiring and benchmark target.
	- Target files: `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.test.md`
	- Dependencies: T-BENCH-001
	- Acceptance criteria: Red-state selectors clearly fail against current repo state without implementation changes.
	- Validation command: `cd rust_core; cargo bench --bench stats_baseline -- --help`
	- Owner: `@5test`

### Milestone M2 - Minimal Baseline Implementation
- [ ] T-BENCH-003 (parallel-safe)
	- Objective: Add Criterion dev dependency and bench target registration.
	- Target files: `rust_core/Cargo.toml`
	- Dependencies: T-BENCH-002
	- Acceptance criteria: AC-BENCH-001 satisfied; bench target resolves by name.
	- Validation command: `cd rust_core; cargo bench --bench stats_baseline -- --help`
	- Owner: `@6code`

- [ ] T-BENCH-004 (parallel-safe)
	- Objective: Implement deterministic baseline benchmark file for 1-2 bounded stats functions.
	- Target files: `rust_core/benches/stats_baseline.rs`
	- Dependencies: T-BENCH-002
	- Acceptance criteria: AC-BENCH-002 naming contract met (`stats/<domain>` and `<function>/<dataset>`), compile and execute with Criterion.
	- Validation command: `cd rust_core; cargo bench --bench stats_baseline -- --noplot`
	- Owner: `@6code`

- [ ] T-BENCH-005 (sequential-only)
	- Objective: Convergence merge for baseline harness after parallel tasks complete.
	- Target files: `rust_core/Cargo.toml`, `rust_core/benches/stats_baseline.rs`, `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.code.md`
	- Dependencies: T-BENCH-003, T-BENCH-004
	- Acceptance criteria: Single coherent implementation documented; no duplicate benchmark target names; narrow scope preserved.
	- Validation command: `cd rust_core; cargo bench --bench stats_baseline -- --noplot`
	- Owner: `@6code`

### Milestone M3 - CI Smoke Hook Only
- [ ] T-BENCH-006 (sequential-only)
	- Objective: Add one CI smoke step for benchmark harness health and artifact existence.
	- Target files: `.github/workflows/ci.yml`
	- Dependencies: T-BENCH-005
	- Acceptance criteria: AC-BENCH-005 and AC-BENCH-006 satisfied; step runs `cargo bench --bench stats_baseline -- --noplot` and checks `rust_core/target/criterion/` exists.
	- Validation command: `rg -n "stats_baseline|target/criterion|cargo bench --bench" .github/workflows/ci.yml`
	- Owner: `@6code`

### Milestone M4 - Runtime and Quality Closure
- [ ] T-BENCH-007 (sequential-only)
	- Objective: Execute runtime validation and record command evidence for benchmark smoke.
	- Target files: `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.exec.md`
	- Dependencies: T-BENCH-006
	- Acceptance criteria: AC-BENCH-003 and AC-BENCH-004 evidenced with exit code `0` and artifact path confirmation.
	- Validation command: `cd rust_core; cargo bench --bench stats_baseline -- --noplot`
	- Owner: `@7exec`

- [ ] T-BENCH-008 (sequential-only)
	- Objective: Perform quality/security review and verify non-threshold CI behavior.
	- Target files: `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.ql.md`
	- Dependencies: T-BENCH-007
	- Acceptance criteria: AC-BENCH-006 and AC-BENCH-007 confirmed; no threshold gating added.
	- Validation command: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`
	- Owner: `@8ql`

### Milestone M5 - Git Handoff Closure
- [ ] T-BENCH-009 (sequential-only)
	- Objective: Prepare narrow staging, branch validation evidence, and handoff summary for commit/PR.
	- Target files: `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.git.md`
	- Dependencies: T-BENCH-008
	- Acceptance criteria: branch still equals `prj0000116-rust-criterion-benchmarks`; staged files limited to plan-approved scope.
	- Validation command: `git branch --show-current`
	- Owner: `@9git`

## Parallel Ownership Map
| Task ID | Parallel mode | File ownership | Lock rule |
|---|---|---|---|
| T-BENCH-001 | sequential-only | `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.test.md` | Exclusive |
| T-BENCH-002 | sequential-only | `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.test.md` | Exclusive |
| T-BENCH-003 | parallel-safe | `rust_core/Cargo.toml` | Disjoint from T-BENCH-004 |
| T-BENCH-004 | parallel-safe | `rust_core/benches/stats_baseline.rs` | Disjoint from T-BENCH-003 |
| T-BENCH-005 | sequential-only | `rust_core/Cargo.toml`, `rust_core/benches/stats_baseline.rs`, `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.code.md` | Convergence owner `@6code` |
| T-BENCH-006 | sequential-only | `.github/workflows/ci.yml` | Exclusive |
| T-BENCH-007 | sequential-only | `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.exec.md` | Exclusive |
| T-BENCH-008 | sequential-only | `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.ql.md` | Exclusive |
| T-BENCH-009 | sequential-only | `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.git.md` | Exclusive |

Convergence rule:
1. T-BENCH-003 and T-BENCH-004 may execute in parallel only after T-BENCH-002 is done.
2. T-BENCH-005 is the mandatory sync barrier and merge decision point before any CI workflow edits.

## Milestones
| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Benchmark contract + red tests | T-BENCH-001, T-BENCH-002 | PLANNED |
| M2 | Baseline benchmark implementation | T-BENCH-003, T-BENCH-004, T-BENCH-005 | PLANNED |
| M3 | CI smoke hook (only) | T-BENCH-006 | PLANNED |
| M4 | Runtime + quality closure | T-BENCH-007, T-BENCH-008 | PLANNED |
| M5 | Git handoff closure | T-BENCH-009 | PLANNED |

## Validation Commands by Milestone
### M1
```powershell
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
cd rust_core; cargo bench --bench stats_baseline -- --help
```

### M2
```powershell
cd rust_core; cargo bench --bench stats_baseline -- --help
cd rust_core; cargo bench --bench stats_baseline -- --noplot
```

### M3
```powershell
rg -n "stats_baseline|target/criterion|cargo bench --bench" .github/workflows/ci.yml
```

### M4
```powershell
cd rust_core; cargo bench --bench stats_baseline -- --noplot
python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py
```

### M5
```powershell
git branch --show-current
git status --short
```

## Dependencies and Sequence
1. T-BENCH-001 -> T-BENCH-002.
2. T-BENCH-002 -> parallel wave (T-BENCH-003 + T-BENCH-004).
3. Parallel wave -> T-BENCH-005 convergence.
4. T-BENCH-005 -> T-BENCH-006 -> T-BENCH-007 -> T-BENCH-008 -> T-BENCH-009.

## Handoff Package to @5test
1. Start with T-BENCH-001 and T-BENCH-002 only.
2. Keep tests/contract scoped to benchmark baseline and CI smoke behavior.
3. Do not introduce threshold/regression gate assertions in this slice.
