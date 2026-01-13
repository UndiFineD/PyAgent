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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Engine for Multi-agent 'Society of Mind' consensus protocols.
Agents vote on proposed solutions to ensure higher quality and redundancy.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Dict, List
from .ConsensusCore import ConsensusCore

__version__ = VERSION

class ConsensusEngine:
    """
    Manages voting and agreement between multiple agents.
    Shell for ConsensusCore.
    """
    
    def __init__(self, fleet_manager) -> None:
        self.fleet = fleet_manager
        self.core = ConsensusCore()
        self._votes: dict[str, list[str]] = {}

    def request_consensus(self, task: str, agent_names: list[str]) -> str:
        """Asks multiple agents for solutions and picks the best one by voting."""
        logging.info(f"CONSENSUS: Requesting agreement on '{task}' from {agent_names}")
        proposals: list[str] = []
        valid_agents: list[str] = []
        
        for name in agent_names:
            # Check registry
            agent = getattr(self.fleet.agents, name, None)
            if agent:
                try:
                    res = agent.improve_content(task)
                    proposals.append(res)
                    valid_agents.append(name)
                except Exception as e:
                    logging.error(f"Agent {name} failed during consensus: {e}")
        
        if not proposals:
            return "Consensus failed: No valid proposals received."
            
        # Phase 119: Inject weighted reliability scores
        weights = self.fleet.telemetry.get_reliability_weights(valid_agents)
        
        winner = self.core.calculate_winner(proposals, weights=weights)
        score = self.core.get_agreement_score(proposals, winner)
        
        logging.info(f"CONSENSUS: Multi-agent agreement reached (Score: {score:.2f}). Winner: {winner[:50]}...")
        return winner

    def get_consensus_report(self) -> str:
        """Summary of consensus activity."""
        return "Consensus Engine: Active and facilitating multi-agent protocols."