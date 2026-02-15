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
Tests for Task Manager Mixin.
Tests structured task tracking and management inspired by Adorable's todo tool.
"""

import pytest
from src.core.base.mixins.task_manager_mixin import TaskManagerMixin, TaskItem
from src.core.base.common.models.communication_models import CascadeContext

class MockTaskManagerMixin(TaskManagerMixin):
    """Test implementation of TaskManagerMixin."""
    def __init__(self, **kwargs):
        self._workspace_root = kwargs.get('_workspace_root')
        super().__init__(**kwargs)

class TestTaskManager:
    """Test cases for TaskManagerMixin."""
    @pytest.fixture
    def task_manager(self, tmp_path):
        return MockTaskManagerMixin(_workspace_root=str(tmp_path))
    @pytest.fixture
    def cascade_context(self):
        return CascadeContext(task_id="test_task", agent_id="test_agent", workflow_id="test_workflow")
    def test_initialization(self, task_manager):
        assert task_manager.tasks == []
        assert task_manager.auto_save
        assert task_manager.max_tasks == 50
    def test_task_item_creation(self):
        task = TaskItem(description="Test task", priority=2)
        assert task.description == "Test task"
        assert not task.completed
        assert task.priority == 2
        assert task.completed_at is None
        task.complete()
        assert task.completed
        assert task.completed_at is not None
        task.reset()
        assert not task.completed
        assert task.completed_at is None
    def test_task_item_serialization(self):
        task = TaskItem(description="Test task", completed=True, priority=3, created_at=1234567890.0, completed_at=1234567900.0)
        data = task.to_dict()
        assert data["description"] == "Test task"
        assert data["completed"]
        assert data["priority"] == 3
        assert data["created_at"] == 1234567890.0
        assert data["completed_at"] == 1234567900.0
        restored_task = TaskItem.from_dict(data)
        assert restored_task.description == task.description
        assert restored_task.completed == task.completed
        assert restored_task.priority == task.priority
    @pytest.mark.asyncio
    async def test_update_task_list_empty(self, task_manager, cascade_context):
        result = await task_manager.update_task_list([], cascade_context)
        assert result["success"]
        assert "Updated 0 tasks" in result["message"]
        assert result["task_count"] == 0
        assert result["completed_count"] == 0
    @pytest.mark.asyncio
    async def test_update_task_list_new_tasks(self, task_manager, cascade_context):
        task_data = [
            {"description": "Task 1", "completed": False, "priority": 1},
            {"description": "Task 2", "completed": True, "priority": 2},
        ]
        result = await task_manager.update_task_list(task_data, cascade_context)
        assert result["success"]
        assert result["task_count"] == 2
        assert result["completed_count"] == 1
        assert len(task_manager.tasks) == 2
        assert task_manager.tasks[0].description == "Task 2"
        assert task_manager.tasks[0].completed
        assert task_manager.tasks[1].description == "Task 1"
        assert not task_manager.tasks[1].completed
    @pytest.mark.asyncio
    async def test_update_task_list_update_existing(self, task_manager, cascade_context):
        await task_manager.add_task("Existing task", priority=1)
        task_data = [
            {"description": "Existing task", "completed": True, "priority": 3},
        ]
        result = await task_manager.update_task_list(task_data, cascade_context)
        assert result["success"]
        assert result["task_count"] == 1
        assert result["completed_count"] == 1
        task = task_manager.tasks[0]
        assert task.description == "Existing task"
        assert task.completed
        assert task.priority == 3
    @pytest.mark.asyncio
    async def test_get_task_status(self, task_manager, cascade_context):
        await task_manager.add_task("Task 1", priority=1)
        await task_manager.add_task("Task 2", priority=2)
        await task_manager.complete_task("Task 2")
        status = await task_manager.get_task_status(cascade_context)
        assert status["total_tasks"] == 2
        assert status["completed_tasks"] == 1
        assert status["pending_tasks"] == 1
        assert status["completion_rate"] == 0.5
        assert len(status["tasks"]) == 2
    @pytest.mark.asyncio
    async def test_add_task(self, task_manager, cascade_context):
        result = await task_manager.add_task("New task", priority=2, cascade_context=cascade_context)
        assert result["success"]
        assert result["task"]["description"] == "New task"
        assert result["task"]["priority"] == 2
        assert len(task_manager.tasks) == 1
    @pytest.mark.asyncio
    async def test_add_duplicate_task(self, task_manager, cascade_context):
        await task_manager.add_task("Duplicate task")
        result = await task_manager.add_task("Duplicate task", cascade_context=cascade_context)
        assert not result["success"]
        assert "already exists" in result["error"]
    @pytest.mark.asyncio
    async def test_add_empty_task(self, task_manager, cascade_context):
        result = await task_manager.add_task("", cascade_context=cascade_context)
        assert not result["success"]
        assert "cannot be empty" in result["error"]
    @pytest.mark.asyncio
    async def test_complete_task(self, task_manager, cascade_context):
        await task_manager.add_task("Test task")
        result = await task_manager.complete_task("Test task", cascade_context)
        assert result["success"]
        assert task_manager.tasks[0].completed
        assert task_manager.tasks[0].completed_at is not None
    @pytest.mark.asyncio
    async def test_complete_nonexistent_task(self, task_manager, cascade_context):
        result = await task_manager.complete_task("Nonexistent", cascade_context)
        assert not result["success"]
        assert "not found" in result["error"]
    @pytest.mark.asyncio
    async def test_clear_completed_tasks(self, task_manager, cascade_context):
        await task_manager.add_task("Task 1")
        await task_manager.add_task("Task 2")
        await task_manager.complete_task("Task 1")
        result = await task_manager.clear_completed_tasks(cascade_context)
        assert result["success"]
        assert result["removed_count"] == 1
        assert result["remaining_tasks"] == 1
        assert len(task_manager.tasks) == 1
        assert task_manager.tasks[0].description == "Task 2"
    def test_task_persistence(self, tmp_path):
        tmp_path / ".pyagent_tasks.json"
        manager1 = MockTaskManagerMixin(_workspace_root=str(tmp_path))
        manager1.tasks = [
            TaskItem("Task 1", completed=True, priority=2),
            TaskItem("Task 2", completed=False, priority=1)
        ]
        manager1.update_task_list([t.to_dict() for t in manager1.tasks], CascadeContext(task_id="persist", agent_id="persist", workflow_id="persist"))
        manager2 = MockTaskManagerMixin(_workspace_root=str(tmp_path))
        assert len(manager2.tasks) == 2
        assert manager2.tasks[0].description == "Task 1"
        assert manager2.tasks[0].completed
        assert manager2.tasks[1].description == "Task 2"
        assert not manager2.tasks[1].completed
    @pytest.mark.asyncio
    async def test_task_limit(self, task_manager):
        task_manager.max_tasks = 3
        for i in range(5):
            await task_manager.add_task(f"Task {i}")
        assert len(task_manager.tasks) == 3
        assert task_manager.tasks[0].description == "Task 0"
        assert task_manager.tasks[1].description == "Task 1"
        assert task_manager.tasks[2].description == "Task 2"
