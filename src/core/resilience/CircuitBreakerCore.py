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

"""Core state-machine logic for provider circuit-breakers."""

from __future__ import annotations

import time

from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig
from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState


class CircuitBreakerCore:
    """Implements transitions for CLOSED, OPEN, and HALF_OPEN states."""

    time = time

    def record_success(self, state: CircuitBreakerState) -> None:
        """Record a successful provider call.

        Args:
            state: Mutable provider state.

        """
        state.total_calls += 1
        state.total_successes += 1
        state.consecutive_failures = 0
        state.probe_in_flight = False
        state.state = CircuitState.CLOSED

    def record_failure(self, state: CircuitBreakerState, config: CircuitBreakerConfig) -> None:
        """Record a failed provider call and transition if threshold is reached.

        Args:
            state: Mutable provider state.
            config: Provider circuit configuration.

        """
        state.total_calls += 1
        state.total_failures += 1
        state.consecutive_failures += 1
        state.last_failure_time = self.time.monotonic()

        if state.state is CircuitState.HALF_OPEN:
            state.state = CircuitState.OPEN
            state.probe_in_flight = False
            return

        if state.consecutive_failures >= config.failure_threshold:
            state.state = CircuitState.OPEN

    def should_allow(self, state: CircuitBreakerState, config: CircuitBreakerConfig) -> bool:
        """Check whether the next call may proceed for the provider.

        Args:
            state: Mutable provider state.
            config: Provider circuit configuration.

        Returns:
            ``True`` if a call should proceed, otherwise ``False``.

        """
        if state.state is CircuitState.CLOSED:
            return True

        if state.state is CircuitState.OPEN:
            elapsed = self.time.monotonic() - state.last_failure_time
            if elapsed >= config.recovery_timeout:
                state.state = CircuitState.HALF_OPEN
                if state.probe_in_flight:
                    return False
                state.probe_in_flight = True
                return True
            return False

        if state.probe_in_flight:
            return False

        state.probe_in_flight = True
        return True

    def reset(self, state: CircuitBreakerState) -> None:
        """Reset a provider circuit to baseline CLOSED state.

        Args:
            state: Mutable provider state.

        """
        state.state = CircuitState.CLOSED
        state.consecutive_failures = 0
        state.probe_in_flight = False

    def check_state(self, state: CircuitBreakerState, config: CircuitBreakerConfig) -> CircuitState:
        """Return effective state and promote OPEN to HALF_OPEN when timeout elapsed.

        Args:
            state: Mutable provider state.
            config: Provider circuit configuration.

        Returns:
            Effective state after timeout promotion checks.

        """
        if state.state is CircuitState.OPEN:
            elapsed = self.time.monotonic() - state.last_failure_time
            if elapsed >= config.recovery_timeout:
                state.state = CircuitState.HALF_OPEN
        return state.state


def validate() -> bool:
    """Validate this module wiring for structure tests.

    Returns:
        Always ``True``.

    """
    return True
