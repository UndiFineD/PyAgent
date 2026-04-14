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

"""Circuit-breaker state model and enum."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CircuitState(Enum):
    """Finite states of the circuit-breaker state machine."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass(slots=True)
class CircuitBreakerState:
    """Mutable runtime state for one provider circuit.

    Args:
        provider_key: Provider identifier.
        state: Current machine state.
        consecutive_failures: Current consecutive failure count.
        last_failure_time: Monotonic timestamp of the last failure.
        probe_in_flight: Whether a HALF_OPEN probe is currently running.
        total_calls: Total call attempts observed for this provider.
        total_failures: Total failed attempts observed for this provider.
        total_successes: Total successful attempts observed for this provider.

    """

    provider_key: str
    state: CircuitState = CircuitState.CLOSED
    consecutive_failures: int = 0
    last_failure_time: float = 0.0
    probe_in_flight: bool = False
    total_calls: int = 0
    total_failures: int = 0
    total_successes: int = 0


def validate() -> bool:
    """Validate this module wiring for structure tests.

    Returns:
        Always ``True``.

    """
    return True
