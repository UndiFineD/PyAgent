#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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

"""
FleetConsensusManager
Consensus management for the FleetManager.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.infrastructure.swarm.fleet.fleet_manager import FleetManager


class FleetConsensusManager:
    """Manages multi-agent consensus workflows."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    async def execute_with_consensus(
        self,
        task: str,
        primary_agent: str | None = None,
        secondary_agents: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        [Pillar 1: Swarm Consensus]
        Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner.
        Fully asynchronous implementation for v4.0.0.
        """
        logging.info(f"Fleet: Running consensus vote for task: {task[:50]}")

        # 1. Committee Formation
        judge = self.fleet.agents.get("ByzantineConsensusAgent") or self.fleet.agents.get("byzantine_judge")
        if not judge:
            return {"decision": "REJECTED", "reason": "ByzantineConsensusAgent not found."}

        if not primary_agent or not secondary_agents:
            available = [a for a in self.fleet.agents.keys() if a not in ["ByzantineConsensusAgent", "FleetManager"]]
            committee = judge.select_committee(task, available)
            if not committee:
                return {"decision": "REJECTED", "reason": "Committee formation failed."}
            primary_agent = committee[0]
            secondary_agents = committee[1:]

        # 2. Parallel Proposal Generation
        all_agents = [primary_agent] + (secondary_agents or [])
        proposals: dict[str, str] = {}

        tasks = []
        for agent_name in all_agents:
            if not agent_name:
                continue
            agent = self.fleet.agents.get(agent_name)
            if agent:
                # We assume 'improve_content' or similar primary action exists
                action = getattr(agent, "improve_content", None) or getattr(agent, "run_task", None)
                if action:
                    tasks.append((agent_name, action(task)))

        # Wait for all proposals in parallel
        for agent_name, coro in tasks:
            if not agent_name:
                continue
            try:
                res = await coro
                if isinstance(res, dict):
                    content = res.get("result") or res.get("content") or str(res)
                else:
                    content = str(res)
                proposals[agent_name] = content
            except (asyncio.TimeoutError, asyncio.CancelledError, RuntimeError) as e:
                logging.error(f"Fleet Consensus: Agent {agent_name} proposal error: {e}")

        if not proposals:
            return {"decision": "REJECTED", "reason": "No valid proposals gathered."}

        # 3. [Phase 3.0] Multi-surgeon BFT Audit
        # Selection of 'surgeons' (agents with security/audit skills)
        surgeons = [a for a in all_agents if a and ("security" in a.lower() or "audit" in a.lower())]
        if not surgeons and judge:
            # Fallback to general practitioners if no specialists available
            surgeons = (secondary_agents or [])[:2]

        audit_report = self.fleet.agents.get("ByzantineConsensusAgent").core.run_multi_surgeon_audit(
            proposals, surgeons
        )

        # 4. Byzantine Vote with Audit Weights
        result = await judge.run_committee_vote(task, proposals, audit_results=audit_report)

        # Broadcast lesson via Federated Knowledge
        if result["decision"] == "ACCEPTED" and getattr(self.fleet, "federated_knowledge", None):
            try:
                # Phase 319: Federated Knowledge is now async (Voyager)
                asyncio.create_task(
                    self.fleet.federated_knowledge.broadcast_lesson(
                        lesson_id=f"consensus_{int(time.time())}",
                        lesson_data={
                            "agent": result.get("winner"),
                            "task_type": "high_integrity_code",
                            "success": True,
                            "fix": f"Consensus reached by {result.get('winner')} for {task[:30]}",
                        },
                    )
                )
            except Exception:  # pylint: disable=broad-exception-caught
                logging.warning("FleetConsensus: Failed to trigger federated broadcast")

        return result
