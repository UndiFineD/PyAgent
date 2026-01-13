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

from __future__ import annotations
from src.core.base.version import VERSION
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

__version__ = VERSION

class StatusManager:
    """Manages project execution status for the DirectorAgent and GUI."""
    
    def __init__(self) -> None:
        self.status_file = Path("src/infrastructure/orchestration/status.json")
        self.clear_status()

    def clear_status(self) -> None:
        """Resets the status file."""
        initial_data = {
            "last_updated": datetime.now().isoformat(),
            "active_project": None,
            "steps": [],
            "current_step_index": -1,
            "overall_status": "Idle"
        }
        self._write(initial_data)

    def start_project(self, goal: str, steps_count: int) -> None:
        """Initializes a new project tracking session."""
        data = {
            "last_updated": datetime.now().isoformat(),
            "active_project": goal,
            "steps": [],
            "current_step_index": 0,
            "overall_status": "Running"
        }
        self._write(data)

    def add_step(self, agent: str, file: str, prompt: str) -> None:
        """Adds a scheduled step to the plan."""
        data = self._read()
        data["steps"].append({
            "agent": agent,
            "file": file,
            "prompt": prompt,
            "status": "Pending",
            "result": None
        })
        self._write(data)

    def update_step_status(self, index: int, status: str, result: Any = None) -> None:
        """Updates the status of a specific step."""
        data = self._read()
        if 0 <= index < len(data["steps"]):
            data["steps"][index]["status"] = status
            if result:
                data["steps"][index]["result"] = result
            data["current_step_index"] = index
            data["last_updated"] = datetime.now().isoformat()
            self._write(data)

    def finish_project(self, success: bool = True) -> None:
        """Marks the project as complete."""
        data = self._read()
        data["overall_status"] = "Completed" if success else "Failed"
        data["last_updated"] = datetime.now().isoformat()
        self._write(data)

    def _read(self) -> dict[str, Any]:
        if not self.status_file.exists():
            self.clear_status()
        with open(self.status_file) as f:
            return json.load(f)

    def _write(self, data: dict[str, Any]) -> None:
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.status_file, "w") as f:
            json.dump(data, f, indent=4)