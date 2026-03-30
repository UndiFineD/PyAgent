# ADR-0005 - Specialized Agent Library Hybrid Adapter Runtime

## Status

- Proposed

## Date

- 2026-03-30

## Owners

- @3design
- Reviewers: @4plan, @5test, @6code, @8ql

## Context

Project `prj0000107-idea000015-specialized-agent-library` addresses a gap between documented specialized agent capabilities and Python runtime implementation. A direct full-class specialization approach creates a larger migration surface, while universal-only capability packs do not provide enough explicit specialization contracts.

Repository architecture requires orchestration-thin agent classes, domain logic in `*Core` classes, composition via mixins, and policy-governed execution. The chosen design must therefore expose explicit interfaces while remaining compatible with existing universal shell routing primitives.

## Decision

Adopt a hybrid adapter architecture (Option B):

1. Versioned specialization manifests define specialization descriptors.
2. A specialization registry validates descriptors and version compatibility.
3. A runtime adapter translates descriptors into normalized shell execution requests.
4. Capability authorization is deny-by-default through an explicit policy matrix.
5. Core execution binds through explicit `*Core` contracts.
6. Any schema/version/policy failure triggers deterministic fail-closed fallback.
7. Every decision path emits redacted correlation-linked provenance telemetry.

## Alternatives considered

### Alternative A - Dedicated Specialized Class Library

- Summary: Introduce direct specialized runtime classes for each specialization path.
- Why not chosen: Higher implementation churn and maintenance burden before contract surfaces are stabilized.

### Alternative C - Universal-Only Capability Packs

- Summary: Keep specialization entirely in universal shell metadata/policies with no adapter layer.
- Why not chosen: Insufficient explicit interfaces and weaker traceability against specialized-agent-library objective.

## Consequences

### Positive

- Explicit specialized contracts without immediate class explosion.
- Reuse of proven universal shell primitives reduces migration risk.
- Deterministic policy and fallback controls improve security and reliability posture.
- Adapter contract versioning enables controlled evolution and compatibility checks.

### Negative / Trade-offs

- Added indirection across manifest, adapter, and shell layers increases debugging complexity.
- Contract-version governance becomes an ongoing operational responsibility.
- Parity and deterministic replay tests become mandatory release gates.

## Implementation impact

- Affected components:
  - specialization registry and schema validation layer
  - specialized runtime adapter contract
  - capability policy enforcement contract
  - specialization-to-core binding contract
  - fallback and telemetry bridge contracts
- Migration/rollout notes:
  - introduce adapter path behind feature flag/shadow routing
  - enforce manifest-to-request parity before broad enablement
- Backward compatibility notes:
  - existing universal shell path remains fallback baseline for rollback
  - major adapter contract version mismatches are rejected pre-execution

## Validation and monitoring

- Tests or checks required:
  - manifest schema and version gate tests
  - deterministic adapter mapping replay tests
  - policy allow/deny matrix contract tests
  - core binding contract tests
  - fail-closed fault-injection tests
  - telemetry schema and redaction tests
- Runtime signals or metrics to monitor:
  - `specialization_adapter_latency_ms`
  - `specialization_fallback_rate`
  - `policy_denied_capability_count`
  - `manifest_request_parity_rate`
  - `adapter_contract_version_distribution`
- Rollback triggers:
  - sustained fallback-rate spike above governance threshold
  - manifest-request parity regression
  - policy authorization anomalies indicating contract drift

## Related links

- Related project artifact(s):
  - docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.think.md
  - docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.design.md
- Related architecture docs:
  - docs/architecture/adr/0001-architecture-decision-record-template.md
  - docs/architecture/1agents.md
- Supersedes/Superseded-by (if any):
  - none