# llm-gateway - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-04-04_

## Root Cause Analysis
1. PyAgent already has partial primitives for gateway capabilities, but they are fragmented across modules and surfaces:
	- provider adapter and tool loop in `src/core/providers/FlmChatAdapter.py`
	- per-provider resilience and fallback in `src/core/resilience/CircuitBreakerRegistry.py` and `src/core/resilience/CircuitBreakerMixin.py`
	- policy-first routing contracts in `src/core/routing/prompt_routing_facade.py`
	- auth/session/rate limits and memory APIs in `backend/app.py`, `backend/auth.py`, `backend/rate_limiter.py`, and `backend/memory_store.py`
2. There is no single gateway lifecycle that composes auth, policy, routing, token budget, semantic cache, model fallback, observability, context shaping, and tool interception as one deterministic path.
3. Existing architecture direction strongly prefers fail-closed policy sequencing and fallback telemetry (`docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md`), which should be reused rather than replaced.

## Step 1 Research Evidence
| Task Type | Findings | Evidence |
|---|---|---|
| Literature review | Existing code already has policy-first routing and fallback taxonomy patterns suitable for gateway orchestration. | `src/core/routing/prompt_routing_facade.py`, `src/core/routing/guardrail_policy_engine.py`, `src/core/routing/routing_fallback_policy.py` |
| Alternative enumeration | 4 viable architectures emerged: in-process, sidecar service, hybrid split-plane, and adapter-over-existing-router. | `src/core/providers/FlmChatAdapter.py`, `backend/app.py`, `src/core/universal/UniversalAgentShell.py` |
| Prior-art search | Historical ADRs and prior projects consistently favor fail-closed controls, staged rollout, and fallback baseline retention. | `docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md`, `docs/architecture/adr/0005-specialized-agent-library-hybrid-adapter-runtime.md`, `docs/project/archive/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.think.md` |
| Constraint mapping | Project boundary requires docs-only output; architecture conventions require mixin modularization, core/agent separation, and transaction discipline. | `docs/project/prj0000124-llm-gateway/llm-gateway.project.md`, `.github/copilot-instructions.md` |
| Stakeholder impact | Changes touch core runtime abstractions, backend auth/runtime edge, observability, and downstream test agents. | `src/core/providers/__init__.py`, `backend/auth.py`, `backend/tracing.py`, `docs/project/prj0000124-llm-gateway/llm-gateway.project.md` |
| Risk enumeration | Main risks are policy bypass, budget inconsistency, cache poisoning/staleness, and fallback storms; all require explicit validation gates. | `docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md`, `src/core/resilience/CircuitBreakerRegistry.py` |

## Constraints (Explicit)
- Branch gate: active branch matches expected branch (`prj0000124-llm-gateway`).
- Scope for this phase: analysis and artifacts only; no runtime implementation.
- Keep compatibility with PyAgent patterns: thin orchestration shell, logic in core classes, composition/mixins.
- Gateway must cover all required capabilities: routing/load balancing, auth/access control, token budgeting, guardrails/policy, semantic caching, model fallback, observability, context handling, memory integration, tool/skill catchers.
- Fail-closed behavior remains mandatory on policy/schema/provider faults, aligned with prior ADR direction.

## Options
### Option A - In-Process Gateway Core (Python-First, Embedded)
**Boundaries/components**
- New `src/core/gateway/` package with:
  - `GatewayCore` (request pipeline orchestration)
  - `ProviderAdapter` interface (wrap existing `FlmChatAdapter` first)
  - `GatewayPolicyEngine` (pre/prompt/post/tool guardrails)
  - `BudgetManager` (token accounting by tenant/agent/project)
  - `SemanticCacheCore` (lookup/write + invalidation)
  - `FallbackManager` (provider and model chain)
  - `GatewayTelemetryEmitter` (OTel/log/metrics correlation)
- Agents call `GatewayCore` directly from Python runtime.

**Request lifecycle pipeline**
1. Auth context resolution (agent/session/project identity)
2. Pre-prompt guardrail and access policy check (deny-by-default)
3. Token budget reservation
4. Semantic cache lookup
5. Provider/model route selection + load balancing
6. Provider call with resilience/fallback
7. Post-response guardrail + tool/skill catcher interception
8. Context compaction + memory write-through
9. Telemetry emit + budget commit/finalize

**SWOT**
- Strengths: Lowest latency; direct reuse of existing Python contracts; easiest phase-1 bootstrap.
- Weaknesses: Tight coupling to Python process lifecycle; harder horizontal scaling boundary.
- Opportunities: Fast iteration and quick delivery of full feature envelope.
- Threats: In-process faults can affect caller runtime; policy drift if not centralized by contract tests.

**Security risk analysis (risk -> testability signal)**
- Policy bypass in embedded callers (M/H) -> contract tests for mandatory `GatewayCore` entrypoint before provider calls.
- Cross-agent budget leakage (M/H) -> deterministic budget ledger invariants and per-scope accounting tests.
- Cache poisoning or stale unsafe reuse (M/M) -> semantic cache key/redaction tests plus TTL/invalidation scenario tests.

