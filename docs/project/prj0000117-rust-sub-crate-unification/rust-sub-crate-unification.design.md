# rust-sub-crate-unification - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-03_

## Selected Option
Option B: root workspace unification at `rust_core/Cargo.toml`.

Rationale:
1. It unifies dependency resolution under one workspace graph while preserving the existing `maturin` contract that targets `rust_core/Cargo.toml`.
2. It centralizes lockfile and patch governance, especially the `p2p` security patch handling, into one deterministic control point.
3. It minimizes migration blast radius compared with a virtual workspace split and keeps command paths stable for current build and benchmark workflows.

## Architecture
### High-level shape
- Keep `rust_core/Cargo.toml` as a package manifest for the Python extension crate.
- Add workspace configuration to the same root manifest (non-virtual workspace).
- Register sub-crates as workspace members:
  - `rust_core/crdt`
  - `rust_core/p2p`
  - `rust_core/security`
- Govern shared dependency and patch policy at workspace root.
- Converge to a single workspace lockfile in `rust_core/Cargo.lock`.

### File-level change design
| File | Change type | Design intent |
|---|---|---|
| `rust_core/Cargo.toml` | Update | Add `[workspace]` members and centralize root-level dependency/patch governance while preserving existing root package metadata used by `maturin`. |
| `rust_core/crdt/Cargo.toml` | Update | Remove duplicate lock/patch governance assumptions and align dependency declarations with workspace policy (prefer `workspace = true` where feasible in implementation phase). |
| `rust_core/p2p/Cargo.toml` | Update | Move crate-local `[patch.crates-io]` responsibility to root workspace and keep package-local constraints only where truly crate-specific. |
| `rust_core/security/Cargo.toml` | Update | Align dependency declarations and remove duplicated governance fields that must be root-owned in a workspace. |
| `rust_core/Cargo.lock` | Update/regenerate | Become the canonical workspace lockfile. |
| `rust_core/crdt/Cargo.lock` | Delete | Remove crate-local lockfile after workspace convergence. |
| `rust_core/p2p/Cargo.lock` | Delete | Remove crate-local lockfile after workspace convergence. |
| `rust_core/security/Cargo.lock` | Delete | Remove crate-local lockfile after workspace convergence. |
| `.github/workflows/ci.yml` | Targeted update (if needed) | Keep benchmark smoke command behavior stable; use explicit package/manifest flags only where workspace semantics require clarity. |
| `install.ps1` | No behavioral change expected | Keep `maturin develop --manifest-path rust_core/Cargo.toml` contract intact; only adjust if workspace introduces required explicit flags. |

### Lockfile strategy
- Contract: one lockfile under `rust_core/Cargo.lock` is authoritative for workspace members.
- Transition: remove sub-crate lockfiles in the same implementation slice that introduces workspace membership.
- Determinism signal: no `Cargo.lock` files remain under `rust_core/crdt/`, `rust_core/p2p/`, or `rust_core/security/` after migration.

### CI implications
- Preserve benchmark smoke execution semantics currently anchored at `rust_core/`.
- Preserve extension build path semantics for `maturin`.
- Add or adjust package-scoped checks (`cargo test -p <pkg>`, `cargo build -p <pkg>`) only where needed to avoid ambiguous defaults in workspace context.

## Interfaces & Contracts
### IFACE-WS-001 Build command continuity
- Contract: Existing root extension build command remains valid:
  - `maturin develop --manifest-path rust_core/Cargo.toml`
- Verification signal: command exits successfully in CI/local validation lane without path rewrites.

### IFACE-WS-002 Workspace package build/test command clarity
- Contract: Crate-specific validation uses explicit package targeting from workspace root:
  - `cargo build -p rust_core_crdt --manifest-path rust_core/Cargo.toml`
  - `cargo build -p rust_core_p2p --manifest-path rust_core/Cargo.toml`
  - `cargo build -p rust_core_security --manifest-path rust_core/Cargo.toml`
  - `cargo test -p rust_core_crdt --manifest-path rust_core/Cargo.toml`
  - `cargo test -p rust_core_p2p --manifest-path rust_core/Cargo.toml`
  - `cargo test -p rust_core_security --manifest-path rust_core/Cargo.toml`
- Verification signal: each command resolves package targets and returns zero in validation workflow.

### IFACE-WS-003 Benchmark command compatibility
- Contract: Existing benchmark smoke behavior remains compatible:
  - `cargo bench --bench stats_baseline -- --noplot`
- Verification signal: CI benchmark smoke step still passes from the `rust_core/` working directory or equivalent manifest-targeted invocation.

### IFACE-WS-004 Lockfile behavior
- Contract: Workspace root lockfile (`rust_core/Cargo.lock`) is the only lockfile source for workspace crates.
- Verification signal: repository scan finds no `Cargo.lock` under workspace member subdirectories; `cargo` commands do not regenerate member-local lockfiles.

