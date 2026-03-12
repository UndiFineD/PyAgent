#!/usr/bin/env python3
"""Memory management for PyAgent."""
from typing import Any


class SharedMemory:
    """A simple in-memory key-value store for sharing data across agents."""

    def __init__(self) -> None:
        """Initialize the shared memory."""
        self._store: dict[Any, Any] = {}

    def put(self, k: Any, v: Any) -> None:
        """Store a value in the shared memory under the given key."""
        self._store[k] = v

    def get(self, k: Any) -> Any:
        """Retrieve a value from the shared memory by key, or None if not found."""
        return self._store.get(k)


class AgentMemory:
    """A simple in-memory key-value store for an individual agent's private memory."""

    def __init__(self, agent_id: str) -> None:
        """Initialize the agent memory with an identifier."""
        self.agent_id = agent_id
        self._local: dict[Any, Any] = {}

    def set(self, k: Any, v: Any) -> None:
        """Store a value in the agent's private memory under the given key."""
        self._local[k] = v

    def get(self, k: Any) -> Any:
        """Retrieve a value from the agent's private memory by key, or None if not found."""
        return self._local.get(k)
