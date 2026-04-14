# rust-sub-crate-unification - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-03_

## Root Cause Analysis
1. `rust_core/crdt/`, `rust_core/p2p/`, and `rust_core/security/` are currently standalone crates with independent `Cargo.toml` and `Cargo.lock` files, so dependency resolution is fragmented instead of governed as one graph.
2. Multiple lockfiles already show version skew and duplication risks. Examples include `base64` (`0.22.1` in `rust_core/Cargo.toml` vs `0.21.x` in standalone crates) and drift potential around shared ecosystem crates (`clap`, `anyhow`, `tokio`, `pyo3`).
3. Existing CI/build/test flows mix root-crate assumptions and sub-crate assumptions:
	- `.github/workflows/ci.yml` runs benchmark smoke from `rust_core/` (`cargo bench --bench stats_baseline -- --noplot`).
	- `install.ps1` builds extension with `maturin develop --manifest-path rust_core/Cargo.toml`.
	- tests target standalone binaries and lockfiles (for example `tests/test_security_rotation.py`, `tests/test_rust_p2p_binary.py`, `tests/security/test_rust_p2p_deps.py`).
4. Security-patch governance for `p2p` currently relies on crate-local `[patch.crates-io]` in `rust_core/p2p/Cargo.toml`; Cargo workspace rules indicate patch governance is recognized at workspace root, which is a risk if topology changes are not explicit.

## Discovery Evidence
### Literature Review (Repository)
- `docs/project/ideas/idea000018-rust-sub-crate-unification.md`
- `rust_core/Cargo.toml`, `rust_core/Cargo.lock`
- `rust_core/crdt/Cargo.toml`, `rust_core/crdt/Cargo.lock`
- `rust_core/p2p/Cargo.toml`, `rust_core/p2p/Cargo.lock`
- `rust_core/security/Cargo.toml`, `rust_core/security/Cargo.lock`
- `install.ps1`, `.github/workflows/ci.yml`
- `tests/test_security_rotation.py`, `tests/test_rust_p2p_binary.py`, `tests/security/test_rust_p2p_deps.py`

### Alternative Enumeration
- Option A: Keep standalone crates and add lockfile/dependency-governance automation only.
- Option B: Unify under a root workspace at `rust_core/Cargo.toml` (recommended).
- Option C: Create a virtual workspace split (move current root package, larger migration).

### Prior-Art Search (Repository)
- `docs/project/archive/prj0000005/prj005-llm-swarm-architecture.project.md` (origin of separate `p2p/crdt/security` crates)
- `docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md` (Rust topology and PyO3 integration tradeoffs)
- `docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md` (existing Rust-core integration direction)
- `docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.think.md` (recent Cargo/CI benchmark governance pattern)

### Constraint Mapping
- Branch gate: expected branch is `prj0000117-rust-sub-crate-unification` from the project overview.
- @2think scope remains docs-only; no production Cargo changes in this phase.
- Must align with `docs/project/code_of_conduct.md` and `docs/project/naming_standards.md`.
- Build path must preserve `maturin` compatibility for `rust_core/Cargo.toml`.
- CI benchmark smoke in `.github/workflows/ci.yml` should remain deterministic during migration.
- Windows and Linux behavior must remain valid for binary-smoke tests and extension build paths.

### Stakeholder Impact
- @3design: must choose workspace topology that preserves `maturin` build contract and sub-crate binary contracts.
- @4plan/@5test: must define lockfile, dependency, and command migration acceptance criteria.
- @6code: will touch Cargo manifests/lockfiles and likely test command wiring.
- @7exec/@8ql: must validate runtime, supply-chain, and patch-governance outcomes.
- @9git: must enforce narrow scope and guard against unrelated lockfile churn.

### Risk Enumeration Baseline
- Dependency skew leading to divergent behavior across crates.
- Security patch scope regressions if `[patch.crates-io]` ownership is misplaced during workspace conversion.
- CI breakage due to command context shifts (`cargo bench`, crate-specific build/test commands).

