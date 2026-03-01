# CircuitBreaker

**File**: `src\infrastructure\resilience\CircuitBreaker.py`  
**Type**: Python Module  
**Summary**: 5 classes, 3 functions, 15 imports  
**Lines**: 470  
**Complexity**: 30 (complex)

## Overview

CircuitBreaker - Resilience pattern for failing gracefully.

Goes beyond vLLM with production-grade circuit breaker implementation
for protecting against cascading failures in distributed systems.

States:
- CLOSED: Normal operation, requests flow through
- OPEN: Failures exceeded threshold, requests rejected immediately
- HALF_OPEN: Testing if service recovered with limited requests

Phase 18: Beyond vLLM - Resilience Patterns

## Classes (5)

### `CircuitState`

**Inherits from**: Enum

Circuit breaker states.

### `CircuitStats`

Statistics for circuit breaker monitoring.

**Methods** (3):
- `failure_rate(self)`
- `success_rate(self)`
- `to_dict(self)`

### `CircuitBreakerError`

**Inherits from**: Exception

Raised when circuit is open.

**Methods** (1):
- `__init__(self, message, retry_after)`

### `CircuitBreaker`

Thread-safe circuit breaker for protecting against cascading failures.

Example:
    >>> breaker = CircuitBreaker(
    ...     failure_threshold=5,
    ...     recovery_timeout=30.0,
    ...     half_open_max_calls=3,
    ... )
    >>> 
    >>> @breaker
    ... def call_external_service():
    ...     return requests.get("http://api.example.com")
    >>> 
    >>> try:
    ...     result = call_external_service()
    ... except CircuitBreakerError as e:
    ...     print(f"Circuit open, retry after {e.retry_after}s")

**Methods** (17):
- `__init__(self, failure_threshold, recovery_timeout, half_open_max_calls, failure_rate_threshold, success_threshold, excluded_exceptions, name)`
- `state(self)`
- `stats(self)`
- `is_closed(self)`
- `is_open(self)`
- `_check_state_transition(self)`
- `_transition_to(self, new_state)`
- `_should_allow_request(self)`
- `_record_success(self)`
- `_record_failure(self)`
- ... and 7 more methods

### `CircuitBreakerRegistry`

Registry for managing multiple circuit breakers.

Example:
    >>> registry = CircuitBreakerRegistry()
    >>> 
    >>> @registry.breaker("openai_api")
    ... def call_openai(prompt):
    ...     return openai.chat(prompt)
    >>> 
    >>> print(registry.get_all_stats())

**Methods** (6):
- `__init__(self)`
- `get_or_create(self, name)`
- `breaker(self, name)`
- `get_stats(self, name)`
- `get_all_stats(self)`
- `reset_all(self)`

## Functions (3)

### `circuit_breaker(name)`

Decorator to protect a function with a circuit breaker.

Example:
    >>> @circuit_breaker("external_api", failure_threshold=3)
    ... def call_api():
    ...     return requests.get("http://api.example.com")

### `get_circuit_stats(name)`

Get stats for a circuit breaker.

### `get_all_circuit_stats()`

Get stats for all circuit breakers.

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `functools`
- `inspect`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Generic`
- `typing.ParamSpec`
- `typing.TypeVar`

---
*Auto-generated documentation*
