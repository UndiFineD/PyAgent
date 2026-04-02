# n8n-workflow-bridge - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-27_

## Selected Option
Option B - Stdlib-only HTTP integration layer + event adapter.

Rationale:
1. Meets the bi-directional bridge goal (PyAgent -> n8n trigger and n8n -> PyAgent callback) without adding new dependencies.
2. Preserves existing backend security and routing posture by reusing current auth patterns.
3. Creates a clean bridge boundary that can later evolve to durable queueing without breaking v1 contracts.

## Architecture
### Overview
The design introduces a dedicated bridge package at `src/core/n8nbridge/` with five runtime modules and two package files.
The bridge is intentionally thin and dependency-light.

Inbound path:
1. Backend endpoint receives n8n callback event payload.
2. `N8nEventAdapter` validates and normalizes the raw payload to internal canonical event shape.
3. `N8nBridgeCore` performs idempotency check and dispatch decision.
4. Caller receives normalized bridge response with correlation and error semantics.

Outbound path:
1. Host agent or service calls `N8nBridgeMixin.trigger_workflow(...)`.
2. `N8nBridgeCore` builds canonical outbound event and adapter maps to n8n request shape.
3. `N8nHttpClient` executes stdlib HTTP call with timeout, bounded retry/backoff, optional request signing.
4. `N8nBridgeCore` returns structured result with retry metadata.

### Proposed Module Layout
1. `src/core/n8nbridge/N8nBridgeConfig.py`
   - Runtime config model and config validation.
   - Normalizes environment-driven bridge settings.
2. `src/core/n8nbridge/N8nEventAdapter.py`
   - Canonical contract translation between internal and n8n payloads.
   - Inbound/outbound schema validation and mapping helpers.
3. `src/core/n8nbridge/N8nHttpClient.py`
   - Stdlib-only HTTP transport (`urllib.request`) with retries and timeout handling.
   - Optional outbound signature and deterministic header construction.
4. `src/core/n8nbridge/N8nBridgeCore.py`
   - Orchestration logic for inbound callbacks and outbound workflow triggers.
   - Idempotency cache window and business-level response shaping.
5. `src/core/n8nbridge/N8nBridgeMixin.py`
   - Agent-facing helper methods.
   - Keeps host-agent classes thin and delegates to `N8nBridgeCore`.
6. `src/core/n8nbridge/exceptions.py`
   - Typed bridge error taxonomy.
7. `src/core/n8nbridge/__init__.py`
   - Stable package exports for consumers.

### Component Responsibilities
1. Contract layer (`N8nEventAdapter`):
   - Enforce required event fields.
   - Translate versioned event schemas.
   - Sanitize unsupported keys.
2. Transport layer (`N8nHttpClient`):
   - Build and execute HTTP requests.
   - Handle retryable vs non-retryable failures.
3. Domain orchestration (`N8nBridgeCore`):
   - Coordinate config, adapter, and client.
   - Manage idempotency TTL cache for inbound events.
4. Integration layer (`N8nBridgeMixin`):
   - Expose ergonomic methods to host agents.
   - Preserve host-agent orchestration boundaries.

## Interfaces & Contracts
### Canonical Event Shapes
All canonical contracts include `schema_version: "1.0"` in v1.

Inbound canonical event:
```python
N8nInboundEvent = TypedDict(
	"N8nInboundEvent",
	{
		"schema_version": str,
		"event_id": str,
		"event_type": str,
		"workflow_id": str,
		"execution_id": str,
		"occurred_at": str,
		"source": str,
		"correlation_id": str,
		"payload": dict,
		"auth_context": dict,
	},
)
```

Outbound canonical event:
```python
N8nOutboundEvent = TypedDict(
	"N8nOutboundEvent",
	{
		"schema_version": str,
		"event_id": str,
		"event_type": str,
		"target_workflow": str,
		"triggered_at": str,
		"correlation_id": str,
		"payload": dict,
		"metadata": dict,
	},
)
```

Bridge response contract:
```python
N8nBridgeResult = TypedDict(
	"N8nBridgeResult",
	{
		"ok": bool,
		"status": str,
		"http_status": int,
		"correlation_id": str,
		"event_id": str,
		"attempts": int,
		"retryable": bool,
		"error_code": str | None,
		"message": str,
		"data": dict,
	},
)
```

### `N8nBridgeConfig.py`
```python
class N8nBridgeConfig:
	base_url: str
	inbound_enabled: bool
	outbound_enabled: bool
	api_key_header: str
	api_key_value: str | None
	request_timeout_seconds: float
	max_retries: int
	backoff_seconds: float
	idempotency_ttl_seconds: int
	signing_secret: str | None

	@classmethod
	def from_env(cls, env: Mapping[str, str]) -> "N8nBridgeConfig": ...
	def validate(self) -> None: ...
```

Contract notes:
1. `validate` hard-fails invalid timeout, retry, and URL settings.
2. Empty `api_key_value` is allowed only when inbound auth is explicitly disabled.

### `N8nEventAdapter.py`
```python
class N8nEventAdapter:
	def to_inbound_event(self, raw_payload: dict, headers: Mapping[str, str]) -> N8nInboundEvent: ...
	def to_n8n_trigger_payload(self, event: N8nOutboundEvent) -> dict: ...
	def from_n8n_response(self, response_payload: dict, *, correlation_id: str) -> N8nBridgeResult: ...
```

