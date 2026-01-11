#!/usr/bin/env python3

from __future__ import annotations
import logging
import uuid
from typing import Dict, List, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.infrastructure.fleet.FleetManager import FleetManager

class SubSwarm:
    """A lightweight sub-swarm with a subset of capabilities."""
    def __init__(self, swarm_id: str, agents: List[str], parent_fleet: FleetManager) -> None:
        self.swarm_id = swarm_id
        self.agents = agents
        self.fleet = parent_fleet
        self.task_log: List[str] = []

    def execute_mini_task(self, task: str) -> str:
        logging.info(f"SubSwarm {self.swarm_id}: Executing mini-task: {task}")
        if not self.agents:
            return "Error: Sub-swarm has no agents."
        
        # We try to find a tool that matches the requested agent/capability
        agent_name = self.agents[0]
        try:
            # We use call_by_capability with the agent name as the goal
            result = self.fleet.call_by_capability(agent_name, input_text=task, technical_report=task, user_query=task)
            self.task_log.append(task)
            return result
        except Exception as e:
            return f"SubSwarm execution failed: {e}"

class SubSwarmSpawner:
    """
    Implements Autonomous Sub-Swarm Spawning (Phase 33).
    Allows the fleet to spawn specialized mini-swarms for micro-tasks.
    """
    
    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.active_sub_swarms: Dict[str, SubSwarm] = {}

    def spawn_sub_swarm(self, capabilities: List[str]) -> str:
        """
        Creates a new sub-swarm based on requested capabilities or agent names.
        """
        swarm_id = f"swarm_{uuid.uuid4().hex[:8]}"
        logging.info(f"SubSwarmSpawner: Spawning sub-swarm {swarm_id} with {capabilities}")
        
        # In a real system, we'd filter fleet agents by capability
        # For now, we assume provide agent names
        new_swarm = SubSwarm(swarm_id, capabilities, self.fleet)
        self.active_sub_swarms[swarm_id] = new_swarm
        
        if hasattr(self.fleet, 'signals'):
            self.fleet.signals.emit("SUB_SWARM_SPAWNED", {
                "swarm_id": swarm_id,
                "agents": capabilities
            })
            
        return swarm_id

    def list_sub_swarms(self) -> List[str]:
        return list(self.active_sub_swarms.keys())

    def get_sub_swarm(self, swarm_id: str) -> Optional[SubSwarm]:
        return self.active_sub_swarms.get(swarm_id)
