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
Test Tracing Benchmark module.
"""

import timeit
import statistics
from src.observability.stats.core.tracing_core import TracingCore


def benchmark_tracing():
    core = TracingCore()

    # 1. Benchmark span context creation

    def run_span():
        core.create_span_context("trace-12345", "span-67890")

    times_span = timeit.repeat(run_span, repeat=5, number=100000)
    avg_span = statistics.mean(times_span) / 100000 * 1e6

    print(f"create_span_context: {avg_span:.4f} μs per call")

    # 2. Benchmark latency breakdown
    def run_latency():
        core.calculate_latency_breakdown(1.5, 0.3)

    times_lat = timeit.repeat(run_latency, repeat=5, number=100000)
    avg_lat = statistics.mean(times_lat) / 100000 * 1e6
    print(f"calculate_latency_breakdown: {avg_lat:.4f} μs per call")


if __name__ == "__main__":
    benchmark_tracing()