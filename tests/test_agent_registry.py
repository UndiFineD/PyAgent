import time

from swarm.agent_registry import AgentRegistry


def test_register_and_query() -> None:
    """Registering an agent and then querying it should return the correct information."""
    reg = AgentRegistry()
    agent_id = reg.register(agent_type="security", capabilities=["scan"])
    assert reg.get(agent_id)["type"] == "security"


def test_heartbeat_marks_healthy() -> None:
    """Sending a heartbeat for an agent should mark it as healthy."""
    reg = AgentRegistry()
    aid = reg.register(agent_type="coder", capabilities=[])
    reg.heartbeat(aid)
    assert reg.is_healthy(aid)


def test_missing_heartbeat_unhealthy() -> None:
    """If an agent misses its heartbeat, it should be marked as unhealthy."""
    reg = AgentRegistry(heartbeat_interval=1)
    aid = reg.register(agent_type="coder", capabilities=[])
    time.sleep(1.5)
    assert not reg.is_healthy(aid)
