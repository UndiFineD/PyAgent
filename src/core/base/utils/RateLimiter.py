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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.core.base.models import RateLimitConfig
from typing import Any
import threading
import time

__version__ = VERSION


class RateLimiter:
    """Rate limiter for API calls using token bucket algorithm.

    Manages API call rate to prevent throttling and ensure fair usage.
    Supports multiple strategies and configurable limits.

    Attributes:
        config: Rate limiting configuration.
        tokens: Current number of available tokens.
        last_refill: Timestamp of last token refill.
    """

    def __init__(self, config: RateLimitConfig | None = None) -> None:
        """Initialize the rate limiter.

        Args:
            config: Rate limiting configuration. Uses defaults if not provided.
        """
        self.config = config or RateLimitConfig()
        self.tokens = float(self.config.burst_size)
        self.last_refill = time.time()
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._request_timestamps: list[float] = []

    def _refill_tokens(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = elapsed * self.config.requests_per_second
        self.tokens = min(float(self.config.burst_size), self.tokens + refill_amount)
        self.last_refill = now

    def acquire(self, timeout: float | None = None) -> bool:
        """Acquire a token for making an API call.

        Blocks until a token is available or timeout expires.

        Args:
            timeout: Maximum time to wait for a token. None=wait forever.

        Returns:
            bool: True if token acquired, False if timeout.
        """
        start_time = time.time()

        with self._condition:
            while True:
                self._refill_tokens()

                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    self._request_timestamps.append(time.time())
                    # Clean old timestamps
                    cutoff = time.time() - 60
                    self._request_timestamps = [
                        t for t in self._request_timestamps if t > cutoff
                    ]
                    return True

                # Calculate wait time for at least 1 token
                wait_time = (1.0 - self.tokens) / self.config.requests_per_second

                # Check timeout
                elapsed = time.time() - start_time
                if timeout is not None:
                    if elapsed >= timeout:
                        return False
                    wait_time = min(wait_time, timeout - elapsed)

                # Wait before retry using condition, avoiding blocking sleep
                self._condition.wait(timeout=max(wait_time, 0.01))

    def get_stats(self) -> dict[str, Any]:
        """Get rate limiter statistics.

        Returns:
            Dict with current tokens, request count, etc.
        """
        with self._lock:
            return {
                "tokens_available": self.tokens,
                "requests_last_minute": len(self._request_timestamps),
                "requests_per_second": self.config.requests_per_second,
                "burst_size": self.config.burst_size,
            }
