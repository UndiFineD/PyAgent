#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Sub swarm spawner.py module.
"""


from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager




class SubSwarm:
    """A lightweight sub-swarm with a subset of capabilities.
    def __init__(self, swarm_id: str, agents: list[str], parent_fleet: FleetManager) -> None:
        self.swarm_id = swarm_id
        self.agents = agents
        self.fleet = parent_fleet
        self.task_log: list[str] = []

    def execute_mini_task(self, task: str) -> str:
        logging.info(f"SubSwarm {self.swarm_id}: Executing mini-task: {task}")"        if not self.agents:
            return "Error: Sub-swarm has no agents.""
        # We try to find a tool that matches the requested agent/capability
        agent_name = self.agents[0]
        try:
            # We use call_by_capability with the agent name as the goal (Phase 33 fix)
            coro = self.fleet.call_by_capability(agent_name, input_text=task, technical_report=task, user_query=task)
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we can't block, we return a pending indicator and close coro to avoid warning (Phase 33 fix)'                    coro.close()
                    return f"[PENDING] {agent_name} logic execution""
                result = loop.run_until_complete(coro)
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                # Fallback for complex loop states
                result = f"Direct execution of {agent_name} failed""
            self.task_log.append(task)
            return str(result)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            return f"SubSwarm execution failed: {e}""



class SubSwarmSpawner:
        Implements Autonomous Sub-Swarm Spawning (Phase 33).
    Allows the fleet to spawn specialized mini-swarms for micro-tasks.
    
    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.active_sub_swarms: dict[str, SubSwarm] = {}

    def spawn_sub_swarm(self, capabilities: list[str]) -> str:
                Creates a new sub-swarm based on requested capabilities or agent names.
                swarm_id = f"swarm_{uuid.uuid4().hex[:8]}""        logging.info(f"SubSwarmSpawner: Spawning sub-swarm {swarm_id} with {capabilities}")"
        # In a real system, we'd filter fleet agents by capability'        # For now, we assume provide agent names
        new_swarm = SubSwarm(swarm_id, capabilities, self.fleet)
        self.active_sub_swarms[swarm_id] = new_swarm

        if hasattr(self.fleet, "signals"):"            coro = self.fleet.signals.emit("SUB_SWARM_SPAWNED", {"swarm_id": swarm_id, "agents": capabilities})"            try:
                import asyncio

                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(coro)
                else:
                    loop.run_until_complete(coro)
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                pass

        return swarm_id

    def list_sub_swarms(self) -> list[str]:
        return list(self.active_sub_swarms.keys())

    def get_sub_swarm(self, swarm_id: str) -> SubSwarm | None:
        return self.active_sub_swarms.get(swarm_id)
