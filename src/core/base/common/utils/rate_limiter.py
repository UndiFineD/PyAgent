#!/usr/bin/env python3
from __future__ import annotations

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
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Rate limiter utilities (token-bucket).

"""
Minimal, well-typed implementation used by tests. Config may be provided
via a RateLimitConfig-like object with attributes `requests_per_second` and
`burst_size`.
"""
import threading
import time
from typing import Any

try:
    from src.core.base.common.models import RateLimitConfig
except Exception:
    # Fallback simple config dataclass for tests
    class RateLimitConfig:  # type: ignore
        def __init__(self, requests_per_second: float = 1.0, burst_size: int = 1) -> None:
            self.requests_per_second = requests_per_second
            self.burst_size = burst_size


class RateLimiter:
"""
A simple token-bucket rate limiter.""
def __init__(self, config: RateLimitConfig | None = None) -> None:
        self.config = config or RateLimitConfig()
        self.tokens = float(self.config.burst_size)
        self.last_refill = time.time()
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._request_timestamps: list[float] = []

    def _refill_tokens(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = elapsed * self.config.requests_per_second
        self.tokens = min(float(self.config.burst_size), self.tokens + refill_amount)
        self.last_refill = now

    def acquire(self, timeout: float | None = None) -> bool:
"""
Acquire a token for making an API call.

        Blocks until a token is available or timeout expires.
"""
start_time = time.time()

        with self._condition:
            while True:
                self._refill_tokens()

                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    self._request_timestamps.append(time.time())
                    # Clean old timestamps (last minute)
                    cutoff = time.time() - 60
                    self._request_timestamps = [t for t in self._request_timestamps if t > cutoff]
                    return True

                # Calculate wait time for at least 1 token
                wait_time = (1.0 - self.tokens) / max(self.config.requests_per_second, 1e-9)

                # Check timeout
                elapsed = time.time() - start_time
                if timeout is not None:
                    if elapsed >= timeout:
                        return False
                    wait_time = min(wait_time, timeout - elapsed)

                # Wait before retry using condition
                self._condition.wait(timeout=max(wait_time, 0.01))

    def get_stats(self) -> dict[str, Any]:
"""
Return simple stats about the limiter.""
with self._lock:
            return {
                "tokens_available": self.tokens,
                "requests_last_minute": len(self._request_timestamps),
                "requests_per_second": self.config.requests_per_second,
                "burst_size": self.config.burst_size,
            }
