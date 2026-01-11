#!/usr/bin/env python3

"""Engine for Multi-agent 'Society of Mind' consensus protocols.
Agents vote on proposed solutions to ensure higher quality and redundancy.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any, Optional
from .ConsensusCore import ConsensusCore

class ConsensusEngine:
    """
    Manages voting and agreement between multiple agents.
    Shell for ConsensusCore.
    """
    
    def __init__(self, fleet_manager) -> None:
        self.fleet = fleet_manager
        self.core = ConsensusCore()
        self._votes: Dict[str, List[str]] = {}

    def request_consensus(self, task: str, agent_names: List[str]) -> str:
        """Asks multiple agents for solutions and picks the best one by voting."""
        logging.info(f"CONSENSUS: Requesting agreement on '{task}' from {agent_names}")
        proposals: List[str] = []
        valid_agents: List[str] = []
        
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
