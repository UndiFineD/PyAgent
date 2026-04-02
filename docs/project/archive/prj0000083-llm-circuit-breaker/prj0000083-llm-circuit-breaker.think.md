# prj0000083 — llm-circuit-breaker — Options Exploration

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-26_

## Problem Statement

When an LLM provider (OpenAI, Anthropic, local vLLM via FLM) becomes unreliable —
returning 5xx errors, timing out, or exhausting rate limits — every agent in the
swarm blindly retries against the same unavailable endpoint. This amplifies latency,
burns quota, and can cascade into a full-swarm stall.

The root cause is the absence of a **failure-isolation layer** between agents and
outbound LLM calls. The existing `retry()` in `src/tools/common.py` applies a flat
delay with no state — it has no concept of "this provider has been broken for 30
seconds; skip it and use a fallback." `FlmChatAdapter.create_completion()` is the
primary call site; it delegates directly to the OpenAI-compatible client with no
circuit-break guard.

Required behaviours:
- Track per-provider failure counts over a sliding time window.
- Open the circuit after `failure_threshold` consecutive failures — immediately
  returning `CircuitOpenError` without making an outbound call.
- After `recovery_timeout` seconds, probe with one request (HALF_OPEN); close on
  success, reset OPEN timer on failure.
- Transparently route to the next available fallback provider when primary is OPEN.
- Emit Prometheus metrics for circuit state transitions.

---

## Option A — Async Decorator / `@circuit_breaker`

**Approach.** A module-level `CircuitBreakerRegistry` dict (keyed by provider string)
holds `ProviderCircuitBreaker` state machines. Call sites wrap any async callable with
a `route_call(provider, coro_fn, fallbacks=[...])` free function. No mixin or base
class required.

```
src/core/resilience/
    CircuitBreakerCore.py   # ProviderCircuitBreaker, CircuitBreakerRegistry, backoff
    __init__.py
```

Integration at `FlmChatAdapter.create_completion()`:
```python
result = await route_call("flm", adapter.create_completion, fallbacks=["openai"])
```

**Pros:**
- Minimal surface area — 2 files.
- No inheritance required; works with any callable, not just agent classes.
- Easy to unit-test by mocking the callable.

**Cons:**
- No architecture fit: the project instructions explicitly require a
  `CircuitBreakerMixin` for agent composition (matching the `SandboxMixin` pattern).
- Registry is a module-level global; concurrent test isolation requires careful
  teardown.
- Agents would need to import and call a free function — not composable via `self.`.

**Risk (H/M/L):**
- Global state race in async tests — M/H without `asyncio.Lock` on registry writes.
- Call sites must be individually updated to wrap every LLM invocation — M (scope creep).
- Free functions are harder to mock per-agent in integration tests — L.

---

## Option B — `CircuitBreakerMixin` + `CircuitBreakerCore` (Recommended)

**Approach.** Split domain logic from agent interface following the Core/Agent pattern
mandated by `copilot-instructions.md`. The mixin exposes `await
self.llm_call_with_breaker(provider, coro_fn, fallbacks=[...])` — identical pattern to
`SandboxMixin.sandbox_tx()`. Agents compose it via multiple inheritance and set
`self._circuit_registry` to a shared `CircuitBreakerRegistry` instance.

```
src/core/resilience/
    CircuitBreakerCore.py   # CircuitBreakerState enum, ProviderCircuitBreaker,
                            # CircuitBreakerRegistry, CircuitOpenError, backoff
    CircuitBreakerMixin.py  # Agent-composable mixin, mirrors SandboxMixin
    __init__.py
```

State machine inside `CircuitBreakerCore`:
```
CLOSED ──(failure_threshold exceeded)──► OPEN
OPEN   ──(recovery_timeout elapsed)────► HALF_OPEN
HALF_OPEN ──(probe success)────────────► CLOSED
HALF_OPEN ──(probe failure)────────────► OPEN (reset timer)
```

`CircuitBreakerRegistry` holds `dict[str, ProviderCircuitBreaker]`, one per provider
key.  All state mutations guarded by `asyncio.Lock`.

Backoff in `CircuitBreakerCore.backoff_seconds(attempt)`:
```
delay = min(base_delay * (2 ** attempt) + random.uniform(0, jitter), max_delay)
```

**Pros:**
- Exact match to project architecture constraints (`CircuitBreakerMixin`, mixin-based,
  `CircuitBreakerCore`, async, PascalCase filenames).
- Mirrors `SandboxMixin` / `SandboxedStorageTransaction` — zero learning curve for
  `@6code`.
- `Core` class is fully testable without any agent plumbing.
- 3 files — fits the "S" budget.
- Prometheus metrics live in `Core`; fallback import pattern mirrors `src/chat/api.py`.
- Registry is injectable (not global), enabling per-test isolation.

**Cons:**
- Agents must be updated to inherit `CircuitBreakerMixin` — minor but real change.
- Slightly more boilerplate than Option A (mixin + core vs. just core).

**Risk (H/M/L):**
- `asyncio.Lock` must be per-registry, not module-level — L (straightforward with
  `dataclass`).
- HALF_OPEN probe race: two concurrent callers both see HALF_OPEN when the probe slot
  should be exclusive  — M. Mitigation: an `_probe_in_flight: bool` flag guarded by
  the lock.
- Prometheus `LabeledMetricConflict` if registry is re-created in tests — L. Mitigation:
  lazy singleton or `try/except` on registration.

