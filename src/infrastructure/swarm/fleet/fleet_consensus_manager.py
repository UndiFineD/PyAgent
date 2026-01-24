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

"""Consensus management for the FleetManager."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .FleetManager import FleetManager


class FleetConsensusManager:
    """Manages multi-agent consensus workflows."""

    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet

    def execute_with_consensus(
        self,
        task: str,
        primary_agent: str | None = None,
        secondary_agents: list[str] | None = None,
    ) -> dict[str, Any]:
        """Executes a task across multiple agents and uses ByzantineConsensusAgent to pick the winner."""
        logging.info(f"Fleet: Running consensus vote for task: {task[:50]}")

        # Dynamic Committee Formation
        if not primary_agent or not secondary_agents:
            available = list(set(list(self.fleet.agents.registry_configs.keys()) + list(self.fleet.agents.keys())))
            available = [
                a for a in available if a not in ["ByzantineConsensus", "ByzantineConsensusAgent", "FleetManager"]
            ]

            judge = getattr(self.fleet, "ByzantineConsensus", None)
            if not judge:
                for name in ["byzantine_judge", "ByzantineConsensusAgent"]:
                    judge = getattr(self.fleet, name, None)
                    if judge:
                        break

            if not judge:
                return {
                    "decision": "REJECTED",
                    "reason": "ByzantineConsensus agent not available.",
                }

            committee = judge.select_committee(task, available)
            if not committee:
                return {
                    "decision": "REJECTED",
                    "reason": "No committee could be formed.",
                }
            primary_agent = committee[0]
            secondary_agents = committee[1:]
            logging.info(f"Fleet: Formed dynamic committee: {primary_agent}, {secondary_agents}")

        proposals: dict[str, str] = {}
        all_agents = [primary_agent] + secondary_agents

        for agent_name in all_agents:
            if agent_name in self.fleet.agents:
                try:
                    res = self.fleet.agents[agent_name].improve_content(task)
                    proposals[agent_name] = res
                except Exception as e:
                    logging.error(f"Fleet: Agent {agent_name} failed to provide consensus proposal: {e}")

        if not proposals:
            return {
                "decision": "REJECTED",
                "reason": "No agents could provide proposals.",
            }

        # Run the committee vote
        if "judge" not in locals():
            judge = getattr(self.fleet, "ByzantineConsensus", None)

        if not judge:
            return {
                "decision": "REJECTED",
                "reason": "ByzantineConsensus not found for voting.",
            }

        result = judge.run_committee_vote(task, proposals)

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
            except Exception as e:
                logging.warning(f"FleetConsensus: Failed to trigger federated broadcast: {e}")

        return result
