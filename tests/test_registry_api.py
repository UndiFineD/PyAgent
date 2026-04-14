#!/usr/bin/env python3
"""Test the AgentRegistry API using FastAPI's TestClient."""

from typing import cast

import pytest

# skip the entire module if FastAPI cannot be imported (pydantic mismatch).
try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
except SystemError as e:
    pytest.skip(f"Skipping registry API tests due to FastAPI import error: {e}", allow_module_level=True)

from src.swarm.agent_registry import AgentRegistry

# small FastAPI app for testing
app = FastAPI()
registry = AgentRegistry()


@app.post("/register")
def register_agent(info: dict[str, object]) -> dict[str, object]:
    """In a real implementation, you'd want to validate the input and handle errors appropriately."""
    # AgentRegistry.register expects agent_type parameter name
    # cast values pulled from untyped dict before passing to registry
    aid = registry.register(
        agent_type=cast(str, info["type"]),
        capabilities=cast(list[str], info.get("capabilities", [])),
    )
    return {"agent_id": aid}


@app.post("/heartbeat/{agent_id}")
def heartbeat(agent_id: str) -> dict[str, str]:
    """Handle heartbeat for an agent.

    In real code, consider returning a structured error if the ``agent_id``
    is unknown.
    """
    registry.heartbeat(agent_id)
    return {"status": "ok"}


@app.get("/agents/{agent_id}")
def get_agent(agent_id: str) -> dict[str, object]:
    """Return agent info for testing purposes.

    In a real implementation, exclude sensitive fields.
    """
    return cast(dict[str, object], registry.get(agent_id))


@app.get("/agents")
def list_agents() -> list[dict[str, object]]:
    """Return all agents for tests.

    Production code should page or limit this result.
    """
    return [{"agent_id": agent_id, **agent_info} for agent_id, agent_info in registry._agents.items()]


client = TestClient(app)


def test_registry_http_endpoints() -> None:
    """Test the basic HTTP endpoints of the AgentRegistry."""
    # register
    resp = client.post("/register", json={"type": "test", "capabilities": ["a"]})
    assert resp.status_code == 200
    data = resp.json()
    aid = data["agent_id"]
    assert isinstance(aid, str)

    # heartbeat
    resp = client.post(f"/heartbeat/{aid}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

    # get agent
    resp = client.get(f"/agents/{aid}")
    assert resp.status_code == 200
    agent = resp.json()
    assert agent["type"] == "test"

    # list agents
    resp = client.get("/agents")
    assert resp.status_code == 200
    agents = resp.json()
    assert any(agent["agent_id"] == aid for agent in agents)
