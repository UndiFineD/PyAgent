#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Integration tests for the PyAgent GUI application."""

import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import os
import json
from src.interface.ui.gui.MainApp import PyAgentGUI
from src.interface.ui.gui.SessionManager import SessionManager

class TestGUIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
            cls._tk_available = True
        except Exception as e: Exception:
            logging.warning(f"Skipping GUI tests: Tkinter not available: {e}")
            cls._tk_available = False

    @classmethod
    def tearDownClass(cls) -> None:
        if cls._tk_available:
            cls.root.destroy()

    def setUp(self) -> None:
        if not self._tk_available:
            self.skipTest("Tkinter not available in this environment")
        self.app = PyAgentGUI(self.root)

    def test_app_initialization(self) -> None:
        self.assertIn("PyAgent Control Center", self.app.root.title())
        self.assertTrue(self.app.theme_manager.is_dark_mode)
        self.assertEqual(self.app.project_root_var.get(), os.getcwd())

    def test_theme_toggle(self) -> None:
        initial_mode: bool = self.app.theme_manager.is_dark_mode
        self.app.theme_manager.toggle_theme()
        self.assertNotEqual(initial_mode, self.app.theme_manager.is_dark_mode)
        self.app.theme_manager.toggle_theme()
        self.assertEqual(initial_mode, self.app.theme_manager.is_dark_mode)

    def test_add_agent_column(self) -> None:
        initial_count: int = len(self.app.agent_manager.agent_columns)
        self.app.add_agent_column("TestAgent")
        self.assertEqual(len(self.app.agent_manager.agent_columns), initial_count + 1)
        self.assertEqual(self.app.agent_manager.agent_columns[-1].agent_name, "TestAgent")

    def test_session_manager_save_load(self) -> None:
        # Mock file dialogs
        test_session_file = "test_session.json"
        session_data = {
            "root": "/mock/path",
            "global_context": "Mock Context",
            "agents": [
                {
                    "name": "Coder",
                    "file": "test.py",
                    "backend": "copilot",
                    "model": "gpt-4o"
                }
            ]
        }
        
        # Test loading logic in MainApp which uses SessionManager
        with patch('tkinter.filedialog.askopenfilename', return_value=test_session_file):
            with patch('builtins.open', unittest.mock.mock_open(read_data=json.dumps(session_data))):
                self.app.load_session()
                
        self.assertEqual(self.app.project_root_var.get(), "/mock/path")
        self.assertIn("Mock Context", self.app.global_context.get("1.0", tk.END))
        self.assertEqual(len(self.app.agent_manager.agent_columns), 1)
        self.assertEqual(self.app.agent_manager.agent_columns[0].agent_name, "Coder")


if __name__ == "__main__":
    unittest.main()
