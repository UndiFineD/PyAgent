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
"""Tests for SwarmMemory and SwarmNode (prj0000022)."""

import pytest

from swarm.memory_store import SwarmMemory
from swarm.swarm_node import SwarmNode


@pytest.mark.asyncio
async def test_shared_set_get():
    mem = SwarmMemory()
    await mem.shared_set("key", "value")
    assert await mem.shared_get("key") == "value"


@pytest.mark.asyncio
async def test_shared_get_default():
    mem = SwarmMemory()
    assert await mem.shared_get("missing", "default") == "default"


@pytest.mark.asyncio
async def test_local_set_get():
    mem = SwarmMemory()
    await mem.local_set("node1", "x", 42)
    assert await mem.local_get("node1", "x") == 42


@pytest.mark.asyncio
async def test_local_isolated_per_node():
    mem = SwarmMemory()
    await mem.local_set("node1", "x", 1)
    await mem.local_set("node2", "x", 2)
    assert await mem.local_get("node1", "x") == 1
    assert await mem.local_get("node2", "x") == 2


@pytest.mark.asyncio
async def test_shared_keys():
    mem = SwarmMemory()
    await mem.shared_set("a", 1)
    await mem.shared_set("b", 2)
    keys = await mem.shared_keys()
    assert set(keys) == {"a", "b"}


def test_memory_metrics():
    mem = SwarmMemory()
    m = mem.metrics()
    assert "swarm_memory_shared_keys" in m


@pytest.mark.asyncio
async def test_swarm_node_ping():
    node = SwarmNode("node-A")
    msg = await node.ping("node-B")
    assert msg["type"] == "ping"
    assert msg["source"] == "node-A"
    assert msg["destination"] == "node-B"


@pytest.mark.asyncio
async def test_swarm_node_pong_on_ping():
    node = SwarmNode("node-B")
    ping = await SwarmNode("node-A").ping("node-B")
    reply = await node.receive(ping)
    assert reply is not None
    assert reply["type"] == "pong"
    assert reply["destination"] == "node-A"


@pytest.mark.asyncio
async def test_swarm_node_process_one():
    sender = SwarmNode("sender")
    receiver = SwarmNode("receiver")
    ping = await sender.ping("receiver")
    await receiver.enqueue(ping)
    reply = await receiver.process_one()
    assert reply is not None
    assert reply["type"] == "pong"
