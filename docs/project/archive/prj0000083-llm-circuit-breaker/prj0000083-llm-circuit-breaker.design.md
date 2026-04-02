# prj0000083 — llm-circuit-breaker — Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-26_

## Selected Approach

Option B from `@2think`: **`CircuitBreakerMixin` + `CircuitBreakerCore`**. A
`CircuitBreakerMixin` exposes `await self.cb_call(provider_key, coro)` to any agent
that inherits it — mirroring `SandboxMixin.sandbox_tx()` exactly. Pure state-machine
logic lives in `CircuitBreakerCore`, which operates on `CircuitBreakerState` objects
and is fully testable without agent plumbing. A `CircuitBreakerRegistry` maps `str`
provider keys to `CircuitBreakerState` instances, is passed into agents via constructor
injection (no global singletons), and exposes `get_or_create` / `get_fallback` for the
mixin to use. Exceptions live in a dedicated `exceptions.py`. The design adds 7 new
files inside `src/core/resilience/` and touches zero existing files.

---

## Module Layout

| File | Responsibility |
|------|---------------|
| `src/core/resilience/__init__.py` | Public re-exports for the package |
| `src/core/resilience/CircuitBreakerConfig.py` | `@dataclass` — per-provider thresholds and fallback list |
| `src/core/resilience/CircuitBreakerState.py` | `CircuitState` enum + `@dataclass` — per-provider mutable state and counters |
| `src/core/resilience/CircuitBreakerCore.py` | Stateless logic — `record_success`, `record_failure`, `should_allow`, `reset`, `check_state` |
| `src/core/resilience/CircuitBreakerRegistry.py` | `str → CircuitBreakerState` mapping; all mutations under `asyncio.Lock` |
| `src/core/resilience/CircuitBreakerMixin.py` | Agent mixin — `cb_call(provider_key, coro)`, `_setup_circuit_breaker(registry)` |
| `src/core/resilience/exceptions.py` | `CircuitOpenError`, `AllCircuitsOpenError` |

---

## API Contracts

### CircuitBreakerConfig

```python
@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    # consecutive failures before OPEN transition
    recovery_timeout: float = 30.0
    # seconds before OPEN → HALF_OPEN probe
    window_seconds: float = 60.0
    # sliding window for failure counting (future use)
    fallback_providers: list[str] = field(default_factory=list)
    # ordered fallback provider keys e.g. ["openai", "anthropic"]
```

### CircuitBreakerState

```python
class CircuitState(Enum):
    CLOSED   = "closed"
    OPEN     = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerState:
    provider_key: str
    # --- state machine ---
    state: CircuitState = CircuitState.CLOSED
    consecutive_failures: int = 0
    last_failure_time: float = 0.0        # time.monotonic() timestamp
    probe_in_flight: bool = False          # True while the single HALF_OPEN probe is executing
    # --- counters (no Prometheus dependency) ---
    total_calls: int = 0
    total_failures: int = 0
    total_successes: int = 0
```

### CircuitBreakerCore

Stateless helper; all methods accept state/config objects so they are trivially unit-testable.

```python
class CircuitBreakerCore:

    def record_success(
        self,
        state: CircuitBreakerState,
    ) -> None:
        """Increment total_successes; reset consecutive_failures; transition HALF_OPEN → CLOSED;
        release probe_in_flight slot."""

    def record_failure(
        self,
        state: CircuitBreakerState,
        config: CircuitBreakerConfig,
    ) -> None:
        """Increment total_failures and consecutive_failures; record last_failure_time;
        transition CLOSED → OPEN when consecutive_failures >= failure_threshold;
        release probe_in_flight slot on HALF_OPEN failure; reset OPEN timer."""

    def should_allow(
        self,
        state: CircuitBreakerState,
        config: CircuitBreakerConfig,
    ) -> bool:
        """Return True if a call should proceed.
        CLOSED: always True.
        OPEN: False (unless recovery_timeout elapsed → promotes to HALF_OPEN first).
        HALF_OPEN: True only when probe_in_flight is False; sets probe_in_flight = True atomically."""

    def reset(
        self,
        state: CircuitBreakerState,
    ) -> None:
        """Force circuit to CLOSED; zero consecutive_failures and probe_in_flight."""

    def check_state(
        self,
        state: CircuitBreakerState,
        config: CircuitBreakerConfig,
    ) -> CircuitState:
        """Compute effective state without mutation; promotes OPEN → HALF_OPEN when
        time.monotonic() - last_failure_time >= recovery_timeout."""
```

### CircuitBreakerRegistry

