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
