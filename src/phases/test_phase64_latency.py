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
Test Phase64 Latency module.
"""
# Tests for Phase 64: MoE Routing Latency Optimization

import pytest
import asyncio
import time
from src.infrastructure.swarm.orchestration.swarm.moe_gatekeeper import MoEGatekeeper
from src.infrastructure.engine.models.similarity import EmbeddingSimilarityService
from src.core.base.common.models.communication_models import ExpertProfile


@pytest.mark.asyncio
async def test_gatekeeper_caching():
    sim_service = EmbeddingSimilarityService()
    # Mock embedding with a small delay to simulate model latency
    original_get = sim_service.get_embedding

    call_count = 0

    async def slow_get(text):
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.05)
        return await original_get(text)

    sim_service.get_embedding = slow_get

    gatekeeper = MoEGatekeeper(sim_service)
    gatekeeper.register_expert(ExpertProfile(agent_id="e1", domains=["test"]))

    task = "Find the bug in this rust code"

    # First call: should be slow and increment call_count
    start = time.time()
    await gatekeeper.route_task(task)
    duration1 = time.time() - start
    assert call_count == 1

    # Second call: should be fast (cache hit) and NOT increment call_count
    start = time.time()
    await gatekeeper.route_task(task)
    duration2 = time.time() - start
    assert call_count == 1  # Still 1!
    assert duration2 < duration1


@pytest.mark.asyncio
async def test_gatekeeper_batch_routing():
    sim_service = EmbeddingSimilarityService()
    gatekeeper = MoEGatekeeper(sim_service)
    gatekeeper.register_expert(ExpertProfile(agent_id="e1", domains=["test"]))

    prompts = ["Task 1", "Task 2", "Task 3"]
    decisions = await gatekeeper.batch_route_tasks(prompts)

    assert len(decisions) == 3
    assert all(hasattr(d, "selected_experts") for d in decisions)
