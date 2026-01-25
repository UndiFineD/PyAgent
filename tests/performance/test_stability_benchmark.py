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
Test Stability Benchmark module.
"""

import timeit
import statistics
from src.observability.stats.core.stability_core import StabilityCore, FleetMetrics


def benchmark_stability():
    core = StabilityCore()
    metrics = FleetMetrics(0.01, 5000, 20, 1500.0)

    anomalies = 1

    # 1. Benchmark score calculation
    def run_calc():
        core.calculate_stability_score(metrics, anomalies)

    times_calc = timeit.repeat(run_calc, repeat=5, number=100000)
    avg_calc = statistics.mean(times_calc) / 100000 * 1e6  # microseconds
    print(f"calculate_stability_score: {avg_calc:.4f} μs per call")

    # 2. Benchmark stasis check
    history = [0.5, 0.51, 0.49, 0.5, 0.52, 0.48, 0.5, 0.51, 0.49, 0.5]

    def run_stasis():
        core.is_in_stasis(history)

    times_stasis = timeit.repeat(run_stasis, repeat=5, number=100000)
    avg_stasis = statistics.mean(times_stasis) / 100000 * 1e6
    print(f"is_in_stasis: {avg_stasis:.4f} μs per call")


if __name__ == "__main__":
    benchmark_stability()