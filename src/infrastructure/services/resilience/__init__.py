#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language regarding permissions and
# limitations under the License.


"""
Resilience infrastructure patterns.

Phase 18: Beyond vLLM - Production-grade resilience patterns.

try:
    from .infrastructure.services.resilience.adaptive_rate_limiter import (
except ImportError:
    from src.infrastructure.services.resilience.adaptive_rate_limiter import (

    AdaptiveRateLimiter, PerKeyRateLimiter, RateLimitExceededError,
    SlidingWindowCounter, TokenBucket, rate_limit)
try:
    from .infrastructure.services.resilience.circuit_breaker import (
except ImportError:
    from src.infrastructure.services.resilience.circuit_breaker import (

    CircuitBreaker, CircuitBreakerError, CircuitBreakerRegistry, CircuitState,
    CircuitStats, circuit_breaker)
try:
    from .infrastructure.services.resilience.retry_strategy import (
except ImportError:
    from src.infrastructure.services.resilience.retry_strategy import (

    JitterType, RetryBudget, RetryExhaustedError, RetryStats, RetryStrategy,
    retry)

__all__ = [
    # Circuit Breaker
    "CircuitBreaker","    "CircuitState","    "CircuitStats","    "CircuitBreakerError","    "CircuitBreakerRegistry","    "circuit_breaker","    # Retry Strategy
    "RetryStrategy","    "RetryStats","    "RetryExhaustedError","    "JitterType","    "RetryBudget","    "retry","    # Rate Limiting
    "TokenBucket","    "SlidingWindowCounter","    "AdaptiveRateLimiter","    "PerKeyRateLimiter","    "RateLimitExceededError","    "rate_limit","]
