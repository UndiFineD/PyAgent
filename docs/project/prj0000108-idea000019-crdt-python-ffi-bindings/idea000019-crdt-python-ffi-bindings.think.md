# idea000019-crdt-python-ffi-bindings - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-31_

## Root Cause Analysis
1. Bridge mismatch: CRDT behavior is implemented in `rust_core/crdt/` as a standalone CLI binary, while Python currently calls it via subprocess in `src/core/crdt_bridge.py` instead of using in-process Rust bindings.
2. Packaging split: `rust_core/Cargo.toml` already uses PyO3/maturin for Python extension delivery, but `rust_core/crdt/Cargo.toml` is a separate crate with no PyO3 exposure.
3. Performance and reliability ceiling: temp-file plus process-spawn patterns in the current bridge increase latency, add platform variance, and widen failure modes compared to direct FFI.

## Discovery Evidence
### Literature Review (Repository)
- `docs/project/ideas/idea000019-crdt-python-ffi-bindings.md` identifies the intended CRDT Python FFI gap.
- `src/core/crdt_bridge.py` confirms subprocess/file-based integration.
- `rust_core/Cargo.toml` shows current PyO3 extension-module packaging path.
- `rust_core/crdt/Cargo.toml` shows CRDT crate is currently non-PyO3.
- `.github/workflows/ci.yml` already uses maturin for `rust_core`, proving established build path.

### Alternative Enumeration
Three distinct options were explored:
- Option A: keep standalone CRDT crate and harden subprocess bridge.
- Option B: integrate CRDT APIs into existing `rust_core` PyO3 module.
- Option C: ship CRDT as a separate PyO3 extension package/crate.

### Prior-Art Search
- `docs/project/prj0000056/rust-async-transport-activation.think.md`
- `docs/project/prj0000067/rust-file-watcher.think.md`
- `docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.think.md`
- `docs/architecture/archive/10adr-practice.md`

### Constraint Mapping
- Branch gate must remain `prj0000108-idea000019-crdt-python-ffi-bindings` from `idea000019-crdt-python-ffi-bindings.project.md`.
- @2think phase must stay documentation-only and in project artifact scope.
- Policy compliance required with `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
- Architecture direction prefers Rust acceleration with thin Python orchestration (`.github/copilot-instructions.md`).
- Existing CI/build pipelines already assume maturin-based extension path for `rust_core`.

### Stakeholder Impact
- @3design: must select extension topology (single-module vs split-module) and ADR needs.
- @4plan/@5test: need deterministic acceptance tests for merge correctness, failure handling, and packaging behavior.
- @6code: depends on clear ownership boundary between `rust_core` and `rust_core/crdt`.
- @7exec/@8ql: require runtime checks for cross-platform builds and subprocess-removal security posture.
- @9git: must stage narrow docs changes only in this phase.

### External Pattern Evidence (Approved Domains)
- `https://github.com/PyO3/pyo3` emphasizes direct extension-module patterns (`#[pymodule]`, `#[pyfunction]`) and matching module names for import stability.
- `https://github.com/PyO3/maturin` documents mixed Rust/Python packaging patterns and recommends predictable module naming with `maturin develop/build` flows.
- `https://github.com/automerge/automerge` describes CRDT core orientation and notes Rust APIs are lower-level, indicating wrapper design should provide Python-safe higher-level contracts.

## Options
### Option A - Harden Existing Subprocess Bridge (No PyO3 for CRDT)
Keep CRDT as a standalone binary and improve the Python bridge reliability without introducing direct FFI.

Evidence anchors:
- `src/core/crdt_bridge.py`
- `rust_core/crdt/src/main.rs`
- `tests/test_rust_crdt_merge.py`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Lowest immediate implementation complexity.
- Minimal Rust module refactor required.
- Preserves existing binary behavior and tests.

Cons:
- Does not satisfy core objective of Python FFI bindings.
- Retains process/file overhead and transient-file risk surface.
- Harder to evolve typed Python API ergonomics.

SWOT:
- Strengths: fast stabilization path, minimal migration.
- Weaknesses: objective mismatch and runtime overhead.
- Opportunities: can serve as short-lived fallback path.
- Threats: technical debt hardens around subprocess boundary.

Security risk analysis with testability mapping:
1. Risk: subprocess argument/path injection regressions.
	- Likelihood: M | Impact: H
	- Mitigation: strict command construction and path validation.
	- Testability signal: negative subprocess invocation tests with malicious path payloads.
2. Risk: temporary-file exposure or race conditions.
	- Likelihood: M | Impact: M
	- Mitigation: secure temp handling and restrictive file permissions.
	- Testability signal: concurrency stress tests for temp-dir collisions and leakage checks.
3. Risk: platform-specific binary discovery failures.
	- Likelihood: M | Impact: M
	- Mitigation: deterministic binary resolution + explicit fallback errors.
	- Testability signal: matrix smoke tests on Windows/Linux path resolution.

### Option B - Integrate CRDT into Existing rust_core PyO3 Module (Recommended)
Expose CRDT merge operations as `#[pyfunction]` within the existing `rust_core` extension path, while keeping Python layer as thin orchestration.

