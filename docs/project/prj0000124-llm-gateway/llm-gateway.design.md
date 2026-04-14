# llm-gateway - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-04-04_

## Selected Option
Option C: Hybrid Split-Plane Gateway.

Rationale:
1. Preserves fail-closed policy-first control sequencing already established in routing and resilience modules.
2. Delivers phase-one in-process integration quickly while keeping Rust-ready boundaries for hot-path acceleration.
3. Aligns with PyAgent conventions: thin orchestration shell, core domain logic in dedicated classes, and transaction discipline for mutable state.

## Problem Statement And Design Goals
PyAgent needs one deterministic gateway path that enforces all required capabilities for model invocation:
1. Routing and load balancing.
2. Authentication and access control.
3. Token budgeting.
4. Guardrails and policy enforcement.
5. Semantic cache.
6. Model fallback.
7. Observability.
8. Context management.
9. Memory integration.
10. Tool and skill interception.

The design goal is to unify these capabilities behind explicit contracts in `src/core/gateway/` without implementing runtime code in this phase.

## Architecture Overview
Hybrid split-plane in-process topology for phase one:

```
Ingress (Agent/Backend)
  -> GatewayCore (orchestration boundary)
	  -> Control Plane
		  - GatewayPolicyEngine
		  - GatewayRouter
		  - GatewayFallbackManager
		  - GatewayTelemetryEmitter
		  - ToolSkillCatcher
	  -> Data Plane (Python implementation, Rust-ready contracts)
		  - ProviderRuntimeAdapter
		  - GatewaySemanticCache
		  - GatewayBudgetManager
	  -> State integrations
		  - backend/memory_store.py
		  - backend/tracing.py
		  - backend/auth.py
```

Control plane owns policy, route, fallback governance, and telemetry correlation.
Data plane owns provider execution, semantic cache operations, and budget commit path.

## Component Boundaries
### Boundary Rules
1. `GatewayCore` is the only phase-one public orchestration entrypoint.
2. Policy checks execute before provider execution and before tool dispatch.
3. Budget reserve happens before provider call; budget commit/finalize happens after response/failure resolution.
4. Cache writes are blocked when policy outcome is deny or response classification is unsafe.
5. Control-plane and data-plane payloads cross boundaries only via typed envelopes.

### Proposed Package Shape (Design Only)
`src/core/gateway/`
- `gateway_core.py` -> `GatewayCore`
- `gateway_policy_engine.py` -> `GatewayPolicyEngine`
- `gateway_router.py` -> `GatewayRouter`
- `provider_runtime_adapter.py` -> `ProviderRuntimeAdapter`
- `gateway_budget_manager.py` -> `GatewayBudgetManager`
- `gateway_semantic_cache.py` -> `GatewaySemanticCache`
- `gateway_fallback_manager.py` -> `GatewayFallbackManager`
- `gateway_telemetry_emitter.py` -> `GatewayTelemetryEmitter`
- `tool_skill_catcher.py` -> `ToolSkillCatcher`

## Interfaces And Contracts
### IFACE-GW-001 GatewayCore
Purpose: deterministic request orchestration across control and data planes.

Proposed methods:
- `async handle(self, envelope: GatewayRequestEnvelope) -> GatewayResultEnvelope`
- `async handle_stream(self, envelope: GatewayRequestEnvelope) -> GatewayStreamHandle`

Contract requirements:
1. Must always produce `GatewayResultEnvelope` with `decision`, `budget`, and `telemetry` sections populated.
2. Must fail-closed when any mandatory policy gate is unavailable.

### IFACE-GW-002 GatewayPolicyEngine
Purpose: evaluate access and guardrail policy at pre-provider, post-provider, and pre-tool stages.

Proposed methods:
- `evaluate_pre_request(self, envelope: GatewayRequestEnvelope) -> PolicyDecision`
- `evaluate_post_response(self, envelope: GatewayRequestEnvelope, response: ProviderResponseEnvelope) -> PolicyDecision`
- `evaluate_tool_call(self, envelope: GatewayRequestEnvelope, tool_call: ToolCallEnvelope) -> PolicyDecision`

Contract requirements:
1. Deny-by-default for missing policy version or malformed policy context.
2. Include policy rule ids and policy version in every decision.

