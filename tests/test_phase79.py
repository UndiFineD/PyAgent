import unittest
import sys
from pathlib import Path

# Ensure src is in sys.path
root = Path(__file__).parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))

from src.classes.fleet.FleetManager import FleetManager

class TestPhase79(unittest.TestCase):
    def setUp(self):
        self.workspace = "c:/DEV/PyAgent"
        self.fleet = FleetManager(self.workspace)

    def test_swarm_visualizer(self) -> None:
        print("\nTesting Phase 79: Neural Network Topology & Swarm Visualization...")
        
        # 1. Log interactions
        self.fleet.swarm_visualizer.log_interaction("AgentA", "AgentB", "task_delegation")
        self.fleet.swarm_visualizer.log_interaction("AgentB", "AgentC", "query")
        self.fleet.swarm_visualizer.log_interaction("AgentC", "AgentA", "response")
        
        # 2. Update positions
        self.fleet.swarm_visualizer.update_agent_position("AgentA", 10.0, 20.0)
        self.fleet.swarm_visualizer.update_agent_position("AgentB", 50.0, 50.0)
        
        # 3. Generate topology map
        topology = self.fleet.swarm_visualizer.generate_topology_map()
        print(f"Topology: {topology}")
        self.assertEqual(len(topology["nodes"]), 3)
        self.assertEqual(len(topology["edges"]), 3)
        
        # 4. Get visualization data
        viz_data = self.fleet.swarm_visualizer.get_visualization_data()
        print(f"Viz Data: {viz_data}")
        self.assertEqual(viz_data["metrics"]["total_interactions"], 3)
        self.assertEqual(viz_data["metrics"]["active_agents"], 2)

if __name__ == "__main__":
    unittest.main()
