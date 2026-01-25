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
Test Model Fallback Benchmark module.
"""

import timeit
import statistics
from src.observability.stats.metrics_core import ModelFallbackCore


def benchmark_fallback():
    core = ModelFallbackCore()

    # 1. Benchmark logic selection

    def run_select():
        core.select_best_model({"max_cost": 0.5, "required_speed": 0.5})

    times_select = timeit.repeat(run_select, repeat=5, number=100000)
    avg_select = statistics.mean(times_select) / 100000 * 1e6

    print(f"select_best_model: {avg_select:.4f} μs per call")

    # 2. Benchmark fallback chain
    def run_chain():
        core.get_fallback_chain("gpt-4")

    times_chain = timeit.repeat(run_chain, repeat=5, number=100000)
    avg_chain = statistics.mean(times_chain) / 100000 * 1e6
    print(f"get_fallback_chain: {avg_chain:.4f} μs per call")


if __name__ == "__main__":
    benchmark_fallback()