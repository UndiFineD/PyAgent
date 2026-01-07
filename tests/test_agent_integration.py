import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from agent import Agent

class TestAgentIntegration(unittest.TestCase):
    def setUp(self):
        self.agent = Agent(repo_root=".")
        self.agent._run_command = MagicMock()
        self.agent.repo_root = Path("/tmp/repo")

    def test_strategy_flag_passed_to_subagent(self):
        """Test that --strategy flag is passed to sub-agents."""
        self.agent.strategy = "reflexion"
        
        # Mock _run_command to return success
        self.agent._run_command.return_value.returncode = 0
        
        # Call update_code which calls sub-agent
        self.agent.update_code(Path("test_file.py"))
        
        # Check calls
        calls = self.agent._run_command.call_args_list
        found = False
        for call in calls:
            args = call[0][0]
            # args is a list of command parts
            if "--strategy" in args and "reflexion" in args:
                found = True
                break
        
        self.assertTrue(found, "Sub-agent command should contain --strategy reflexion")

    def test_async_flag_initialization(self):
        """Test that enable_async flag is set correctly."""
        agent = Agent(repo_root=".", enable_async=True)
        self.assertTrue(agent.enable_async)

if __name__ == "__main__":
    unittest.main()
