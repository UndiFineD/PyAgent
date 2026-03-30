# ADR-0003 - Base Mixin Canonical Namespace and Compatibility Shim Policy

## Status

- Proposed

## Date

- 2026-03-30

## Owners

- @3design
- Reviewers: @4plan, @5test, @6code

## Context

The repository guidance requires a base mixin architecture rooted in src/core/base/mixins/, but that canonical namespace is missing. Existing mixins are spread across legacy module locations, which creates inconsistency, weak extension seams, and migration risk. We need a design that establishes a canonical namespace while preserving operational compatibility during rollout.

## Decision

Adopt a staged migration to a canonical base mixin namespace under src/core/base/mixins/ using explicit, time-boxed compatibility shims at legacy import paths. Enforce host contract validation, behavior parity testing, shim expiry gates, and migration observability signals at each migration wave boundary.

## Alternatives considered

### Alternative A - Scaffold-only canonical package

- Summary: Create canonical package but defer migration and shims.
- Why not chosen: Leaves immediate adoption unresolved and risks permanent placeholder architecture.

### Alternative B - Incremental migration with compatibility shims

- Summary: Migrate in waves, preserve old imports temporarily, add parity and expiry gates.
- Why chosen: Best balance of low regression risk, near-term adoption, and controlled retirement of legacy paths.

### Alternative C - Manifest-driven runtime composition framework

- Summary: Build full configuration-driven composition system first.
- Why not chosen: Excessive complexity and schedule risk for this project slice.

## Consequences

### Positive

- Canonical architecture boundary becomes explicit and enforceable.
- Migration risk is reduced through parity checks and reversible wave gates.
- Legacy import breakage is minimized during transition.

### Negative / Trade-offs

- Temporary dual-path complexity while shims are active.
- Additional maintenance overhead for parity tests and deprecation lifecycle.
- Potential delay if wave gates are under-specified by implementation plan.

## Implementation impact

- Affected components:
  - src/core/base/mixins/ (new canonical package)
  - Selected legacy mixin modules under src/core/* (shim re-exports)
  - Base host classes adopting canonical mixins in later wave
- Migration/rollout notes:
  - Execute in waves W0-W4 with explicit entry/exit gates.
- Backward compatibility notes:
  - Legacy paths remain valid only during W1-W3 and must fail closed after expiry gate.

## Validation and monitoring

- Tests or checks required:
  - Canonical export contract tests
  - Host contract conformance tests
  - Differential parity tests old vs canonical import path
  - Circular import smoke tests
  - Shim expiry fail-closed test
- Runtime signals or metrics to monitor:
  - shim_used
  - parity_failed
  - import_error
  - host_contract_error
- Rollback triggers:
  - Any parity or import smoke gate failure at wave boundary
  - Host contract validation failures in adoption wave

## Related links

- Related project artifact(s):
  - docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.design.md
- Related architecture docs:
  - docs/architecture/adr/0001-architecture-decision-record-template.md
  - docs/architecture/adr/0002-secret-remediation-control-plane.md
- Supersedes/Superseded-by (if any):
  - none
