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

"""Theme Management logic for the PyAgent GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ThemeManager:
    """Handles switching between light and dark themes for the GUI."""

    def __init__(self, root: tk.Tk) -> None:
        self.root: Any = root
        self.is_dark_mode = True

    def apply_theme(self) -> None:
        style = ttk.Style()
        if self.is_dark_mode:
            bg, fg = "#2d2d2d", "#ffffff"
            style.theme_use("clam")
            style.configure("TFrame", background=bg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("TLabelframe", background=bg, foreground=fg)
            style.configure("TLabelframe.Label", background=bg, foreground=fg)
            style.configure("TButton", background="#4a4a4a", foreground=fg)
            style.configure("Header.TFrame", background="#3e3e42")
            style.configure(
                "Treeview",
                background="#3d3d3d",
                foreground=fg,
                fieldbackground="#3d3d3d",
            )
            self.root.configure(bg=bg)
        else:
            style.theme_use("default")
            style.configure("Header.TFrame", background="#e1e1e1")
            self.root.configure(bg="#f0f0f0")

        self.refresh_widgets(self.root)

    def toggle_theme(self) -> None:
        self.is_dark_mode: bool = not self.is_dark_mode
        self.apply_theme()

    def refresh_widgets(self, parent: tk.Misc) -> None:
        bg: str = "#2d2d2d" if self.is_dark_mode else "#f0f0f0"
        fg: str = "white" if self.is_dark_mode else "black"
        text_bg: str = "#1e1e1e" if self.is_dark_mode else "white"

        for child in parent.winfo_children():
            if isinstance(child, tk.Text):
                child.configure(bg=text_bg, fg=fg, insertbackground=fg)
            elif isinstance(child, (tk.Entry, tk.Listbox)):
                try:
                    child.configure(bg=text_bg, fg=fg, insertbackground=fg)
                except tk.TclError:
                    pass
            elif isinstance(child, tk.Label):
                # Don't change background of phase labels with colors
                if child.cget("bg") not in ["#007acc", "#d04437", "#2e7d32"]:
                    child.configure(bg=bg, fg=fg)
            self.refresh_widgets(child)
