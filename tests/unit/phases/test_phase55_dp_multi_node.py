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
Test DP Multi-Node.
"""

import pytest
from src.infrastructure.swarm.distributed.v2.dp_coordinator import DPCoordinatorV2
from src.infrastructure.swarm.distributed.v2.dp_engine_sync import DPEngineSync
from src.infrastructure.swarm.distributed.v2.multi_node_executor import MultiNodeExecutor
from src.infrastructure.swarm.distributed.v2.load_balancer_client import LoadBalancerClient


@pytest.mark.asyncio
async def test_dp_coordinator_zmq():
    """Test ZMQ-based DP coordination stubs."""
    master = DPCoordinatorV2(port=5566, is_master=True)
    worker = DPCoordinatorV2(port=5566, is_master=False)

    # In a real test we'd perform actual ZMQ exchange, but here we test the class structure
    assert master.is_master is True
    assert worker.is_master is False

    master.rank_stats[0] = {"latency": 0.1, "throughput": 1000}
    stats = master.aggregate_stats()
    assert stats["avg_latency"] == 0.1
    assert stats["total_throughput"] == 1000

    await master.close()
    await worker.close()


def test_dp_engine_sync():
    """Test wave synchronization logic."""
    sync = DPEngineSync(rank=0, world_size=4)
    assert sync.all_ready() is False

    for i in range(4):
        sync.mark_ready(i)

    assert sync.all_ready() is True

    sync.reset_ready()
    assert sync.all_ready() is False


def test_multi_node_executor_split():
    """Test cross-node tensor split calculation."""
    executor = MultiNodeExecutor(node_id=0, total_nodes=2)
    shape = (1, 12, 4096)

    splits = executor.coordinate_tp_split(shape)
    assert len(splits) == 2
    # Rust implementation returns lists in the dict values, verify value content regardless of container type
    assert list(splits[0]) == [1, 12, 2048]
    assert list(splits[1]) == [1, 12, 2048]


def test_load_balancer_p2c():
    """Test Power of Two Choices load balancing selection."""
    lb = LoadBalancerClient(endpoint_ranks=[0, 1, 2, 3])

    # Simulate heavy load on rank 0
    lb.update_rank_stats(0, load=0.96, latency=0.5)
    lb.update_rank_stats(1, load=0.1, latency=0.01)

    # P2C should ideally select the lower load if 0 and 1 are picked
    # Since it's random, we just check it returns a valid rank
    rank = lb.select_rank_p2c()
    assert rank in [0, 1, 2, 3]

    health = lb.get_health_map()
    assert health[0] == "CONGESTED"
    assert health[1] == "OK"
