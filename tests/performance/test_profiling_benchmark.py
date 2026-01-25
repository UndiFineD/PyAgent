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
Test Profiling Benchmark module.
"""

import timeit
import statistics
from src.observability.stats.core.profiling_core import ProfilingCore, ProfileStats


def benchmark_profiling():
    core = ProfilingCore()
    stats_obj = ProfileStats("slow_func", 1000, 5.0, 0.005)

    # 1. Benchmark priority calculation
    def run_priority():
        core.calculate_optimization_priority(stats_obj)

    times_prio = timeit.repeat(run_priority, repeat=5, number=100000)
    avg_prio = statistics.mean(times_prio) / 100000 * 1e6
    print(f"calculate_optimization_priority: {avg_prio:.4f} μs per call")

    # 2. Benchmark bottleneck identification
    # Create a list of 100 stats
    stats_list = [ProfileStats(f"func_{i}", 100, i * 0.01, 0.0001) for i in range(100)]

    def run_bottleneck():
        core.identify_bottlenecks(stats_list, threshold_ms=500.0)

    times_bottle = timeit.repeat(run_bottleneck, repeat=5, number=10000)
    avg_bottle = statistics.mean(times_bottle) / 10000 * 1e6
    print(f"identify_bottlenecks: {avg_bottle:.4f} μs per call")


if __name__ == "__main__":
    benchmark_profiling()