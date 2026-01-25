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
Test Tracing Core module.
"""

import unittest
from hypothesis import given, strategies as st
from src.observability.stats.core.tracing_core import TracingCore


class TestTracingCore(unittest.TestCase):
    def setUp(self):
        self.core = TracingCore()

    @given(st.text(), st.text())
    def test_create_span_context(self, trace_id, span_id):
        context = self.core.create_span_context(trace_id, span_id)
        self.assertEqual(context["trace_id"], trace_id)
        self.assertEqual(context["span_id"], span_id)
        self.assertEqual(context["version"], "OTel-1.1")

    @given(
        total_time=st.floats(min_value=0.001, max_value=1000.0),
        network_fraction=st.floats(min_value=0.0, max_value=1.0),
    )
    def test_calculate_latency_breakdown(self, total_time, network_fraction):
        # network_time cannot exceed total_time logically, so we derive it
        network_time = total_time * network_fraction

        breakdown = self.core.calculate_latency_breakdown(total_time, network_time)

        self.assertAlmostEqual(breakdown["total_latency_ms"], total_time * 1000)
        self.assertAlmostEqual(breakdown["network_latency_ms"], network_time * 1000)

        thinking_time = total_time - network_time

        self.assertAlmostEqual(breakdown["agent_thinking_ms"], thinking_time * 1000)

        # Check ratio
        self.assertAlmostEqual(breakdown["think_ratio"], thinking_time / total_time)

    def test_calculate_latency_breakdown_zero(self):
        breakdown = self.core.calculate_latency_breakdown(0.0, 0.0)
        self.assertEqual(breakdown["think_ratio"], 0)

    @given(st.text(), st.dictionaries(st.text(), st.integers()))
    def test_format_otel_log(self, name, attributes):
        log = self.core.format_otel_log(name, attributes)

        self.assertIn("timestamp", log)

        self.assertIsInstance(log["timestamp"], int)
        self.assertEqual(log["name"], name)
        self.assertEqual(log["attributes"], attributes)
        self.assertEqual(log["kind"], "INTERNAL")


if __name__ == "__main__":
    unittest.main()