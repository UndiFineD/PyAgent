# idea000080-smart-prompt-routing-system - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-30_

## Selected Option
Option B - Hybrid Router (deterministic guardrails + semantic classifier + conditional tie-break).

Rationale:
1. Preserves deterministic policy control for safety and auditability.
2. Improves route quality for ambiguous prompts versus rules-only routing.
3. Keeps initial rollout complexity and blast radius lower than event-mediated service decomposition.

Design lock:
- This design locks Option B for v1.
- Option A remains fallback if hybrid confidence controls fail to meet acceptance hooks.
- Option C is deferred to a future ADR/project once scale and decoupling needs justify service extraction.

## Architecture
### High-level flow
1. Request enters `PromptRoutingFacade` with normalized routing context.
2. `GuardrailPolicyEngine` applies hard constraints (risk class, tool eligibility, latency/cost budgets, tenant policy).
3. If guardrails produce a deterministic winner, route is finalized.
4. If ambiguous, `PromptSemanticClassifier` computes route candidates + confidence.
5. If confidence is below threshold and ambiguity persists, `TieBreakResolver` runs low-cost deterministic tie-break.
6. `RouteDecisionRecord` is emitted with provenance and handed to the orchestrator/model adapter.
7. Fallback policy applies on classifier/tie-break failure (fail-closed safe route).

### Components and responsibilities
| Component | Responsibility | Inputs | Outputs |
|---|---|---|---|
| `PromptRoutingFacade` | Single entrypoint for routing decisions | Prompt envelope + execution constraints | `RouteDecisionRecord` |
| `GuardrailPolicyEngine` | Enforce non-negotiable policy constraints first | Normalized routing request | Guardrail decision or unresolved state |
| `PromptSemanticClassifier` | Resolve ambiguous intent/workload class | Unresolved routing request | Candidate routes + confidence |
| `TieBreakResolver` | Deterministic low-cost tie-break for low-confidence ambiguity | Classifier candidates + fixed seed/config | Final route candidate |
| `RoutingFallbackPolicy` | Fail-closed safety fallback | Error/timeout/invalid output state | Safe default route + reason |
| `RoutingTelemetryEmitter` | Emit provenance and control metrics | Final decision + stage timings | Structured audit/metrics events |

### Data flow constraints
- Guardrail precedence is absolute: downstream stages cannot override hard policy outcomes.
- Tie-break invocation is conditional and bounded by strict timeout.
- Route provenance is mandatory for every decision path.
- No raw secret or full prompt persistence in telemetry payloads.

## Interfaces & Contracts
### Interface contracts
| Interface ID | Interface | Contract summary | Acceptance hook |
|---|---|---|---|
| IFACE-SPR-001 | `PromptRoutingFacade.route(request) -> RouteDecisionRecord` | Stable async entrypoint; always returns a route or explicit fail-closed fallback | AC-SPR-001, AC-SPR-006 |
| IFACE-SPR-002 | `GuardrailPolicyEngine.evaluate(request) -> GuardrailOutcome` | Deterministic policy evaluation with immutable precedence over all later stages | AC-SPR-002 |
| IFACE-SPR-003 | `PromptSemanticClassifier.classify(request) -> ClassifierResult` | Produces bounded candidate set with calibrated confidence score and feature attribution tags | AC-SPR-003 |
| IFACE-SPR-004 | `TieBreakResolver.resolve(candidates, context) -> RouteCandidate` | Deterministic tie-break (fixed seed/config) with strict timeout and schema-valid output | AC-SPR-004, AC-SPR-007 |
| IFACE-SPR-005 | `RoutingFallbackPolicy.apply(reason, context) -> RouteDecisionRecord` | Fail-closed fallback with explicit reason taxonomy and safe default route guarantee | AC-SPR-005 |
| IFACE-SPR-006 | `RoutingTelemetryEmitter.emit(record) -> None` | Emits redacted provenance event with stage timings, confidence, fallback reason, and correlation IDs | AC-SPR-008 |

### Core data contracts
| Data shape | Required fields | Notes |
|---|---|---|
| `PromptRoutingRequest` | `request_id`, `tenant_id`, `intent_hint`, `risk_class`, `tool_requirement`, `latency_budget_ms`, `cost_budget_class`, `context_summary` | `context_summary` must be pre-redacted and bounded |
| `RouteDecisionRecord` | `request_id`, `final_route`, `decision_stage`, `guardrail_hit`, `classifier_confidence`, `tie_break_used`, `fallback_reason`, `policy_version`, `correlation_id` | Canonical provenance payload consumed by observability and replay tests |
| `ClassifierResult` | `candidate_routes`, `confidence`, `feature_tags`, `model_version` | Candidate list sorted by score descending |
| `GuardrailOutcome` | `is_resolved`, `route`, `policy_rules_matched`, `deny_reason` | `deny_reason` required when route is blocked |

