import time
from typing import Any, Dict


class AgentRegistry:
    """Registry to manage agent registrations and heartbeats."""

    def __init__(self, heartbeat_interval: float = 30.0) -> None:
        self.heartbeat_interval = heartbeat_interval
        self._agents: Dict[str, Dict[str, Any]] = {}

    def register(self, agent_type: str, capabilities: list[str]) -> str:
        """Register a new agent and return its ID."""
        aid = f"agent-{len(self._agents)+1}"
        self._agents[aid] = {
            "type": agent_type,
            "capabilities": capabilities,
            "last_seen": time.time(),
        }
        return aid

    def heartbeat(self, agent_id: str) -> None:
        """Update the last seen time for the given agent ID."""
        self._agents[agent_id]["last_seen"] = time.time()

    def get(self, agent_id: str) -> dict[str, Any]:
        """Get the agent info for the given agent ID."""
        return self._agents[agent_id]

    def is_healthy(self, agent_id: str) -> bool:
        """Check if the agent is healthy based on its last heartbeat."""
        # this should return a bool in
        last = self._agents[agent_id]["last_seen"]
        return (time.time() - last) < self.heartbeat_interval

    # metrics implementation stub, to be used later
    def metrics(self) -> str:
        """Return a string in Prometheus text format with metrics about the agents."""
        # simple prometheus text output showing number of agents
        lines = [f"agent_registered_total {len(self._agents)}"]
        return "\n".join(lines)
