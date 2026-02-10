
"""
Fleet delegation mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class FleetDelegationMixin:
    """Mixin for agent delegation logic in FleetManager."""

    async def delegate_to(self: FleetManager, agent_type: str, prompt: str, target_file: str | None = None) -> str:
        """Synaptic Delegation: Hands off a sub-task to a specialized agent or Universal Shard."""
        logging.info(f"Fleet: Delegating {agent_type} (Target: {target_file})")

        # Step 1: Check existing specialized agents
        if agent_type in self.agents:
            sub_agent = self.agents[agent_type]
            res = sub_agent.improve_content(prompt, target_file=target_file)
            import asyncio
            if asyncio.iscoroutine(res):
                return await res
            return res

        # Step 2: Swarm Singularity - Check for Universal Shard Manifest
        manifest = self.manifest_repo.get_manifest(agent_type)
        if manifest:
            from src.core.base.lifecycle.base_agent import BaseAgent
            # Instantiate a Universal Agent shell with the manifest
            universal_agent = BaseAgent(manifest=manifest.__dict__)
            await universal_agent.setup()
            
            # Execute task using the new cognitive loop
            task_result = await universal_agent.run_task({
                "context": prompt,
                "target_file": target_file
            })
            return str(task_result)

        raise KeyError(f"Agent or Manifest '{agent_type}' not found in Fleet.")