### Constraints and invariants
1. Guardrail decisions are final and cannot be overridden.
2. If classifier output fails schema validation, fallback policy triggers immediately.
3. Tie-break path must execute with deterministic settings (fixed seed, fixed temperature profile).
4. Every route decision emits a provenance record with correlation ID.
5. Shadow-mode and active-mode share identical decision contracts; only actuation differs.

## Non-Functional Requirements
- Performance:
	- p95 routing decision latency <= 40 ms in active mode (excluding downstream model execution).
	- Tie-break stage timeout <= 20 ms; timeout auto-triggers fallback.
	- Route cache (where used) must preserve policy-version safety (no cross-version reuse).
- Security:
	- Telemetry must redact prompt content and secrets.
	- Guardrail policy versioning must be immutable and auditable.
	- High-risk prompt classes default to safe route if uncertainty exists.
- Reliability:
	- Route decision path must fail closed on classifier/tie-break failure.
	- Deterministic replay support for route decisions required in test harness.
- Testability:
	- All interface contracts have explicit acceptance hooks and deterministic fixtures.
	- Route provenance schema must support exact assertion testing.

## Acceptance Criteria
| AC ID | Requirement | Verification hook |
|---|---|---|
| AC-SPR-001 | Router facade returns a route decision or explicit safe fallback for every valid request | Contract tests for `PromptRoutingFacade.route` |
| AC-SPR-002 | Guardrail precedence is enforced over classifier/tie-break outputs | Precedence tests with adversarial candidate overrides |
| AC-SPR-003 | Classifier outputs schema-valid candidates + confidence within calibrated range | Schema + calibration tests |
| AC-SPR-004 | Tie-break output is deterministic across repeated runs with fixed config | Deterministic replay tests |
| AC-SPR-005 | Fail-closed fallback triggers on timeout/schema failure/provider error | Fault-injection tests |
| AC-SPR-006 | Shadow mode decision equals active mode decision for same input and policy version | Dual-mode parity tests |
| AC-SPR-007 | Tie-break timeout never exceeds bounded limit and emits timeout reason | Timeout boundary tests + telemetry assertions |
| AC-SPR-008 | Provenance telemetry includes required redacted fields and correlation IDs | Telemetry schema tests + redaction checks |

## Interface-to-Task Traceability
| Planned Task ID (@4plan) | Interface/Contract | Delivery expectation |
|---|---|---|
| T-SPR-01 | IFACE-SPR-001 | Implement routing facade entrypoint and response envelope handling |
| T-SPR-02 | IFACE-SPR-002 | Implement deterministic guardrail policy engine + rule table loader |
| T-SPR-03 | IFACE-SPR-003 | Implement classifier adapter and confidence normalization |
| T-SPR-04 | IFACE-SPR-004 | Implement deterministic tie-break resolver with timeout controls |
| T-SPR-05 | IFACE-SPR-005 | Implement fallback policy and reason taxonomy |
| T-SPR-06 | IFACE-SPR-006 | Implement telemetry emitter and redaction policy |
| T-SPR-07 | AC-SPR-002, AC-SPR-005 | Build precedence and fail-closed contract test suite |
| T-SPR-08 | AC-SPR-004, AC-SPR-006 | Build deterministic replay and shadow/active parity tests |
| T-SPR-09 | AC-SPR-008 | Build provenance schema + redaction validation tests |
| T-SPR-10 | NFR performance hooks | Add routing latency metrics and threshold alerts |

## ADR Impact
- New ADR required: hybrid routing architecture with deterministic guardrails and tie-break governance.
- Proposed ADR file: `docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md`.
- This ADR captures:
	- Why Option B is selected over rule-only and event-mediated alternatives.
	- Guardrail precedence as a hard architectural invariant.
	- Deterministic tie-break + fail-closed fallback as reliability controls.

## Open Questions
Resolved for handoff readiness:
1. Canonical taxonomy source: versioned routing policy artifact (owned by routing policy module).
2. Tie-break threshold policy: invoke only below calibrated confidence threshold with guardrail unresolved state.
3. Promotion gate: shadow-mode parity + latency + fallback-rate thresholds must pass before active rollout.

No blocking open design questions remain for @4plan decomposition.

## Open Questions
TBD for @4plan.
