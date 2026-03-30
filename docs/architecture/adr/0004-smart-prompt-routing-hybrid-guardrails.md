# ADR-0004 - Smart Prompt Routing Hybrid Guardrails

## Status

- Proposed

## Date

- 2026-03-30

## Owners

- @3design
- Reviewers: @4plan, @5test, @6code, @8ql

## Context

The platform needs a smart prompt routing architecture that improves decision quality for ambiguous prompts without sacrificing deterministic safety controls and auditability. Rule-only routing is reliable but rigid under ambiguous intent. Full event-mediated service decomposition adds higher operational complexity and broader rollout risk than required for the current scope.

The selected project branch and project constraints require a design that is testable, phased, and compatible with existing fallback and observability patterns.

## Decision

Adopt a hybrid routing architecture (Option B) with hard deterministic guardrail precedence, followed by a semantic classifier for ambiguous cases, and a bounded deterministic tie-break stage only when confidence remains below threshold.

Fail-closed fallback is mandatory on any schema violation, timeout, or provider failure in classifier/tie-break stages. Every decision must emit a redacted provenance record.

## Alternatives considered

### Alternative A - Deterministic Rule Router Only

- Summary: Use policy table routing with no semantic ambiguity layer.
- Why not chosen: Lower routing quality for ambiguous or multi-intent prompts and higher long-term policy drift burden.

### Alternative C - Event-Mediated Router Service

- Summary: Extract routing into a mediator/event-bus service.
- Why not chosen: Higher complexity, larger blast radius, and operational overhead not justified for this lifecycle stage.

## Consequences

### Positive

- Preserves deterministic safety constraints and auditability.
- Improves routing quality in ambiguous prompt scenarios.
- Supports phased rollout through shadow-mode parity validation before active route actuation.

### Negative / Trade-offs

- Additional classifier and tie-break components increase design surface area.
- Threshold tuning and calibration governance become new operational responsibilities.
- Deterministic replay requirements must be enforced continuously to prevent drift.

## Implementation impact

- Affected components:
  - Routing facade and policy engine interfaces
  - Classifier adapter contract
  - Tie-break resolver contract
  - Fallback policy and telemetry schema contracts
- Migration/rollout notes:
  - Introduce in shadow mode first.
  - Promote to active mode only after acceptance gates pass.
- Backward compatibility notes:
  - Existing deterministic route path remains fallback baseline if hybrid quality gates fail.

## Validation and monitoring

- Tests or checks required:
  - Guardrail precedence contract tests
  - Deterministic tie-break replay tests
  - Fail-closed fallback fault-injection tests
  - Shadow vs active decision parity tests
  - Telemetry schema + redaction tests
- Runtime signals or metrics to monitor:
  - `routing_decision_latency_ms`
  - `routing_fallback_rate`
  - `tie_break_invocation_rate`
  - `shadow_active_parity_rate`
  - `route_distribution_by_policy_version`
- Rollback triggers:
  - Parity regression above threshold
  - Latency SLO breach sustained across release window
  - Unexpected fallback spike suggesting schema or reliability degradation

## Related links

- Related project artifact(s):
  - docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.design.md
  - docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.think.md
- Related architecture docs:
  - docs/architecture/adr/0001-architecture-decision-record-template.md
  - docs/architecture/archive/agents.md
- Supersedes/Superseded-by (if any):
  - none
