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

"""
Task Management Mixin for BaseAgent.
Provides structured task tracking and management, inspired by Adorable's todo tool.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path

from src.core.base.common.models.communication_models import CascadeContext


@dataclass
class TaskItem:
    """Represents a single task item."""
    description: str
    completed: bool = False
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    priority: int = 1  # 1=low, 2=medium, 3=high

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "priority": self.priority
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TaskItem:
        return cls(
            description=data["description"],
            completed=data.get("completed", False),
            created_at=data.get("created_at", time.time()),
            completed_at=data.get("completed_at"),
            priority=data.get("priority", 1)
        )

    def complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.completed_at = time.time()

    def reset(self) -> None:
        """Reset the task to incomplete."""
        self.completed = False
        self.completed_at = None


class TaskManagerMixin:
    """
    Mixin providing structured task management capabilities.
    Inspired by Adorable's todo tool for tracking agent tasks and workflows.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.tasks: List[TaskItem] = []
        self.task_file: Optional[Path] = None
        self.auto_save: bool = kwargs.get('auto_save_tasks', True)
        self.max_tasks: int = kwargs.get('max_tasks', 50)

        # Initialize task persistence
        if hasattr(self, '_workspace_root') and self._workspace_root:
            self.task_file = Path(self._workspace_root) / '.pyagent_tasks.json'
            self._load_tasks()

    async def update_task_list(self, items: List[Dict[str, Any]], cascade_context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """
        Update the task list with new items.
        Inspired by Adorable's todo tool interface.
        """
        try:
            # Clear existing tasks if this is a complete reset
            if not items:
                self.tasks.clear()
            else:
                # Update existing tasks and add new ones
                for item_data in items:
                    description = item_data.get("description", "").strip()
                    if not description:
                        continue

                    completed = item_data.get("completed", False)
                    priority = item_data.get("priority", 1)

                    # Find existing task or create new one
                    existing_task = None
                    for task in self.tasks:
                        if task.description == description:
                            existing_task = task
                            break

                    if existing_task:
                        # Update existing task
                        if completed and not existing_task.completed:
                            existing_task.complete()
                        elif not completed and existing_task.completed:
                            existing_task.reset()
                        existing_task.priority = priority
                    else:
                        # Create new task
                        new_task = TaskItem(
                            description=description,
                            completed=completed,
                            priority=priority
                        )
                        self.tasks.append(new_task)

            # Sort tasks by priority (high first) and completion status
            self.tasks.sort(key=lambda t: (-t.priority, t.completed, t.created_at))

            # Limit number of tasks
            if len(self.tasks) > self.max_tasks:
                self.tasks = self.tasks[:self.max_tasks]

            # Auto-save if enabled
            if self.auto_save:
                self._save_tasks()

            return {
                "success": True,
                "message": f"Updated {len(self.tasks)} tasks",
                "task_count": len(self.tasks),
                "completed_count": sum(1 for t in self.tasks if t.completed)
            }

        except Exception as e:
            logging.error(f"Error updating task list: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_task_status(self, cascade_context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Get current task status summary."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed

        high_priority = sum(1 for t in self.tasks if t.priority >= 3 and not t.completed)
        medium_priority = sum(1 for t in self.tasks if t.priority == 2 and not t.completed)
        low_priority = sum(1 for t in self.tasks if t.priority <= 1 and not t.completed)

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "completion_rate": completed / total if total > 0 else 0,
            "priority_breakdown": {
                "high": high_priority,
                "medium": medium_priority,
                "low": low_priority
            },
            "tasks": [task.to_dict() for task in self.tasks]
        }

    async def add_task(self, description: str, priority: int = 1, cascade_context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Add a new task to the list."""
        if not description.strip():
            return {"success": False, "error": "Task description cannot be empty"}

        # Check for duplicate
        for task in self.tasks:
            if task.description == description.strip():
                return {"success": False, "error": "Task already exists"}

        new_task = TaskItem(description=description.strip(), priority=priority)
        self.tasks.append(new_task)

        # Sort and limit
        self.tasks.sort(key=lambda t: (-t.priority, t.completed, t.created_at))
        if len(self.tasks) > self.max_tasks:
            self.tasks = self.tasks[:self.max_tasks]

        if self.auto_save:
            self._save_tasks()

        return {
            "success": True,
            "message": "Task added successfully",
            "task": new_task.to_dict()
        }

    async def complete_task(self, description: str, cascade_context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Mark a task as completed."""
        for task in self.tasks:
            if task.description == description:
                if not task.completed:
                    task.complete()
                    if self.auto_save:
                        self._save_tasks()
                    return {
                        "success": True,
                        "message": "Task completed",
                        "task": task.to_dict()
                    }
                else:
                    return {"success": False, "error": "Task already completed"}

        return {"success": False, "error": "Task not found"}

    async def clear_completed_tasks(self, cascade_context: Optional[CascadeContext] = None) -> Dict[str, Any]:
        """Remove all completed tasks."""
        original_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task.completed]

        removed_count = original_count - len(self.tasks)

        if self.auto_save:
            self._save_tasks()

        return {
            "success": True,
            "message": f"Cleared {removed_count} completed tasks",
            "remaining_tasks": len(self.tasks),
            "removed_count": removed_count
        }

    def _load_tasks(self) -> None:
        """Load tasks from persistent storage."""
        if not self.task_file or not self.task_file.exists():
            return

        try:
            with open(self.task_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.tasks = []
            for item_data in data.get("tasks", []):
                try:
                    task = TaskItem.from_dict(item_data)
                    self.tasks.append(task)
                except (KeyError, ValueError) as e:
                    logging.warning(f"Skipping invalid task data: {e}")

            # Sort tasks
            self.tasks.sort(key=lambda t: (-t.priority, t.completed, t.created_at))

        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading tasks: {e}")

    def _save_tasks(self) -> None:
        """Save tasks to persistent storage."""
        if not self.task_file:
            return

        try:
            self.task_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "version": "1.0",
                "last_updated": time.time(),
                "tasks": [task.to_dict() for task in self.tasks]
            }

            with open(self.task_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except IOError as e:
            logging.error(f"Error saving tasks: {e}")
