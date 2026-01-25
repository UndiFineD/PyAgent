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
Test Phase91 module.
"""

import unittest
import os
import sys

# Ensure the project root is in PYTHONPATH

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