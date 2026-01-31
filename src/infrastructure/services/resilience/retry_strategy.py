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
RetryStrategy - Exponential backoff with jitter for resilient retries.

Goes beyond vLLM with production-grade retry patterns including:
- Exponential backoff with configurable base and max
- Jitter (full, equal, decorrelated) to prevent thundering herd
- Retry budgets to limit total retry attempts
- Retryable exception filtering

Phase 18: Beyond vLLM - Resilience Patterns
"""

from __future__ import annotations

import asyncio
import functools
import inspect
import random
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class JitterType(Enum):
    """Types of jitter for backoff."""

    NONE = auto()  # No jitter (not recommended)
    FULL = auto()  # Random between 0 and backoff
    EQUAL = auto()  # Half backoff + random half
    DECORRELATED = auto()  # AWS-style decorrelated jitter


@dataclass
class RetryStats:
    """Statistics for retry operations."""

    total_attempts: int = 0
    successful_attempts: int = 0
    failed_attempts: int = 0
    total_retries: int = 0
    total_wait_time: float = 0.0
    last_error: str | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "total_attempts": self.total_attempts,
            "successful_attempts": self.successful_attempts,
            "failed_attempts": self.failed_attempts,
            "total_retries": self.total_retries,
            "avg_retries": round(self.total_retries / max(1, self.total_attempts), 2),
            "total_wait_time_ms": round(self.total_wait_time * 1000, 2),
            "last_error": self.last_error,
        }


class RetryExhaustedError(Exception):
    """Raised when all retries are exhausted."""

    def __init__(
        self,
        message: str,
        attempts: int,
        last_exception: Exception | None = None,
    ):
        super().__init__(message)
        self.attempts = attempts
        self.last_exception = last_exception


class RetryStrategy:
    """
    Configurable retry strategy with exponential backoff and jitter.

    Example:
        >>> retry = RetryStrategy(
        ...     max_attempts=5,
        ...     base_delay=1.0,
        ...     max_delay=60.0,
        ...     jitter=JitterType.FULL,
        ...     retryable_exceptions=(ConnectionError, TimeoutError),
        ... )
        >>>
        >>> @retry
        ... def flaky_operation():
        ...     return external_api_call()
        >>>
        >>> result = flaky_operation()
    """

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: JitterType = JitterType.FULL,
        retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
        non_retryable_exceptions: tuple[type[Exception], ...] = (),
        on_retry: Callable[[int, Exception, float], None] | None = None,
        *,
        sleep_fn: Callable[[float], None] | None = None,
    ) -> None:
        """
        Initialize retry strategy.

        Args:
            max_attempts: Maximum number of attempts (including first)
            base_delay: Base delay in seconds
            max_delay: Maximum delay cap in seconds
            exponential_base: Base for exponential backoff (default 2.0)
            jitter: Type of jitter to apply
            retryable_exceptions: Exceptions that trigger retry
            non_retryable_exceptions: Exceptions that should not retry
            on_retry: Callback(attempt, exception, delay) before each retry
            sleep_fn: Optional blocking sleep function for sync retries (defaults to time.sleep).
        """
        self._max_attempts = max_attempts
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._exponential_base = exponential_base
        self._jitter = jitter
        self._retryable_exceptions = retryable_exceptions
        self._non_retryable_exceptions = non_retryable_exceptions
        self._on_retry = on_retry
        self._stats = RetryStats()

        # For decorrelated jitter
        self._last_delay = base_delay

        # Sleep function used by sync execute (injectable for testing/async compatibility)
        import time as _time
        self._sleep_fn: Callable[[float], None] = sleep_fn or _time.sleep
        """
        Initialize retry strategy.

        Args:
            max_attempts: Maximum number of attempts (including first)
            base_delay: Base delay in seconds
            max_delay: Maximum delay cap in seconds
            exponential_base: Base for exponential backoff (default 2.0)
            jitter: Type of jitter to apply
            retryable_exceptions: Exceptions that trigger retry
            non_retryable_exceptions: Exceptions that should not retry
            on_retry: Callback(attempt, exception, delay) before each retry
        """
        self._max_attempts = max_attempts
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._exponential_base = exponential_base
        self._jitter = jitter
        self._retryable_exceptions = retryable_exceptions
        self._non_retryable_exceptions = non_retryable_exceptions
        self._on_retry = on_retry
        self._stats = RetryStats()

        # For decorrelated jitter
        self._last_delay = base_delay

    @property
    def stats(self) -> RetryStats:
        """Get retry statistics."""
        return self._stats

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number."""
        if self._jitter == JitterType.DECORRELATED:
            # AWS-style: delay = min(cap, random(base, last_delay * 3))
            delay = random.uniform(self._base_delay, self._last_delay * 3)
            delay = min(delay, self._max_delay)
            self._last_delay = delay
            return delay

        # Exponential backoff
        exp_delay = self._base_delay * (self._exponential_base**attempt)
        delay = min(exp_delay, self._max_delay)

        if self._jitter == JitterType.NONE:
            return delay

        if self._jitter == JitterType.FULL:
            # Random between 0 and delay
            return random.uniform(0, delay)

        if self._jitter == JitterType.EQUAL:
            # Half delay + random half
            return delay / 2 + random.uniform(0, delay / 2)

        return delay

    def _is_retryable(self, exc: Exception) -> bool:
        """Check if exception should trigger retry."""
        # Non-retryable takes precedence
        if isinstance(exc, self._non_retryable_exceptions):
            return False

        return isinstance(exc, self._retryable_exceptions)

    def execute(
        self,
        func: Callable[P, R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        """
        Execute function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            RetryExhaustedError: If all retries exhausted
        """
        self._stats.total_attempts += 1
        last_exception: Exception | None = None

        for attempt in range(self._max_attempts):
            try:
                result = func(*args, **kwargs)
                self._stats.successful_attempts += 1
                return result

            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                last_exception = e
                self._stats.last_error = str(e)

                # Check if we should retry
                if not self._is_retryable(e):
                    self._stats.failed_attempts += 1
                    raise

                # Check if we have more attempts
                if attempt + 1 >= self._max_attempts:
                    self._stats.failed_attempts += 1
                    raise RetryExhaustedError(
                        f"Retry exhausted after {attempt + 1} attempts",
                        attempts=attempt + 1,
                        last_exception=e,
                    ) from e

                # Calculate delay and wait
                delay = self._calculate_delay(attempt)
                self._stats.total_retries += 1
                self._stats.total_wait_time += delay

                if self._on_retry:
                    self._on_retry(attempt + 1, e, delay)

                # Use injectable blocking sleep function for sync callers
                self._sleep_fn(delay)

        # Should never reach here
        self._stats.failed_attempts += 1
        raise RetryExhaustedError(
            "Retry exhausted",
            attempts=self._max_attempts,
            last_exception=last_exception,
        )

    async def execute_async(
        self,
        func: Callable[P, Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Any:
        """
        Execute async function with retry logic.
        """
        self._stats.total_attempts += 1
        last_exception: Exception | None = None

        for attempt in range(self._max_attempts):
            try:
                result = await func(*args, **kwargs)
                self._stats.successful_attempts += 1
                return result

            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                last_exception = e
                self._stats.last_error = str(e)

                if not self._is_retryable(e):
                    self._stats.failed_attempts += 1
                    raise

                if attempt + 1 >= self._max_attempts:
                    self._stats.failed_attempts += 1
                    raise RetryExhaustedError(
                        f"Retry exhausted after {attempt + 1} attempts",
                        attempts=attempt + 1,
                        last_exception=e,
                    ) from e

                delay = self._calculate_delay(attempt)
                self._stats.total_retries += 1
                self._stats.total_wait_time += delay

                if self._on_retry:
                    self._on_retry(attempt + 1, e, delay)

                await asyncio.sleep(delay)

        self._stats.failed_attempts += 1
        raise RetryExhaustedError(
            "Retry exhausted",
            attempts=self._max_attempts,
            last_exception=last_exception,
        )

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        """Decorator for wrapping functions with retry logic."""
        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return await self.execute_async(func, *args, **kwargs)

            return async_wrapper  # type: ignore
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return self.execute(func, *args, **kwargs)

            return sync_wrapper


def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: JitterType = JitterType.FULL,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for retrying functions with exponential backoff.

    Example:
        >>> @retry(max_attempts=3, base_delay=1.0)
        ... def unstable_operation():
        ...     return risky_call()
    """
    strategy = RetryStrategy(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        jitter=jitter,
        retryable_exceptions=retryable_exceptions,
    )
    return strategy


class RetryBudget:
    """
    Token bucket for limiting total retries across operations.

    Prevents excessive retries during widespread failures.

    Example:
        >>> budget = RetryBudget(max_retries_per_second=10.0)
        >>>
        >>> if budget.can_retry():
        ...     budget.record_retry()
        ...     do_retry()
    """

    def __init__(
        self,
        max_retries_per_second: float = 10.0,
        min_retries_per_second: float = 1.0,
        retry_ratio: float = 0.2,
    ) -> None:
        """
        Initialize retry budget.

        Args:
            max_retries_per_second: Maximum retry rate
            min_retries_per_second: Minimum guaranteed retries
            retry_ratio: Ratio of requests that can be retries (0.0-1.0)
        """
        self._max_rate = max_retries_per_second
        self._min_rate = min_retries_per_second
        self._retry_ratio = retry_ratio

        self._tokens = max_retries_per_second
        self._last_refill = time.monotonic()
        self._requests_count = 0
        self._retry_count = 0

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self._last_refill

        # Add tokens based on elapsed time
        added = elapsed * self._max_rate
        self._tokens = min(self._max_rate, self._tokens + added)
        self._last_refill = now

    def record_request(self) -> None:
        """Record a request (for ratio calculation)."""
        self._requests_count += 1

    def can_retry(self) -> bool:
        """Check if retry is allowed."""
        self._refill()

        # Always allow minimum rate
        if self._tokens >= 1.0:
            return True

        # Check retry ratio
        if self._requests_count > 0:
            current_ratio = self._retry_count / self._requests_count
            if current_ratio < self._retry_ratio:
                return True

        return False

    def record_retry(self) -> bool:
        """
        Record a retry attempt.

        Returns:
            True if retry was allowed, False if budget exceeded
        """
        if not self.can_retry():
            return False

        self._tokens -= 1.0
        self._retry_count += 1
        return True

    def get_stats(self) -> dict:
        """Get budget statistics."""
        return {
            "available_tokens": round(self._tokens, 2),
            "requests": self._requests_count,
            "retries": self._retry_count,
            "retry_ratio": round(self._retry_count / max(1, self._requests_count), 4),
        }


__all__ = [
    "JitterType",
    "RetryStats",
    "RetryExhaustedError",
    "RetryStrategy",
    "retry",
    "RetryBudget",
]
