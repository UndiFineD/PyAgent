# -*- coding: utf-8 -*-
"""
Unit tests for safe and strategic command execution in AgentCommandHandler.
"""

from __future__ import annotations
import unittest
import os
import sys
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.core.base.AgentCommandHandler import AgentCommandHandler

class TestAgentCommandHandler(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(os.getcwd())
        self.models_config = {
            "test_agent": {
                "provider": "test_provider",
                "model": "test_model",
                "temperature": 0.7
            }
        }
        self.handler = AgentCommandHandler(self.repo_root, models_config=self.models_config)

    @patch("subprocess.run")
    def test_run_command_basic(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ls"], returncode=0, stdout="file1\nfile2", stderr=""
        )
        result = self.handler.run_command(["ls"])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "file1\nfile2")
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_run_command_retry_logic(self, mock_run):
        # Fail first, succeed second
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=["fail"], returncode=1, stdout="", stderr="error"),
            subprocess.CompletedProcess(args=["fail"], returncode=0, stdout="success", stderr="")
        ]
        
        # We use a small timeout for wait in the handler if we wanted to speed this up,
        # but here we just mock the run calls.
        result = self.handler.run_command(["fail"], max_retries=2)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "success")
        self.assertEqual(mock_run.call_count, 2)

    def test_prepare_command_environment_agent(self):
        # Simulate an agent script being called
        agent_script = str(self.repo_root / "agent_tester.py")
        cmd = [sys.executable, agent_script, "--arg1"]
        
        local_cmd, env = self.handler._prepare_command_environment(cmd)
        
        self.assertIn("--no-cascade", local_cmd)
        self.assertEqual(env.get("DV_AGENT_PARENT"), "1")
        self.assertEqual(env.get("DV_AGENT_MODEL_PROVIDER"), "test_provider")
        self.assertEqual(env.get("DV_AGENT_MODEL_NAME"), "test_model")

    def test_with_agent_env_context_manager(self):
        with self.handler.with_agent_env("test_agent"):
            self.assertEqual(os.environ.get("DV_AGENT_MODEL_PROVIDER"), "test_provider")
            self.assertEqual(os.environ.get("DV_AGENT_MODEL_NAME"), "test_model")
        
        self.assertNotIn("DV_AGENT_MODEL_PROVIDER", os.environ)

if __name__ == "__main__":
    unittest.main()
