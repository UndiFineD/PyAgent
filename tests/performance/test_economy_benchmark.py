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
Test Economy Benchmark module.
"""

import time
import random
from src.infrastructure.swarm.fleet.core.economy_core import EconomyCore


def test_economy_benchmark():
    # Setup
    size = 1_000_000
    credits = [random.uniform(10, 1000) for _ in range(size)]
    importance = [random.random() for _ in range(size)]
    urgency = [random.random() for _ in range(size)]

    # Benchmark Priority Calculation loop
    start = time.perf_counter()

    priorities = []
    for c, i, u in zip(credits, importance, urgency):
        priorities.append(EconomyCore.calculate_bid_priority(c, i, u))
    duration_prio = (time.perf_counter() - start) * 1000

    print(f"Economy Prio Calc (N={size}): {duration_prio:.4f} ms")

    # Benchmark Surcharge
    vram = [random.uniform(4, 24) for _ in range(size)]

    util = [random.random() for _ in range(size)]

    start = time.perf_counter()
    surcharges = []
    for v, u in zip(vram, util):
        surcharges.append(EconomyCore.calculate_gpu_surcharge(v, u))
    duration_sur = (time.perf_counter() - start) * 1000

    print(f"Economy Surcharge Calc (N={size}): {duration_sur:.4f} ms")


if __name__ == "__main__":
    test_economy_benchmark()