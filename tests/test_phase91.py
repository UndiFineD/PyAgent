import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.classes.specialized.StrategicPlanningAgent import StrategicPlanningAgent

class TestStrategicPlanning(unittest.TestCase):
    def setUp(self):
        self.agent = StrategicPlanningAgent(os.getcwd())

    def test_goal_setting(self) -> None:
        goal = self.agent.set_long_term_goal("Achieve Swarm Autonomy", "2027-01-01")
        self.assertEqual(goal['description'], "Achieve Swarm Autonomy")
        self.assertEqual(goal['status'], "In Progress")

    def test_milestones(self) -> None:
        goal = self.agent.set_long_term_goal("Build Mars Colony AI", "2030-12-31")
        goal_id = goal['id']
        self.agent.add_milestone_to_goal(goal_id, "Design Habitat Life Support")
        self.agent.add_milestone_to_goal(goal_id, "Optimize Rocket Trajectories")
        
        self.agent.mark_milestone_complete(goal_id, "Design Habitat Life Support")
        
        roadmap = self.agent.generate_roadmap()
        self.assertEqual(len(roadmap), 1)
        self.assertEqual(roadmap[0]['completion'], 50.0)

    def test_summary(self) -> None:
        self.agent.set_long_term_goal("Global Warming Mitigation", "2040-01-01")
        summary = self.agent.get_strategic_summary()
        self.assertEqual(summary['active_goals'], 1)
        self.assertEqual(summary['overall_health'], "On Track")

if __name__ == "__main__":
    unittest.main()
