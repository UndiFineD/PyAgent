#!/usr/bin/env python3

"""Agent specializing in automated testing and coverage analysis.
Inspired by SGI-Bench and py.test.
"""

import logging
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

class TestAgent(BaseAgent):
    """Executes unit and integration tests and analyzes failures."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self._system_prompt = (
            "You are the Test Agent. "
            "Your role is to ensure the functional correctness of the codebase. "
            "Execute pytest suites, capture failures, and explain them to the developers. "
            "Always suggest a potential cause for every test failure."
        )

    @as_tool
    def run_tests(self, path: str = "tests") -> str:
        """Executes pytest on the specified directory."""
        logging.info(f"TestAgent running tests in: {path}")
        try:
            import sys
            # Converted to list-based execution to prevent shell injection
            cmd = [sys.executable, "-m", "pytest", path, "--tb=short", "--maxfail=5"]
            result = subprocess.run(cmd, shell=False, capture_output=True, text=True)
            
            report = ["## 🧪 Test Execution Report\n"]
            if result.returncode == 0:
                report.append("✅ **Status**: All tests passed.")
                report.append(f"```text\n{result.stdout.splitlines()[-1]}\n```") # Last line summary
            else:
                report.append(f"❌ **Status**: {result.returncode} tests FAILED.\n")
                report.append("### Failure Details")
                report.append(f"```text\n{result.stdout}\n```")
            
            return "\n".join(report)
        except Exception as e:
            return f"Error running tests: {e}"

    @as_tool
    def run_file_tests(self, file_path: str) -> str:
        """Runs tests for a single file."""
        return self.run_tests(file_path)

    def improve_content(self, prompt: str) -> str:
        """Runs tests based on user prompt."""
        return self.run_tests()

