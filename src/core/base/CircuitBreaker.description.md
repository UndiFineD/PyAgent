# CircuitBreaker

**File**: `src\core\base\CircuitBreaker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 213  
**Complexity**: 7 (moderate)

## Overview

Auto-extracted class from agent.py

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

**Imports** (10):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `inspect`
- `logging`
- `src.core.base.Version.VERSION`
- `src.core.base.core.ResilienceCore.ResilienceCore`
- `src.observability.stats.exporters.OTelManager`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
