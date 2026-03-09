from swarm.memory import SharedMemory, AgentMemory


def test_shared_memory_put_get() -> None:
    """Putting a value in SharedMemory and then getting it should return the same value."""
    mem = SharedMemory()
    assert mem.get("key") is None
    mem.put("key", "value")
    assert mem.get("key") == "value"
    # overwrite
    mem.put("key", 123)
    assert mem.get("key") == 123


def test_agent_memory_independence() -> None:
    """Two AgentMemory instances should not interfere with each other's data."""
    a1 = AgentMemory("agent1")
    a2 = AgentMemory("agent2")
    assert a1.get("foo") is None
    assert a2.get("foo") is None
    a1.set("foo", "bar")
    assert a1.get("foo") == "bar"
    assert a2.get("foo") is None
