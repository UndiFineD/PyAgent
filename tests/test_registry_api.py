from fastapi import FastAPI
from fastapi.testclient import TestClient
from swarm.agent_registry import AgentRegistry


# small FastAPI app for testing
app = FastAPI()
registry = AgentRegistry()


@app.post("/register")
def register_agent(info: dict):
    """In a real implementation, you'd want to validate the input and handle errors appropriately."""
    # AgentRegistry.register expects agent_type parameter name
    aid = registry.register(agent_type=info["type"], capabilities=info.get("capabilities", []))
    return {"agent_id": aid}


@app.post("/heartbeat/{agent_id}")
def heartbeat(agent_id: str):
    """In a real implementation, you'd likely want to handle the case where the agent_id is not found and return an appropriate error response."""
    registry.heartbeat(agent_id)
    return {"status": "ok"}


@app.get("/agents/{agent_id}")
def get_agent(agent_id: str):
    """Return agent info for testing purposes. In a real implementation, you'd likely want to exclude sensitive info."""
    return registry.get(agent_id)


@app.get("/agents")
def list_agents():
    """For testing purposes, we return the full registry here. In a real implementation, you'd likely want to paginate or limit this."""
    return registry._agents


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
    assert aid in resp.json()
