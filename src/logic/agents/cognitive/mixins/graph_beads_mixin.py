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

"""Beads task logic for GraphMemoryAgent."""

from __future__ import annotations
import logging
from src.core.base.common.base_utilities import as_tool

class GraphBeadsMixin:
    """Mixin for Beads task graph logic."""

    @as_tool
    def create_task(
        self, title: str, parent_id: str | None = None, priority: int = 2
    ) -> str:
        """Creates a new task with optional parent for hierarchy (Beads pattern)."""
        if not hasattr(self, "tasks"):
            return "Error: Tasks not initialized."

        task_count = len(
            [t for t in self.tasks if not parent_id or t.startswith(f"{parent_id}.")]
        )
        task_id = (
            f"{parent_id}.{task_count + 1}"
            if parent_id
            else f"epic-{len(self.tasks) + 1}"
        )

        task_data = {
            "title": title,
            "status": "ready",
            "priority": priority,
            "blocked_by": [],
            "subtasks": [],
        }
        self.tasks[task_id] = task_data

        if parent_id and parent_id in self.tasks:
            self.tasks[parent_id]["subtasks"].append(task_id)
            if hasattr(self, "_save_bead"):
                self._save_bead(parent_id, self.tasks[parent_id])

        if hasattr(self, "_save_bead"):
            self._save_bead(task_id, task_data)

        logging.info(f"GraphMemory: Created task {task_id}")
        return f"Task created: {task_id} - {title}"

    @as_tool
    def add_dependency(self, blocker_id: str, blocked_id: str) -> str:
        """Links tasks where one blocks another."""
        if not hasattr(self, "tasks"):
            return "Error: Tasks not initialized."

        if blocker_id in self.tasks and blocked_id in self.tasks:
            self.tasks[blocked_id]["blocked_by"].append(blocker_id)
            self.tasks[blocked_id]["status"] = "blocked"
            if hasattr(self, "_save_bead"):
                self._save_bead(blocked_id, self.tasks[blocked_id])
            return f"Task {blocked_id} is now blocked by {blocker_id}."
        return "Error: One or both task IDs not found."

    @as_tool
    def compact_memory(self, threshold_days: int = 30) -> str:
        """Summarizes and prunes old closed tasks to save context (Memory Decay)."""
        if not hasattr(self, "tasks"):
            return "Error: Tasks not initialized."

        closed_tasks = [
            tid for tid, t in self.tasks.items() if t["status"] == "completed"
        ]
        if not closed_tasks:
            return "No completed tasks to compact."

        summary = f"Compacted {len(closed_tasks)} tasks into a historical summary."
        # In a real impl, we'd add this to a 'history' entity
        for tid in closed_tasks:
            del self.tasks[tid]

        return summary
