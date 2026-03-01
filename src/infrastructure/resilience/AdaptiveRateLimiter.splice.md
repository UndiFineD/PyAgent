# Class Breakdown: AdaptiveRateLimiter

**File**: `src\infrastructure\resilience\AdaptiveRateLimiter.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RateLimitExceededError`

**Line**: 27  
**Inherits**: Exception  
**Methods**: 1

Raised when rate limit is exceeded.

[TIP] **Suggested split**: Move to `ratelimitexceedederror.py`

---

### 2. `RateLimiterStats`

**Line**: 35  
**Methods**: 2

Statistics for rate limiter.

[TIP] **Suggested split**: Move to `ratelimiterstats.py`

---

### 3. `TokenBucket`

**Line**: 60  
**Methods**: 6

Token bucket rate limiter with burst capacity.

Allows bursts up to bucket capacity while maintaining
average rate over time.

Example:
    >>> bucket = TokenBucket(rate=10.0, capacity=20)
    >>> 
  ...

[TIP] **Suggested split**: Move to `tokenbucket.py`

---

### 4. `SlidingWindowCounter`

**Line**: 202  
**Methods**: 6

Sliding window rate limiter using fixed window counters.

More accurate than fixed window, less memory than sliding log.

Example:
    >>> limiter = SlidingWindowCounter(limit=100, window_seconds=60)
...

[TIP] **Suggested split**: Move to `slidingwindowcounter.py`

---

### 5. `AdaptiveRateLimiter`

**Line**: 289  
**Methods**: 8

Rate limiter that adapts based on error rates.

Reduces rate when errors increase, restores when healthy.

Example:
    >>> limiter = AdaptiveRateLimiter(
    ...     base_rate=100.0,
    ...     min_...

[TIP] **Suggested split**: Move to `adaptiveratelimiter.py`

---

### 6. `PerKeyRateLimiter`

**Line**: 451  
**Inherits**: Unknown  
**Methods**: 6

Rate limiter with per-key limits for multi-tenant scenarios.

Example:
    >>> limiter = PerKeyRateLimiter(rate=10.0, capacity=20)
    >>> 
    >>> # Rate limit per user
    >>> if limiter.acquire("us...

[TIP] **Suggested split**: Move to `perkeyratelimiter.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
