# rust-criterion-benchmarks - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-03_

## Root Cause Analysis
1. There is no Rust-native benchmark harness in `rust_core`: no `benches/` directory and no Criterion configuration in `rust_core/Cargo.toml`.
2. Existing benchmark signal is Python-side only (`performance/metrics_bench.py`) and focuses on loop behavior around `metrics_engine`, not direct Rust microbench coverage.
3. Performance-sensitive Rust functions exist (`rust_core/src/stats/general.rs`, `rust_core/src/stats/metrics.rs`), but there is no crate-level benchmark regression contract.

## Discovery Evidence
### Literature Review (Repository)
- `docs/project/ideas/idea000017-rust-criterion-benchmarks.md`
- `rust_core/Cargo.toml`
- `performance/metrics_bench.py`
- `rust_core/src/stats/general.rs`
- `rust_core/src/stats/metrics.rs`

### Alternative Enumeration
- Option A: Rust-native Criterion minimal slice (manual invocation only).
- Option B: Rust-native Criterion + lightweight CI smoke benchmark lane.
- Option C: Keep Python benchmark as primary signal and defer Rust Criterion to later.

### Prior-Art Search
- `docs/architecture/1agents.md`
- `docs/architecture/archive/9operations-observability.md`
- `docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md`
- `docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md`

### Constraint Mapping
- Must stay on branch `prj0000116-rust-criterion-benchmarks`.
- @2think scope is documentation and analysis only (no production code changes).
- Must comply with `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
- Project intent explicitly requests governance-compliant minimal first slice for Rust-side Criterion.
- Validation command required: `python -m pytest -q tests/docs/test_agent_workflow_policy_docs.py`.

### Stakeholder Impact
- @3design: chooses benchmark topology and CI integration depth.
- @4plan/@5test: defines acceptance checks for determinism and runtime budgets.
- @6code: implements Cargo/bench files and any workflow hooks.
- @7exec/@8ql: validates runtime stability and quality/security impact.
- @9git: enforces narrow staging for project-scope docs changes.

### External Pattern Evidence (Allowed Domains)
- `https://crates.io/crates/criterion` (quickstart + stable Rust benchmark pattern).
- `https://github.com/bheisler/criterion.rs` (project-level guidance and benchmark workflow context).

## Options
### Option A - Minimal Rust Criterion Slice (Manual Run, No CI Gate Yet)
Add Criterion to `rust_core` dev dependencies and create a minimal benchmark target for one or two `stats` functions. Keep execution manual (`cargo bench`) in v1.

Evidence anchors:
- `rust_core/Cargo.toml`
- `rust_core/src/stats/general.rs`
- `rust_core/src/stats/metrics.rs`
- `performance/metrics_bench.py`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Tradeoffs:
- Complexity: Medium
- CI runtime cost: Low
- Maintenance: Low-Medium

Pros:
- Delivers direct Rust-layer benchmark capability quickly.
- Keeps governance-compliant minimal first slice.
- Avoids immediate CI flakiness risk from benchmark variance.

Cons:
- No automatic regression enforcement in CI.
- Risk of benchmark drift if contributors do not run locally.

SWOT:
- Strengths: fastest path to true Rust benchmark coverage.
- Weaknesses: weak enforcement without CI signal.
- Opportunities: clean foundation for later CI rollout.
- Threats: manual-only usage can become stale.

Security risk analysis and testability mapping:
1. Threat vector: accidental benchmark inputs that trigger panics in Rust benchmark path.
	- Likelihood: M | Impact: M
	- Mitigation: bound and sanitize benchmark fixtures.
	- Testability signal: benchmark smoke run in local dev task.
2. Threat vector: benchmark harness introduces non-deterministic external dependencies.
	- Likelihood: L | Impact: M
	- Mitigation: isolate pure computation benches only.
	- Testability signal: repeated local run variance thresholds.
3. Threat vector: stale benchmark contracts over time.
	- Likelihood: M | Impact: M
	- Mitigation: document required benchmark touchpoints in plan artifacts.
	- Testability signal: docs-policy/project artifact review in each project cycle.

### Option B - Minimal Rust Criterion + Lightweight CI Smoke Benchmark (Recommended)
Implement the same minimal Criterion harness as Option A, plus a lightweight CI benchmark smoke step that validates harness health (not strict performance thresholds) to prevent silent breakage.

