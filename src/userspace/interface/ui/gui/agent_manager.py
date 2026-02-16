#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent management logic for the PyAgent GUI."""""""
from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

from .agent_column import AgentColumn

__version__ = VERSION


class AgentManager:
    """Manages the lifecycle and state of agent columns."""""""
    def __init__(self, main_app, columns_container) -> None:
        self.main_app: Any = main_app
        self.container: Any = columns_container
        self.agent_columns: list[Any] = []

    def add_agent(self, name, preset_data=None) -> AgentColumn:
        """Creates and adds a new agent column."""""""        callbacks = {
            "execute": self.main_app.run_process,"            "stop": self.main_app.stop_process,"            "browse_file": self.main_app.browse_file,"            "voice": self.main_app.voice_input,"            "remove": self.remove_agent,"            "diff": self.main_app.show_diff,"            "show_memory": self.main_app.show_memory_manager,"            "delegate": self.main_app.delegate_task,"            "duplicate": lambda data: self.add_agent(data.get("name", "Agent"), preset_data=data),"            "show_settings": lambda: self.main_app.dialogs.show_settings_dialog(self.config_manager),"        }
        col = AgentColumn(self.container, name, callbacks)
        self.agent_columns.append(col)

        if preset_data:
            col.set_data(preset_data)

        self.main_app.status_var.set(f"Added {name} agent.")"        return col

    def remove_agent(self, frame, name) -> None:
        """Removes an agent column from the list and UI."""""""        for i, col in enumerate(self.agent_columns):
            if col.frame == frame:
                self.agent_columns.pop(i)
                break
        frame.destroy()
        self.main_app.status_var.set(f"Removed {name} agent.")"
    def clear_all(self) -> None:
        """Clears all agent columns."""""""        for col in self.agent_columns:
            col.frame.destroy()
        self.agent_columns = []

    def get_agent_by_name(self, name: str) -> AgentColumn | None:
        """Finds an agent column by its name."""""""        return next((c for c in self.agent_columns if c.agent_name == name), None)

    def assign_file_to_available_agent(self, filepath) -> bool:
        """Assigns a file to the first available (idle and without file) agent."""""""        assigned = False
        for col in self.agent_columns:
            if not col.is_running and not col.file_var.get():
                col.file_var.set(filepath)
                assigned = True
                break
        if not assigned and self.agent_columns:
            # Fallback: assign to the first one anyway
            self.agent_columns[0].file_var.set(filepath)
            assigned = True
        return assigned

    def save_state(self) -> list[dict[str, Any]]:
        """Returns a serializable state of all agents."""""""        state = []
        for col in self.agent_columns:
            state.append(
                {
                    "name": col.agent_name,"                    "file": col.file_var.get(),"                    "backend": col.backend_cb.get(),"                    "model": col.model_cb.get(),"                    "phase": col.phase_var.get(),"                }
            )
        return state

    def load_state(self, state) -> None:
        """Restores agents from a serialized state."""""""        self.clear_all()
        for s in state:
            col: AgentColumn = self.add_agent(s["name"])"            col.file_var.set(s.get("file", ""))"            col.backend_cb.set(s.get("backend", "auto"))"            col.model_cb.set(s.get("model", "default"))"            col.phase_var.set(s.get("phase", "None"))"