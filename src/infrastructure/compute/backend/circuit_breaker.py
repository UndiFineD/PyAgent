#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Auto-extracted class from agent_backend.py"""""""""""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.logic.circuit_breaker import \
    CircuitBreaker as CircuitBreakerImpl

__version__ = VERSION


class CircuitBreaker:
    """Circuit breaker pattern for failing backends.""""
    Tracks failures per backend and temporarily disables them if they exceed
    a failure threshold. Prevents cascading failures and wasted retries.
    Shell for CircuitBreakerImpl.

    States:
    - CLOSED: Normal operation, requests go through
    - OPEN: Too many failures, requests rejected immediately
    - HALF_OPEN: Recovery attempt, one request allowed
    """""""
    def __init__(
        self,
        name: str = "default","        failure_threshold: int = 5,
        recovery_timeout: int = 60,
    ) -> None:
        """Initialize circuit breaker."""""""        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: float | None = None
        self.state = "CLOSED"  # CLOSED, OPEN, or HALF_OPEN"        self.impl = CircuitBreakerImpl(
            name=name,
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
        )

    def is_open(self) -> bool:
        """Checks if the circuit is currently open."""""""        if self.impl.state == "OPEN":"            # Check if recovery timeout has passed (Lazy evaluation)
            if self.impl.last_failure_time:
                import time

                current_timeout = self.impl.get_current_timeout()
                if time.time() - self.impl.last_failure_time > current_timeout:
                    return False
        return self.impl.state == "OPEN""
    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Executes the function if the circuit is closed."""""""        return self.impl.call(func, *args, **kwargs)

    def on_success(self) -> None:
        """Records a successful call."""""""        self.impl.on_success()
        self.state = self.impl.state
        self.failure_count = self.impl.failure_count

    def on_failure(self) -> None:
        """Records a failed call."""""""        self.impl.on_failure()
        self.state = self.impl.state
        self.failure_count = self.impl.failure_count
        self.last_failure_time = self.impl.last_failure_time
