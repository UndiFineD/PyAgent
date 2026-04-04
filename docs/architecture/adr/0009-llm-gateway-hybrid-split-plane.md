# ADR-0009 - LLM Gateway Hybrid Split-Plane Architecture

## Status

- Accepted

## Date

- 2026-04-04

## Owners

- @3design
- Reviewers: @4plan, @8ql

## Context

PyAgent needs one governed LLM gateway path that combines policy-first controls, routing, fallback, budget accounting, semantic caching, observability correlation, context handling, memory integration, and tool interception. Existing capabilities exist but are distributed across provider adapters, routing modules, resilience modules, and backend surfaces.

The architecture must satisfy:
1. Phase-one delivery as in-process integration.
2. Fail-closed behavior for policy/security paths.
3. Future acceleration path for hot-path operations in `rust_core/`.
4. Compatibility with PyAgent conventions: core/agent separation, composition over inheritance, and transaction discipline for mutable state.

## Decision

Adopt a hybrid split-plane gateway architecture:
1. Control plane in Python for auth/policy decisions, route governance, fallback policy, telemetry correlation, and tool/skill interception.
2. Data plane contracts defined now and implemented in Python in phase one, with explicit migration path to Rust-backed implementations for provider execution hot path, semantic cache operations, and budget accounting.
3. Keep phase one in-process and defer optional service mode to a later phase without breaking envelope contracts.

## Alternatives considered

### Alternative A - Fully In-Process Monoplane Gateway

- Summary: Keep all logic in one Python orchestration plane with minimal boundary distinction.
- Why not chosen: Faster start, but weaker long-term performance evolution and less explicit contract isolation for Rust acceleration.

### Alternative B - Immediate Dedicated Gateway Service

- Summary: Introduce gateway as network service at phase one.
- Why not chosen: Higher operational complexity and rollout risk before contract and reliability baselines are proven in-process.

### Alternative C - Thin Adapter Over Existing Routing Modules

- Summary: Minimal wrapper over existing routing/resilience/provider logic.
- Why not chosen: Leaves capability fragmentation and does not establish stable interfaces for all required pillars.

## Consequences

### Positive

- Creates explicit contracts that unify all ten capability pillars behind one deterministic gateway path.
- Preserves fail-closed governance with policy-first sequencing.
- Enables phased performance evolution to Rust without rewriting control-plane policy behavior.
- Minimizes initial deployment risk by staying in-process in phase one.

### Negative / Trade-offs

- Adds upfront design and interface complexity.
- Requires strict contract testing to prevent control/data plane drift.
- Temporary duplication risk while existing modules are wrapped into the new gateway contracts.

## Implementation impact

- Affected components:
  - `src/core/gateway/` (new contract boundary)
  - `src/core/providers/FlmChatAdapter.py`
  - `src/core/routing/*`
  - `src/core/resilience/*`
  - `backend/auth.py`
  - `backend/app.py`
  - `backend/tracing.py`
  - `backend/memory_store.py`
- Migration/rollout notes:
  - Phase 1: in-process contract implementation.
  - Phase 2: reliability and safety hardening.
  - Phase 3: Rust acceleration and optional service mode.
- Backward compatibility notes:
  - Existing call paths remain functional while gateway adoption is staged.

## Validation and monitoring

- Tests or checks required:
  - Policy fail-closed path tests.
  - Budget reserve/commit idempotency tests.
  - Fallback chain determinism tests.
  - Cache write safety tests (deny/unsafe responses never persisted).
  - Tool interception allow/deny tests.
- Runtime signals or metrics to monitor:
  - Fallback rate by provider/model.
  - Deny-rate by policy decision stage.
  - Budget reservation and commit mismatches.
  - Cache hit ratio and invalidation errors.
  - End-to-end latency and p95/p99 by route.
- Rollback triggers:
  - Sustained policy bypass indicators.
  - Budget reconciliation drift above agreed threshold.
  - Fallback storm behavior that breaches reliability SLOs.

## Related links

- Related project artifact(s):
  - `docs/project/prj0000124-llm-gateway/llm-gateway.design.md`
  - `docs/project/prj0000124-llm-gateway/llm-gateway.think.md`
- Related architecture docs:
  - `docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md`
  - `docs/architecture/adr/0005-specialized-agent-library-hybrid-adapter-runtime.md`
- Supersedes/Superseded-by (if any):
  - none
