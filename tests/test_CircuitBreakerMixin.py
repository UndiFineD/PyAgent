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

"""Per-module tests for src/core/resilience/CircuitBreakerMixin.py.

Comprehensive resilience integration tests live in tests/test_circuit_breaker.py.
This file satisfies the test_each_core_has_test_file convention.
"""

from __future__ import annotations

import pytest
from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig  # type: ignore[import]
from src.core.resilience.CircuitBreakerMixin import CircuitBreakerMixin, validate  # type: ignore[import]
from src.core.resilience.CircuitBreakerRegistry import CircuitBreakerRegistry  # type: ignore[import]


class _Agent(CircuitBreakerMixin):
    """Minimal concrete mixin host used for per-module smoke checks."""

    def __init__(self) -> None:
        """Initialize with a fresh registry for deterministic behavior."""
        self._circuit_breaker_registry = CircuitBreakerRegistry()


def test_circuit_breaker_mixin_validate() -> None:
    """Ensure the CircuitBreakerMixin validate() helper returns True."""
    assert validate() is True


@pytest.mark.asyncio
async def test_circuit_breaker_mixin_cb_call_success_path() -> None:
    """Ensure cb_call returns a coroutine result on the simple success path."""
    agent = _Agent()
    cfg = CircuitBreakerConfig(provider_key="provider-a")

    async def _ok() -> int:
        """Return a deterministic integer payload."""
        return 7

    result = await agent.cb_call("provider-a", _ok, cfg)
    assert result == 7