```python
class CircuitBreakerRegistry:

    def __init__(self) -> None:
        # _states: dict[str, CircuitBreakerState]
        # _configs: dict[str, CircuitBreakerConfig]
        # _lock: asyncio.Lock  — created lazily on first async access
        # _core: CircuitBreakerCore

    async def get_or_create(
        self,
        key: str,
        config: CircuitBreakerConfig,
    ) -> CircuitBreakerState:
        """Return existing state for *key*, or create and register a new one with *config*."""

    async def get_fallback(
        self,
        key: str,
    ) -> str | None:
        """Return the first CLOSED fallback provider from key's config.fallback_providers,
        or None when all are OPEN / HALF_OPEN or no fallbacks configured."""

    async def record_success(self, key: str) -> None:
        """Delegate to CircuitBreakerCore.record_success under lock."""

    async def record_failure(self, key: str) -> None:
        """Delegate to CircuitBreakerCore.record_failure under lock."""

    async def should_allow(self, key: str) -> bool:
        """Delegate to CircuitBreakerCore.should_allow under lock."""

    async def reset(self, key: str) -> None:
        """Delegate to CircuitBreakerCore.reset under lock."""
```

### CircuitBreakerMixin

Mirrors `SandboxMixin`. Consuming agent sets `self._circuit_registry` before first `cb_call`.

```python
class CircuitBreakerMixin:

    _circuit_registry: CircuitBreakerRegistry

    def _setup_circuit_breaker(
        self,
        registry: CircuitBreakerRegistry,
    ) -> None:
        """Bind a registry to this agent instance. Called from agent __init__."""

    async def cb_call(
        self,
        provider_key: str,
        coro: Coroutine[Any, Any, T],
        config: CircuitBreakerConfig | None = None,
    ) -> T:
        """Execute *coro* through the circuit breaker for *provider_key*.

        If the circuit is OPEN:
          - Attempt fallback providers from config.fallback_providers in order.
          - Raise AllCircuitsOpenError if every provider (primary + fallbacks) is OPEN.
        If the circuit is HALF_OPEN:
          - Allow exactly one probe; other callers raise CircuitOpenError immediately.
        On success: record_success on the executing provider.
        On failure: record_failure on the executing provider; re-raise original exception.
        """

    def _validate_circuit(
        self,
        provider_key: str,
    ) -> None:
        """Raise AttributeError if _circuit_registry is not set (mirrors SandboxMixin._validate_host pattern)."""
```

### Exceptions

```python
class CircuitOpenError(Exception):
    """Raised when a request is blocked because the circuit for provider_key is OPEN.

    Attributes:
        provider_key: str — the provider whose circuit is open.
        state: CircuitState — OPEN or HALF_OPEN (probe_in_flight).
    """
    def __init__(self, provider_key: str, state: CircuitState) -> None: ...

class AllCircuitsOpenError(Exception):
    """Raised by cb_call when every provider in the chain (primary + fallbacks) is OPEN.

    Attributes:
        tried_keys: list[str] — ordered list of provider keys that were attempted.
    """
    def __init__(self, tried_keys: list[str]) -> None: ...
```

---

## Data Flow

```
Agent calls: await self.cb_call("flm", llm_coro)
       │
       ▼
CircuitBreakerMixin.cb_call("flm", llm_coro)
       │
       ├─ registry.get_or_create("flm", config)  ──► CircuitBreakerState(provider_key="flm")
       │
       ├─ registry.should_allow("flm")
       │       └─ core.should_allow(state, config)
       │              ├─ CLOSED  → True
       │              ├─ OPEN (timeout elapsed) → promote to HALF_OPEN → True (sets probe_in_flight)
       │              ├─ OPEN (timeout not elapsed) → False
       │              └─ HALF_OPEN + probe already in flight → False
       │
       ├─ [False] ─► registry.get_fallback("flm")
       │                    └─ iterate config.fallback_providers
       │                           ├─ "openai" CLOSED → use "openai"
       │                           └─ all OPEN → raise AllCircuitsOpenError(["flm", "openai", ...])
       │
       ├─ [True] ─► await coro  (or await fallback_coro routed to fallback provider)
       │
       ├─ success → registry.record_success(active_key) → state.total_successes++
       │                                                  consecutive_failures = 0
       │                                                  HALF_OPEN → CLOSED
       │
       └─ failure → registry.record_failure(active_key) → state.total_failures++
                                                          consecutive_failures++
                                                          if >= threshold → OPEN
                                                          probe_in_flight = False
                                                          re-raise exception
```

---

## Test Scope (inputs for @4plan)

