# universal-agent-shell - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-27_

## Selected Option
Option B - Universal Shell Facade with Controlled Legacy Fallback.

Rationale:
1. Delivers dynamic core resolution by intent in v1.
2. Keeps current specialized routing intact as a deterministic fallback.
3. Enables incremental migration through an explicit allowlist and policy guardrails.

## Architecture
### Overview
Introduce a minimal facade module at `src/core/universal/` with five files:
1. `UniversalIntentRouter.py`
2. `UniversalCoreRegistry.py`
3. `UniversalAgentShell.py`
4. `exceptions.py`
5. `__init__.py`

The facade sits between intent ingress and existing specialized execution.

### Components and responsibilities
1. `UniversalIntentRouter`
- Normalizes a task envelope to a canonical intent key.
- Applies v1 allowlist rules and returns routing intent metadata.
- Produces a `RoutingDecision` that explicitly states `CORE` vs `LEGACY` route candidate and reason.

2. `UniversalCoreRegistry`
- Maintains an in-memory map from `intent -> core_factory`.
- Resolves core handlers for core-eligible intents.
- Enforces registration-time and resolve-time contract checks.

3. `UniversalAgentShell`
- Orchestrates end-to-end dispatch.
- Executes core path when allowed and resolvable.
- Falls back exactly once to legacy route on unsupported intent, resolver miss, timeout, or handled core error.
- Emits structured route telemetry for decision and fallback reason.

4. `exceptions`
- Defines strict error model for routing, registry, and shell execution boundaries.

5. `__init__`
- Exports public facade API for stable imports.

### High-level data flow
1. Caller provides `TaskEnvelope` to `UniversalAgentShell.dispatch(...)`.
2. Shell asks `UniversalIntentRouter.classify(envelope)` for normalized intent and route eligibility.
3. If decision is `legacy`, shell immediately invokes `legacy_dispatcher(envelope)`.
4. If decision is `core`, shell asks `UniversalCoreRegistry.resolve(intent)`.
5. If resolve succeeds, shell executes core via timeout guard.
6. On successful core execution, shell returns `DispatchResult(route="core", ...)`.
7. On known core failure categories, shell performs single fallback to legacy and returns `DispatchResult(route="legacy", fallback_reason=...)`.
8. On non-recoverable shell/contract errors, shell raises explicit facade exception without retry loop.

### Failure-loop prevention
1. Fallback attempts are capped at one per dispatch.
2. A dispatch-scoped `fallback_used` guard blocks recursion.
3. Legacy path never re-enters shell for the same dispatch ID.

## Interfaces & Contracts
### Module: `UniversalIntentRouter.py`

```python
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class TaskEnvelope:
	task_id: str
	intent: str | None
	payload: Mapping[str, Any]
	metadata: Mapping[str, Any]

@dataclass(frozen=True)
class RoutingDecision:
	normalized_intent: str
	preferred_route: str  # "core" | "legacy"
	reason: str

class UniversalIntentRouter:
	def __init__(self, *, core_allowlist: set[str]) -> None: ...
	def classify(self, envelope: TaskEnvelope) -> RoutingDecision: ...
	def normalize_intent(self, raw_intent: str | None) -> str: ...
```

Contract rules:
1. `normalize_intent` is deterministic and side-effect free.
2. Unknown or empty intents map to `"unknown"` and route `legacy`.
3. Router does not execute business logic.

### Module: `UniversalCoreRegistry.py`

```python
from typing import Protocol

class CoreHandler(Protocol):
	async def execute(self, envelope: TaskEnvelope) -> dict: ...

class UniversalCoreRegistry:
	def register(self, intent: str, factory: callable) -> None: ...
	def unregister(self, intent: str) -> None: ...
	def resolve(self, intent: str) -> CoreHandler: ...
	def has_intent(self, intent: str) -> bool: ...
	def list_intents(self) -> tuple[str, ...]: ...
```

Contract rules:
1. `register` rejects duplicates unless explicit overwrite flag is later introduced.
2. `resolve` raises `CoreNotRegisteredError` for misses.
3. Returned handler must expose async `execute(envelope)`.

