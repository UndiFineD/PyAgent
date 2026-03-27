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

"""Coverage tests for CircuitBreakerState module."""

from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState, validate


def test_circuit_breaker_state_defaults() -> None:
    """CircuitBreakerState should initialize with expected default values."""
    state = CircuitBreakerState(provider_key="provider-a")
    assert state.provider_key == "provider-a"
    assert state.state is CircuitState.CLOSED
    assert state.consecutive_failures == 0
    assert state.total_calls == 0


def test_circuit_breaker_state_validate_hook() -> None:
    """Module-level validate hook should return True."""
    assert validate() is True
