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
Test Phase89 module.
"""

import unittest

# Ensure the project root is in PYTHONPATH

from src.infrastructure.orchestration.intel.IntelligenceOrchestrator import (
    IntelligenceOrchestrator,
)


class TestIntelligence(unittest.TestCase):
    def setUp(self):
        self.orchestrator = IntelligenceOrchestrator(None)

    def test_synthesis(self) -> None:
        self.orchestrator.contribute_insight(
            "AgentA", "Detected quantum fluctuation in memory", 0.9
        )
        self.orchestrator.contribute_insight(
            "AgentB", "Quantum patterns appearing in the shard", 0.8
        )

        patterns = self.orchestrator.synthesize_collective_intelligence()
        self.assertTrue(any("quantum" in p.lower() for p in patterns))

        report = self.orchestrator.get_intelligence_report()
        self.assertEqual(report["insights_collected"], 2)
        self.assertEqual(report["patterns_identified"], 1)


if __name__ == "__main__":
    unittest.main()