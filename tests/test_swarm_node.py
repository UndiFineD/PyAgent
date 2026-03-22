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

"""Tests for SwarmNode ping/pong connectivity."""

from __future__ import annotations

import asyncio

import pytest

from swarm.swarm_node import SwarmNode


@pytest.mark.asyncio
async def test_ping_pong_exchange() -> None:
    """Two SwarmNode instances connect and successfully exchange a ping/pong."""
    node1 = SwarmNode(node_id="node-1")
    node2 = SwarmNode(node_id="node-2")

    await node1.start()
    await node2.start()

    host, port = node1.address
    _, writer = await node2.connect(host, port)

    await node2.ping(writer)

    # node1 should receive the ping, auto-reply with pong;
    # node2's _read_loop queues the pong into node2.received
    pong = await asyncio.wait_for(node2.received.get(), timeout=2.0)
    assert pong["type"] == "pong"
    assert pong["from"] == "node-1"
    assert pong["to"] == "node-2"

    writer.close()
    await node1.stop()
    await node2.stop()


@pytest.mark.asyncio
async def test_node_receives_ping_on_server_side() -> None:
    """The server node queues the incoming ping in its received queue."""
    server = SwarmNode(node_id="server")
    client = SwarmNode(node_id="client")

    await server.start()
    host, port = server.address
    _, writer = await client.connect(host, port)

    await client.ping(writer)

    # Give a moment for the server coroutine to process the message
    ping_msg = await asyncio.wait_for(server.received.get(), timeout=2.0)
    assert ping_msg["type"] == "ping"
    assert ping_msg["from"] == "client"

    writer.close()
    await server.stop()
    await client.stop()
