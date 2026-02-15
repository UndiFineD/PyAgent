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
Test Profiling Core module.
"""

import unittest
from hypothesis import given, strategies as st, settings, HealthCheck
from unittest.mock import MagicMock
from src.observability.stats.core.profiling_core import ProfilingCore, ProfileStats


class TestProfilingCore(unittest.TestCase):
    def setUp(self):
        self.core = ProfilingCore()

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        call_count=st.integers(min_value=0, max_value=1000000),
        total_time=st.floats(min_value=0.0, max_value=1000.0),
    )
    def test_calculate_optimization_priority(self, call_count, total_time):
        stats = ProfileStats(
            function_name="test_func",
            call_count=call_count,
            total_time=total_time,
            per_call=0.0,
        )
        priority = self.core.calculate_optimization_priority(stats)
        expected = call_count * total_time
        self.assertAlmostEqual(priority, expected)

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        threshold_ms=st.floats(min_value=0.0, max_value=1000.0),
        stats_list=st.lists(
            st.tuples(st.text(min_size=1), st.floats(min_value=0.0, max_value=10.0)),
            min_size=0,
            max_size=20,
            unique_by=lambda x: x[0],
        ),
    )
    def test_identify_bottlenecks(self, threshold_ms, stats_list):
        # Create ProfileStats list
        profiles = [
            ProfileStats(name, 1, time_val, time_val) for name, time_val in stats_list
        ]

        bottlenecks = self.core.identify_bottlenecks(profiles, threshold_ms)

        threshold_sec = threshold_ms / 1000.0
        for name, time_val in stats_list:
            if time_val > threshold_sec:
                self.assertIn(name, bottlenecks)
            else:
                self.assertNotIn(name, bottlenecks)

    def test_analyze_stats_mock_logic(self):
        # Mock pstats object structure
        # keys: (filename, line, funcname)
        # values: (cc, nc, tt, ct, callers)
        mock_stats_data = {
            ("file.py", 10, "func_a"): (10, 10, 0.1, 0.5, {}),
            ("file.py", 20, "func_b"): (5, 5, 0.01, 0.05, {}),
        }

        mock_pstats = MagicMock()
        mock_pstats.stats = mock_stats_data

        # We need to simulate sort_stats behavior if we rely on it,
        # but analyze_stats iterates .items() which isn't guaranteed order in Python < 3.7
        # assuming basic interaction works.

        results = self.core.analyze_stats(mock_pstats, limit=10)

        self.assertEqual(len(results), 2)
        func_names = {r.function_name for r in results}
        self.assertIn("('file.py', 10, 'func_a')", func_names)

        # Verify calculation: per_call = ct / cc
        # func_a: 0.5 / 10 = 0.05
        func_a = next(r for r in results if "func_a" in r.function_name)
        self.assertAlmostEqual(func_a.per_call, 0.05)


if __name__ == "__main__":
    unittest.main()
