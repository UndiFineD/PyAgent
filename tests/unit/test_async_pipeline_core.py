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

import pytest
import asyncio
import pytest_asyncio
from unittest.mock import AsyncMock
from src.core.base.logic.async_pipeline_core import (
    AsyncPipelineCore,
    PipelineConfig,
    PipelineTask,
    TaskStatus,
    TaskPriority
)


class TestAsyncPipelineCore:
    """Test cases for AsyncPipelineCore"""

    @pytest_asyncio.fixture
    async def pipeline(self):
        """Create AsyncPipelineCore instance"""
        config = PipelineConfig(max_concurrent_tasks=5, max_queue_size=50)
        pipeline = AsyncPipelineCore(config)
        await pipeline.start()
        yield pipeline
        await pipeline.stop()

    @pytest.fixture
    def sample_task(self):
        """Create a sample task"""
        return PipelineTask(
            task_id="test_task_1",
            name="Test Task",
            priority=TaskPriority.NORMAL,
            metadata={'task_type': 'test'}
        )

    @pytest.mark.asyncio
    async def test_pipeline_initialization(self, pipeline):
        """Test pipeline initialization"""
        assert pipeline.config.max_concurrent_tasks == 5
        assert pipeline.config.max_queue_size == 50
        assert len(pipeline.tasks) == 0
        assert len(pipeline.running_tasks) == 0

    @pytest.mark.asyncio
    async def test_register_handler(self, pipeline):
        """Test handler registration"""
        async def dummy_handler(task):
            return "success"

        pipeline.register_handler("test", dummy_handler)
        assert "test" in pipeline.task_handlers

    @pytest.mark.asyncio
    async def test_submit_task(self, pipeline, sample_task):
        """Test task submission"""
        task_id = await pipeline.submit_task(sample_task)
        assert task_id == "test_task_1"
        assert task_id in pipeline.tasks
        assert pipeline.tasks[task_id].status == TaskStatus.PENDING

    @pytest.mark.asyncio
    async def test_submit_duplicate_task(self, pipeline, sample_task):
        """Test submitting duplicate task raises error"""
        await pipeline.submit_task(sample_task)

        with pytest.raises(ValueError, match="already exists"):
            await pipeline.submit_task(sample_task)

    @pytest.mark.asyncio
    async def test_task_execution_success(self, pipeline):
        """Test successful task execution"""
        # Register handler
        async def success_handler(task):
            await asyncio.sleep(0.1)  # Simulate work
            return "success_result"

        pipeline.register_handler("test", success_handler)

        # Submit task
        task = PipelineTask(
            task_id="success_task",
            name="Success Task",
            metadata={'task_type': 'test'}
        )
        await pipeline.submit_task(task)

        # Wait for completion
        completed_task = await pipeline.wait_for_task("success_task", timeout=5.0)

        assert completed_task.status == TaskStatus.COMPLETED
        assert completed_task.result == "success_result"
        assert completed_task.error is None
        assert completed_task.started_at is not None
        assert completed_task.completed_at is not None

    @pytest.mark.asyncio
    async def test_task_execution_failure(self, pipeline):
        """Test task execution failure"""
        # Register failing handler
        async def failing_handler(task):
            await asyncio.sleep(0.1)
            raise ValueError("Task failed")

        pipeline.register_handler("test", failing_handler)

        # Submit task
        task = PipelineTask(
            task_id="fail_task",
            name="Fail Task",
            metadata={'task_type': 'test'},
            max_retries=0
        )
        await pipeline.submit_task(task)

        # Wait for completion
        completed_task = await pipeline.wait_for_task("fail_task", timeout=5.0)

        assert completed_task.status == TaskStatus.FAILED
        assert completed_task.error == "Task failed"
        assert completed_task.result is None

    @pytest.mark.asyncio
    async def test_task_retry_logic(self, pipeline):
        """Test task retry on failure"""
        call_count = 0

        async def failing_handler(task):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError(f"Attempt {call_count} failed")
            return "success"

        pipeline.register_handler("test", failing_handler)

        # Submit task with retry
        task = PipelineTask(
            task_id="retry_task",
            name="Retry Task",
            max_retries=3,
            metadata={'task_type': 'test'}
        )
        await pipeline.submit_task(task)

        # Wait for completion
        completed_task = await pipeline.wait_for_task("retry_task", timeout=10.0)

        assert completed_task.status == TaskStatus.COMPLETED
        assert completed_task.result == "success"
        assert completed_task.retry_count == 2  # Failed twice before success

    @pytest.mark.asyncio
    async def test_task_dependencies(self, pipeline):
        """Test task dependency resolution"""
        results = []

        async def handler(task):
            results.append(task.task_id)
            return f"result_{task.task_id}"

        pipeline.register_handler("test", handler)

        # Create dependent tasks
        task1 = PipelineTask(
            task_id="dep_task_1",
            name="Dependency Task 1",
            metadata={'task_type': 'test'}
        )

        task2 = PipelineTask(
            task_id="dep_task_2",
            name="Dependency Task 2",
            dependencies=["dep_task_1"],
            metadata={'task_type': 'test'}
        )

        # Submit tasks
        await pipeline.submit_task(task1)
        await pipeline.submit_task(task2)

        # Wait for both to complete
        completed = await pipeline.wait_for_all(["dep_task_1", "dep_task_2"], timeout=10.0)

        assert len(completed) == 2
        assert all(task.status == TaskStatus.COMPLETED for task in completed)

        # Task 1 should complete before task 2
        assert results[0] == "dep_task_1"
        assert results[1] == "dep_task_2"

    @pytest.mark.asyncio
    async def test_task_timeout(self, pipeline):
        """Test task timeout"""
        async def slow_handler(task):
            await asyncio.sleep(10)  # Much longer than timeout
            return "should_not_reach"

        pipeline.register_handler("test", slow_handler)

        # Configure short timeout
        pipeline.config.task_timeout = 0.5

        task = PipelineTask(
            task_id="timeout_task",
            name="Timeout Task",
            metadata={'task_type': 'test'},
            max_retries=0
        )
        await pipeline.submit_task(task)

        completed_task = await pipeline.wait_for_task("timeout_task", timeout=5.0)

        assert completed_task.status == TaskStatus.FAILED
        assert "timed out" in completed_task.error.lower()

    @pytest.mark.asyncio
    async def test_batch_submission(self, pipeline):
        """Test batch task submission"""
        async def handler(task):
            return f"result_{task.task_id}"

        pipeline.register_handler("test", handler)

        # Create batch of tasks
        tasks = [
            PipelineTask(
                task_id=f"batch_task_{i}",
                name=f"Batch Task {i}",
                metadata={'task_type': 'test'}
            )
            for i in range(5)
        ]

        # Submit batch
        task_ids = await pipeline.submit_batch(tasks)

        assert len(task_ids) == 5
        assert all(task_id in pipeline.tasks for task_id in task_ids)

        # Wait for all to complete
        completed = await pipeline.wait_for_all(task_ids, timeout=10.0)

        assert len(completed) == 5
        assert all(task.status == TaskStatus.COMPLETED for task in completed)

    @pytest.mark.asyncio
    async def test_priority_queue(self, pipeline):
        """Test task priority ordering"""
        execution_order = []

        async def handler(task):
            execution_order.append(task.task_id)
            await asyncio.sleep(0.1)  # Small delay to ensure ordering
            return "done"

        pipeline.register_handler("test", handler)

        # Create tasks with different priorities
        tasks = [
            PipelineTask(
                task_id="low_priority",
                name="Low Priority",
                priority=TaskPriority.LOW,
                metadata={'task_type': 'test'}
            ),
            PipelineTask(
                task_id="high_priority",
                name="High Priority",
                priority=TaskPriority.HIGH,
                metadata={'task_type': 'test'}
            ),
            PipelineTask(
                task_id="critical_priority",
                name="Critical Priority",
                priority=TaskPriority.CRITICAL,
                metadata={'task_type': 'test'}
            )
        ]

        # Submit tasks
        for task in tasks:
            await pipeline.submit_task(task)

        # Wait for all to complete
        await pipeline.wait_for_all([t.task_id for t in tasks], timeout=10.0)

        # Critical should execute first, then high, then low
        assert execution_order[0] == "critical_priority"
        assert execution_order[1] == "high_priority"
        assert execution_order[2] == "low_priority"

    @pytest.mark.asyncio
    async def test_convenience_methods(self, pipeline):
        """Test convenience methods for coding tasks"""
        async def code_handler(task):
            return f"executed_{task.metadata.get('code', 'unknown')}"

        async def test_handler(task):
            return f"tested_{task.metadata.get('code', 'unknown')}"

        pipeline.register_handler("execute_code", code_handler)
        pipeline.register_handler("run_tests", test_handler)

        # Test code task
        code_task_id = await pipeline.submit_code_task(
            "Compile service",
            "print('hello')",
            task_type="execute_code"
        )

        # Test test task
        test_task_id = await pipeline.submit_test_task(
            "Run unit tests",
            "pytest tests/"
        )

        # Wait for completion
        code_result = await pipeline.wait_for_task(code_task_id)
        test_result = await pipeline.wait_for_task(test_task_id)

        assert code_result.status == TaskStatus.COMPLETED
        assert test_result.status == TaskStatus.COMPLETED
        assert code_result.result == "executed_print('hello')"
        assert test_result.result == "tested_pytest tests/"

    def test_task_status_queries(self, pipeline):
        """Test task status query methods"""
        # Initially empty
        assert len(pipeline.get_pending_tasks()) == 0
        assert len(pipeline.get_running_tasks()) == 0
        assert len(pipeline.get_completed_tasks()) == 0

        # Add some tasks
        task1 = PipelineTask(task_id="query_task_1", name="Query Task 1")
        task2 = PipelineTask(task_id="query_task_2", name="Query Task 2")

        # Manually add to test queries (normally done via submit_task)
        pipeline.tasks["query_task_1"] = task1
        pipeline.tasks["query_task_2"] = task2

        assert len(pipeline.get_pending_tasks()) == 2
        assert len(pipeline.get_running_tasks()) == 0
        assert len(pipeline.get_completed_tasks()) == 0

        # Change status
        task1.status = TaskStatus.RUNNING
        task2.status = TaskStatus.COMPLETED

        assert len(pipeline.get_pending_tasks()) == 0
        assert len(pipeline.get_running_tasks()) == 1
        assert len(pipeline.get_completed_tasks()) == 1
