# AdaptiveRateLimiter

**File**: `src\infrastructure\resilience\AdaptiveRateLimiter.py`  
**Type**: Python Module  
**Summary**: 6 classes, 1 functions, 14 imports  
**Lines**: 598  
**Complexity**: 30 (complex)

## Overview

AdaptiveRateLimiter - Token bucket with burst handling and adaptive limits.

Goes beyond vLLM with production-grade rate limiting including:
- Token bucket algorithm with burst capacity
- Sliding window rate limiting
- Adaptive rate adjustment based on error rates
- Per-key rate limiting for multi-tenant scenarios

Phase 18: Beyond vLLM - Resilience Patterns

## Classes (6)

### `RateLimitExceededError`

**Inherits from**: Exception

Raised when rate limit is exceeded.

**Methods** (1):
- `__init__(self, message, retry_after)`

### `RateLimiterStats`

Statistics for rate limiter.

**Methods** (2):
- `rejection_rate(self)`
- `to_dict(self)`

### `TokenBucket`

Token bucket rate limiter with burst capacity.

Allows bursts up to bucket capacity while maintaining
average rate over time.

Example:
    >>> bucket = TokenBucket(rate=10.0, capacity=20)
    >>> 
    >>> if bucket.acquire():
    ...     process_request()
    >>> else:
    ...     reject_request()

**Methods** (6):
- `__init__(self, rate, capacity)`
- `stats(self)`
- `available_tokens(self)`
- `_refill(self)`
- `acquire(self, tokens, block)`
- `time_to_available(self, tokens)`

### `SlidingWindowCounter`

Sliding window rate limiter using fixed window counters.

More accurate than fixed window, less memory than sliding log.

Example:
    >>> limiter = SlidingWindowCounter(limit=100, window_seconds=60)
    >>> 
    >>> if limiter.is_allowed():
    ...     process_request()

**Methods** (6):
- `__init__(self, limit, window_seconds)`
- `stats(self)`
- `_update_window(self)`
- `_get_weighted_count(self)`
- `is_allowed(self)`
- `get_remaining(self)`

### `AdaptiveRateLimiter`

Rate limiter that adapts based on error rates.

Reduces rate when errors increase, restores when healthy.

Example:
    >>> limiter = AdaptiveRateLimiter(
    ...     base_rate=100.0,
    ...     min_rate=10.0,
    ...     error_threshold=0.1,
    ... )
    >>> 
    >>> @limiter
    ... def api_call():
    ...     return requests.get(url)

**Methods** (8):
- `__init__(self, base_rate, min_rate, max_rate, error_threshold, recovery_rate, reduction_rate, window_seconds)`
- `current_rate(self)`
- `_update_rate(self)`
- `acquire(self, block)`
- `record_success(self)`
- `record_error(self)`
- `__call__(self, func)`
- `get_stats(self)`

### `PerKeyRateLimiter`

**Inherits from**: Unknown

Rate limiter with per-key limits for multi-tenant scenarios.

Example:
    >>> limiter = PerKeyRateLimiter(rate=10.0, capacity=20)
    >>> 
    >>> # Rate limit per user
    >>> if limiter.acquire("user_123"):
    ...     process_request()

**Methods** (6):
- `__init__(self, rate, capacity, cleanup_interval)`
- `_cleanup_old_buckets(self)`
- `_get_bucket(self, key)`
- `acquire(self, key, tokens, block)`
- `get_stats(self, key)`
- `get_all_stats(self)`

## Functions (1)

### `rate_limit(rate, capacity, block)`

Decorator for rate limiting functions.

Example:
    >>> @rate_limit(rate=10.0, capacity=20)
    ... def api_call():
    ...     return requests.get(url)

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `asyncio`
- `collections.defaultdict`
- `dataclasses.dataclass`
- `dataclasses.field`
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