### External Pattern Evidence (Allowed Domains)
- Cargo workspace reference (`github.com/rust-lang/cargo/.../workspaces.md`): shared workspace `Cargo.lock`, shared target output, and root-only handling of `[patch]`/profiles.
- Cargo override reference (`github.com/rust-lang/cargo/.../overriding-dependencies.md`): root-level `[patch]` semantics and transitive override behavior.

## Options
### Option A - Keep Standalone Crates, Add Governance Automation
Keep current crate topology and lockfiles; add scripts/checks to detect dependency drift and enforce synchronized version policy where needed.

Evidence anchors:
- `rust_core/crdt/Cargo.toml`
- `rust_core/p2p/Cargo.toml`
- `rust_core/security/Cargo.toml`
- `tests/security/test_rust_p2p_deps.py`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Lowest immediate migration effort.
- Minimal disruption to existing binary and test command paths.
- Fast rollback (mostly policy/script changes).

Cons:
- Does not actually unify the dependency graph.
- Ongoing maintenance burden across multiple lockfiles.
- Security and duplication risks remain structurally present.

SWOT:
- Strengths: low change footprint, low short-term instability.
- Weaknesses: core objective under-fulfilled.
- Opportunities: can be a temporary risk-control bridge.
- Threats: slow drift accumulation and repeated dependency incidents.

Security risk analysis with testability mapping:
1. Risk: cross-crate CVE remediation drift.
	- Likelihood: M | Impact: H
	- Mitigation: dependency policy checker over all sub-crates.
	- Testability signal: CI drift test that fails on version-policy mismatch.
2. Risk: inconsistent cryptographic dependency updates between security and other crates.
	- Likelihood: M | Impact: H
	- Mitigation: explicit allowlist/denylist and periodic audit automation.
	- Testability signal: scheduled audit diff report by crate.
3. Risk: lockfile divergence causes non-reproducible builds.
	- Likelihood: H | Impact: M
	- Mitigation: lockfile regeneration policy and gate.
	- Testability signal: deterministic build matrix comparing crate lock resolution snapshots.

### Option B - Root Workspace Unification at rust_core/Cargo.toml (Recommended)
Retain `rust_core` root package for `maturin`, add `[workspace]` and members for `crdt`, `p2p`, `security` (and optionally `runtime`), move patch/dependency governance to workspace root, and converge to one lockfile strategy.

Evidence anchors:
- `rust_core/Cargo.toml`
- `install.ps1`
- `.github/workflows/ci.yml`
- `rust_core/p2p/Cargo.toml`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Delivers direct objective: unified dependency graph and lockfile strategy.
- Preserves existing root-manifest path expected by `maturin` and benchmark CI.
- Centralizes `[patch]` and dependency governance in one place.

Cons:
- Moderate migration complexity (manifest and command rewiring).
- Some crate-specific test commands may need explicit `-p` usage.
- Lockfile churn likely in first migration wave.

SWOT:
- Strengths: best objective fit with manageable migration scope.
- Weaknesses: non-trivial coordination across tests and scripts.
- Opportunities: establish shared `workspace.dependencies` and stronger supply-chain posture.
- Threats: accidental command breakage if package selection is not explicit.

Security risk analysis with testability mapping:
1. Risk: `[patch.crates-io]` migration error drops the p2p yamux security patch.
	- Likelihood: M | Impact: H
	- Mitigation: move/verify patch at workspace root and assert dependency graph.
	- Testability signal: CI check proving patched crate source/version is active.
2. Risk: workspace-level updates introduce incompatible transitive versions.
	- Likelihood: M | Impact: M
	- Mitigation: staged lockfile convergence with crate-level smoke tests.
	- Testability signal: per-crate build/test matrix via `cargo test -p <pkg>` and binary smoke tests.
3. Risk: command-context regressions in CI/install scripts.
	- Likelihood: M | Impact: M
	- Mitigation: explicit manifest-path/package flags and command contract tests.
	- Testability signal: update-and-pass of `tests/ci/test_ci_workflow.py` and install-structure tests.

### Option C - Virtual Workspace Split (Move Root rust_core Package)
Create a pure virtual workspace root and relocate current `rust_core` package into a subdirectory crate, then migrate all commands to the new path structure.

