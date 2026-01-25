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
Test Pruning Core module.
"""

import unittest
from hypothesis import given, strategies as st
import math
import time
from src.core.base.logic.core.pruning_core import PruningCore, SynapticWeight


class TestPruningCore(unittest.TestCase):
    def setUp(self):
        self.core = PruningCore()

    @given(
        current_weight=st.floats(min_value=0.0, max_value=1.0),
        idle_time=st.floats(min_value=0.0, max_value=100000.0),
        half_life=st.floats(min_value=1.0, max_value=10000.0),
    )
    def test_calculate_decay(self, current_weight, idle_time, half_life):
        new_weight = self.core.calculate_decay(current_weight, idle_time, half_life)

        # Check bounds
        self.assertGreaterEqual(new_weight, 0.05)
        self.assertLessEqual(new_weight, max(current_weight, 0.05))

        # Check calculation logic manually
        # const = ln(2) / half_life
        # weight * exp(-const * idle)
        const = math.log(2) / half_life
        expected = current_weight * math.exp(-const * idle_time)
        expected = max(expected, 0.05)
        self.assertAlmostEqual(new_weight, expected)

    @given(refractory_until=st.floats(min_value=0, max_value=2000000000))
    def test_is_in_refractory(self, refractory_until):
        weight = SynapticWeight(
            agent_id="test", weight=0.5, last_fired=0, refractory_until=refractory_until
        )
        # We can't strictly control time.time(), so we test relative
        now = time.time()
        result = self.core.is_in_refractory(weight)

        if now < refractory_until:
            self.assertTrue(result)
        else:
            self.assertFalse(result)

    @given(
        current_weight=st.floats(min_value=0.0, max_value=1.0), success=st.booleans()
    )
    def test_update_weight_on_fire(self, current_weight, success):
        new_weight = self.core.update_weight_on_fire(current_weight, success)

        if success:
            expected = min(current_weight * 1.1, 1.0)
            self.assertAlmostEqual(new_weight, expected)
        else:
            expected = max(current_weight * 0.8, 0.1)

            self.assertAlmostEqual(new_weight, expected)

    @given(
        weight=st.floats(min_value=0.0, max_value=1.0),
        threshold=st.floats(min_value=0.0, max_value=1.0),
    )
    def test_should_prune(self, weight, threshold):
        result = self.core.should_prune(weight, threshold)
        self.assertEqual(result, weight < threshold)


if __name__ == "__main__":
    unittest.main()