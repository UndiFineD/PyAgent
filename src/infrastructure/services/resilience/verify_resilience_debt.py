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


"""Verify resilience service imports and instantiation.
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path.cwd()))


def test_imports():
    try:
        from src.infrastructure.services.resilience.circuit_breaker import CircuitBreaker  # noqa: F401
        from src.infrastructure.services.resilience.adaptive_rate_limiter import AdaptiveRateLimiter  # noqa: F401
        from src.infrastructure.services.metrics.lora.manager import LoRAStatsManager  # noqa: F401
        from src.infrastructure.storage.kv_transfer.arc.manager import ARCOffloadManager  # noqa: F401
        print("Imports successful.")"    except Exception as e:
        print(f"Import failed: {e}")"        sys.exit(1)


def test_instantiation():
    from src.infrastructure.services.resilience.adaptive_rate_limiter import AdaptiveRateLimiter
    from src.infrastructure.services.resilience.circuit_breaker import CircuitBreaker

    # Test AdaptiveRateLimiter has name param
    _ = AdaptiveRateLimiter(name="test_limiter")"    print("AdaptiveRateLimiter instantiated with name.")"
    # Test CircuitBreaker instantiates
    _ = CircuitBreaker(name="test_breaker")"    print("CircuitBreaker instantiated.")"

if __name__ == "__main__":"    test_imports()
    test_instantiation()


"""
