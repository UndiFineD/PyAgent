# rust-criterion-benchmarks - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-03_

## Problem Statement and Goals
Project `prj0000116-rust-criterion-benchmarks` needs a minimal, Rust-native performance benchmark baseline for `rust_core/` using Criterion, with a lightweight CI smoke signal to prevent silent harness drift.

Goals for this slice:
1. Add a stable benchmark harness for selected pure `stats` functions in `rust_core`.
2. Define deterministic benchmark naming and command entry points for local and CI execution.
3. Produce baseline benchmark artifacts that are machine-checkable without enforcing strict performance thresholds yet.

## Selected Option
**Option B (from think artifact) - Minimal Rust Criterion + lightweight CI smoke benchmark.**

Rationale:
1. Preserves a minimal-first implementation footprint while adding anti-drift enforcement.
2. Aligns with project intent to establish Rust-side benchmark coverage now, not deferred.
3. Keeps risk manageable by using smoke-style pass criteria (harness health + bounded runtime), not noisy hard performance gates.

## Architecture Overview
The design introduces a thin benchmark lane around `rust_core`:
1. `rust_core/Cargo.toml` gains Criterion dev dependency and bench target registration.
2. A new benchmark module under `rust_core/benches/` runs microbenchmarks against bounded, deterministic `stats`-layer functions.
3. CI invokes a smoke benchmark command on project/main PR lanes and validates harness execution success and expected output artifact presence.

Data/control flow:
1. Developer or CI runs `cargo bench` in `rust_core`.
2. Criterion executes named benchmark groups/functions.
3. Criterion writes output under `rust_core/target/criterion/**`.
4. CI treats successful execution + artifact generation as pass; no threshold comparison in v1.

## New/Changed Files (Exact Paths)
1. `rust_core/Cargo.toml` (changed)
2. `rust_core/benches/stats_baseline.rs` (new)
3. `.github/workflows/ci.yml` (changed, minimal smoke hook only)
4. `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.plan.md` (future @4plan output)
5. `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.test.md` (future @5test output)

Notes:
1. `rust_core/src/lib.rs` export changes are **not required by default**; add only if selected benchmark targets are not currently reachable from benches.
2. No additional CI workflow files are introduced in this slice.

## Interfaces and Contracts

### IFACE-BENCH-001 Benchmark File Contract
1. File: `rust_core/benches/stats_baseline.rs`.
2. Must compile with stable Rust toolchain already used by repository.
3. Must define Criterion benchmark groups/functions with deterministic names.

Naming contract:
1. Group name pattern: `stats/<module_or_domain>` (example: `stats/general`).
2. Benchmark ID pattern: `<function_name>/<dataset_tag>` (example: `compute_entropy/small`).
3. Full benchmark display path must be predictable: `stats/<module_or_domain>/<function_name>/<dataset_tag>`.

### IFACE-BENCH-002 Local Command Entry Point Contract
1. Primary command: `cargo bench --bench stats_baseline` from `rust_core/`.
2. Optional full run command: `cargo bench` from `rust_core/`.
3. Command returns exit code `0` when harness is healthy.

### IFACE-BENCH-003 CI Smoke Command Contract
1. CI step runs a bounded smoke command from `rust_core/`:
	- `cargo bench --bench stats_baseline -- --noplot`
2. CI step pass criteria:
	- Exit code `0`.
	- Criterion artifact directory exists: `rust_core/target/criterion/`.
3. CI step must not enforce statistical regression thresholds in v1.

### IFACE-BENCH-004 Artifact Contract
On successful run, expected outputs:
1. `rust_core/target/criterion/` directory created.
2. At least one benchmark report path matching benchmark names in IFACE-BENCH-001.
3. CI logs include benchmark group/function labels for traceability.

### IFACE-BENCH-005 Scope Boundary Contract
Allowed implementation scope for this project:
1. `rust_core/Cargo.toml`
2. `rust_core/benches/*.rs`
3. `.github/workflows/ci.yml` (single minimal smoke step only)

Disallowed in this slice:
1. Broad refactors of Rust core logic.
2. Performance threshold policy enforcement.
3. Multi-OS benchmark matrix expansion.

