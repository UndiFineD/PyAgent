#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
AdaptiveRateLimiter - Token bucket with burst handling and adaptive limits.

Goes beyond vLLM with production-grade rate limiting including:
- Token bucket algorithm with burst capacity
- Sliding window rate limiting
- Adaptive rate adjustment based on error rates
- Per-key rate limiting for multi-tenant scenarios

Phase 18: Beyond vLLM - Resilience Patterns
"""

from __future__ import annotations

import asyncio
import functools
import inspect
import threading
import time
from dataclasses import dataclass
from typing import Callable, Generic, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
K = TypeVar("K")


class RateLimitExceededError(Exception):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: float | None = None):
        super().__init__(message)
        self.retry_after = retry_after


@dataclass
class RateLimiterStats:
    """Statistics for rate limiter."""

    total_requests: int = 0
    allowed_requests: int = 0
    rejected_requests: int = 0
    total_wait_time: float = 0.0

    @property
    def rejection_rate(self) -> float:
        """Calculate rejection rate."""
        if self.total_requests == 0:
            return 0.0
        return self.rejected_requests / self.total_requests

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "total_requests": self.total_requests,
            "allowed_requests": self.allowed_requests,
            "rejected_requests": self.rejected_requests,
            "rejection_rate": round(self.rejection_rate, 4),
            "total_wait_time_ms": round(self.total_wait_time * 1000, 2),
        }


class TokenBucket:
    """
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
    """

    def __init__(
        self,
        rate: float,
        capacity: float | None = None,
    ) -> None:
        """
        Initialize token bucket.

        Args:
            rate: Tokens per second (refill rate)
            capacity: Maximum tokens (burst capacity)
                     Defaults to rate (1 second of burst)
        """
        self._rate = rate
        self._capacity = capacity if capacity is not None else rate
        self._tokens = self._capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()
        self._stats = RateLimiterStats()

    @property
    def stats(self) -> RateLimiterStats:
        """Get statistics."""
        return self._stats

    @property
    def available_tokens(self) -> float:
        """Get available tokens."""
        with self._lock:
            self._refill()
            return self._tokens

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self._last_refill

        if elapsed > 0:
            added = elapsed * self._rate
            self._tokens = min(self._capacity, self._tokens + added)
            self._last_refill = now

    def acquire(self, tokens: float = 1.0, block: bool = False) -> bool:
        """
        Acquire tokens from bucket.

        Args:
            tokens: Number of tokens to acquire
            block: If True, wait until tokens available

        Returns:
            True if tokens acquired, False otherwise
        """
        with self._lock:
            self._stats.total_requests += 1
            self._refill()

            if self._tokens >= tokens:
                self._tokens -= tokens
                self._stats.allowed_requests += 1
                return True

            if not block:
                self._stats.rejected_requests += 1
                return False

        # Blocking mode
        wait_time = self.time_to_available(tokens)
        self._stats.total_wait_time += wait_time
        time.sleep(wait_time)

        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                self._stats.allowed_requests += 1
                return True

            self._stats.rejected_requests += 1
            return False

    async def acquire_async(
        self,
        tokens: float = 1.0,
        block: bool = False,
    ) -> bool:
        """Async version of acquire."""
        with self._lock:
            self._stats.total_requests += 1
            self._refill()

            if self._tokens >= tokens:
                self._tokens -= tokens
                self._stats.allowed_requests += 1
                return True

            if not block:
                self._stats.rejected_requests += 1
                return False

        wait_time = self.time_to_available(tokens)
        self._stats.total_wait_time += wait_time
        await asyncio.sleep(wait_time)

        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                self._stats.allowed_requests += 1
                return True

            self._stats.rejected_requests += 1
            return False

    def time_to_available(self, tokens: float = 1.0) -> float:
        """Calculate time until tokens are available."""
        with self._lock:
            self._refill()

            if self._tokens >= tokens:
                return 0.0

            needed = tokens - self._tokens
            return needed / self._rate


class SlidingWindowCounter:
    """
    Sliding window rate limiter using fixed window counters.

    More accurate than fixed window, less memory than sliding log.

    Example:
        >>> limiter = SlidingWindowCounter(limit=100, window_seconds=60)
        >>>
        >>> if limiter.is_allowed():
        ...     process_request()
    """

    def __init__(
        self,
        limit: int,
        window_seconds: float = 60.0,
    ) -> None:
        """
        Initialize sliding window counter.

        Args:
            limit: Maximum requests per window
            window_seconds: Window size in seconds
        """
        self._limit = limit
        self._window = window_seconds
        self._current_count = 0
        self._previous_count = 0
        self._current_window_start = time.monotonic()
        self._lock = threading.Lock()
        self._stats = RateLimiterStats()

    @property
    def stats(self) -> RateLimiterStats:
        """Get statistics."""
        return self._stats

    def _update_window(self) -> None:
        """Update window if needed."""
        now = time.monotonic()
        window_elapsed = now - self._current_window_start

        if window_elapsed >= self._window:
            # Move to new window
            windows_passed = int(window_elapsed / self._window)

            if windows_passed == 1:
                self._previous_count = self._current_count
            else:
                self._previous_count = 0

            self._current_count = 0
            self._current_window_start += windows_passed * self._window

    def _get_weighted_count(self) -> float:
        """Get weighted count across windows."""
        now = time.monotonic()
        window_elapsed = now - self._current_window_start
        weight = window_elapsed / self._window

        return self._current_count + self._previous_count * (1 - weight)

    def is_allowed(self) -> bool:
        """Check if request is allowed."""
        with self._lock:
            self._stats.total_requests += 1
            self._update_window()

            weighted = self._get_weighted_count()

            if weighted < self._limit:
                self._current_count += 1
                self._stats.allowed_requests += 1
                return True

            self._stats.rejected_requests += 1
            return False

    def get_remaining(self) -> int:
        """Get remaining requests in current window."""
        with self._lock:
            self._update_window()
            weighted = self._get_weighted_count()
            return max(0, int(self._limit - weighted))


class AdaptiveRateLimiter:
    """
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
    """

    def __init__(
        self,
        base_rate: float = 100.0,
        min_rate: float = 10.0,
        max_rate: float | None = None,
        error_threshold: float = 0.1,
        recovery_rate: float = 1.1,
        reduction_rate: float = 0.5,
        window_seconds: float = 10.0,
    ) -> None:
        """
        Initialize adaptive rate limiter.

        Args:
            base_rate: Starting rate (requests per second)
            min_rate: Minimum rate floor
            max_rate: Maximum rate ceiling (default: 2x base)
            error_threshold: Error rate threshold to trigger reduction
            recovery_rate: Multiplier for rate recovery (>1.0)
            reduction_rate: Multiplier for rate reduction (<1.0)
            window_seconds: Window for measuring error rate
        """
        self._base_rate = base_rate
        self._min_rate = min_rate
        self._max_rate = max_rate if max_rate is not None else base_rate * 2
        self._error_threshold = error_threshold
        self._recovery_rate = recovery_rate
        self._reduction_rate = reduction_rate
        self._window = window_seconds

        self._current_rate = base_rate
        self._bucket = TokenBucket(rate=base_rate, capacity=base_rate * 2)

        self._window_start = time.monotonic()
        self._window_requests = 0
        self._window_errors = 0
        self._lock = threading.Lock()

    @property
    def current_rate(self) -> float:
        """Get current rate."""
        return self._current_rate

    def _update_rate(self) -> None:
        """Update rate based on error rate."""
        now = time.monotonic()
        elapsed = now - self._window_start

        if elapsed < self._window:
            return

        # Calculate error rate
        if self._window_requests > 0:
            error_rate = self._window_errors / self._window_requests

            if error_rate > self._error_threshold:
                # Reduce rate
                new_rate = self._current_rate * self._reduction_rate
                self._current_rate = max(self._min_rate, new_rate)
            else:
                # Recover rate
                new_rate = self._current_rate * self._recovery_rate
                self._current_rate = min(self._max_rate, new_rate)

            # Update bucket
            self._bucket = TokenBucket(
                rate=self._current_rate,
                capacity=self._current_rate * 2,
            )

        # Reset window
        self._window_start = now
        self._window_requests = 0
        self._window_errors = 0

    def acquire(self, block: bool = False) -> bool:
        """Acquire permission to proceed."""
        with self._lock:
            self._update_rate()
            self._window_requests += 1

        return self._bucket.acquire(block=block)

    async def acquire_async(self, block: bool = False) -> bool:
        """Async version of acquire."""
        with self._lock:
            self._update_rate()
            self._window_requests += 1

        return await self._bucket.acquire_async(block=block)

    def record_success(self) -> None:
        """Record a successful request."""
        pass  # Success doesn't change error count

    def record_error(self) -> None:
        """Record an error."""
        with self._lock:
            self._window_errors += 1

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorator for rate limiting functions."""
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                acquired = await self.acquire_async(block=True)
                if not acquired:
                    raise RateLimitExceededError("Rate limit exceeded")
                try:
                    result = await func(*args, **kwargs)
                    self.record_success()
                    return result
                except Exception:
                    self.record_error()
                    raise

            return async_wrapper  # type: ignore
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                acquired = self.acquire(block=True)
                if not acquired:
                    raise RateLimitExceededError("Rate limit exceeded")
                try:
                    result = func(*args, **kwargs)
                    self.record_success()
                    return result
                except Exception:
                    self.record_error()
                    raise

            return sync_wrapper

    def get_stats(self) -> dict:
        """Get limiter statistics."""
        return {
            "current_rate": round(self._current_rate, 2),
            "base_rate": self._base_rate,
            "min_rate": self._min_rate,
            "max_rate": self._max_rate,
            "window_requests": self._window_requests,
            "window_errors": self._window_errors,
            "bucket_stats": self._bucket.stats.to_dict(),
        }


