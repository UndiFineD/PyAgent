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
"""Tests for the agents package (BaseAgent, AgentLifecycle, AgentManifest)."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from src.agents.BaseAgent import AgentLifecycle, AgentManifest, BaseAgent


# ---------------------------------------------------------------------------
# Minimal concrete agent for testing
# ---------------------------------------------------------------------------

class EchoAgent(BaseAgent):
    """A minimal concrete agent that echoes its task back as result."""

    async def run(self, task: dict[str, Any]) -> dict[str, Any]:
        return {"ok": True, "echo": task.get("payload")}


# ---------------------------------------------------------------------------
# Manifest tests
# ---------------------------------------------------------------------------

def test_manifest_defaults() -> None:
    m = AgentManifest(name="TestAgent")
    assert m.name == "TestAgent"
    assert m.version == "1.0.0"
    assert m.capabilities == []
    assert m.agent_id  # non-empty UUID


def test_manifest_custom_fields() -> None:
    m = AgentManifest(
        name="CoderAgent",
        version="2.0.0",
        description="Codes stuff",
        capabilities=["code_gen", "review"],
    )
    assert m.capabilities == ["code_gen", "review"]
    assert m.description == "Codes stuff"


# ---------------------------------------------------------------------------
# Lifecycle tests
# ---------------------------------------------------------------------------

def test_initial_state_is_idle() -> None:
    agent = EchoAgent()
    assert agent.state is AgentLifecycle.IDLE


def test_start_transitions_to_running() -> None:
    agent = EchoAgent()
    agent.start()
    assert agent.state is AgentLifecycle.RUNNING


def test_stop_transitions_to_stopped() -> None:
    agent = EchoAgent()
    agent.start()
    agent.stop()
    assert agent.state is AgentLifecycle.STOPPED


def test_reset_from_stopped_to_idle() -> None:
    agent = EchoAgent()
    agent.start()
    agent.stop()
    agent.reset()
    assert agent.state is AgentLifecycle.IDLE


def test_start_raises_if_already_running() -> None:
    agent = EchoAgent()
    agent.start()
    with pytest.raises(RuntimeError, match="Cannot start"):
        agent.start()


def test_reset_raises_if_running() -> None:
    agent = EchoAgent()
    agent.start()
    with pytest.raises(RuntimeError, match="Cannot reset a running agent"):
        agent.reset()


# ---------------------------------------------------------------------------
# Async dispatch tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_dispatch_echoes_payload() -> None:
    agent = EchoAgent()
    agent.start()
    result = await agent.dispatch({"payload": "hello"})
    assert result["ok"] is True
    assert result["echo"] == "hello"


@pytest.mark.asyncio
async def test_dispatch_raises_if_not_running() -> None:
    agent = EchoAgent()
    with pytest.raises(RuntimeError, match="not running"):
        await agent.dispatch({"payload": "oops"})


@pytest.mark.asyncio
async def test_dispatch_respects_max_concurrency() -> None:
    """With concurrency=1, tasks run sequentially."""
    order: list[int] = []

    class OrderedAgent(BaseAgent):
        async def run(self, task: dict[str, Any]) -> dict[str, Any]:
            idx = task["idx"]
            await asyncio.sleep(0.02)
            order.append(idx)
            return {"ok": True}

    agent = OrderedAgent(max_concurrency=1)
    agent.start()
    await asyncio.gather(
        agent.dispatch({"idx": 0}),
        agent.dispatch({"idx": 1}),
        agent.dispatch({"idx": 2}),
    )
    # With concurrency=1, order must be sequential 0→1→2
    assert order == [0, 1, 2]


# ---------------------------------------------------------------------------
# BaseAgent.validate
# ---------------------------------------------------------------------------

def test_validate_returns_true() -> None:
    assert BaseAgent.validate() is True


# ---------------------------------------------------------------------------
# Repr
# ---------------------------------------------------------------------------

def test_repr_contains_name() -> None:
    agent = EchoAgent(AgentManifest(name="EchoAgent"))
    r = repr(agent)
    assert "EchoAgent" in r
    assert "IDLE" in r