### IFACE-GW-003 GatewayRouter
Purpose: produce route plan using policy, intent, and resilience state.

Proposed methods:
- `route(self, envelope: GatewayRequestEnvelope, policy: PolicyDecision) -> RoutePlanEnvelope`

Contract requirements:
1. Integrates `PromptRoutingFacade` outputs where available.
2. Returns deterministic safe route when confidence/tie-break path fails.

### IFACE-GW-004 ProviderRuntimeAdapter
Purpose: execute provider calls on selected route.

Proposed methods:
- `async execute(self, route: RoutePlanEnvelope, envelope: GatewayRequestEnvelope) -> ProviderResponseEnvelope`

Contract requirements:
1. Wraps `FlmChatAdapter` first.
2. Maps provider/runtime errors to typed `GatewayErrorEnvelope` categories.

### IFACE-GW-005 GatewayBudgetManager
Purpose: reserve, reconcile, and commit token/cost budget.

Proposed methods:
- `reserve(self, envelope: GatewayRequestEnvelope) -> BudgetReservationEnvelope`
- `commit_success(self, reservation: BudgetReservationEnvelope, usage: TokenUsageEnvelope) -> BudgetCommitEnvelope`
- `commit_failure(self, reservation: BudgetReservationEnvelope, error: GatewayErrorEnvelope) -> BudgetCommitEnvelope`

Contract requirements:
1. Idempotent commit keys.
2. Reserve-before-execute and finalize-after-outcome enforcement.

### IFACE-GW-006 GatewaySemanticCache
Purpose: similarity-aware cache lookup and write.

Proposed methods:
- `lookup(self, envelope: GatewayRequestEnvelope) -> CacheLookupEnvelope`
- `write(self, envelope: GatewayRequestEnvelope, response: ProviderResponseEnvelope) -> CacheWriteEnvelope`

Contract requirements:
1. Key includes policy version and model route identity.
2. Unsafe or denied responses are never cached.

### IFACE-GW-007 GatewayFallbackManager
Purpose: provider/model fallback orchestration across policy and circuit state.

Proposed methods:
- `resolve(self, route: RoutePlanEnvelope, error: GatewayErrorEnvelope | None) -> FallbackPlanEnvelope`

Contract requirements:
1. Integrates `src/core/resilience/CircuitBreakerRegistry.py`.
2. Emits fallback reason taxonomy values compatible with routing taxonomy.

### IFACE-GW-008 GatewayTelemetryEmitter
Purpose: emit traces/metrics/audit events for each lifecycle stage.

Proposed methods:
- `emit_request_start(self, envelope: GatewayRequestEnvelope) -> None`
- `emit_decision(self, decision: PolicyDecision, route: RoutePlanEnvelope) -> None`
- `emit_result(self, result: GatewayResultEnvelope) -> None`

Contract requirements:
1. Correlation id is immutable per request.
2. Uses backend tracer and redacted structured fields only.

### IFACE-GW-009 ToolSkillCatcher
Purpose: intercept tool/skill calls with policy and telemetry hooks.

Proposed methods:
- `intercept_before(self, envelope: GatewayRequestEnvelope, tool_call: ToolCallEnvelope) -> PolicyDecision`
- `intercept_after(self, envelope: GatewayRequestEnvelope, tool_result: ToolResultEnvelope) -> ToolAuditEnvelope`

Contract requirements:
1. Block disallowed tools before execution.
2. Record allow/deny rationale and governance tags.

## Data Contracts
### GatewayRequestEnvelope
Required fields:
- `request_id: str`
- `correlation_id: str`
- `agent_id: str`
- `user_id: str | None`
- `project_id: str`
- `session_id: str | None`
- `auth_context: AuthContextEnvelope`
- `prompt: PromptEnvelope`
- `policy_context: PolicyContextEnvelope`
- `budget_context: BudgetContextEnvelope`
- `context_window: ContextWindowEnvelope`
- `memory_refs: list[MemoryRefEnvelope]`
- `tool_context: ToolContextEnvelope`

### GatewayResultEnvelope
Required fields:
- `request_id: str`
- `correlation_id: str`
- `status: Literal["success", "denied", "fallback_success", "failed"]`
- `decision: PolicyDecision`
- `route: RoutePlanEnvelope`
- `provider_response: ProviderResponseEnvelope | None`
- `error: GatewayErrorEnvelope | None`
- `budget: BudgetCommitEnvelope`
- `cache: CacheOutcomeEnvelope`
- `memory_outcome: MemoryWriteEnvelope`
- `tool_audit: list[ToolAuditEnvelope]`
- `telemetry: TelemetryEnvelope`

