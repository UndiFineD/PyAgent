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
Test Phase52 module.
"""

import unittest
import asyncio
from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase52(IsolatedAsyncioTestCase):
    def setUp(self):
        self.fleet = FleetManager(str(Path(__file__).resolve().parents[2]))

    async def test_neuro_optimization(self) -> None:
        print("\nTesting Phase 52: Evolutionary Neuro-Optimization...")
        # Mock fleet stats
        stats = {
            "LinguisticAgent": {"success_rate": 0.5, "avg_latency": 1.2},  # Failing
            "ReasoningAgent": {"success_rate": 0.95, "avg_latency": 4.5},  # Succeeding
        }

        res = self.fleet.evolution.optimize_hyperparameters(stats)
        if asyncio.iscoroutine(res):
            optimized = await res
        else:
            optimized = res

        print(f"Optimized Params: {optimized}")

        # Checking logic
        self.assertLess(optimized["LinguisticAgent"]["temperature"], 0.7)
        self.assertGreater(optimized["ReasoningAgent"]["temperature"], 0.7)


if __name__ == "__main__":
    unittest.main()