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

"""Per-module tests for src/core/resilience/CircuitBreakerRegistry.py.

Comprehensive resilience integration tests live in tests/test_circuit_breaker.py.
This file satisfies the test_each_core_has_test_file convention.
"""

from __future__ import annotations

import pytest

from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig  # type: ignore[import]
from src.core.resilience.CircuitBreakerRegistry import CircuitBreakerRegistry, validate  # type: ignore[import]


def test_circuit_breaker_registry_validate() -> None:
    """Ensure the CircuitBreakerRegistry validate() helper returns True."""
    assert validate() is True


@pytest.mark.asyncio
async def test_circuit_breaker_registry_get_or_create_returns_state() -> None:
    """Ensure get_or_create produces a state object for a provider key."""
    registry = CircuitBreakerRegistry()
    cfg = CircuitBreakerConfig(provider_key="provider-a")
    state = await registry.get_or_create("provider-a", cfg)
    assert state.provider_key == "provider-a"