## Acceptance Criteria
| AC ID | Requirement | Measurable Check | Evidence Owner |
|---|---|---|---|
| AC-BENCH-001 | Criterion is configured for `rust_core` benchmark target | `cargo bench --bench stats_baseline -- --help` exits `0` | @6code/@7exec |
| AC-BENCH-002 | Benchmark file follows naming contract | Source review confirms `stats/<domain>` group and `<function>/<dataset>` IDs | @5test/@8ql |
| AC-BENCH-003 | Local benchmark smoke run succeeds | `cd rust_core && cargo bench --bench stats_baseline -- --noplot` exits `0` | @7exec |
| AC-BENCH-004 | Criterion artifacts are generated | `rust_core/target/criterion/` exists after run | @7exec |
| AC-BENCH-005 | CI includes lightweight benchmark smoke hook | `.github/workflows/ci.yml` contains smoke step invoking IFACE-BENCH-003 command | @6code/@8ql |
| AC-BENCH-006 | CI smoke hook is non-threshold and bounded | Workflow checks only command success + artifact presence; no fail-on-regression rule | @8ql |
| AC-BENCH-007 | Scope remains minimal-first | Diff limited to allowed paths in IFACE-BENCH-005 | @9git |

## Interface-to-Task Traceability (For @4plan)
| Interface ID | Planned Task ID | Task Intent |
|---|---|---|
| IFACE-BENCH-001 | TSK-BENCH-001 | Add `stats_baseline` Criterion benchmark file with deterministic naming |
| IFACE-BENCH-002 | TSK-BENCH-002 | Wire `rust_core/Cargo.toml` bench target and dev dependency |
| IFACE-BENCH-003 | TSK-BENCH-003 | Add CI smoke benchmark invocation in `ci.yml` |
| IFACE-BENCH-004 | TSK-BENCH-004 | Add artifact existence assertion in CI smoke step |
| IFACE-BENCH-005 | TSK-BENCH-005 | Add scope guard checks in plan/test artifacts for narrow staging |

## Non-Functional Requirements
1. Performance: Smoke benchmark completes within a practical CI budget (target <= 120 seconds on ubuntu-latest).
2. Security: Benchmark inputs remain bounded and deterministic; no external network, secrets, or untrusted runtime inputs.
3. Testability: Commands and artifact paths are explicit and machine-verifiable.
4. Maintainability: Naming contract and single-bench entry point reduce operational ambiguity.

## Risk and Rollback Plan

### Risks
1. CI variance/noise may create unstable timings.
2. Benchmark scope creep may expand into non-deterministic or expensive paths.
3. Developers may misinterpret smoke lane as a strict performance gate.

### Mitigations
1. Keep v1 as harness-health gate only; do not compare against baseline thresholds.
2. Restrict to bounded pure `stats` targets in initial benchmark set.
3. Document explicit non-goals and pass criteria in plan/test artifacts.

### Rollback
1. Revert only benchmark smoke step in `.github/workflows/ci.yml` if CI instability is introduced.
2. Keep local Criterion harness in place unless it blocks core development.
3. If full rollback required, remove `stats_baseline` target and Criterion dev dependency in a narrow revert commit.

## Non-Goals (Scope Guard)
1. No strict regression-threshold gating in CI for this slice.
2. No benchmark matrix across multiple OS/toolchains.
3. No conversion of existing Python benchmarks; Python and Rust benchmark lanes remain complementary.
4. No broad Rust module export refactor unless strictly required for benchmark reachability.
5. No new ADR unless design changes architecture beyond benchmark harness + smoke CI scope.

## ADR Impact
No ADR update is required for this minimal benchmark harness slice because it does not alter core system architecture, runtime boundaries, or trust model.

## Open Questions for @4plan
1. Which exact `stats` functions should be the initial benchmark targets (`1-2` functions maximum)?
2. Should CI artifact retention include Criterion reports in v1, or only assert local path existence?
3. Do we enforce a stricter runtime cap than 120 seconds after first execution data is captured?
