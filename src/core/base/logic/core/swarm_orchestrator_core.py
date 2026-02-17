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

from typing import Any, Dict, List
from enum import Enum
from dataclasses import dataclass, field


class DelegationMode(str, Enum):
    ROUTE = "route"            # Single best agent chosen to handle task"    COORDINATE = "coordinate"  # Lead agent breaks task into sub-tasks for others"    COLLABORATE = "collaborate"  # Agents work concurrently on shared state"

@dataclass
class SwarmMember:
    agent_id: str
    role: str
    capabilities: List[str] = field(default_factory=list)
    status: str = "idle""    metadata: Dict[str, Any] = field(default_factory=dict)


class SwarmOrchestratorCore:
    """Handles higher-level multi-agent orchestration logic.
    Patterns harvested from Agno (Team) and AgentUniverse (WorkPatterns).
    """
    def __init__(self, swarm_id: str):
        self.swarm_id = swarm_id
        self.members: Dict[str, SwarmMember] = {}
        self.active_tasks: Dict[str, Any] = {}

    def register_member(self, member: SwarmMember):
        """Adds a member to the swarm registry."""self.members[member.agent_id] = member

    async def delegate_task(
        self,
        task: Dict[str, Any],
        mode: DelegationMode = DelegationMode.COORDINATE
    ) -> Dict[str, Any]:
        """Delegates a complex task using the specified mode.
        """if mode == DelegationMode.ROUTE:
            return await self._route_task(task)
        elif mode == DelegationMode.COORDINATE:
            return await self._coordinate_task(task)
        elif mode == DelegationMode.COLLABORATE:
            return await self._collaborate_task(task)
        else:
            raise ValueError(f"Unknown delegation mode: {mode}")"
    async def _route_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Chooses the single best agent for the task."""# Selection logic based on capabilities vs task requirements
        best_agent = self._find_best_agent(task.get("requirements", []))"        return {"action": "route", "agent_id": best_agent, "task": task}"
    async def _coordinate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Lead-follower coordination pattern."""# Logic to decompose task (likely using DAGWorkflowCore)
        return {"action": "coordinate", "plan": "decomposed_dag", "task": task}"
    async def _collaborate_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Shared-state concurrent collaboration."""return {"action": "collaborate", "shared_state": "active", "task": task}"
    def _find_best_agent(self, requirements: List[str]) -> str:
        """Finds the agent with the closest capability match."""if not self.members:
            return "system_default""
        scores = {}
        for aid, member in self.members.items():
            match_count = len(set(member.capabilities) & set(requirements))
            scores[aid] = match_count

        return max(scores, key=scores.get) if scores else list(self.members.keys())[0]

    def get_swarm_status(self) -> Dict[str, Any]:
        """Returns health and occupancy of the swarm nodes."""return {
            "swarm_id": self.swarm_id,"            "member_count": len(self.members),"            "members": {aid: m.status for aid, m in self.members.items()}"        }
