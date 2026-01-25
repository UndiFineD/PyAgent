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

"""Unit tests for agent execution strategies (Direct, CoT, Reflexion)."""
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
from pathlib import Path

# Add src to path

from src.core.base.entrypoint import BaseAgent
from src.logic.strategies.plan_executor import DirectStrategy, ChainOfThoughtStrategy, ReflexionStrategy

class TestStrategies(unittest.TestCase):
    def setUp(self) -> str:
        # Create a dummy file so BaseAgent init doesn't fail
        with open("test_file.txt", 'w', encoding='utf-8') as f:
            f.write("Original Content")
            
        self.agent = BaseAgent("test_file.txt")
        self.agent.previous_content = "Original Content"
        self.agent.run_subagent = MagicMock(return_value="Improved Content")
        
        # Disable cache and retries
        self.agent._config.cache_enabled = False
        self.agent._config.retry_count = 0
        
        # Mock quality check to always pass
        self.agent._score_response_quality = MagicMock(return_value=MagicMock(value=100)) # High value

    def tearDown(self) -> str:
        if os.path.exists("test_file.txt"):
            os.remove("test_file.txt")

    def test_direct_strategy(self) -> None:
        self.agent.set_strategy(DirectStrategy())
        self.agent.improve_content("Fix bugs")
        
        # Check if run_subagent was called once
        self.agent.run_subagent.assert_called_once()
        args = self.agent.run_subagent.call_args
        # args[0] is (description, prompt, original_content)
        # prompt is at index 1
        self.assertIn("Fix bugs", args[0][1]) 

    def test_cot_strategy(self) -> None:
        self.agent.set_strategy(ChainOfThoughtStrategy())
        self.agent.improve_content("Fix bugs")
        
        # Check if run_subagent was called twice (Reasoning + Implementation)
        self.assertEqual(self.agent.run_subagent.call_count, 2)
        
        # Check first call (Reasoning)
        args1 = self.agent.run_subagent.call_args_list[0]
        self.assertIn("Think step-by-step", args1[0][1])
        
        # Check second call (Implementation)
        args2 = self.agent.run_subagent.call_args_list[1]
        self.assertIn("Based on the following reasoning", args2[0][1])

    def test_reflexion_strategy(self) -> None:
        self.agent.set_strategy(ReflexionStrategy())
        # Mock run_subagent to return different values based on prompt
        def side_effect(desc, prompt, content) -> str:
            if "Critique" in prompt:
                return "Critique: Good but needs X"
            if "Revise" in prompt:
                return "Revised Content"
            return "Draft Content"
            
        self.agent.run_subagent = MagicMock(side_effect=side_effect)
        
        self.agent.improve_content("Fix bugs")
        
        # Should be called 3 times (Draft, Critique, Revise)
        self.assertEqual(self.agent.run_subagent.call_count, 3)

if __name__ == '__main__':
    unittest.main()