**Complexity/cost estimate**
- Complexity: Medium
- Cost: Medium
- Time-to-first-value: High

**Migration path from current code**
- Wrap current FLM path (`src/core/providers/FlmChatAdapter.py`) behind provider adapter.
- Reuse routing guardrail contracts from `src/core/routing/prompt_routing_facade.py`.
- Reuse backend auth/session identity claims from `backend/auth.py` and `backend/app.py` for request context.

### Option B - Sidecar/Service Gateway (Backend-Facing API)
**Boundaries/components**
- Gateway runs as dedicated service endpoint (reuse/extend backend transport patterns).
- Agents and runtime call gateway over internal HTTP/WS.
- Centralized policy, budgeting, cache, fallback, and telemetry in one service tier.

**Request lifecycle pipeline**
1. Service authn/authz at gateway edge
2. Tenant/project/agent policy binding
3. Budget check + reserve
4. Cache lookup
5. Route + LB + fallback call
6. Guardrails on response + tool interception
7. Cache write + memory side-effects
8. Emit traces/metrics/logs + finalize budget

**SWOT**
- Strengths: Strong separation of concerns; easier multi-tenant controls and centralized governance.
- Weaknesses: Added network hop and deployment complexity.
- Opportunities: Clear platform team ownership and standardized provider integration surface.
- Threats: Gateway bottleneck/SPOF risk if scaling/HA not implemented early.

**Security risk analysis (risk -> testability signal)**
- Gateway as high-value target (M/H) -> authz boundary tests + abuse/rate-limit tests at edge.
- Service outage causes broad blast radius (M/H) -> resilience/chaos tests with graceful degradation assertions.
- Credential propagation mistakes (L/H) -> end-to-end identity/claim propagation tests across gateway calls.

**Complexity/cost estimate**
- Complexity: High
- Cost: High
- Time-to-first-value: Medium-Low

**Migration path from current code**
- Start by exposing provider mediation endpoint near existing backend API patterns in `backend/app.py`.
- Move policy and routing logic behind service contracts; agents use client SDK.

### Option C - Hybrid Split-Plane Gateway (Recommended)
**Boundaries/components**
- Control plane (Python): authz/policy, routing decisions, fallback strategy, observability correlation.
- Data plane (hot path): provider execution, semantic cache similarity lookup, and token accounting optimized for Rust-ready acceleration.
- Keep in-process adapter first, with optional service mode later.

**Request lifecycle pipeline**
1. Control-plane auth context and policy decision
2. Budget pre-check + reservation
3. Data-plane cache query and route scoring
4. Provider execution with circuit/fallback policy
5. Post-response guardrail and tool/skill interception
6. Context shaping + memory write intent
7. Data-plane commit (budget/cache) and control-plane telemetry publish

**SWOT**
- Strengths: Balances speed and governance; aligns with Rust acceleration strategy; keeps phased rollout flexibility.
- Weaknesses: More interface design effort up front than Option A.
- Opportunities: Introduces stable contracts for future multi-provider/multi-tenant scale.
- Threats: Split-plane contract drift if ownership/tests are weak.

**Security risk analysis (risk -> testability signal)**
- Plane boundary mismatch or bypass (M/H) -> contract compatibility tests and fail-closed cross-plane error-path tests.
- Budget/cache race or double-spend (M/H) -> transactional idempotency tests under concurrency stress.
- Tool interception gaps (M/M) -> interceptor chain tests verifying pre/post/tool guardrails always execute.

**Complexity/cost estimate**
- Complexity: Medium-High
- Cost: Medium-High
- Time-to-first-value: High (with phased cut)

**Migration path from current code**
- Phase 1 keeps provider execution in Python using `FlmChatAdapter`; define data-plane interfaces now.
- Route/fallback policy borrows from existing routing and resilience modules.
- Promote selected hot-path operations to `rust_core/` only after parity tests and telemetry baselines.

### Option D - Adapter-Over-Existing Routing/Resilience (Minimal Delta)
**Boundaries/components**
- Thin gateway facade that composes current modules (`PromptRoutingFacade`, `CircuitBreakerRegistry`, `FlmChatAdapter`) with minimal new abstractions.

**Request lifecycle pipeline**
1. Existing auth context
2. Existing guardrail routing decision
3. Existing resilience + fallback wrapper
4. Add limited cache/budget hooks
5. Emit telemetry through existing channels

**SWOT**
- Strengths: Lowest immediate change footprint.
- Weaknesses: Leaves feature fragmentation and weak long-term boundaries.
- Opportunities: Fast proof-of-value pilot.
- Threats: Technical debt and incompatible interfaces for later multi-provider expansion.

