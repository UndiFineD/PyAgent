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
"""
Test Convergence Benchmark module.
"""

import timeit
from src.core.base.logic.core.convergence_core import ConvergenceCore


def benchmark_convergence():
    core = ConvergenceCore("/tmp")
    # Setup data
    small_fleet = {f"Agent_{i}": True for i in range(10)}
    mixed_fleet = {f"Agent_{i}": i % 2 == 0 for i in range(100)}

    large_fleet = {f"Agent_{i}": True for i in range(1000)}

    t_small = timeit.timeit(lambda: core.verify_fleet_health(small_fleet), number=10000)
    t_mixed = timeit.timeit(lambda: core.verify_fleet_health(mixed_fleet), number=10000)
    t_large = timeit.timeit(lambda: core.verify_fleet_health(large_fleet), number=1000)

    print(f"Verify Health (Small 10): {t_small / 10000 * 1e6:.2f} us")
    print(f"Verify Health (Mixed 100): {t_mixed / 10000 * 1e6:.2f} us")
    print(f"Verify Health (Large 1000): {t_large / 1000 * 1e6:.2f} us")


if __name__ == "__main__":
    benchmark_convergence()