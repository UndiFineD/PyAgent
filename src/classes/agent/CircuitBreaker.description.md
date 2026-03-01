# CircuitBreaker

**File**: `src\classes\agent\CircuitBreaker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 169  
**Complexity**: 7 (moderate)

## Overview

Python module containing implementation for CircuitBreaker.

## Classes (1)

### `CircuitBreaker`

Circuit breaker pattern for failing backends with Jittered Backoff.

Manages failing backends with exponential backoff and recovery.
Tracks failure state and prevents cascading failures.
Includes Phase 144 Jitter and 2-min max failure TTL.
Delegates transition logic to ResilienceCore (Phase 231).

States:
    CLOSED: Normal operation, requests pass through
    OPEN: Too many failures, requests fail immediately
    HALF_OPEN: Testing if backend recovered

**Methods** (7):
- `__init__(self, name, failure_threshold, recovery_timeout, backoff_multiplier, otel_manager)`
- `_get_thresholds(self)`
- `_get_current_timeout(self)`
- `_export_to_otel(self, old_state, new_state)`
- `call(self, func)`
- `on_success(self)`
- `on_failure(self)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `logging`
- `random`
- `src.core.base.core.ResilienceCore.ResilienceCore`
- `src.core.base.version.VERSION`
- `src.observability.stats.exporters.OTelManager.OTelManager`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
