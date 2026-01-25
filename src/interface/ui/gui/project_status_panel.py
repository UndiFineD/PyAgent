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

"""
Project status panel.py module.
"""


from __future__ import annotations

import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ProjectStatusPanel:
    """A panel that displays the current orchestration status from status.json."""

    def __init__(self, parent) -> None:
        self.frame: ttk.Labelframe = ttk.LabelFrame(parent, text="Orchestration Status", padding=10)
        self.status_file = Path("src/infrastructure/orchestration/status.json")

        self.goal_label = ttk.Label(self.frame, text="Active Project: None", font=("Segoe UI", 10, "bold"))
        self.goal_label.pack(anchor="w")

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(self.frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)

        self.steps_text = tk.Text(self.frame, height=8, width=50, font=("Consolas", 9))
        self.steps_text.pack(fill=tk.BOTH, expand=True)

        self.refresh()

    def refresh(self) -> None:
        """Polls the status file and updates the UI."""
        if self.status_file.exists():
            try:
                with open(self.status_file, encoding='utf-8') as f:
                    data = json.load(f)

                goal = data.get("active_project", "None") or "None"
                self.goal_label.config(text=f"Active Project: {goal}")

                steps = data.get("steps", [])
                completed: int = sum(1 for s in steps if s.get("status") == "Completed")
                total: int = len(steps)

                if total > 0:
                    self.progress_var.set((completed / total) * 100)
                else:
                    self.progress_var.set(0)

                self.steps_text.delete("1.0", tk.END)
                for i, step in enumerate(steps):
                    status = step.get("status", "Pending")
                    agent = step.get("agent", "Unknown")
                    file = step.get("file", "unknown")
                    self.steps_text.insert(tk.END, f"[{i + 1}/{total}] {status:10} | {agent} -> {file}\n")

            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                self.steps_text.delete("1.0", tk.END)
                self.steps_text.insert(tk.END, f"Error reading status: {e}")

        self.frame.after(2000, self.refresh)  # Polling every 2s