Evidence anchors:
- `rust_core/Cargo.toml`
- `.github/workflows/ci.yml`
- `docs/architecture/archive/9operations-observability.md`
- `docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Tradeoffs:
- Complexity: Medium-High
- CI runtime cost: Medium
- Maintenance: Medium

Pros:
- Provides Rust-native benchmark capability with immediate anti-drift protection.
- Keeps first slice small while improving governance confidence.
- Aligns with observability guidance to track regressions with measurable benchmarks.

Cons:
- Adds CI minutes and potential platform variance management.
- Requires careful scope to avoid turning into a heavy benchmark gate prematurely.

SWOT:
- Strengths: best balance of capability and enforceability.
- Weaknesses: more setup burden than purely local harness.
- Opportunities: evolve smoke checks into threshold-based regression checks later.
- Threats: if CI step is too heavy/noisy, contributors may bypass or disable it.

Security risk analysis and testability mapping:
1. Threat vector: CI benchmark execution instability causes false negatives/positives.
	- Likelihood: M | Impact: M
	- Mitigation: smoke-only assertions (exit success + basic output validation), no strict perf thresholds in v1.
	- Testability signal: CI job pass-rate and retry-rate trend.
2. Threat vector: benchmark code path enables unsafe/expensive workloads in CI.
	- Likelihood: L | Impact: M
	- Mitigation: benchmark scope restricted to bounded pure functions in `stats`.
	- Testability signal: benchmark runtime budget checks in CI logs.
3. Threat vector: benchmark pipeline obscures actual regressions due to noisy environment.
	- Likelihood: M | Impact: H
	- Mitigation: treat v1 as harness-health gate; defer threshold enforcement until stability data is collected.
	- Testability signal: periodic variance review reports before enabling hard gates.

### Option C - Python-Only Benchmark Continuation (Defer Rust Criterion)
Continue with Python benchmark (`performance/metrics_bench.py`) and postpone Rust Criterion setup.

Evidence anchors:
- `performance/metrics_bench.py`
- `src/observability/stats/metrics_engine.py`
- `docs/project/ideas/idea000017-rust-criterion-benchmarks.md`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Tradeoffs:
- Complexity: Low
- CI runtime cost: Low
- Maintenance: Low (short-term), High (long-term capability debt)

Pros:
- No Rust benchmark setup effort in current slice.
- Lowest immediate disruption risk.

Cons:
- Fails to meet stated project objective for Rust-side Criterion benchmarks.
- Keeps blind spot at Rust layer and weakens regression detection at kernel level.

SWOT:
- Strengths: near-zero short-term implementation effort.
- Weaknesses: objective mismatch and technical debt continuation.
- Opportunities: none meaningful for this project intent.
- Threats: long-term performance regressions hidden behind Python-layer noise.

Security risk analysis and testability mapping:
1. Threat vector: Rust regressions remain undetected until production-like workloads.
	- Likelihood: M | Impact: H
	- Mitigation: none within this option beyond ad hoc profiling.
	- Testability signal: absence of direct signal (this is the core weakness).
2. Threat vector: false confidence from Python-only benchmark coverage.
	- Likelihood: H | Impact: M
	- Mitigation: explicit documentation warning that Rust layer is unbenchmarked.
	- Testability signal: review checklist requiring acknowledgment of blind spot.
3. Threat vector: delayed benchmark adoption increases future migration risk.
	- Likelihood: M | Impact: M
	- Mitigation: time-boxed follow-up project commitment.
	- Testability signal: scheduled project registration in kanban.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---:|---:|---:|
| Goal alignment (Rust Criterion in rust_core) | 4 | 5 | 1 |
| Complexity (higher = simpler) | 4 | 3 | 5 |
| CI runtime cost (higher = cheaper) | 5 | 3 | 5 |
| Maintenance burden (higher = lower burden) | 4 | 3 | 2 |
| Regression detection strength | 2 | 4 | 1 |
| Governance confidence | 3 | 5 | 2 |
| Total | 22 | 23 | 16 |

## Recommendation
**Option B** - Minimal Rust Criterion plus lightweight CI smoke benchmark.

Rationale:
1. Best balance for a minimal first slice: it delivers Rust-native Criterion quickly while adding anti-drift guardrails.
2. Fits repository architecture direction that favors Rust performance paths with measurable regressions (`docs/architecture/1agents.md`, `docs/architecture/archive/9operations-observability.md`).
3. Mirrors recent prior-art pattern: introduce capability first with bounded validation, then tighten gates after stability data (`docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md`, `docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md`).

Risk-to-testability summary for the recommendation:
- CI variance risk -> smoke-only pass criteria and runtime budget checks.
- Benchmark drift risk -> mandatory CI harness-health execution.
- Over-scoping risk -> v1 target limited to one or two pure `stats` functions.

Concrete file list for downstream design/code:
- `rust_core/Cargo.toml`
- `rust_core/benches/` (new directory)
- `rust_core/benches/stats_benchmark.rs` (or equivalent minimal bench file)
- `.github/workflows/ci.yml` (only if Option B CI smoke step is accepted)
- `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.design.md`
- `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.plan.md`

## Open Questions
1. Should v1 benchmark scope include only `stats` pure functions, or include additional Rust kernels in the first slice?
2. For CI smoke execution, should the benchmark run on one OS only initially (for variance control) or a matrix?
3. Should benchmark outputs be stored as build artifacts in v1, or deferred until threshold gating is introduced?
4. Is an ADR update required if CI benchmark smoke is added, or can this remain within project design/plan artifacts?
5. What is the exact promotion criterion from smoke-only checks to regression-threshold enforcement?