Contract notes:
1. Rejects missing `event_id`, `event_type`, or workflow identifiers with `N8nSchemaError`.
2. Must preserve `correlation_id` end-to-end for tracing.

### `N8nHttpClient.py`
```python
class N8nHttpClient:
	def __init__(self, config: N8nBridgeConfig) -> None: ...

	async def post_json(
		self,
		path: str,
		payload: dict,
		*,
		correlation_id: str,
		extra_headers: Mapping[str, str] | None = None,
	) -> tuple[int, dict, dict]: ...
```

Contract notes:
1. Uses bounded retries for network and retryable 5xx status codes.
2. Raises typed transport exceptions for timeout and connection failure paths.

### `N8nBridgeCore.py`
```python
class N8nBridgeCore:
	def __init__(
		self,
		*,
		config: N8nBridgeConfig,
		adapter: N8nEventAdapter,
		http_client: N8nHttpClient,
	) -> None: ...

	async def handle_inbound_event(
		self,
		raw_payload: dict,
		headers: Mapping[str, str],
	) -> N8nBridgeResult: ...

	async def trigger_workflow(
		self,
		*,
		workflow_id: str,
		event_type: str,
		payload: dict,
		correlation_id: str | None = None,
	) -> N8nBridgeResult: ...
```

Contract notes:
1. Maintains in-memory idempotency map keyed by `event_id` with TTL eviction.
2. Returns structured result for expected failures; raises only for programmer/config errors.

### `N8nBridgeMixin.py`
```python
class N8nBridgeMixin:
	async def n8n_trigger(
		self,
		workflow_id: str,
		event_type: str,
		payload: dict,
		*,
		correlation_id: str | None = None,
	) -> N8nBridgeResult: ...

	async def n8n_handle_callback(
		self,
		raw_payload: dict,
		headers: Mapping[str, str],
	) -> N8nBridgeResult: ...
```

Contract notes:
1. Requires host object to expose `self._n8n_bridge_core`.
2. Should not embed business decision logic; delegates to core.

### `exceptions.py`
```python
class N8nBridgeError(Exception): ...
class N8nConfigError(N8nBridgeError): ...
class N8nSchemaError(N8nBridgeError): ...
class N8nAuthError(N8nBridgeError): ...
class N8nIdempotencyError(N8nBridgeError): ...
class N8nTransportError(N8nBridgeError): ...
class N8nTimeoutError(N8nTransportError): ...
class N8nHttpStatusError(N8nTransportError): ...
```

### `__init__.py`
```python
from .N8nBridgeConfig import N8nBridgeConfig
from .N8nEventAdapter import N8nEventAdapter
from .N8nHttpClient import N8nHttpClient
from .N8nBridgeCore import N8nBridgeCore
from .N8nBridgeMixin import N8nBridgeMixin
from .exceptions import (
	N8nBridgeError,
	N8nConfigError,
	N8nSchemaError,
	N8nAuthError,
	N8nIdempotencyError,
	N8nTransportError,
	N8nTimeoutError,
	N8nHttpStatusError,
)
```

## Non-Functional Requirements
- Performance:
  - Inbound adapter validation and mapping target <= 5 ms p95 per event in local baseline.
  - Outbound trigger path target <= 150 ms p95 excluding remote n8n processing time.
  - Idempotency cache operations target O(1) average lookup/insert.
- Security:
  - Inbound auth defaults to API-key enabled in non-dev environments.
  - Optional HMAC signing uses constant-time digest comparison.
  - Never log secrets or raw auth headers.
- Reliability:
  - Retry policy: max 3 attempts with bounded linear backoff in v1.
  - Distinguish retryable transport failures from deterministic contract failures.
- Testability:
  - `N8nBridgeCore` must be fully injectable with fake adapter/client.
  - No hidden globals except bounded in-memory idempotency cache with explicit TTL.

## Test Scope (18 tests)
Target: 18 tests across unit and integration-style seams.

1. Config `from_env` loads required fields and defaults.
2. Config validation rejects invalid base URL.
3. Config validation rejects non-positive timeout and negative retries.
4. Adapter maps valid inbound payload to canonical event.
5. Adapter rejects inbound payload missing required identifiers.
6. Adapter preserves correlation ID from headers.
7. Adapter maps outbound canonical event to n8n trigger payload.
8. HTTP client includes API-key header when configured.
9. HTTP client applies timeout value to request execution.
10. HTTP client retries retryable failures up to max attempts.
11. HTTP client does not retry non-retryable 4xx responses.
12. Core `handle_inbound_event` rejects duplicate event IDs inside TTL window.
13. Core `handle_inbound_event` accepts same event ID after TTL expiry.
14. Core `trigger_workflow` returns success bridge result on 2xx response.
15. Core `trigger_workflow` maps transport timeout to typed retryable failure result.
16. Mixin `n8n_trigger` delegates to core with passthrough args.
17. Mixin `n8n_handle_callback` delegates to core and returns core result.
18. End-to-end contract test: canonical outbound event -> adapter -> client mock -> normalized bridge result.

## Open Questions
1. Should v1 inbound auth allow JWT parity or remain API-key-only for tighter control?
2. Is HMAC signing mandatory in v1 for outbound requests, or optional behind config?
3. Confirm idempotency TTL default for callbacks: 300s vs 900s.
4. Should callback processing return synchronous business status, or always 202-accepted style acknowledgment?

## Handoff Readiness
Design is implementation-ready for @4plan with concrete module boundaries, public APIs, contracts, and a 15-20 test target scope.
