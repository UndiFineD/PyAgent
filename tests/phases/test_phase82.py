import unittest
import os

# Ensure the project root is in PYTHONPATH

from src.logic.agents.system.performance_profiling_agent import PerformanceProfilingAgent


class TestPerformanceProfiling(unittest.TestCase):
    def setUp(self):
        self.agent = PerformanceProfilingAgent(os.getcwd())

    def test_profiling_and_analysis(self) -> None:
        agents = ["AgentA", "AgentB", "AgentC"]

        # Capture snapshot
        snapshot = self.agent.profile_fleet_usage(agents)
        self.assertEqual(len(snapshot["agents"]), 3)
        self.assertIn("cpu_usage", snapshot["agents"]["AgentA"])

        # Analysis (might return empty if random values are low, but let's check structure)
        bottlenecks = self.agent.analyze_bottlenecks()
        self.assertIsInstance(bottlenecks, list)

        # Force a bottleneck to test detection
        self.agent.metrics_history[-1]["agents"]["AgentA"]["latency_ms"] = 1000
        bottlenecks = self.agent.analyze_bottlenecks()
        self.assertTrue(
            any(
                b["agent"] == "AgentA" and b["issue"] == "High Latency"
                for b in bottlenecks
            )
        )


if __name__ == "__main__":
    unittest.main()
