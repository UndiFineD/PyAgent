import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to path so we can import 'src'
sys.path.append(str(Path(__file__).parent.parent))

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
        self.agent.command_handler.run_command.return_value = MagicMock(returncode=0, stdout="Success")
        
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
