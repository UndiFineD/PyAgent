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
Test Autonomy Core module.
"""

import unittest
from hypothesis import given, strategies as st
from src.core.base.logic.core.autonomy_core import AutonomyCore


class TestAutonomyCore(unittest.TestCase):
    def setUp(self):
        self.core = AutonomyCore("test_agent_01")

    @given(
        success_rate=st.floats(min_value=0.0, max_value=1.0),
        task_diversity=st.floats(min_value=0.0, max_value=1.0),
    )
    def test_identify_blind_spots(self, success_rate, task_diversity):
        blind_spots = self.core.identify_blind_spots(success_rate, task_diversity)

        if success_rate < 0.7:
            self.assertIn("GENERAL_REASONING_RELIABILITY", blind_spots)
        else:
            self.assertNotIn("GENERAL_REASONING_RELIABILITY", blind_spots)

        if task_diversity < 0.3:
            self.assertIn("DOMAIN_SPECIFIC_RIGIDITY", blind_spots)
        else:
            self.assertNotIn("DOMAIN_SPECIFIC_RIGIDITY", blind_spots)

    @given(st.floats(min_value=0.0, max_value=2.0))
    def test_calculate_daemon_sleep_interval(self, optimization_score):
        interval = self.core.calculate_daemon_sleep_interval(optimization_score)

        if optimization_score >= 1.0:
            self.assertEqual(interval, 3600)
        elif optimization_score > 0.8:
            self.assertEqual(interval, 600)

        else:
            self.assertEqual(interval, 60)

    @given(st.lists(st.text(min_size=1), min_size=0, max_size=5))
    def test_generate_self_improvement_plan(self, blind_spots):
        plan = self.core.generate_self_improvement_plan(blind_spots)

        self.assertIn(self.core.agent_id, plan)
        if not blind_spots:
            self.assertIn("Optimal", plan)

        else:
            self.assertIn("Expand training data", plan)
            for spot in blind_spots:
                self.assertIn(spot, plan)


if __name__ == "__main__":
    unittest.main()