### IFACE-WS-005 Patch governance ownership
- Contract: Any crates-io patch override that affects workspace members is declared at workspace root (not crate-local), including the current p2p security override.
- Verification signal: dependency resolution output confirms patched source/version is active for affected package graph.

## Acceptance Criteria
| AC ID | Requirement | Verification signal |
|---|---|---|
| AC-WS-001 | Root manifest includes valid workspace membership for targeted sub-crates while retaining root package metadata needed by `maturin`. | `cargo metadata --manifest-path rust_core/Cargo.toml` succeeds and lists root package plus members. |
| AC-WS-002 | Canonical lockfile strategy is enforced with one workspace lockfile. | `rust_core/Cargo.lock` exists; sub-crate `Cargo.lock` files are absent. |
| AC-WS-003 | Existing extension build contract is preserved. | `maturin develop --manifest-path rust_core/Cargo.toml` exits 0 in designated validation lane. |
| AC-WS-004 | Benchmark smoke command compatibility is preserved. | CI/local smoke command `cargo bench --bench stats_baseline -- --noplot` exits 0 under workspace migration branch. |
| AC-WS-005 | Package-scoped build/test commands are deterministic in workspace mode. | `cargo build/test -p <pkg> --manifest-path rust_core/Cargo.toml` commands pass for `rust_core_crdt`, `rust_core_p2p`, `rust_core_security`. |
| AC-WS-006 | Patch governance is root-owned and effective for security-sensitive override. | Root manifest contains required `[patch.crates-io]` entry; dependency graph evidence confirms override is active. |
| AC-WS-007 | CI command context remains explicit and stable post-unification. | CI workflow diff shows only targeted command/context updates; benchmark and build lanes pass without path regressions. |

## Interface-to-Task Traceability
| Interface | Planned task ID for @4plan | Task intent |
|---|---|---|
| IFACE-WS-001 | T-WS-001 | Update root `Cargo.toml` to mixed package+workspace shape without breaking `maturin` contract. |
| IFACE-WS-002 | T-WS-002 | Standardize package-scoped cargo build/test command usage and CI invocation points. |
| IFACE-WS-003 | T-WS-003 | Validate benchmark smoke compatibility and adjust CI command context if required. |
| IFACE-WS-004 | T-WS-004 | Converge lockfiles to single root lockfile and prevent member-local reintroduction. |
| IFACE-WS-005 | T-WS-005 | Move and verify patch governance at workspace root, including p2p security override. |

## Non-Functional Requirements
- Performance: Workspace migration must not introduce benchmark smoke regressions attributable to command-context changes; benchmark lane remains green.
- Security: Root-level patch governance must retain existing security patch effect for p2p dependency chain.
- Testability: Every acceptance criterion maps to deterministic shell/CI commands with explicit pass/fail outcomes.
- Operability: Build and benchmark command entrypoints remain stable for contributors and automation.

## Risks and Rollback
### Risks
1. Root/patch migration error can drop security override behavior for p2p transitive dependencies.
2. Lockfile convergence can produce high churn and transient dependency incompatibilities.
3. Workspace command-context changes can break CI or local scripts that assumed crate-local execution.

### Rollback strategy
1. Keep migration atomic to a dedicated PR slice: workspace manifest edits + lockfile convergence + command updates together.
2. If AC-WS-003/004/005 fail, revert the unification commit set and restore prior per-crate lockfiles and manifest patch placement.
3. Re-run pre-migration command baseline to confirm restored behavior:
   - `maturin develop --manifest-path rust_core/Cargo.toml`
   - benchmark smoke command from existing CI context
   - crate-specific tests/binary smoke currently used by test suite.

## Non-Goals
1. No virtual-workspace path relocation (do not move root package out of `rust_core/`).
2. No broad dependency-version harmonization beyond what is required for workspace lockfile convergence.
3. No broad CI redesign; only targeted command/context updates necessary for workspace compatibility.
4. No refactor of Rust crate internal APIs or Python-facing extension logic in this lane.

## Open Questions
1. Include `rust_core/runtime` as workspace member in wave 1, or defer to wave 2 after baseline stabilization?
2. Which dependencies are promoted to `workspace.dependencies` in wave 1 versus deferred to a follow-up hardening lane?
3. Which exact CI jobs should enforce lockfile-singleton validation to prevent reintroduction of member lockfiles?# rust-sub-crate-unification - Design

_Status: NOT_STARTED_
_Designer: @3design | Updated: 2026-04-03_

## Selected Option
TBD

## Architecture
TBD

## Interfaces & Contracts
TBD

## Non-Functional Requirements
- Performance: TBD
- Security: TBD

## Open Questions
Pending design.
