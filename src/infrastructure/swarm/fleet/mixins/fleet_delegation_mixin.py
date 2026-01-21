# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
from typing import Any, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager

class FleetDelegationMixin:
    """Mixin for agent delegation logic in FleetManager."""

    async def delegate_to(
        self: FleetManager, agent_type: str, prompt: str, target_file: str | None = None
    ) -> str:
        """Synaptic Delegation: Hands off a sub-task to a specialized agent."""
        logging.info(f"Fleet: Delegating {agent_type} (Target: {target_file})")

        if agent_type in self.agents:
            sub_agent = self.agents[agent_type]

            # Execute via improve_content or similar primary entrypoint
            # We pass target_file explicitly to avoid mutating shared state (Phase 317)
            res = sub_agent.improve_content(prompt, target_file=target_file)
            import asyncio
            if asyncio.iscoroutine(res):
                return await res
            return res

        raise KeyError(f"Agent '{agent_type}' not found in Fleet.")
