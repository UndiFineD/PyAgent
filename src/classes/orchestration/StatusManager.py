import json
import os
from pathlib import Path
from datetime import datetime

class StatusManager:
    """Manages project execution status for the DirectorAgent and GUI."""
    
    def __init__(self):
        self.status_file = Path("src/classes/orchestration/status.json")
        self.clear_status()

    def clear_status(self):
        """Resets the status file."""
        initial_data = {
            "last_updated": datetime.now().isoformat(),
            "active_project": None,
            "steps": [],
            "current_step_index": -1,
            "overall_status": "Idle"
        }
        self._write(initial_data)

    def start_project(self, goal, steps_count):
        """Initializes a new project tracking session."""
        data = {
            "last_updated": datetime.now().isoformat(),
            "active_project": goal,
            "steps": [],
            "current_step_index": 0,
            "overall_status": "Running"
        }
        self._write(data)

    def add_step(self, agent, file, prompt):
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

    def update_step_status(self, index, status, result=None):
        """Updates the status of a specific step."""
        data = self._read()
        if 0 <= index < len(data["steps"]):
            data["steps"][index]["status"] = status
            if result:
                data["steps"][index]["result"] = result
            data["current_step_index"] = index
            data["last_updated"] = datetime.now().isoformat()
            self._write(data)

    def finish_project(self, success=True):
        """Marks the project as complete."""
        data = self._read()
        data["overall_status"] = "Completed" if success else "Failed"
        data["last_updated"] = datetime.now().isoformat()
        self._write(data)

    def _read(self):
        if not self.status_file.exists():
            self.clear_status()
        with open(self.status_file, "r") as f:
            return json.load(f)

    def _write(self, data):
        self.status_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.status_file, "w") as f:
            json.dump(data, f, indent=4)
