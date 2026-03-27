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

"""Per-module tests for src/core/resilience/CircuitBreakerConfig.py.

Comprehensive resilience integration tests live in tests/test_circuit_breaker.py.
This file satisfies the test_each_core_has_test_file convention.
"""

from __future__ import annotations

from src.core.resilience.CircuitBreakerConfig import CircuitBreakerConfig, validate  # type: ignore[import]


def test_circuit_breaker_config_validate() -> None:
    """Ensure the CircuitBreakerConfig validate() helper returns True."""
    assert validate() is True


def test_circuit_breaker_config_defaults_are_constructible() -> None:
    """Ensure CircuitBreakerConfig can be instantiated with only provider_key."""
    cfg = CircuitBreakerConfig(provider_key="provider-a")
    assert cfg.provider_key == "provider-a"