class PerKeyRateLimiter(Generic[K]):
    """
    Rate limiter with per-key limits for multi-tenant scenarios.

    Example:
        >>> limiter = PerKeyRateLimiter(rate=10.0, capacity=20)
        >>>
        >>> # Rate limit per user
        >>> if limiter.acquire("user_123"):
        ...     process_request()
    """

    def __init__(
        self,
        rate: float,
        capacity: float | None = None,
        cleanup_interval: float = 300.0,
    ) -> None:
        """
        Initialize per-key rate limiter.

        Args:
            rate: Tokens per second per key
            capacity: Bucket capacity per key
            cleanup_interval: Seconds between bucket cleanup
        """
        self._rate = rate
        self._capacity = capacity if capacity is not None else rate
        self._cleanup_interval = cleanup_interval

        self._buckets: dict[K, TokenBucket] = {}
        self._last_access: dict[K, float] = {}
        self._last_cleanup = time.monotonic()
        self._lock = threading.Lock()

    def _cleanup_old_buckets(self) -> None:
        """Remove old unused buckets."""
        now = time.monotonic()

        if now - self._last_cleanup < self._cleanup_interval:
            return

        expired_keys = [key for key, last in self._last_access.items() if now - last > self._cleanup_interval]

        for key in expired_keys:
            del self._buckets[key]
            del self._last_access[key]

        self._last_cleanup = now

    def _get_bucket(self, key: K) -> TokenBucket:
        """Get or create bucket for key."""
        with self._lock:
            self._cleanup_old_buckets()

            if key not in self._buckets:
                self._buckets[key] = TokenBucket(
                    rate=self._rate,
                    capacity=self._capacity,
                )

            self._last_access[key] = time.monotonic()
            return self._buckets[key]

    def acquire(self, key: K, tokens: float = 1.0, block: bool = False) -> bool:
        """Acquire tokens for a specific key."""
        bucket = self._get_bucket(key)
        return bucket.acquire(tokens=tokens, block=block)

    async def acquire_async(
        self,
        key: K,
        tokens: float = 1.0,
        block: bool = False,
    ) -> bool:
        """Async version of acquire."""
        bucket = self._get_bucket(key)
        return await bucket.acquire_async(tokens=tokens, block=block)

    def get_stats(self, key: K) -> dict | None:
        """Get stats for a specific key."""
        bucket = self._buckets.get(key)
        if bucket:
            return bucket.stats.to_dict()
        return None

    def get_all_stats(self) -> dict[K, dict]:
        """Get stats for all keys."""
        return {key: bucket.stats.to_dict() for key, bucket in self._buckets.items()}


def rate_limit(
    rate: float,
    capacity: float | None = None,
    block: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for rate limiting functions.

    Example:
        >>> @rate_limit(rate=10.0, capacity=20)
        ... def api_call():
        ...     return requests.get(url)
    """
    bucket = TokenBucket(rate=rate, capacity=capacity)

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                acquired = await bucket.acquire_async(block=block)
                if not acquired:
                    raise RateLimitExceededError(
                        "Rate limit exceeded",
                        retry_after=bucket.time_to_available(),
                    )
                return await func(*args, **kwargs)

            return async_wrapper  # type: ignore
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                acquired = bucket.acquire(block=block)
                if not acquired:
                    raise RateLimitExceededError(
                        "Rate limit exceeded",
                        retry_after=bucket.time_to_available(),
                    )
                return func(*args, **kwargs)

            return sync_wrapper

    return decorator


__all__ = [
    "RateLimitExceededError",
    "RateLimiterStats",
    "TokenBucket",
    "SlidingWindowCounter",
    "AdaptiveRateLimiter",
    "PerKeyRateLimiter",
    "rate_limit",
]
