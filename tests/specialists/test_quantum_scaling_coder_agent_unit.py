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
Unit tests for QuantumScalingCoderAgent.
"""

import unittest
from src.logic.agents.specialized.quantum_scaling_coder_agent import QuantumScalingCoderAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

class TestQuantumScalingCoderAgent(unittest.TestCase):
    """
    Test suite for the QuantumScalingCoderAgent class.
    """

    def setUp(self) -> None:
        """
        Set up the test case.
        """
        self.agent = QuantumScalingCoderAgent("dummy_path.py")

    def test_initialization(self) -> None:
        """
        Test that the agent initializes correctly.
        """
        self.assertIsNotNone(self.agent)
        self.assertIn("QuantumScalingCoderAgent", self.agent.__class__.__name__)

if __name__ == "__main__":
    unittest.main()
