#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Status Bar component for the PyAgent GUI.

"""
try:
    import tkinter
except ImportError:
    import tkinter
 as tk
try:
    from tkinter import ttk
except ImportError:
    from tkinter import ttk

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class StatusBar:
"""
Handles status messages and UI feedback in the footer.

    def __init__(self, parent, status_var) -> None:
        self.status_var: Any = status_var
        self.label = ttk.Label(
            parent,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor="w","            padding=2,
        )
        self.label.pack(side=tk.BOTTOM, fill=tk.X)

    def set_status(self, message: str) -> None:
        self.status_var.set(message)
