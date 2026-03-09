from swarm.agent_registry import AgentRegistry


def test_metrics_contains_agent_count():
    """The metrics output should include the total number of registered agents."""
    reg = AgentRegistry()
    reg.register(agent_type="x", capabilities=[])
    text = reg.metrics()
    assert "agent_registered_total" in text
