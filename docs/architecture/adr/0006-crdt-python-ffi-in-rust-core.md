# ADR-0006 - CRDT Python FFI Integration in rust_core

## Status

- Proposed

## Date

- 2026-03-31

## Owners

- @3design
- Reviewers: @4plan, @5test, @6code, @8ql

## Context

Project `prj0000108-idea000019-crdt-python-ffi-bindings` targets a migration from subprocess-based CRDT invocation to in-process Python FFI. Current runtime behavior routes CRDT merge through a binary execution boundary, which introduces process startup overhead, temp-file handling risks, and cross-platform fragility.

The repository already has an established `rust_core` PyO3+maturin path. A design decision is needed for topology: integrate CRDT FFI into existing `rust_core` extension vs keeping subprocess model vs introducing a separate CRDT extension package.

## Decision

Adopt Option B: integrate CRDT Python FFI into the existing `rust_core` PyO3 module.

1. Keep `src/core/crdt_bridge.py` as a stable Python facade during migration.
2. Route merge execution through a new `rust_core` CRDT FFI entrypoint by default (feature-gated).
3. Refactor CRDT merge logic into library-callable Rust interfaces rather than CLI-only invocation.
4. Enforce schema validation and typed Rust-to-Python error mapping at the FFI boundary.
5. Preserve temporary deterministic fallback controls until parity and stability gates pass.

## Alternatives considered

### Alternative A - Harden existing subprocess bridge

- Summary: retain binary subprocess execution and improve reliability/safety around files and process handling.
- Why not chosen: does not satisfy the primary objective of direct Python FFI and retains process/file overhead.

### Alternative C - Separate CRDT extension package

- Summary: expose CRDT via a dedicated PyO3 package independent of existing `rust_core` module.
- Why not chosen: increases packaging and release complexity before API contracts are stabilized.

## Consequences

### Positive

- Removes process-spawn overhead and temp-file dependency from primary merge path.
- Reuses existing PyO3+maturin tooling and CI posture already used in repository.
- Improves contract-level testability at the Python/Rust boundary.
- Aligns with architecture preference for Rust acceleration and thin Python orchestration.

### Negative / Trade-offs

- Requires moderate refactor of CRDT implementation from CLI orientation to library interfaces.
- Introduces strict FFI contract/version governance burden.
- Demands robust parity and failure-path tests before subprocess fallback retirement.

## Implementation impact

- Affected components:
  - `src/core/crdt_bridge.py` (facade behavior and feature-gated routing)
  - `rust_core` PyO3 module exports
  - CRDT Rust merge library interfaces and payload codec
  - observability hooks for FFI path parity/latency
- Migration/rollout notes:
  - shadow/feature-flag rollout (`CRDT_FFI_ENABLED`)
  - parity gate against legacy subprocess corpus before default cutover
  - fallback rollback switch maintained until stability threshold met
- Backward compatibility notes:
  - Python merge facade remains API-stable through migration
  - subprocess route retained as temporary fallback only

## Validation and monitoring

- Tests or checks required:
  - Python facade schema contract tests
  - FFI boundary validation/error-path tests
  - payload codec round-trip equivalence tests
  - merge determinism replay tests
  - legacy subprocess vs FFI parity corpus tests
  - cross-platform wheel/import smoke tests (Windows + Linux)
- Runtime signals or metrics to monitor:
  - `crdt_merge_latency_ms_p95`
  - `crdt_ffi_error_rate`
  - `crdt_ffi_vs_subprocess_parity_rate`
  - `crdt_merge_fallback_rate`
- Rollback triggers:
  - parity regression below agreed threshold
  - sustained FFI error-rate spike above baseline
  - cross-platform import/runtime instability post-cutover

## Related links

- Related project artifact(s):
  - docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.think.md
  - docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.design.md
- Related architecture docs:
  - docs/architecture/adr/0001-architecture-decision-record-template.md
  - docs/architecture/adr/0005-specialized-agent-library-hybrid-adapter-runtime.md
- Supersedes/Superseded-by (if any):
  - none