Evidence anchors:
- `rust_core/Cargo.toml`
- `install.ps1`
- `docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md`

Research coverage:
- Literature review: yes
- Alternative enumeration: yes
- Prior-art search: yes
- Constraint mapping: yes
- Stakeholder impact: yes
- Risk enumeration: yes

Pros:
- Clean long-term monorepo-style workspace structure.
- Strong explicit separation between workspace governance and package implementation.

Cons:
- Highest migration effort.
- Highest CI/install command breakage risk due to path changes.
- Harder rollback once package paths are moved.

SWOT:
- Strengths: architecturally clean end-state.
- Weaknesses: heavy churn for little near-term additional value over Option B.
- Opportunities: future large-scale Rust crate expansion.
- Threats: broad disruption to Python-extension build pipeline.

Security risk analysis with testability mapping:
1. Risk: path migration mistakes break secure build/deploy assumptions.
	- Likelihood: M | Impact: H
	- Mitigation: phased path migration and dual-path transition checks.
	- Testability signal: path contract tests for install and CI manifests.
2. Risk: temporary duplication of manifests increases attack surface for configuration drift.
	- Likelihood: M | Impact: M
	- Mitigation: strict transition window and deprecation checklist.
	- Testability signal: manifest inventory test that enforces expected single-source structure.
3. Risk: rollback complexity under partial migration.
	- Likelihood: M | Impact: M
	- Mitigation: tagged migration checkpoints and atomic PR slicing.
	- Testability signal: rollback rehearsal in dry-run branch with command parity checks.

## Decision Matrix
| Criterion | Option A | Option B | Option C |
|---|---:|---:|---:|
| Complexity (higher = simpler) | 5 | 3 | 1 |
| Risk (higher = lower risk) | 3 | 4 | 2 |
| Migration effort (higher = less effort) | 5 | 3 | 1 |
| Rollback ease (higher = easier) | 5 | 3 | 1 |
| CI impact (higher = lower disruption) | 4 | 3 | 1 |
| Objective fit: true unification | 1 | 5 | 4 |
| Dependency-governance strength | 2 | 5 | 4 |
| Total | 25 | 26 | 14 |

## Recommendation
**Option B - Root workspace unification at `rust_core/Cargo.toml`.**

Rationale:
1. It is the best balance between objective completion and operational safety: true unification without breaking the established `maturin` root-manifest contract.
2. It aligns with Cargo workspace semantics (shared lockfile, root-level patch governance) while minimizing disruptive path relocation.
3. It provides the clearest risk-to-testability mapping for phased rollout (lockfile convergence, patch verification, and command-contract validation).

Required prior-art references (historical grounding):
- `docs/project/archive/prj0000005/prj005-llm-swarm-architecture.project.md`
- `docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md`
- `docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md`

Risk-to-testability summary for recommendation:
- Patch-scope risk -> dependency-graph assertion tests for patched `libp2p-yamux`.
- Lockfile churn risk -> deterministic package-scoped cargo build/test runs.
- CI command regression risk -> existing workflow/install structure tests plus explicit command checks.

## Open Questions (for @3design)
1. Should `runtime` be included in the same workspace in the first migration wave or deferred to phase 2?
2. Which dependencies should be moved to `workspace.dependencies` immediately versus left crate-local initially?
3. What is the exact command contract for crate-specific binaries after unification (`cargo build -p rust_core_security`, etc.)?
4. Should lockfile policy be strict single-lockfile-at-root, or is any scoped exception required?
5. Is an ADR update needed to formalize workspace-root patch governance and command conventions?

## Minimal-First Implementation Slice Suggestion
1. Add workspace membership at `rust_core/Cargo.toml` while preserving existing `[package]` for `maturin`.
2. Migrate only patch governance first (`[patch.crates-io]`) with an explicit verification test for the p2p yamux fix.
3. Run package-scoped smoke builds/tests for `crdt`, `p2p`, and `security` using workspace-root commands.
4. Update CI/install commands only where required for explicit package selection; avoid broad command refactors in the first slice.
5. Stabilize with one lockfile convergence PR before any additional dependency harmonization.
