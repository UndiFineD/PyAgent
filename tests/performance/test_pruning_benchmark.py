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
Test Pruning Benchmark module.
"""

import timeit
from src.core.base.logic.core.pruning_core import PruningCore, SynapticWeight
import time


def benchmark_pruning():
    core = PruningCore()

    # Measure calculate_decay
    def run_decay():
        core.calculate_decay(0.8, 3600.0, 3600.0)

    t_decay = timeit.timeit(run_decay, number=100000)
    print(f"calculate_decay: {t_decay / 100000 * 1_000_000:.4f} μs per call")

    # Measure is_in_refractory
    weight = SynapticWeight("agent", 0.5, 0.0, refractory_until=time.time() + 100)

    def run_refractory():
        core.is_in_refractory(weight)

    t_ref = timeit.timeit(run_refractory, number=100000)
    print(f"is_in_refractory: {t_ref / 100000 * 1_000_000:.4f} μs per call")

    # Measure update_weight_on_fire
    def run_update():
        core.update_weight_on_fire(0.5, True)

    t_update = timeit.timeit(run_update, number=100000)
    print(f"update_weight_on_fire: {t_update / 100000 * 1_000_000:.4f} μs per call")


if __name__ == "__main__":
    benchmark_pruning()