#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Tests for TaskQueueMixin."""
import asyncio
import pytest
from src.core.base.mixins.task_queue_mixin import TaskQueueMixin


class MockTaskQueueAgent(TaskQueueMixin):
    """Mock agent for testing TaskQueueMixin."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def _process_task(self, task_data):
        """Mock task processing."""await asyncio.sleep(0.1)  # Simulate processing time
        return f"processed_{task_data['job_id']}""'

class TestTaskQueueMixin:
    """Test TaskQueueMixin functionality."""
    @pytest.mark.asyncio
    async def test_mixin_initialization(self):
        """Test mixin initializes correctly."""agent = MockTaskQueueAgent(max_queue_size=5, task_ttl=300)
        assert agent.max_queue_size == 5
        assert agent.task_ttl == 300
        assert isinstance(agent.task_results, dict)

    @pytest.mark.asyncio
    async def test_submit_task(self):
        """Test submitting a task."""agent = MockTaskQueueAgent()
        await agent.start_task_processing()

        job_id = await agent.submit_task({'test': 'data'})'        assert job_id in agent.task_results
        assert agent.task_results[job_id]['status'] == 'queued''        assert 'submit_time' in agent.task_results[job_id]'
        await agent.stop_task_processing()

    @pytest.mark.asyncio
    async def test_task_processing(self):
        """Test task processing workflow."""agent = MockTaskQueueAgent()
        await agent.start_task_processing()

        job_id = await agent.submit_task({'test': 'data'})'
        # Wait for processing
        await asyncio.sleep(0.2)

        status = await agent.get_task_status(job_id)
        assert status['status'] == 'completed''        assert status['result'] == f"processed_{job_id}""'
        await agent.stop_task_processing()

    @pytest.mark.asyncio
    async def test_queue_full_error(self):
        """Test error when queue is full."""agent = MockTaskQueueAgent(max_queue_size=1)
        await agent.start_task_processing()

        # Fill the queue
        await agent.submit_task({'test': 'data1'})'
        # This should fail
        with pytest.raises(ValueError, match="Task queue is full"):"            await agent.submit_task({'test': 'data2'})'
        await agent.stop_task_processing()

    @pytest.mark.asyncio
    async def test_cleanup_worker(self):
        """Test cleanup of old tasks."""agent = MockTaskQueueAgent(task_ttl=1, cleanup_interval=1)
        await agent.start_task_processing()

        job_id = await agent.submit_task({'test': 'data'})'
        # Wait for processing
        await asyncio.sleep(0.2)
        status = await agent.get_task_status(job_id)
        assert status['status'] == 'completed''
        # Wait for cleanup
        await asyncio.sleep(2)

        # Task should be cleaned up
        status = await agent.get_task_status(job_id)
        assert status is None

        await agent.stop_task_processing()