---

## Option C — `ResilientFlmChatAdapter` Proxy Wrapper

**Approach.** Subclass or compose `FlmChatAdapter` into a `ResilientFlmChatAdapter`
that wraps `create_completion()` with circuit-breaker logic internally. Breaker state
is per-adapter instance (not shared across providers).

```
src/core/providers/
    ResilientFlmChatAdapter.py  # wraps FlmChatAdapter + embedded breaker state
```

**Pros:**
- Drop-in replacement — callers keep using the adapter interface unchanged.
- 1 file.

**Cons:**
- Violates Core/Agent separation: mixing domain logic into the adapter.
- FLM-specific — does not protect calls to OpenAI, Anthropic, or any non-FLM provider.
- No shared registry → cannot implement cross-provider fallback routing.
- Does not meet the project Acceptance Criteria (AC5: `route_call()` across providers).
- Wrong location (`src/core/providers/` vs. the required `src/core/resilience/`).
- Not composable by agents as a mixin.

**Risk (H/M/L):**
- Scope insufficient — AC5 cannot be met without a registry — H.
- Silent state divergence: multiple adapter instances track independent failure counts —
  M.
- Provider-agnostic retry never gets implemented — M.

---

## Decision Matrix

| Criterion                     | A: Decorator | B: Mixin+Core | C: Proxy |
|-------------------------------|:------------:|:-------------:|:--------:|
| Architecture fit (mixin req.) | Low          | **High**      | Low      |
| Passes all ACs (AC5 routing)  | Yes          | **Yes**       | No       |
| Stdlib-only (no new deps)     | Yes          | **Yes**       | Yes      |
| Testability (per-test isolation) | Medium    | **High**      | Medium   |
| File count (S budget ≤ 3)     | 2            | **3**         | 1        |
| Provider-agnostic             | Yes          | **Yes**       | No       |
| Composable by agents          | No           | **Yes**       | No       |
| Mirrors existing patterns     | Partial      | **Full**      | No       |
| HALF_OPEN probe-race safety   | Medium       | **High**      | N/A      |

---

## Recommendation

**Option B — `CircuitBreakerMixin` + `CircuitBreakerCore`**

Rationale:
- It is the only option that satisfies all nine Acceptance Criteria, particularly AC5
  (cross-provider fallback routing via `CircuitBreakerRegistry`).
- It exactly mirrors the project's mixin architecture (`SandboxMixin` pattern) — no
  new conventions needed.
- The Core/Mixin split keeps domain logic independently testable while giving agents a
  clean `self.llm_call_with_breaker(...)` interface.
- Three files is the minimum necessary to achieve full separation and is within the S
  budget.
- All state is injectable (`CircuitBreakerRegistry` is a constructor argument), making
  test isolation trivial.

The implementation should be strictly minimal: no external dependencies beyond `asyncio`,
`random`, `time`, `enum`, `dataclasses`, and an optional `prometheus_client` with the
fallback pattern already established in `src/chat/api.py`.

---

## Key Design Questions for @3design

1. **Registry lifecycle** — Should `CircuitBreakerRegistry` be created once by the
   swarm and passed to agents via constructor injection, or should each agent create
   its own isolated registry? (Global shared registry enables AC5 cross-agent fallback;
   per-agent registry enables simpler test teardown.)

2. **FlmChatAdapter integration point** — Where exactly should `CircuitBreakerMixin`
   be inserted into the existing call path? Should `FlmChatAdapter.create_completion()`
   be unchanged and the mixin wrap it externally, or should `BaseAgent` call the mixin
   method which then delegates to the adapter?

3. **HALF_OPEN probe exclusivity** — Should only one concurrent caller pass through
   during HALF_OPEN (all others get `CircuitOpenError`), or should all callers wait on
   an `asyncio.Event` for the probe outcome? The event approach is safer under high
   concurrency but adds ~10 lines of complexity.

4. **Prometheus metric registration** — Should metrics be module-level singletons
   (created once on import) or per-registry instances? Module-level risks
   `ValueError: Duplicated timeseries` in tests that recreate the registry.

5. **Fallback exhaustion** — When all fallback providers' circuits are also OPEN, should
   `route_call()` raise `AllCircuitsOpenError` immediately or try again after the
   shortest remaining `recovery_timeout` among all providers?

6. **`FlmProviderConfig` vs. plain string keys** — Should provider identity in the
   registry be keyed by `str` (e.g., `"flm"`, `"openai"`) or by
   `FlmProviderConfig.base_url`? String keys are simpler; config-based keys allow
   per-endpoint granularity (e.g., two FLM instances at different ports).

---

## Codebase Integration Points

| Module | Integration type |
|--------|-----------------|
| `src/core/providers/FlmChatAdapter.create_completion()` | Primary call site to wrap; no change to signature — mixin wraps externally |
| `src/core/providers/FlmProviderConfig` | Provider key source (`base_url` or a string alias) |
| `src/core/sandbox/SandboxMixin.py` | Pattern reference — mixin structure to mirror exactly |
| `src/tools/common.retry()` | Existing flat-retry helper; `CircuitBreakerCore.backoff_seconds()` replaces its role for LLM calls |
| `src/chat/api.py` | Prometheus fallback import pattern to copy |
| `tests/` | New `tests/core/resilience/` directory for unit tests (state transitions, backoff, fallback routing) |
