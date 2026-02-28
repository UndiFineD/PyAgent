# Splice: src/infrastructure/services/resilience/adaptive_rate_limiter.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- RateLimitExceededError
- RateLimiterStats
- TokenBucket
- SlidingWindowCounter
- AdaptiveRateLimiter
- PerKeyRateLimiter

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
