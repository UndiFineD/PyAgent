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

"""Session Management logic for the PyAgent GUI."""

from __future__ import annotations

import json
from tkinter import filedialog, messagebox
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SessionManager:
    """Handles saving and loading of the GUI state."""

    def __init__(self, default_filename="gui_session.json") -> None:
        self.default_filename: str = default_filename

    def save_session(self, data) -> bool:
        """Saves session data to a JSON file."""
        filepath: str = filedialog.asksaveasfilename(
            initialfile=self.default_filename,
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                return True
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                messagebox.showerror("Save Error", f"Failed to save session: {e}")
        return False

    def load_session(self) -> Any | None:
        """Loads session data from a JSON file."""
        filepath: str = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not filepath:
            return None

        try:
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            messagebox.showerror("Load Error", f"Failed to load session: {e}")
            return None
