#!/usr/bin/env python3
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

try:
    import pytest
except ImportError:
    import pytest

try:
    from infrastructure.services.resilience.circuit_breaker import CircuitState, CircuitStats, CircuitBreakerError, CircuitBreaker, CircuitBreakerRegistry, circuit_breaker, get_circuit_stats, get_all_circuit_stats
except ImportError:
    from infrastructure.services.resilience.circuit_breaker import CircuitState, CircuitStats, CircuitBreakerError, CircuitBreaker, CircuitBreakerRegistry, circuit_breaker, get_circuit_stats, get_all_circuit_stats



def test_circuitstate_basic():
    assert CircuitState is not None


def test_circuitstats_basic():
    assert CircuitStats is not None


def test_circuitbreakererror_basic():
    assert CircuitBreakerError is not None


def test_circuitbreaker_basic():
    assert CircuitBreaker is not None


def test_circuitbreakerregistry_basic():
    assert CircuitBreakerRegistry is not None


def test_circuit_breaker_basic():
    assert callable(circuit_breaker)


def test_get_circuit_stats_basic():
    assert callable(get_circuit_stats)


def test_get_all_circuit_stats_basic():
    assert callable(get_all_circuit_stats)
