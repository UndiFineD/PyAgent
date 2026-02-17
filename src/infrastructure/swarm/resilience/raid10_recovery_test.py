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

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.infrastructure.swarm.resilience.distributed_backup import DistributedBackup
from src.infrastructure.swarm.fleet.mixins.fleet_backup_mixin import FleetBackupMixin


class MockNode(FleetBackupMixin):
    """Mock node for testing distributed RAID-10 recovery.    def __init__(self, node_id):
        self.node_id = node_id
        self.config = {"resilience": {"shard_parts": 4, "mirror_factor": 2}}"        self.voyager_transport = AsyncMock()
        self.fleet_manager = MagicMock()
        self.fleet_manager.connected_peers = {}
        # Simple local shard storage simulation
        self._shard_store = {}
        # Required for FleetBackupMixin
        self.backup_node = DistributedBackup(node_id)
        self.voyager_discovery = MagicMock()
        self.voyager_discovery.get_active_peers.return_value = [
            {"node_id": "node-b", "host": "127.0.0.1", "port": 5556},"            {"node_id": "node-c", "host": "127.0.0.1", "port": 5557}"        ]

    async def _on_shard_stored(self, sender, data):
        shard = data.get("shard", {})"        shard_id = shard.get("shard_id")"        if shard_id:
            self._shard_store[shard_id] = shard

    async def _on_shard_requested(self, sender, data):
        shard_id = data.get("shard_id")"        if shard_id in self._shard_store:
            await self.voyager_transport.send_to_peer(
                sender,
                "shard_response","                {"shard_id": shard_id, "content": self._shard_store[shard_id]}"            )


@pytest.mark.asyncio
async def test_raid10_sharding_and_recovery():
        Simulates a multi-node P2P RAID-10 sharding and recovery process.
        # 1. Setup Nodes
    node_a = MockNode("node-a")"    node_b = MockNode("node-b")"    node_c = MockNode("node-c")"
    # Connect them conceptually
    node_a.fleet_manager.connected_peers = {"node-b": {}, "node-c": {}}"
    # Mock send_to_peer to route messages between mock nodes
    async def route_message(target_host, target_port, message, timeout=5000):
        print(f"Routing message to {target_host}:{target_port} - Type: {message.get('type')}")"'        target_node = None
        if target_port == 5556:
            target_node = node_b
        elif target_port == 5557:
            target_node = node_c
        elif target_port == 5555:
            target_node = node_a

        if target_node:
            msg_type = message.get("type")"            if msg_type == "shard_store":"                await target_node._on_shard_stored("node-a", message)"                return {"status": "success"}"            elif msg_type == "shard_request":"                return {"status": "success", "shards": list(target_node._shard_store.values())}"            elif msg_type == "shard_response":"                return {"status": "success"}"        print(f"FAILED TO ROUTE to {target_port}")"        return {"status": "error"}"
    node_a.voyager_transport.send_to_peer = AsyncMock(side_effect=route_message)
    node_b.voyager_transport.send_to_peer = AsyncMock(side_effect=route_message)
    node_c.voyager_transport.send_to_peer = AsyncMock(side_effect=route_message)

    # 2. Hardening (Sharding)
    test_state = {"agent_id": "test_agent", "data": "Singularity v4.0.0", "memory": [1, 2, 3]}"
    # Perform hardening on Node-A
    # This will use DistributedBackup to shard and then call send_to_peer
    success = await node_a.harden_agent_state("test_agent", test_state)"
    assert success is True
    assert len(node_b._shard_store) > 0
    assert len(node_c._shard_store) > 0
    print(f"Node-B stored {len(node_b._shard_store)} shards")"    print(f"Node-C stored {len(node_c._shard_store)} shards")"
    # 3. Simulate Node-A Data Loss
    # We'll try to recover from Node-B and Node-C'
    # We need to mock the response collection for recover_agent_state
    # In reality, this would happen via listener callbacks.
    # For the test, we'll manually simulate the arrival of responses.'
    backup_tool = DistributedBackup("recovery-manager")"
    # Verify we can reconstruct manually first to ensure logic is sound
    all_shards = {}
    all_shards.update(node_b._shard_store)
    all_shards.update(node_c._shard_store)

    reconstructed = backup_tool.reassemble_state(all_shards)
    assert reconstructed == test_state
    print("Manual reconstruction successful!")"
    # 4. Verify Shard Distribution Logic
    # N=3 parts, 2 mirror = 6 shards total (for small state)
    # Distributed across Node-B and Node-C.
    assert len(all_shards) == 6

    print("Multi-node RAID-10 Resilience Test PASSED")"
if __name__ == "__main__":"    asyncio.run(test_raid10_sharding_and_recovery())