Evidence anchors:
- `rust_core/Cargo.toml`
- `rust_core/src/lib.rs`
- `.github/workflows/ci.yml`
- `docs/project/prj0000056/rust-async-transport-activation.think.md`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Strongest alignment to project goal (true Python FFI bindings).
- Reuses proven PyO3+maturin pipeline already present in repository.
- Reduces latency and operational complexity versus subprocess bridge.

Cons:
- Requires CRDT API refactor from CLI-style entrypoints to library functions.
- Increases coupling between `rust_core` and CRDT evolution if boundaries are unclear.
- Demands careful error mapping from Rust to Python exceptions.

SWOT:
- Strengths: high objective fit, best runtime path, proven delivery channel.
- Weaknesses: moderate refactor complexity.
- Opportunities: establish reusable Rust-to-Python contract pattern for future crates.
- Threats: poorly scoped integration could bloat `rust_core` surface.

Security risk analysis with testability mapping:
1. Risk: unsafe or overly permissive Python-exposed Rust interfaces.
	- Likelihood: M | Impact: H
	- Mitigation: explicit input schema validation and bounded operations.
	- Testability signal: property/fuzz tests on Python boundary inputs.
2. Risk: panic propagation across FFI boundary.
	- Likelihood: L | Impact: H
	- Mitigation: convert internal errors to `PyResult` with clear exception classes.
	- Testability signal: failure-path tests asserting deterministic Python exceptions.
3. Risk: serialization inconsistencies between Python dict and Rust CRDT structures.
	- Likelihood: M | Impact: M
	- Mitigation: canonical JSON/value conversion layer with round-trip assertions.
	- Testability signal: round-trip parity tests against current merge corpus.

### Option C - Separate CRDT PyO3 Extension Package
Create a dedicated CRDT Python extension crate/package (for example, `rust_core_crdt_py`) and keep main `rust_core` extension unchanged.

Evidence anchors:
- `rust_core/crdt/Cargo.toml`
- `rust_core/Cargo.toml`
- `docs/project/prj0000067/rust-file-watcher.think.md`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Clear separation of concerns and ownership.
- Limits impact radius on existing `rust_core` module.
- Allows independent versioning cadence.

Cons:
- Adds packaging/distribution complexity (extra wheel/module coordination).
- Higher integration overhead in CI and import pathways.
- Risk of duplicated conversion utilities and drift.

SWOT:
- Strengths: isolation and modularity.
- Weaknesses: operational overhead and dual-module maintenance.
- Opportunities: future dedicated CRDT release cadence.
- Threats: module/version skew and support burden.

Security risk analysis with testability mapping:
1. Risk: version skew between extension packages causes undefined behavior.
	- Likelihood: M | Impact: H
	- Mitigation: strict compatibility matrix and pinned version contracts.
	- Testability signal: compatibility matrix tests in CI for paired versions.
2. Risk: divergent error/validation semantics between modules.
	- Likelihood: M | Impact: M
	- Mitigation: shared error model specification and contract tests.
	- Testability signal: cross-module contract conformance tests.
3. Risk: supply-chain increase from additional artifact lifecycle.
	- Likelihood: M | Impact: M
	- Mitigation: unified release signing and dependency scanning across both packages.
	- Testability signal: release-pipeline checks asserting signed artifacts + audit pass.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---:|---:|---:|
| Alignment to CRDT Python FFI objective | 1 | 5 | 4 |
| Reuse of existing repository capabilities | 3 | 5 | 3 |
| Delivery risk (higher score = lower risk) | 4 | 3 | 2 |
| Runtime performance and reliability | 2 | 5 | 4 |
| Security/governance controllability | 3 | 4 | 3 |
| Testability and validation clarity | 3 | 5 | 3 |
| Total | 16 | 27 | 19 |

## Recommendation
**Select Option B (Integrate CRDT into existing `rust_core` PyO3 module).**

Rationale:
1. It is the best direct fit to idea000019 and eliminates the current subprocess bridge bottleneck.
2. It reuses proven project capabilities (PyO3 extension registration and maturin CI paths) instead of introducing an additional packaging stack.
3. It offers the strongest risk-to-testability profile for an incremental rollout: direct boundary tests, parity tests versus current merge behavior, and deterministic Python exception mapping.

Historical prior-art grounding:
- `docs/project/prj0000056/rust-async-transport-activation.think.md`
- `docs/project/prj0000067/rust-file-watcher.think.md`
- `docs/project/prj0000095-source-stub-remediation/prj0000095-source-stub-remediation.think.md`

Reject reasons:
- Option A is rejected because it does not actually deliver FFI bindings and prolongs subprocess operational risk.
- Option C is rejected for v1 because it increases packaging complexity before core API contracts are stabilized.

## Open Questions (for @3design)
1. Should CRDT functions be exposed under the existing `rust_core` module namespace or an internal submodule namespace to preserve API clarity?
2. What is the minimal Python-facing CRDT contract for v1 (single merge entrypoint vs typed operation surface)?
3. Is an ADR update required in this cycle to codify extension topology and rollout constraints per `docs/architecture/archive/10adr-practice.md`?
4. What migration/deprecation window is acceptable for retiring subprocess fallback in `src/core/crdt_bridge.py`?
5. Which cross-platform build/test matrix is mandatory before defaulting to FFI path in runtime?

## Handoff Note
@2think exploration is complete with three options, full tradeoff analysis, SWOT and security mappings, and a clear lead recommendation: **Option B**.
