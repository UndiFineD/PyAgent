"""Unit tests for CLI script wrappers."""
import unittest
import subprocess
import sys
from pathlib import Path
from typing import Any

class TestCLIWrappers(unittest.TestCase):
    def setUp(self) -> None:
        self.python: str = sys.executable
        self.src_dir: Path = Path(__file__).parent.parent.parent / "src"
        
    def run_agent_help(self, script_name: str) -> subprocess.CompletedProcess[str]:
        script_path: Path = self.src_dir / script_name
        result: subprocess.CompletedProcess[str] = subprocess.run(
            [self.python, str(script_path), "--help"],
            capture_output=True,
            text=True
        )
        return result

    def test_agent_errors_help(self) -> None:
        res: subprocess.CompletedProcess[str] = self.run_agent_help("errors/error_handler.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Errors Agent", res.stdout)
        self.assertIn("--context", res.stdout)

    def test_agent_changes_help(self) -> None:
        res: subprocess.CompletedProcess[str] = self.run_agent_help("agent_changes.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Changes Agent", res.stdout)

    def test_agent_coder_help(self) -> None:
        res: subprocess.CompletedProcess[str] = self.run_agent_help("coder/code_generator.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Coder Agent", res.stdout)

    def test_agent_stats_help(self) -> None:
        res: subprocess.CompletedProcess[str] = self.run_agent_help("stats/metrics_collector.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Stats Agent", res.stdout)
        self.assertIn("--files", res.stdout)

    def test_agent_orchestrator_help(self) -> None:
        res: subprocess.CompletedProcess[str] = self.run_agent_help("agent.py")
        self.assertEqual(res.returncode, 0)
        self.assertIn("Orchestrates code improvement agents", res.stdout)

if __name__ == "__main__":
    unittest.main()
