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


"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
import logging
import time
import asyncio
from typing import Any
from collections.abc import Callable
from src.core.base.core.ResilienceCore import ResilienceCore
from src.observability.stats.exporters import OTelManager

__version__ = VERSION


class CircuitBreaker:
    """Circuit breaker pattern for failing backends with Jittered Backoff.

    Manages failing backends with exponential backoff and recovery.
    Tracks failure state and prevents cascading failures.
    Includes Phase 144 Jitter and 2-min max failure TTL.
    Delegates transition logic to ResilienceCore (Phase 231).

    States:
        CLOSED: Normal operation, requests pass through
        OPEN: Too many failures, requests fail immediately
        HALF_OPEN: Testing if backend recovered
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        backoff_multiplier: float = 1.5,
        otel_manager: OTelManager | None = None,
    ) -> None:
        """Initialize circuit breaker.

        Args:
            name: Name of the backend / service
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Base seconds to wait before attempting recovery
            backoff_multiplier: Multiplier for exponential backoff
            otel_manager: Optional OTel manager for telemetry
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
        self.consecutive_successes_needed = (
            3  # Phase 231 requirement for "Wait-for-Success"
        )

        self.resilience_core = ResilienceCore()
        self.otel_manager = otel_manager

    def _get_thresholds(self) -> dict[str, Any]:
        """Returns threshold config for ResilienceCore."""
        return {
            "failure_threshold": self.failure_threshold,
            "recovery_timeout": self.recovery_timeout,
            "max_recovery_timeout": self.max_recovery_timeout,
            "backoff_multiplier": self.backoff_multiplier,
            "consecutive_successes_needed": self.consecutive_successes_needed,
        }

    def _get_current_timeout(self) -> float:
        """Calculates current timeout using ResilienceCore math."""
        return self.resilience_core.calculate_backoff(
            self.failure_count,
            self.failure_threshold,
            self.recovery_timeout,
            self.backoff_multiplier,
            self.max_recovery_timeout,
        )

    def _export_to_otel(self, old_state: str, new_state: str) -> None:
        """Exports state transition to OTel and StructuredLogger (Phase 273)."""
        logging.info(
            f"CircuitBreaker '{self.name}': Transition {old_state} -> {new_state}"
        )

        if self.otel_manager:
            span_id = self.otel_manager.start_span(
                f"Resilience: {self.name} Transition",
                attributes={
                    "resilience.breaker.name": self.name,
                    "resilience.breaker.old_state": old_state,
                    "resilience.breaker.new_state": new_state,
                    "resilience.breaker.failure_count": self.failure_count,
                },
            )
            self.otel_manager.end_span(span_id)

    async def probe(self, health_check_func: Callable[[], Any]) -> bool:
        """
        Periodically attempt a 'Wait-for-Success' probe (Phase 273).
        Exits the OPEN state faster if the backend is healthy.
        """
        if self.state != "OPEN":
            return True

        logging.debug(f"CircuitBreaker '{self.name}': Probing backend health...")
        try:
            # Perform the actual health check provided by the backend wrapper
            if asyncio.iscoroutinefunction(health_check_func):
                result = await health_check_func()
            else:
                result = health_check_func()

            if result:
                logging.info(
                    f"CircuitBreaker '{self.name}': Probe SUCCEEDED. Transitioning to HALF_OPEN early."
                )
                old_state = self.state
                self.state = "HALF_OPEN"
                self.success_count = 1
                self._export_to_otel(old_state, self.state)
                return True
        except Exception as e:
            logging.debug(f"CircuitBreaker '{self.name}': Probe failed: {e}")

        return False

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute function through circuit breaker."""
        if self.state == "OPEN":
            current_timeout = self._get_current_timeout()
            if time.time() - self.last_failure_time > current_timeout:
                old_state = self.state
                self.state = "HALF_OPEN"
                self.success_count = 0
                logging.warning(
                    f"Circuit breaker '{self.name}' entering HALF_OPEN state (after {int(current_timeout)}s backoff)"
                )
                self._export_to_otel(old_state, self.state)
            else:
                raise Exception(
                    f"Circuit breaker '{self.name}' is OPEN (retry in {int(current_timeout - (time.time() - self.last_failure_time))}s)"
                )

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception:
            # noqa: F841
            self.on_failure()
            raise

    def on_success(self) -> None:
        """Record successful call via ResilienceCore."""
        old_state = self.state
        self.state, self.failure_count, self.success_count = (
            self.resilience_core.update_state(
                self.state,
                True,
                self.failure_count,
                self.success_count,
                self.last_failure_time,
                self._get_thresholds(),
            )
        )

        if old_state != self.state:
            logging.info(
                f"Circuit breaker '{self.name}' transitioned from {old_state} to {self.state}"
            )
            self._export_to_otel(old_state, self.state)

    def on_failure(self) -> None:
        """Record failed call via ResilienceCore."""
        old_state = self.state
        self.last_failure_time = time.time()
        self.state, self.failure_count, self.success_count = (
            self.resilience_core.update_state(
                self.state,
                False,
                self.failure_count,
                self.success_count,
                self.last_failure_time,
                self._get_thresholds(),
            )
        )

        if old_state != self.state:
            logging.error(
                f"Circuit breaker '{self.name}' transitioned from {old_state} to {self.state}"
            )
            self._export_to_otel(old_state, self.state)