### Module: `UniversalAgentShell.py`

```python
from dataclasses import dataclass
from typing import Awaitable, Callable

LegacyDispatcher = Callable[[TaskEnvelope], Awaitable[dict]]

@dataclass(frozen=True)
class DispatchResult:
	route: str  # "core" | "legacy"
	intent: str
	payload: dict
	fallback_reason: str | None

class UniversalAgentShell:
	def __init__(
		self,
		*,
		intent_router: UniversalIntentRouter,
		core_registry: UniversalCoreRegistry,
		legacy_dispatcher: LegacyDispatcher,
		core_timeout_seconds: float = 20.0,
	) -> None: ...

	async def dispatch(self, envelope: TaskEnvelope) -> DispatchResult: ...
```

Dispatch behavior contract:
1. Exactly one terminal result per call.
2. Core path is attempted only when router returns `preferred_route="core"`.
3. Shell may fallback once to legacy for recoverable categories:
   - `CoreNotRegisteredError`
   - `CoreExecutionError`
   - `CoreTimeoutError`
4. Shell never swallows `EnvelopeValidationError` and `RoutingContractError`.

### Module: `exceptions.py`

```python
class UniversalShellError(Exception): ...
class EnvelopeValidationError(UniversalShellError): ...
class RoutingContractError(UniversalShellError): ...
class CoreRegistrationError(UniversalShellError): ...
class CoreNotRegisteredError(UniversalShellError): ...
class CoreExecutionError(UniversalShellError): ...
class CoreTimeoutError(UniversalShellError): ...
class LegacyDispatchError(UniversalShellError): ...
```

### Module: `__init__.py`

Public export contract:
1. Export only stable facade types: `TaskEnvelope`, `RoutingDecision`, `DispatchResult`, `UniversalIntentRouter`, `UniversalCoreRegistry`, `UniversalAgentShell`, and exception classes.
2. Keep internal helpers private.

## Test Scope (15-20 tests)
Target: 18 tests focused on API contracts and route correctness.

1. Router normalizes uppercase intent to lowercase canonical form.
2. Router maps missing intent to `unknown`.
3. Router returns `core` for allowlisted intent.
4. Router returns `legacy` for non-allowlisted intent.
5. Router classification is deterministic for identical input.
6. Registry registers valid core factory.
7. Registry rejects duplicate registration.
8. Registry resolves registered intent to handler instance.
9. Registry raises `CoreNotRegisteredError` for missing intent.
10. Registry `list_intents` returns stable tuple output contract.
11. Shell routes allowlisted intent to core and returns route `core`.
12. Shell routes non-allowlisted intent directly to legacy.
13. Shell falls back to legacy when registry miss occurs.
14. Shell falls back to legacy when core execution raises `CoreExecutionError`.
15. Shell falls back to legacy when core execution times out.
16. Shell raises `EnvelopeValidationError` for invalid envelope shape.
17. Shell does not attempt second fallback when legacy path fails.
18. Shell emits decision telemetry with route and fallback reason fields.

## Non-Functional Requirements
- Performance: p95 dispatch overhead added by facade is <= 5ms excluding core/legacy business execution.
- Performance: Core timeout guard defaults to 20s and is configurable via constructor.
- Performance: Registry resolution is O(1) average-case dictionary lookup.
- Security: envelope metadata must be treated as untrusted input and validated before route decisions.
- Security: no sensitive payload fields in route-decision logs (allowlist log fields only).
- Security: exception messages must avoid secret/token leakage.
- Testability: every facade dependency is constructor-injected and mockable.
- Testability: deterministic routing contract enables isolated unit tests without network or filesystem dependencies.

## Open Questions
1. Which v1 intents are in the initial core allowlist at launch?
2. Which existing legacy dispatcher function is the canonical fallback entrypoint?
3. Should telemetry use existing observability counters or define a new namespace under universal shell?
4. Are timeout values globally configured or per-intent configurable in v1?
5. Do we require sync core-handler support, or async-only contract for v1?