### GatewayErrorEnvelope
Required fields:
- `error_code: str`
- `category: Literal["policy", "auth", "budget", "provider", "timeout", "cache", "internal"]`
- `is_retryable: bool`
- `is_fail_closed: bool`
- `fallback_attempted: bool`
- `fallback_reason: str | None`

## End-To-End Request Lifecycle
1. Ingress receives request in agent runtime or backend API layer.
2. `GatewayCore.handle` creates correlation metadata and normalizes input envelope.
3. `GatewayPolicyEngine.evaluate_pre_request` enforces auth/access and prompt guardrails.
4. `GatewayBudgetManager.reserve` reserves budget units for the request.
5. `GatewaySemanticCache.lookup` attempts similarity or exact cache hit.
6. `GatewayRouter.route` computes route plan from policy and routing/resilience signals.
7. `ProviderRuntimeAdapter.execute` calls provider on chosen route.
8. On provider failure, `GatewayFallbackManager.resolve` chooses fallback and retries by policy.
9. `GatewayPolicyEngine.evaluate_post_response` validates output safety/compliance.
10. `ToolSkillCatcher` intercepts any tool-specified execution path.
11. `GatewaySemanticCache.write`, `GatewayBudgetManager.commit_*`, and memory write intents are finalized.
12. `GatewayTelemetryEmitter.emit_result` publishes final lifecycle telemetry and returns result envelope.

## Error Handling And Fail-Closed Behavior
| Failure Condition | Immediate Behavior | Fallback Behavior | Final Status |
|---|---|---|---|
| Missing/invalid auth context | deny | none | denied |
| Policy engine unavailable | fail-closed deny | none | denied |
| Budget reservation failure | deny before provider call | none | denied |
| Router classifier/tie-break error | safe-default route | fallback plan if available | fallback_success or failed |
| Provider timeout/failure | classify error | fallback chain via circuit state | fallback_success or failed |
| Post-response policy deny | block response | no cache write, no tool execution | denied |
| Telemetry emit failure | continue with degraded telemetry | add degraded flag | success/failed by upstream outcome |

Fail-closed invariants:
1. No provider execution without successful pre-policy + budget reservation.
2. No tool execution without tool interception policy allow.
3. No cache write for denied or unsafe responses.

## Security And Policy Enforcement Points
1. Ingress auth claims from `backend/auth.py` become `AuthContextEnvelope`.
2. Pre-request policy gate verifies tenant/project/agent permissions and risk class.
3. Prompt and context redaction policy runs before route computation.
4. Post-response guardrail checks output classification and policy tags.
5. Tool/skill catcher enforces allowlist/denylist and records an immutable audit event.

## State And Persistence Model
### Budget State
- Reserve/commit ledger model with idempotency key: `(request_id, route_id, reservation_id)`.
- Phase one persistence: process-local state with durable append-intent abstraction for later promotion.
- Transaction discipline: budget mutations run in explicit budget transaction scope.

### Semantic Cache State
- Read path: deterministic lookup by normalized prompt + policy version + route identity.
- Write path: only after post-response policy allow.
- TTL and invalidation hooks required in contract for phase two hardening.

### Observability State
- Trace root from `backend/tracing.py`.
- Structured metrics/events include route id, fallback reason, policy version, latency, and token usage.
- Redaction is mandatory for PII/secrets in telemetry payload fields.

### Context And Memory State
- Context window policy identifies include/drop/compress segments.
- Memory integration writes through policy-controlled adapter to `backend/memory_store.py`.
- Transaction discipline: memory write intent is separated from provider execution and retriable.

## Integration Points With Existing Code
### Provider Integration
- `src/core/providers/FlmChatAdapter.py`: phase-one primary provider adapter implementation behind `ProviderRuntimeAdapter`.

### Routing Integration
- `src/core/routing/prompt_routing_facade.py`: route decision substrate.
- `src/core/routing/guardrail_policy_engine.py`: policy primitives reused or wrapped.
- `src/core/routing/routing_fallback_policy.py`: fallback taxonomy compatibility.

