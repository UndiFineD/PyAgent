import unittest
from pathlib import Path
from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class TestPhase75(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(__file__).resolve().parents[2]
        self.fleet = FleetManager(self.workspace)

    def test_memory_replay_agent(self) -> None:
        print("\nTesting Phase 75: Bio-Mimetic Memory Replay...")

        # Simulated episodic memories
        memories = [
            {
                "id": "m1",
                "action": "test_fix",
                "content": "Fixed bug in auth module",
                "success": True,
            },
            {
                "id": "m2",
                "action": "read_file",
                "content": "Just reading readme",
                "success": True,
            },
            {
                "id": "m3",
                "action": "run_error",
                "content": "Syntax error in main.py",
                "success": False,
            },
        ]

        # Start sleep cycle
        res = self.fleet.memory_replay.start_sleep_cycle(memories)

        print(f"Sleep Cycle Result: {res}")
        self.assertEqual(res["memories_processed"], 3)
        self.assertIn("consolidated", res)
        self.assertIn("pruned", res)

        # Check insights
        log = self.fleet.memory_replay.get_dream_log()
        print(f"Dream Log: {log}")
        self.assertGreaterEqual(log["insights_count"], 0)


if __name__ == "__main__":
    unittest.main()
