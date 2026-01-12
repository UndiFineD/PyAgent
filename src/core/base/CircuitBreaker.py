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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent.py"""




import logging
import random
import time
from typing import Any, Callable

class CircuitBreaker:
    """Circuit breaker pattern for failing backends with Jittered Backoff.

    Manages failing backends with exponential backoff and recovery.
    Tracks failure state and prevents cascading failures.
    Includes Phase 144 Jitter and 2-min max failure TTL.

    States:
        CLOSED: Normal operation, requests pass through
        OPEN: Too many failures, requests fail immediately
        HALF_OPEN: Testing if backend recovered
    """

    def __init__(self, name: str, failure_threshold: int = 5,
                 recovery_timeout: int = 60, backoff_multiplier: float = 1.5) -> None:
        """Initialize circuit breaker.

        Args:
            name: Name of the backend / service
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Base seconds to wait before attempting recovery
            backoff_multiplier: Multiplier for exponential backoff
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.backoff_multiplier = backoff_multiplier
        self.max_recovery_timeout = 120  # Phase 144: 2 minute cap

        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.consecutive_successes_needed = 2

    def _get_current_timeout(self) -> float:
        """Calculates current timeout with exponential backoff and jitter."""
        import random
        base = min(self.max_recovery_timeout, self.recovery_timeout * (self.backoff_multiplier ** max(0, self.failure_count - self.failure_threshold)))
        # Add 10% jitter
        jitter = base * 0.1 * random.uniform(-1, 1)
        return max(5, base + jitter)

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute function through circuit breaker."""
        if self.state == "OPEN":
            current_timeout = self._get_current_timeout()
            if time.time() - self.last_failure_time > current_timeout:
                self.state = "HALF_OPEN"
                self.success_count = 0
                logging.info(f"Circuit breaker '{self.name}' entering HALF_OPEN state (after {int(current_timeout)}s backoff)")
            else:
                raise Exception(f"Circuit breaker '{self.name}' is OPEN (retry in {int(current_timeout - (time.time() - self.last_failure_time))}s)")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception:  # noqa: F841
            self.on_failure()
            raise

    def on_success(self) -> None:
        """Record successful call."""
        self.failure_count = 0

        if self.state == "HALF_OPEN":
            self.success_count += 1
            if self.success_count >= self.consecutive_successes_needed:
                self.state = "CLOSED"
                logging.info(f"Circuit breaker '{self.name}' closed (recovered)")

    def on_failure(self) -> None:
        """Record failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logging.error(f"Circuit breaker '{self.name}' opened (too many failures)")
