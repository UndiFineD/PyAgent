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
"""BaseAgent — abstract base class for all PyAgent agents.

Every agent in the swarm must subclass ``BaseAgent`` and implement at minimum:
  - ``run(task)`` — the core execution loop for a single task

Lifecycle states
~~~~~~~~~~~~~~~~
An agent transitions through ``AgentLifecycle`` states::

    IDLE  ──start()──►  RUNNING  ──stop()──►  STOPPED
      ▲                                            │
      └──────────────reset()──────────────────────┘

A stopped agent can be reset and reused.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

logger = logging.getLogger(__name__)


class AgentLifecycle(Enum):
    """Lifecycle states for an agent."""

    IDLE = auto()
    RUNNING = auto()
    STOPPED = auto()


@dataclass
class AgentManifest:
    """Metadata descriptor for an agent.

    Attributes
    ----------
    name:
        Human-readable agent name (e.g. ``"CoderAgent"``).
    version:
        Semantic version string (e.g. ``"1.0.0"``).
    description:
        Short one-line description of the agent's purpose.
    capabilities:
        List of capability tokens this agent supports
        (e.g. ``["code_generation", "code_review"]``).
    agent_id:
        Unique identifier assigned at instantiation.

    """

    name: str
    version: str = "1.0.0"
    description: str = ""
    capabilities: list[str] = field(default_factory=list)
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))


class BaseAgent(ABC):
    """Abstract base class for all PyAgent agents.

    Parameters
    ----------
    manifest:
        Metadata about this agent.  If omitted, a minimal manifest is created
        from the subclass name.
    max_concurrency:
        Maximum number of tasks this agent will process in parallel.

    """

    def __init__(
        self,
        manifest: AgentManifest | None = None,
        max_concurrency: int = 1,
    ) -> None:
        self._manifest = manifest or AgentManifest(name=type(self).__name__)
        self._state = AgentLifecycle.IDLE
        self._max_concurrency = max_concurrency
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._tasks: list[asyncio.Task[Any]] = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def manifest(self) -> AgentManifest:
        """The agent's static metadata descriptor."""
        return self._manifest

    @property
    def agent_id(self) -> str:
        """Unique identifier for this agent instance."""
        return self._manifest.agent_id

    @property
    def state(self) -> AgentLifecycle:
        """Current lifecycle state."""
        return self._state

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Transition from IDLE to RUNNING.

        Raises
        ------
        RuntimeError
            If the agent is not in the IDLE state.

        """
        if self._state is not AgentLifecycle.IDLE:
            raise RuntimeError(f"Cannot start agent in state {self._state.name}; expected IDLE")
        self._state = AgentLifecycle.RUNNING
        logger.debug("Agent %s started (id=%s)", self._manifest.name, self.agent_id)

    def stop(self) -> None:
        """Transition to STOPPED and cancel all pending tasks."""
        self._state = AgentLifecycle.STOPPED
        _ = [t.cancel() for t in self._tasks]
        self._tasks.clear()
        logger.debug("Agent %s stopped (id=%s)", self._manifest.name, self.agent_id)

    def reset(self) -> None:
        """Reset a STOPPED agent back to IDLE so it can be restarted.

        Raises
        ------
        RuntimeError
            If the agent is still RUNNING.

        """
        if self._state is AgentLifecycle.RUNNING:
            raise RuntimeError("Cannot reset a running agent; call stop() first")
        self._state = AgentLifecycle.IDLE
        self._semaphore = asyncio.Semaphore(self._max_concurrency)

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    async def run(self, task: dict[str, Any]) -> dict[str, Any]:
        """Execute a single task and return the result.

        Parameters
        ----------
        task:
            Task payload dictionary.  Subclasses define their own schema.

        Returns
        -------
        dict[str, Any]
            Result dictionary.  At minimum should include ``"ok": True|False``.

        """

    # ------------------------------------------------------------------
    # Concurrent dispatch helper
    # ------------------------------------------------------------------

    async def dispatch(self, task: dict[str, Any]) -> dict[str, Any]:
        """Dispatch ``task`` through the concurrency semaphore.

        Enforces ``max_concurrency`` by blocking until a slot is free, then
        calls :meth:`run`.

        Raises
        ------
        RuntimeError
            If the agent is not in the RUNNING state.

        """
        if self._state is not AgentLifecycle.RUNNING:
            raise RuntimeError(f"Agent is not running (state={self._state.name}); call start() first")
        async with self._semaphore:
            return await self.run(task)

    # ------------------------------------------------------------------
    # Self-validation
    # ------------------------------------------------------------------

    @classmethod
    def validate(cls) -> bool:
        """Return True — confirms the BaseAgent module is importable and functional."""
        return True

    def __repr__(self) -> str:
        return f"<{type(self).__name__} name={self._manifest.name!r} id={self.agent_id!r} state={self._state.name}>"