### Unit — CircuitBreakerCore (stateless, synchronous)
1. `test_core_initial_state_closed` — new `CircuitBreakerState` defaults to `CLOSED`, zero counters.
2. `test_core_record_failure_increments_consecutive` — each `record_failure` increments `consecutive_failures`.
3. `test_core_opens_after_failure_threshold` — after `failure_threshold` calls to `record_failure`, `state.state == OPEN`.
4. `test_core_half_open_after_recovery_timeout` — `check_state` returns `HALF_OPEN` when `time.monotonic() - last_failure_time >= recovery_timeout`.
5. `test_core_probe_success_transitions_to_closed` — `record_success` on `HALF_OPEN` → `state.state == CLOSED`.
6. `test_core_probe_failure_resets_to_open` — `record_failure` on `HALF_OPEN` → `OPEN`, `probe_in_flight = False`.
7. `test_core_half_open_probe_exclusivity` — first `should_allow` sets `probe_in_flight = True`; second call returns `False`.
8. `test_core_reset_forces_closed` — `reset()` zeroes counters, clears `probe_in_flight`, sets `CLOSED`.
9. `test_core_record_success_increments_counters` — `total_successes` increments, `consecutive_failures` resets to 0.

### Unit — CircuitBreakerRegistry
10. `test_registry_get_or_create_same_key_returns_same_object` — two calls with the same key return identical `CircuitBreakerState`.
11. `test_registry_get_fallback_returns_first_closed_provider` — primary OPEN, fallback `"openai"` CLOSED → returns `"openai"`.
12. `test_registry_get_fallback_returns_none_when_all_open` — all fallbacks OPEN → returns `None`.
13. `test_registry_record_and_allow_delegate_to_core` — `record_success/failure` and `should_allow` update state correctly.

### Unit — CircuitBreakerMixin
14. `test_mixin_cb_call_returns_coro_result_on_success` — happy-path: result returned, success recorded.
15. `test_mixin_cb_call_records_failure_and_reraises` — exception in coro → failure recorded, same exception re-raised.
16. `test_mixin_cb_call_open_circuit_raises_circuit_open_error_without_calling_coro` — OPEN circuit: coro never awaited.
17. `test_mixin_cb_call_routes_to_fallback_when_primary_open` — primary OPEN, fallback CLOSED → coro executed, fallback key used.
18. `test_mixin_cb_call_raises_all_circuits_open_when_exhausted` — primary + all fallbacks OPEN → `AllCircuitsOpenError(tried_keys)`.

### Integration
19. `test_integration_open_then_half_open_then_closed_full_cycle` — full state machine cycle through CLOSED → OPEN → HALF_OPEN → CLOSED using async coroutines and monkeypatched `time.monotonic`.
20. `test_integration_concurrent_half_open_only_one_probe_passes` — two concurrent coroutines race in HALF_OPEN state; exactly one proceeds, the other gets `CircuitOpenError`.

---

## Files to Create (Zero Modifications)

**7 new files, 0 modifications to existing files:**

```
src/core/resilience/__init__.py
src/core/resilience/exceptions.py
src/core/resilience/CircuitBreakerConfig.py
src/core/resilience/CircuitBreakerState.py
src/core/resilience/CircuitBreakerCore.py
src/core/resilience/CircuitBreakerRegistry.py
src/core/resilience/CircuitBreakerMixin.py
```

---

## Open Questions Resolved

| # | Question | Decision |
|---|----------|----------|
| 1 | Registry lifecycle | Per-agent constructor injection. `CircuitBreakerRegistry` passed via `__init__` or `_setup_circuit_breaker()`. Tests create fresh registries — no globals. |
| 2 | Integration point | Mixin exposes `cb_call(provider_key, coro)`. Agents call `await self.cb_call("flm", coro)` — wraps any async coroutine. |
| 3 | HALF_OPEN probe exclusivity | `probe_in_flight: bool` flag on `CircuitBreakerState`; only the first caller sets it and proceeds; all others immediately receive `CircuitOpenError`. |
| 4 | Prometheus metrics | Skipped. Simple counters `total_calls`, `total_failures`, `total_successes` on `CircuitBreakerState` — zero external deps. |
| 5 | Fallback exhaustion | `AllCircuitsOpenError(tried_keys)` raised immediately when all fallbacks are OPEN; no partial retry. |
| 6 | Provider key type | Plain `str` (e.g. `"flm"`, `"openai"`, `"anthropic"`). |

## Non-Functional Requirements

- **Performance:** `asyncio.Lock` per registry only (not per call); `check_state` is a simple `time.monotonic()` comparison — O(1). No I/O in the critical path before deciding allow/deny.
- **Security:** No provider credentials stored in state; `provider_key` strings are opaque labels — no injection risk.
- **Testability:** `CircuitBreakerCore` is a pure class with no side effects (except state mutations on passed-in objects); fully synchronous and does not require event-loop. Registry is injectable with `asyncio.Lock` created lazily so tests can pass without a running loop.
