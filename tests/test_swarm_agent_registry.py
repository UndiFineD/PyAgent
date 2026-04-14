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
"""Tests for AgentRegistry (prj0000022)."""

import time

from swarm.agent_registry import AgentRegistry


def test_register_returns_id():
    reg = AgentRegistry()
    aid = reg.register("coder", ["python", "rust"])
    assert aid.startswith("agent-")


def test_register_multiple_agents():
    reg = AgentRegistry()
    a1 = reg.register("coder", [])
    a2 = reg.register("tester", [])
    assert a1 != a2


def test_get_agent():
    reg = AgentRegistry()
    aid = reg.register("coder", ["python"])
    info = reg.get(aid)
    assert info["type"] == "coder"
    assert "python" in info["capabilities"]


def test_heartbeat_updates_timestamp():
    reg = AgentRegistry(heartbeat_interval=60.0)
    aid = reg.register("coder", [])
    old_ts = reg.get(aid)["last_seen"]
    time.sleep(0.01)
    reg.heartbeat(aid)
    new_ts = reg.get(aid)["last_seen"]
    assert new_ts > old_ts


def test_is_healthy_freshly_registered():
    reg = AgentRegistry(heartbeat_interval=60.0)
    aid = reg.register("coder", [])
    assert reg.is_healthy(aid) is True


def test_metrics_output():
    reg = AgentRegistry()
    reg.register("a", [])
    reg.register("b", [])
    metrics = reg.metrics()
    assert "agent_registered_total 2" in metrics
