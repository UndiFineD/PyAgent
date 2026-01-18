#!/usr/bin/env python3
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

"""Header Panel component for the PyAgent GUI."""

from __future__ import annotations
from src.core.base.Version import VERSION
from typing import Any
import tkinter as tk
from tkinter import ttk
from .TemplateManager import TemplateManager

__version__ = VERSION


class HeaderPanel:
    """Handles project root selection and global context input."""

    def __init__(self, parent, project_root_var, callbacks) -> None:
        self.frame = ttk.Frame(parent, padding=5)
        self.project_root_var: Any = project_root_var
        self.callbacks: Any = callbacks
        self.setup_ui()

    def setup_ui(self) -> None:
        root_frame = ttk.Frame(self.frame)
        root_frame.pack(fill=tk.X)

        ttk.Label(root_frame, text="Project Root:").pack(side=tk.LEFT)
        ttk.Entry(root_frame, textvariable=self.project_root_var, width=60).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            root_frame, text="Browse", command=self.callbacks.get("browse_root")
        ).pack(side=tk.LEFT)
        ttk.Button(
            root_frame, text="Refresh", command=self.callbacks.get("refresh_explorer")
        ).pack(side=tk.LEFT, padx=5)

        # Global Prompt Frame
        prompt_frame: ttk.Labelframe = ttk.LabelFrame(
            self.frame, text="Global Context / Task Description", padding=5
        )
        prompt_frame.pack(fill=tk.X, pady=5)

        template_frame = ttk.Frame(prompt_frame)
        template_frame.pack(fill=tk.X)
        ttk.Label(template_frame, text="Templates:").pack(side=tk.LEFT)

        self.template_var = tk.StringVar(value="Select Template...")
        template_cb = ttk.Combobox(
            template_frame,
            textvariable=self.template_var,
            values=TemplateManager.get_template_names(),
            state="readonly",
        )
        template_cb.pack(side=tk.LEFT, padx=5)
        template_cb.bind("<<ComboboxSelected>>", self.on_template_selected)

        self.global_context = tk.Text(prompt_frame, height=4)
        self.global_context.pack(fill=tk.X, pady=2)

        # Meta Data / Status Sub-line
        meta_frame = ttk.Frame(self.frame)
        meta_frame.pack(fill=tk.X)
        ttk.Label(
            meta_frame, text="Methodology: BMAD V6", font=("Segoe UI", 8, "italic")
        ).pack(side=tk.LEFT)
        ttk.Label(
            meta_frame,
            text="| Tracks: Quick, Standard, Enterprise",
            font=("Segoe UI", 8),
        ).pack(side=tk.LEFT, padx=10)

    def on_template_selected(self, event) -> None:
        TemplateManager.apply_template(self.global_context, self.template_var.get())
