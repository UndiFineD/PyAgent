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

import unittest
from unittest.mock import MagicMock
from pathlib import Path

# Add project root to path so we can import 'src'

from src.logic.agents import Agent


class TestAgentIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.agent: Agent = Agent(repo_root=".")
        self.agent.command_handler.run_command = MagicMock()
        self.agent.repo_root = Path("/tmp/repo")

    def test_strategy_flag_passed_to_subagent(self) -> None:
        """Test that --strategy flag is passed to sub-agents."""
        self.agent.strategy = "reflexion"

        # Mock run_command to return success
        self.agent.command_handler.run_command.return_value = MagicMock(
            returncode=0, stdout="Success"
        )

        # Call update_code which calls sub-agent

        self.agent.update_code(Path("test_file.py"))

        # Check calls
        calls = self.agent.command_handler.run_command.call_args_list

        found = False
        for call in calls:
            args = call[0][0]
            # args is a list of command parts
            if "--strategy" in args and "reflexion" in args:
                found = True
                break

        self.assertTrue(found, "Sub-agent command should contain --strategy reflexion")

    def test_async_flag_initialization(self) -> None:
        """Test that enable_async flag is set correctly."""
        agent: Agent = Agent(repo_root=".", enable_async=True)
        self.assertTrue(agent.enable_async)


if __name__ == "__main__":
    unittest.main()
