import unittest
import os
import asyncio
from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from src.infrastructure.fleet.FleetManager import FleetManager


class TestPhase44(IsolatedAsyncioTestCase):
    def setUp(self):
        self.workspace = os.path.abspath(Path(__file__).resolve().parents[2])
        self.fleet = FleetManager(self.workspace)
        # Ensure directories exist
        os.makedirs(
            os.path.join(self.workspace, "data/forge/datasets"), exist_ok=True
        )
        os.makedirs(
            os.path.join(self.workspace, "data/forge/adapters"), exist_ok=True
        )
        os.makedirs(
            os.path.join(self.workspace, "data/memory/agent_store"), exist_ok=True
        )

    async def test_autonomous_fine_tuning(self) -> None:
        print("\nTesting Autonomous Fine-Tuning Trigger...")
        evolution_data = {
            "version": "v12",
            "synthetic_examples": [
                {
                    "instruction": "Write a complex SQL query",
                    "output": "SELECT * FROM agents JOIN capabilities...",
                },
                {
                    "instruction": "Optimize for performance",
                    "output": "Using indexed search...",
                },
            ],
        }
        res = self.fleet.model_forge.trigger_autonomous_tuning(
            "SQLAgent", evolution_data
        )
        if asyncio.iscoroutine(res):
            res = await res
        print(f"Result: {res}")
        self.assertIn("SUCCESS: Fine-tuning job", res)
        self.assertIn("Autonomous Tuning Initialized", res)

        # Verify adapter directory created
        self.assertTrue(
            os.path.exists(
                os.path.join(self.workspace, "data/forge/adapters/opt_SQLAgent_v12")
            )
        )

    async def test_weight_orchestration(self) -> None:
        print("\nTesting Weight Orchestration...")
        # Activate adapter
        res = self.fleet.weight_orchestrator.activate_adapter(
            "SQLAgent", "opt_SQLAgent_v12"
        )
        if asyncio.iscoroutine(res):
            await res

        # Verify registration
        res = self.fleet.weight_orchestrator.get_active_adapter("SQLAgent")
        if asyncio.iscoroutine(res):
            active = await res
        else:
            active = res
        self.assertEqual(active, "opt_SQLAgent_v12")

        # List all

        res = self.fleet.weight_orchestrator.list_registrations()
        if asyncio.iscoroutine(res):
            regs = await res
        else:
            regs = res
        self.assertIn("SQLAgent", regs)

        # Deactivate
        res = self.fleet.weight_orchestrator.deactivate_adapter("SQLAgent")

        if asyncio.iscoroutine(res):
            await res

        res = self.fleet.weight_orchestrator.get_active_adapter("SQLAgent")
        if asyncio.iscoroutine(res):
            active = await res
        else:
            active = res
        self.assertIsNone(active)


if __name__ == "__main__":
    unittest.main()
