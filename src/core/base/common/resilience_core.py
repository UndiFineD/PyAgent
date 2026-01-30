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
Centralized Resilience and Fault Tolerance Core.
Standardizes retry, backoff, and circuit breaker logic across the swarm.
"""

from __future__ import annotations

import asyncio
import functools
import logging
import random
import time
from typing import Any, Callable, Coroutine, TypeVar, cast

try:
    import rust_core as rc
except ImportError:
    rc = None  # type: ignore[assignment]

from .base_core import BaseCore

logger = logging.getLogger("pyagent.resilience")

T = TypeVar("T")


class ResilienceCore(BaseCore):
    """
    Standard implementation of Agent Resilience and Fault Tolerance.
    Inherits from BaseCore for lifecycle management and environment awareness.
    """

    @staticmethod
    def retry(
        retries: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: tuple[type[Exception], ...] = (Exception,),
    ) -> Callable[[Callable[..., T]], Callable[..., T]]:
        """Synchronous retry decorator with exponential backoff."""

        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception = None
                current_delay = delay
                for attempt in range(retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt == retries:
                            break
                        wait = current_delay * (random.random() + 0.5)  # jitter
                        logger.warning(
                            "Retrying %s (attempt %d/%d) after %.2fs due to: %s",
                            func.__name__,
                            attempt + 1,
                            retries,
                            wait,
                            e,
                        )
                        # TODO: Replace with event-driven or async wait for non-blocking retry if possible
                        time.sleep(wait)  # Blocking sleep; consider using asyncio.sleep in async contexts
                        current_delay *= backoff
                if last_exception:
                    raise last_exception
                return cast(T, None)

            return wrapper

        return decorator

    @staticmethod
    def retry_async(
        retries: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        exceptions: tuple[type[Exception], ...] = (Exception,),
    ) -> Callable[[Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]]:
        """Asynchronous retry decorator with exponential backoff."""

        def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
            @functools.wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> T:
                last_exception = None
                current_delay = delay
                for attempt in range(retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt == retries:
                            break
                        wait = current_delay * (random.random() + 0.5)  # jitter
                        logger.warning(
                            "Retrying %s (attempt %d/%d) after %.2fs due to: %s",
                            func.__name__,
                            attempt + 1,
                            retries,
                            wait,
                            e,
                        )
                        await asyncio.sleep(wait)
                        current_delay *= backoff
                if last_exception:
                    raise last_exception
                return cast(T, None)

            return wrapper

        return decorator

    @staticmethod
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def calculate_backoff(
        failure_count: int,
        threshold: int,
        base_timeout: float,
        multiplier: float,
        max_timeout: float,
        jitter_mode: str = "full",
    ) -> float:
        """
        Calculates exponential backoff with configurable jitter.
        """
        if rc:
            try:
                # Use Rust implementation for performance if available
                return rc.calculate_backoff(  # pylint: disable=no-member
                    failure_count, threshold, base_timeout, multiplier, max_timeout
                )
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

        if failure_count < threshold:
            return 0.0

        exponent = max(0, failure_count - threshold)
        backoff = min(max_timeout, base_timeout * (multiplier**exponent))

        if jitter_mode == "full":
            return random.uniform(base_timeout / 2, backoff)
        if jitter_mode == "equal":
            return (backoff / 2) + random.uniform(0, backoff / 2)

        # Legacy 10% jitter
        jitter = backoff * 0.1 * random.uniform(-1, 1)
        return max(base_timeout / 2, backoff + jitter)

    @staticmethod
    def should_attempt_recovery(last_failure_time: float, current_time: float, timeout: float) -> bool:
        """Determines if the cooldown period has passed."""
        if rc:
            try:
                return rc.should_attempt_recovery(  # pylint: disable=no-member
                    last_failure_time, current_time, timeout
                )
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass
        return (current_time - last_failure_time) > timeout

    @staticmethod
    def evaluate_state_transition(
        current_state: str,
        success_count: int,
        consecutive_successes_needed: int,
        failure_count: int,
        failure_threshold: int,
    ) -> str:
        """
        Pure state machine logic for circuit breaker transitions.
        """
        if rc:
            try:
                if hasattr(rc, "evaluate_state_transition"):
                    return rc.evaluate_state_transition(  # pylint: disable=no-member
                        current_state,
                        success_count,
                        consecutive_successes_needed,
                        failure_count,
                        failure_threshold,
                    )
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

        if current_state == "CLOSED":
            if failure_count >= failure_threshold:
                return "OPEN"
        elif current_state == "HALF_OPEN":
            if success_count >= consecutive_successes_needed:
                return "CLOSED"

        return current_state

    @staticmethod
    # pylint: disable=too-many-return-statements
    def update_state(
        current_state: str,
        is_success: bool,
        failure_count: int,
        success_count: int,
        _last_failure_time: float,
        thresholds: dict[str, Any],
    ) -> tuple[str, int, int]:
        """
        Updates circuit breaker state based on the outcome of an operation.
        """
        failure_threshold = thresholds.get("failure_threshold", 5)
        consecutive_successes_needed = thresholds.get("consecutive_successes_needed", 3)

        if is_success:
            new_success_count = success_count + 1
            if current_state == "HALF_OPEN":
                new_state = ResilienceCore.evaluate_state_transition(
                    current_state,
                    new_success_count,
                    consecutive_successes_needed,
                    failure_count,
                    failure_threshold,
                )
                if new_state == "CLOSED":
                    return "CLOSED", 0, 0
                return current_state, failure_count, new_success_count
            if current_state == "CLOSED":
                return "CLOSED", 0, 0
            if current_state == "OPEN":
                return "CLOSED", 0, 0

            return current_state, failure_count, new_success_count

        new_failure_count = failure_count + 1
        if current_state == "HALF_OPEN":
            return "OPEN", new_failure_count, 0

        new_state = ResilienceCore.evaluate_state_transition(
            current_state,
            success_count,
            consecutive_successes_needed,
            new_failure_count,
            failure_threshold,
        )
        return new_state, new_failure_count, 0
