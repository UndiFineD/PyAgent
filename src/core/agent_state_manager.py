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

"""In-memory state manager for agent lifecycle tracking."""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Any


@dataclass(slots=True)
class AgentState:
    """State snapshot for a single agent.

    Args:
        status: Current lifecycle status for the agent.
        updated_at: Unix timestamp of the last state update.
        metadata: Optional state metadata.

    """

    status: str
    updated_at: float
    metadata: dict[str, Any]


class AgentStateManager:
    """Manage in-memory state for multiple agents.

    The manager intentionally keeps a simple dictionary-backed implementation
    to provide deterministic behavior for CLI and lightweight runtime flows.
    """

    def __init__(self) -> None:
        """Initialize an empty state store."""
        self._states: dict[str, AgentState] = {}

    def upsert(self, agent_id: str, status: str, metadata: dict[str, Any] | None = None) -> None:
        """Create or update state for an agent.

        Args:
            agent_id: Stable agent identifier.
            status: New state label.
            metadata: Optional metadata attached to the state.

        Raises:
            ValueError: If agent_id or status are blank.

        """
        normalized_agent_id = agent_id.strip()
        normalized_status = status.strip()
        if not normalized_agent_id:
            raise ValueError("agent_id must not be blank")
        if not normalized_status:
            raise ValueError("status must not be blank")

        self._states[normalized_agent_id] = AgentState(
            status=normalized_status,
            updated_at=time(),
            metadata=dict(metadata or {}),
        )

    def get(self, agent_id: str) -> AgentState | None:
        """Get current state for an agent.

        Args:
            agent_id: Stable agent identifier.

        Returns:
            The current AgentState, or None when not present.

        """
        return self._states.get(agent_id)

    def remove(self, agent_id: str) -> bool:
        """Remove state for an agent.

        Args:
            agent_id: Stable agent identifier.

        Returns:
            True when an existing state was removed, otherwise False.

        """
        return self._states.pop(agent_id, None) is not None

    def count(self) -> int:
        """Return the number of tracked agents.

        Returns:
            Number of agent state entries.

        """
        return len(self._states)


def validate() -> None:
    """Validate core state manager behavior.

    Raises:
        RuntimeError: If basic state manager operations fail.

    """
    manager = AgentStateManager()
    manager.upsert("agent-1", "running", {"kind": "worker"})

    state = manager.get("agent-1")
    if state is None or state.status != "running":
        raise RuntimeError("agent state upsert/get failed")
    if state.metadata.get("kind") != "worker":
        raise RuntimeError("agent state metadata roundtrip failed")

    if manager.count() != 1:
        raise RuntimeError("agent count tracking failed")

    if not manager.remove("agent-1"):
        raise RuntimeError("agent state removal failed")
