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

"""Status Bar component for the PyAgent GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class StatusBar:
    """Handles status messages and UI feedback in the footer."""

    def __init__(self, parent, status_var) -> None:
        self.status_var: Any = status_var
        self.label = ttk.Label(
            parent,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor="w",
            padding=2,
        )
        self.label.pack(side=tk.BOTTOM, fill=tk.X)

    def set_status(self, message: str) -> None:
        self.status_var.set(message)