**Security risk analysis (risk -> testability signal)**
- Inconsistent enforcement across stitched modules (M/H) -> end-to-end policy coverage tests.
- Partial budgeting implementation (M/M) -> budget reconciliation tests against usage traces.
- Weak cache invalidation semantics (M/M) -> replay tests with policy-version keying assertions.

**Complexity/cost estimate**
- Complexity: Low-Medium
- Cost: Low-Medium
- Time-to-first-value: Very High

**Migration path from current code**
- Primarily composition and wrappers around existing files in `src/core/routing/`, `src/core/resilience/`, and `src/core/providers/`.

## Decision Matrix
| Criterion | Option A | Option B | Option C | Option D |
|---|---|---|---|---|
| Requirement coverage (all 10 capabilities) | M | H | H | M |
| Alignment with mixin/core separation conventions | H | M | H | M |
| Phase-1 delivery speed | H | M-L | H | H |
| Long-term scalability and multi-tenant governance | M | H | H | M-L |
| Performance headroom | M | M | H | M |
| Operational complexity | M | H | M-H | M |
| Migration risk from current code | M | H | M | M-L |
| Overall weighted fit for this project | 7.6/10 | 7.2/10 | 8.6/10 | 6.8/10 |

## Recommendation
**Option C - Hybrid Split-Plane Gateway**

Rationale:
1. Best balance of immediate deliverability and long-term architecture quality.
2. Directly matches repository direction that separates orchestration from performance-critical cores and enables Rust acceleration where justified.
3. Preserves fail-closed, guardrail-first behavior from established ADR patterns while avoiding premature service-only complexity.
4. Provides clean path to both in-process phase-1 rollout and future service-mode deployment.

Historical prior art references used:
- `docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md`
- `docs/architecture/adr/0005-specialized-agent-library-hybrid-adapter-runtime.md`
- `docs/project/archive/prj0000088-ai-fuzzing-security/prj0000088-ai-fuzzing-security.think.md`
- `docs/architecture/archive/TASK_COMPLETION_REPORT.md`

Recommendation risks mapped to testability:
- Contract drift between control/data planes -> interface parity tests + schema-version compatibility tests.
- Fallback storm under provider degradation -> fault-injection tests and fallback-rate SLO monitoring.
- Budget/cache race conditions -> concurrency/idempotency tests and transaction reconciliation checks.

## Phased Roadmap
### Phase 1 - Minimal Viable Gateway
- Implement in-process split-plane contracts with Python data-path implementation.
- Required capabilities in v1:
  - routing/LB + fallback
  - auth context + access policy
  - token budget reservation/commit
  - baseline guardrails (pre and post)
  - observability envelope (trace id, route id, policy version)
- Defer semantic vector similarity acceleration to non-blocking path while keeping semantic cache API contract stable.

### Phase 2 - Reliability and Safety Hardening
- Enforce full tool/skill catcher chain with interception policy points.
- Add deterministic fail-closed tests for all policy and provider failure classes.
- Expand cache invalidation strategy and policy-version aware cache keys.
- Add replayable decision logs and redaction validation for sensitive context.

### Phase 3 - Performance and Multi-Tenant Controls
- Move hot operations (semantic lookup + budget accounting) to Rust-backed path after parity gates.
- Introduce stronger tenant isolation controls and quota tiers.
- Add adaptive routing/cost-aware balancing and advanced load-shedding policies.
- Optional service-mode deployment for centralized enterprise governance.

## Open Questions
1. Interface contracts for @3design:
	- Should `GatewayCore.handle(request)` return a single `GatewayResult` envelope including route/fallback/budget/cache metadata?
	- What is the canonical provider adapter contract name: `ProviderAdapter` vs `ModelProviderAdapter`?
2. Naming decisions:
	- Policy engine abstraction: `GatewayPolicyEngine` vs `GuardrailPolicyEngineV2`.
	- Provider abstraction: `ProviderAdapter` vs `ProviderRuntimeAdapter`.
3. Persistence strategy:
	- Budgets: in-memory + durable append log, or immediate backend persistence path?
	- Semantic cache: local embedded store first or backend-managed cache service?
	- Trace metadata: OTel-only vs OTel + structured audit event store.
4. Guardrail enforcement placement:
	- Must pre-prompt and post-response always run in control plane?
	- Should tool interception be centralized in gateway or delegated to per-tool policy wrappers?
5. Context and memory integration:
	- Context compaction at gateway boundary vs caller-managed context assembly.
	- Memory write policy: synchronous commit vs asynchronous write-behind with retry.

## External Pattern Signals (Approved Internet Sources)
- Azure Gateway Routing pattern confirms single-endpoint abstraction, instance/version routing, and gateway bottleneck/SPOF cautions relevant to Option B/C.
- Azure Circuit Breaker pattern reinforces fail-fast open/half-open/closed state behavior, fallback defaults, and observability requirements already reflected in current PyAgent resilience modules.
- LiteLLM public architecture positioning validates market precedent for unified multi-provider gateway surfaces with centralized auth, budget/cost controls, fallback, and observability.
