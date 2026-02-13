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

"""Menu Bar component for the PyAgent GUI."""

from __future__ import annotations

import tkinter as tk
from typing import Any

from src.core.base.lifecycle.version import VERSION

from .constants import BMAD_AGENTS

__version__ = VERSION


class AppMenu:
    """Handles the creation and command routing for the application menu bar."""

    def __init__(self, master, callbacks) -> None:
        self.menubar = tk.Menu(master)
        self.callbacks: Any = callbacks
        self.setup_menus()
        master.config(menu=self.menubar)

    def setup_menus(self) -> None:
        # File Menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="New Session", command=self.callbacks.get("new_session"))
        file_menu.add_command(label="Save Session", command=self.callbacks.get("save_session"))
        file_menu.add_command(label="Load Session", command=self.callbacks.get("load_session"))
        file_menu.add_separator()
        file_menu.add_command(label="Settings...", command=self.callbacks.get("show_settings"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.callbacks.get("exit"))
        self.menubar.add_cascade(label="File", menu=file_menu)

        # View Menu
        view_menu = tk.Menu(self.menubar, tearoff=0)
        view_menu.add_command(label="Toggle Theme", command=self.callbacks.get("toggle_theme"))
        self.menubar.add_cascade(label="View", menu=view_menu)

        # Agents Menu
        agents_menu = tk.Menu(self.menubar, tearoff=0)
        for atype in BMAD_AGENTS:
            agents_menu.add_command(
                label=f"Add {atype} Agent",
                command=lambda t=atype: self.callbacks.get("add_agent")(t),
            )
        agents_menu.add_separator()
        agents_menu.add_command(label="Add Custom Agent...", command=self.callbacks.get("add_custom"))
        self.menubar.add_cascade(label="Agents", menu=agents_menu)

        # BMAD Menu
        bmad_menu = tk.Menu(self.menubar, tearoff=0)
        bmad_menu.add_command(label="BMAD Wizard...", command=self.callbacks.get("bmad_wizard"))
        bmad_menu.add_separator()
        tracks_menu = tk.Menu(bmad_menu, tearoff=0)
        from .constants import BMAD_TRACKS

        for track in BMAD_TRACKS.keys():
            tracks_menu.add_command(label=track, command=lambda t=track: self.callbacks.get("set_track")(t))
        bmad_menu.add_cascade(label="Methodology Tracks", menu=tracks_menu)
        self.menubar.add_cascade(label="BMAD", menu=bmad_menu)
