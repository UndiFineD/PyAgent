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

"""Unit tests for the modular GUI components."""

import unittest
import logging
import tkinter as tk
from tkinter import ttk
import os
from src.interface.ui.gui.WidgetLogger import WidgetLogger
from src.interface.ui.gui.ProjectExplorer import ProjectExplorer
from src.interface.ui.gui.AgentColumn import AgentColumn

class TestGUIModular(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.root = tk.Tk()
            cls.root.withdraw() # Hide window during tests
            cls._tk_available = True
        except Exception as e:
            logging.warning(f"Skipping GUI tests: Tkinter not available: {e}")
            cls._tk_available = False

    def setUp(self):
        if not self._tk_available:
            self.skipTest("Tkinter not available in this environment")

    @classmethod
    def tearDownClass(cls):
        if cls._tk_available:
            cls.root.destroy()

    def test_widget_logger(self):
        text = tk.Text(self.root)
        logger = WidgetLogger(text)
        record = logging.LogRecord("test", logging.INFO, "test.py", 10, "Test Log message", (), None)
        logger.emit(record)
        self.root.update()
        content = text.get("1.0", tk.END).strip()
        self.assertIn("Test Log message", content)

    def test_project_explorer_init(self):
        frame = ttk.Frame(self.root)
        root_var = tk.StringVar(value=os.getcwd())
        def dummy_cb(*args): pass
        explorer = ProjectExplorer(frame, root_var, on_double_click_callback=dummy_cb)
        self.assertIsNotNone(explorer.tree)

    def test_widget_logger_filtering(self):
        text = tk.Text(self.root)
        # Logger with specific thread ID
        logger = WidgetLogger(text, thread_id=123)
        
        # Record from same thread
        record1 = logging.LogRecord("test", logging.INFO, "test.py", 10, "Thread 123 message", (), None)
        record1.thread = 123
        logger.emit(record1)
        
        # Record from different thread
        record2 = logging.LogRecord("test", logging.INFO, "test.py", 10, "Thread 456 message", (), None)
        record2.thread = 456
        logger.emit(record2)
        
        self.root.update()
        content = text.get("1.0", tk.END).strip()
        self.assertIn("Thread 123 message", content)
        self.assertNotIn("Thread 456 message", content)

    def test_project_explorer_search(self):
        frame = ttk.Frame(self.root)
        root_var = tk.StringVar(value=os.getcwd())
        explorer = ProjectExplorer(frame, root_var, on_double_click_callback=lambda x: None)
        
        # Mock search variable
        explorer.search_var.set("agent_gui")
        explorer.filter_tree()
        
        # Check if the file is found (it should find src/agent_gui.py)
        children = explorer.tree.get_children()
        texts = [explorer.tree.item(c)["text"] for c in children]
        found = any("agent_gui.py" in t for t in texts)
        self.assertTrue(found)

    def test_agent_column_data_retrieval(self):
        frame = ttk.Frame(self.root)
        def dummy_cb(*args): pass
        callbacks = {
            "execute": dummy_cb,
            "stop": dummy_cb,
            "browse_file": dummy_cb,
            "voice": dummy_cb,
            "remove": dummy_cb,
            "diff": dummy_cb
        }
        column = AgentColumn(frame, "Coder", callbacks)
        
        column.file_var.set("test_file.py")
        column.backend_cb.set("gh")
        column.prompt_text.insert("1.0", "New Task")
        
        data = column.get_data()
        self.assertEqual(data["file"], "test_file.py")
        self.assertEqual(data["backend"], "gh")
        self.assertEqual(data["prompt"], "New Task")

if __name__ == "__main__":
    unittest.main()
