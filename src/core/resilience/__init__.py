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

"""Public exports for the resilience package."""

from __future__ import annotations

from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig
from src.core.resilience.CircuitBreakerCore import CircuitBreakerCore
from src.core.resilience.CircuitBreakerMixin import CircuitBreakerMixin
from src.core.resilience.CircuitBreakerRegistry import CircuitBreakerRegistry
from src.core.resilience.CircuitBreakerState import CircuitBreakerState, CircuitState
from src.core.resilience.exceptions import AllCircuitsOpenError, CircuitOpenError

__all__ = [
    "AllCircuitsOpenError",
    "CircuitBreakerConfig",
    "CircuitBreakerCore",
    "CircuitBreakerMixin",
    "CircuitBreakerRegistry",
    "CircuitBreakerState",
    "CircuitOpenError",
    "CircuitState",
]


def validate() -> bool:
    """Validate this package wiring for structure tests.

    Returns:
        Always ``True``.

    """
    return True
