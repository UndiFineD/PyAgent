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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Diff Viewer component for the PyAgent GUI."""

from __future__ import annotations
from src.core.base.version import VERSION
import tkinter as tk
from tkinter import ttk, messagebox
import difflib
from typing import Any

__version__ = VERSION

class DiffViewer:
    """A window for viewing differences between original and changed files."""
    def __init__(self, parent: Any) -> None:
        self.parent = parent

    def show_diff(self, original_path: str, changed_content: str, title: str = "Changes Preview") -> None:
        if not original_path:
            messagebox.showwarning("Warning", "No original file specified.")
            return

        try:
            with open(original_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read original file: {e}")
            return

        diff = difflib.unified_diff(
            original_content.splitlines(),
            changed_content.splitlines(),
            fromfile="Original",
            tofile="Proposed",
            lineterm=""
        )
        
        diff_text = "\n".join(list(diff))
        if not diff_text:
            messagebox.showinfo("No Changes", "The proposed content is identical to the original.")
            return

        # Create diff window
        win = tk.Toplevel(self.parent)
        win.title(title)
        win.geometry("900x600")

        text = tk.Text(win, wrap=tk.NONE)
        text.pack(fill=tk.BOTH, expand=True)

        # Basic coloring
        text.tag_configure("add", foreground="green")
        text.tag_configure("remove", foreground="red")
        text.tag_configure("header", foreground="blue", font=("Segoe UI", 10, "bold"))

        for line in diff_text.splitlines():
            if line.startswith('+') and not line.startswith('+++'):
                text.insert(tk.END, line + "\n", "add")
            elif line.startswith('-') and not line.startswith('---'):
                text.insert(tk.END, line + "\n", "remove")
            elif line.startswith('@@') or line.startswith('---') or line.startswith('+++'):
                text.insert(tk.END, line + "\n", "header")
            else:
                text.insert(tk.END, line + "\n")

        # Scrollbars
        h_scroll = ttk.Scrollbar(win, orient=tk.HORIZONTAL, command=text.xview)
        v_scroll = ttk.Scrollbar(win, orient=tk.VERTICAL, command=text.yview)
        text.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)