### Resilience Integration
- `src/core/resilience/CircuitBreakerRegistry.py`: circuit state and fallback provider eligibility.
- `src/core/resilience/CircuitBreakerMixin.py`: reuse pattern guidance for provider wrappers.

### Backend Integration
- `backend/auth.py`: auth context extraction and validation.
- `backend/app.py`: ingress and dependency wiring boundary for gateway call path.
- `backend/tracing.py`: OTel tracer provider integration for correlation.
- `backend/memory_store.py`: async memory append/read bridge with policy-governed writes.

## Phase Constraints For @4plan
### Phase 1 (MVP In-Process Contracts + Baseline)
1. Implement all IFACE-GW-001..009 contracts in Python with in-process wiring.
2. Ship baseline capabilities across all 10 pillars.
3. Keep runtime dependency surface minimal and backward compatible.

### Phase 2 (Safety/Reliability Hardening)
1. Expand deny-path and fallback-path determinism tests.
2. Add stronger cache poisoning protections and policy-versioned invalidation.
3. Strengthen tool interception and audit guarantees.

### Phase 3 (Rust Acceleration + Optional Service Mode)
1. Migrate hot data-plane operations (semantic cache + budget accounting) behind Rust-backed implementations.
2. Preserve envelope contracts and behavior parity.
3. Optional service mode may be introduced without changing control-plane policy invariants.

## Acceptance Criteria
| AC ID | Criterion | Evidence Required |
|---|---|---|
| AC-GW-001 | Design defines explicit control-plane and data-plane responsibilities with fail-closed boundary rules. | Architecture and boundary sections in this artifact. |
| AC-GW-002 | All nine gateway interfaces have concrete responsibilities and callable contract methods. | IFACE-GW-001..009 sections. |
| AC-GW-003 | End-to-end lifecycle covers all ten capability pillars. | Lifecycle + goals sections map each pillar. |
| AC-GW-004 | Error matrix defines fail-closed outcomes for auth/policy/budget/provider/cache/tool paths. | Error handling table and invariants. |
| AC-GW-005 | Existing integration points across providers/routing/resilience/backend are explicitly mapped. | Integration section references concrete files. |
| AC-GW-006 | Phase constraints for @4plan are clear for MVP, hardening, and Rust/service evolution. | Phase constraints section. |
| AC-GW-007 | Interface-to-task traceability exists for @4plan implementation planning. | Traceability table section. |
| AC-GW-008 | ADR decision is recorded for hybrid split-plane adoption. | ADR link in ADR section. |

## Explicit Non-Goals (Phase One)
1. No external gateway service deployment in phase one.
2. No Rust implementation in phase one.
3. No advanced adaptive/cost-optimization routing heuristics beyond baseline policy routing.
4. No multi-region consistency guarantees for cache/budget state in phase one.

## Interface-To-Task Traceability For @4plan
| Interface ID | Planned Task ID For @4plan | Task Intent |
|---|---|---|
| IFACE-GW-001 | PLAN-GW-01 | Orchestration entrypoint and envelope flow wiring |
| IFACE-GW-002 | PLAN-GW-02 | Pre/post/tool policy decisions and fail-closed rules |
| IFACE-GW-003 | PLAN-GW-03 | Routing and safe-default route behavior |
| IFACE-GW-004 | PLAN-GW-04 | Provider runtime adapter over FLM path |
| IFACE-GW-005 | PLAN-GW-05 | Reserve/commit budget manager with idempotency |
| IFACE-GW-006 | PLAN-GW-06 | Semantic cache lookup/write contracts |
| IFACE-GW-007 | PLAN-GW-07 | Fallback manager with circuit integration |
| IFACE-GW-008 | PLAN-GW-08 | Telemetry contract and correlation propagation |
| IFACE-GW-009 | PLAN-GW-09 | Tool/skill interception and audit path |
| Envelope Contracts | PLAN-GW-10 | Shared contract model definitions and validation |

## ADR Decision
ADR created: `docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md`.

## Open Questions For @4plan
1. Which contract models should be dataclasses vs pydantic models in phase one?
2. Should stream handling (`handle_stream`) be in phase-one MVP or phase-two hardening?
3. What minimum telemetry SLO thresholds should be made blocking in @7exec?
