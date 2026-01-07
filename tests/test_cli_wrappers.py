import unittest
import subprocess
import sys
from pathlib import Path

class TestCLIWrappers(unittest.TestCase):
    def setUp(self):
        self.python = sys.executable
        self.src_dir = Path(__file__).parent.parent / "src"
        
    def run_agent_help(self, script_name):
        script_path = self.src_dir / script_name
        result = subprocess.run(
            [self.python, str(script_path), "--help"],
            capture_output=True,
            text=True
        )
        return result

    def test_agent_errors_help(self):
        res = self.run_agent_help("agent_errors.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Errors Agent", res.stdout)
        self.assertIn("--context", res.stdout)

    def test_agent_changes_help(self):
        res = self.run_agent_help("agent_changes.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Changes Agent", res.stdout)

    def test_agent_coder_help(self):
        res = self.run_agent_help("agent_coder.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Coder Agent", res.stdout)

    def test_agent_stats_help(self):
        res = self.run_agent_help("agent_stats.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Stats Agent", res.stdout)
        self.assertIn("--files", res.stdout)

    def test_agent_orchestrator_help(self):
        res = self.run_agent_help("agent.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Orchestrates code improvement agents", res.stdout)

if __name__ == "__main__":
    unittest.main()
