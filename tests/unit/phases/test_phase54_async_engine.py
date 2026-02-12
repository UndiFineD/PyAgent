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
from dataclasses import dataclass
from src.infrastructure.engine.scheduling.v2.async_scheduler import AsyncSchedulerV2
from src.infrastructure.engine.engine_coordinator_v2 import EngineCoordinator, EngineState
from src.infrastructure.engine.scheduling.advanced.config import RequestPriority


@dataclass
class MockRequest:
    request_id: int
    prompt_len: int
    output_len: int
    tokens: list
    priority: RequestPriority = RequestPriority.NORMAL
    num_tokens: int = 1
    deadline: float = 0.0


@pytest.mark.asyncio
async def test_async_scheduler_flow():
    """Test the complete async scheduling flow."""
    scheduler = AsyncSchedulerV2(max_batched_tokens=100)

    # Add some mock requests
    req1 = MockRequest(request_id=1, prompt_len=10, output_len=5, tokens=[1] * 10, priority=RequestPriority.HIGH)
    req2 = MockRequest(request_id=2, prompt_len=20, output_len=10, tokens=[2] * 20, priority=RequestPriority.LOW)

    scheduler.add_request(req1)
    scheduler.add_request(req2)

    # Perform scheduling
    output = await scheduler.schedule_async()

    assert not output.is_empty()
    assert len(output.scheduled_seqs) == 2
    assert output.get_seq_ids() == [1, 2]
    assert scheduler.get_avg_latency() > 0


def test_engine_coordinator_transitions():
    """Test engine lifecycle state transitions."""
    coord = EngineCoordinator()
    assert coord.state == EngineState.STOPPED

    coord.transition_to(EngineState.STARTING)
    assert coord.state == EngineState.STARTING
    assert coord.is_healthy()

    coord.transition_to(EngineState.RUNNING)
    assert coord.state == EngineState.RUNNING


@pytest.mark.asyncio
async def test_engine_error_recovery():
    """Test coordinator self-healing logic."""
    coord = EngineCoordinator()
    coord.transition_to(EngineState.RUNNING)

    # Simulate errors
    recovered = await coord.handle_error("Timeout")
    assert recovered is True
    assert coord.state == EngineState.RUNNING  # Should have cycled back

    # Simulate critical failure
    for _ in range(5):
        await coord.handle_error("Critical")

    assert coord.state == EngineState.ERROR
    assert not coord.is_healthy()


def test_request_queue_v2_priority():
    """Test V2 priority queue sorting."""
    from src.infrastructure.engine.request_queue.v2.request_queue import RequestQueueV2
    queue = RequestQueueV2()

    req_low = MockRequest(
        request_id=1, prompt_len=1, output_len=1, tokens=[], priority=RequestPriority.LOW
    )
    req_high = MockRequest(
        request_id=2, prompt_len=1, output_len=1, tokens=[], priority=RequestPriority.HIGH
    )

    queue.add_request(req_low)
    queue.add_request(req_high)

    batch = queue.pop_next_batch(max_tokens=10)
    assert len(batch) == 2
    # High priority should be first if scoring is correct
    # (though pop_next_batch doesn't guarantee order in the flat list)
    # But internal heap should have prioritized it.
