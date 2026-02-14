#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Dashboard component for managing multiple agent columns."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class AgentDashboard:
    """Manages the agent columns container and provides controls to add agents."""

    def __init__(self, parent, callbacks) -> None:
        self.frame = ttk.Frame(parent)
        self.callbacks: Any = callbacks
        self.setup_ui()

    def setup_ui(self) -> None:
        canvas = tk.Canvas(self.frame)
        v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        self.dash_content = ttk.Frame(canvas)

        self.dash_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # Ensure dash_content matches canvas width
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas_window: int = canvas.create_window((0, 0), window=self.dash_content, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set)

        v_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Control Panel atop Dashboard
        dash_ctrl = ttk.Frame(self.dash_content)
        dash_ctrl.pack(fill=tk.X, pady=5)
        ttk.Label(
            dash_ctrl,
            text="Agent Dashboard (Vertical Stack)",
            font=("Segoe UI", 9, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(dash_ctrl, text="Collapse All", command=self.collapse_all).pack(side=tk.RIGHT, padx=2)
        ttk.Button(dash_ctrl, text="Expand All", command=self.expand_all).pack(side=tk.RIGHT, padx=2)

        ttk.Button(
            dash_ctrl,
            text="+ Full Stack",
            command=lambda: self.callbacks.get("add_agent")("Developer"),
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            dash_ctrl,
            text="+ Architect",
            command=lambda: self.callbacks.get("add_agent")("Architect"),
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            dash_ctrl,
            text="+ PM",
            command=lambda: self.callbacks.get("add_agent")("PM"),
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            dash_ctrl,
            text="+ Security",
            command=lambda: self.callbacks.get("add_agent")("Security"),
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(dash_ctrl, text="+ Custom...", command=self.callbacks.get("add_custom")).pack(side=tk.LEFT, padx=5)

        # Container for columns (rows now)
        self.columns_container = ttk.Frame(self.dash_content)
        self.columns_container.pack(fill=tk.BOTH, expand=True)

    def collapse_all(self) -> None:
        if "collapse_all" in self.callbacks:
            self.callbacks["collapse_all"]()

    def expand_all(self) -> None:
        if "expand_all" in self.callbacks:
            self.callbacks["expand_all"]()
