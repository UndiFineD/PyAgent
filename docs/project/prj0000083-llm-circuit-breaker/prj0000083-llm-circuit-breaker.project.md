# prj0000083 — llm-circuit-breaker — Project Overview

_Status: IN_PROGRESS_
_Owner: @1project | Updated: 2026-03-26_

## Project Identity
**Project ID:** prj0000083
**Short name:** llm-circuit-breaker
**Project folder:** `docs/project/prj0000083-llm-circuit-breaker/`
**Priority:** P3
**Budget tier:** S
**Tags:** resilience, llm, infrastructure

## Summary

Per-provider LLM request circuit breaker with configurable failure thresholds,
exponential backoff, and fallback model routing. The circuit breaker wraps every
outbound LLM call and tracks success / failure rates per provider (e.g. OpenAI,
Anthropic, local vLLM). When a provider exceeds its failure threshold the circuit
opens, redirecting subsequent requests to a configured fallback provider until the
provider recovers (half-open probe, then close if successful).

## Scope

**In scope:**
- `CircuitBreakerState` enum (CLOSED, OPEN, HALF_OPEN)
- `ProviderCircuitBreaker` — per-provider state machine with configurable thresholds
- `CircuitBreakerRegistry` — manages one breaker instance per provider key
- Exponential backoff with jitter for retry scheduling
- Fallback model routing (ordered list of alternatives)
- Integration hook into the existing `BaseAgent` / `LLMClient` call path
- Prometheus counter/gauge metrics for circuit state transitions
- Unit tests for all state transitions and fallback routing

**Out of scope:**
- UI / dashboard for circuit state (observability via Prometheus only)
- Persistent circuit state across process restarts (in-memory only for now)
- Rate-limiting (separate concern, existing `RateLimiter` handles it)
- Changes to `backend/` WebSocket layer

## Acceptance Criteria

| # | Criterion |
|---|-----------|
| AC1 | Circuit opens after `failure_threshold` consecutive failures (default 5) within `window_seconds` (default 60). |
| AC2 | While OPEN, all requests to the affected provider immediately raise `CircuitOpenError` without making an outbound call. |
| AC3 | After `recovery_timeout` seconds (default 30) the circuit transitions to HALF_OPEN and allows exactly one probe request. |
| AC4 | A successful probe closes the circuit; a failed probe resets the OPEN timer and remains OPEN. |
| AC5 | Fallback routing: when the primary provider's circuit is OPEN, `CircuitBreakerRegistry.route_call()` transparently retries with the next fallback provider whose circuit is CLOSED. |
| AC6 | Exponential backoff with jitter is applied to retries before reaching the fallback provider, with configurable `base_delay`, `max_delay`, and `jitter_factor`. |
| AC7 | Prometheus metrics exported: `llm_circuit_state` (gauge per provider), `llm_circuit_transitions_total` (counter), `llm_requests_routed_total` (counter with `provider` and `outcome` labels). |
| AC8 | `pytest tests/structure -q` passes (no structural regressions). |
| AC9 | `pytest tests/ -q` passes with ≥ 90 % coverage on the new module. |

## Branch Plan

**Expected branch:** `prj0000083-llm-circuit-breaker`
**Scope boundary:** `docs/project/prj0000083-llm-circuit-breaker/`, `src/core/`, `tests/`
**Handoff rule:** `@9git` must refuse staging, commit, push, or PR work unless the
active branch is `prj0000083-llm-circuit-breaker` and changed files stay inside the
scope boundary.
**Failure rule:** If the project ID or branch plan is missing, inherited, conflicting,
or ambiguous, return the task to `@0master` before downstream handoff.

## Timeline

| # | Milestone | Agent | Target |
|---|-----------|-------|--------|
| M1 | Options explored | @2think | Sprint 1 |
| M2 | Design confirmed | @3design | Sprint 1 |
| M3 | Plan finalized | @4plan | Sprint 1 |
| M4 | Tests written (TDD) | @5test | Sprint 2 |
| M5 | Code implemented | @6code | Sprint 2 |
| M6 | Integration validated | @7exec | Sprint 2 |
| M7 | Security scan clean | @8ql | Sprint 2 |
| M8 | Committed & PR | @9git | Sprint 2 |

## Milestones

| # | Milestone | Agent | Status |
|---|-----------|-------|--------|
| M1 | Options explored | @2think | |
| M2 | Design confirmed | @3design | |
| M3 | Plan finalized | @4plan | |
| M4 | Tests written | @5test | |
| M5 | Code implemented | @6code | |
| M6 | Integration validated | @7exec | |
| M7 | Security clean | @8ql | |
| M8 | Committed | @9git | |

## Dependencies

| Module / File | Relationship |
|---------------|-------------|
| `src/core/base/base_agent.py` | Integration point — LLM call path to be wrapped |
| `src/core/base/mixins/` | May add a `CircuitBreakerMixin` here |
| `backend/logging_config.py` | Structured logging for state transitions |
| `src/` (Prometheus client) | `prometheus_client` already in `requirements.txt` |
| `tests/conftest.py` | Shared fixtures |

## Risk Notes

- **Concurrency:** Python `asyncio` tasks may race on state updates; use `asyncio.Lock`
  per breaker instance.
- **Clock skew:** Monotonic clocks (`time.monotonic()`) must be used for timeouts to
  avoid wall-clock drift bugs.
- **Existing call path coupling:** Wrapping `BaseAgent` without breaking existing tests
  requires careful injection rather than monkey-patching.
- **Metric cardinality:** Provider keys used as label values must be bounded to avoid
  Prometheus cardinality explosion — validate against an allowlist.

## Status
_Last updated: 2026-03-26_
Project folder created, all 9 artifact stubs initialised. Ready for handoff to @2think.
