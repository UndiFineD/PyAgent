#!/usr/bin/env python3

from __future__ import annotations
import logging
import json
from typing import Dict, List, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.infrastructure.fleet.FleetManager import FleetManager

class ConsensusOrchestrator:
    """
    Advanced orchestrator for resolving conflicts between agents using weighted voting
    and a multi-turn debate system.
    """
    
    def __init__(self, fleet: FleetManager) -> None:
        self.fleet = fleet
        self.reputation_scores: Dict[str, float] = {} # Agent name -> score (0.0 to 1.0)

    def resolve_conflict(self, task: str, agents: List[str]) -> str:
        """
        Orchestrates a debate and weighted vote to reach consensus on a task.
        """
        logging.info(f"ConsensusOrchestrator: Resolving conflict for task: {task} using {agents}")
        
        # 1. Gather initial proposals
        proposals = self._collect_proposals(task, agents)
        
        # 2. Conduct Debate (if needed)
        if len(proposals) > 1:
            proposals = self._conduct_debate(task, proposals)
            
        # 3. Weighted Voting
        final_decision = self._weighted_vote(proposals)
        
        # 4. Phase 55: DBFT Block Verification
        self.verify_state_block(task, final_decision)
        
        return final_decision

    def verify_state_block(self, task: str, decision: str) -> None:
        """
        Phase 55: Distributed Byzantine Fault Tolerance (DBFT).
        Simulates signing a state block after consensus to ensure data integrity
        across a distributed agent network.
        """
        import hashlib
        block_content = f"{task}:{decision}"
        block_hash = hashlib.sha256(block_content.encode()).hexdigest()
        
        logging.info(f"DBFT: State Block Signed. Hash: {block_hash}")
        
        # Broadcast to Inter-Fleet Bridge for cross-fleet sync
        if hasattr(self.fleet, 'inter_fleet_bridge'):
            self.fleet.inter_fleet_bridge.broadcast_signal(
                "CONSENSUS_CRYPTO_VERIFIED", 
                {"task": task, "hash": block_hash}
            )

    def _collect_proposals(self, task: str, agents: List[str]) -> List[Dict[str, Any]]:
        proposals = []
        for agent_name in agents:
            try:
                # Call agent to generate a solution
                res = self.fleet.call_by_capability(f"{agent_name}.process", task=task)
                proposals.append({
                    "agent": agent_name,
                    "content": res,
                    "weight": self.reputation_scores.get(agent_name, 0.5)
                })
            except Exception as e:
                logging.error(f"Agent {agent_name} failed to propose: {e}")
        return proposals

    def _conduct_debate(self, task: str, proposals: List[Dict[str, Any]], rounds: int = 2) -> List[Dict[str, Any]]:
        """
        Agents review each other's proposals and refine their own.
        """
        current_proposals = proposals
        for r in range(rounds):
            logging.info(f"ConsensusOrchestrator: Debate Round {r+1}")
            new_proposals = []
            for i, p in enumerate(current_proposals):
                competitors = [cp for j, cp in enumerate(current_proposals) if i != j]
                context = f"Task: {task}\nYour Proposal: {p['content']}\nOther Proposals: {[cp['content'] for cp in competitors]}"
                
                try:
                    # Agent critiques and improves its own proposal based on others
                    refined = self.fleet.call_by_capability(f"{p['agent']}.refine", context=context)
                    new_proposals.append({
                        "agent": p["agent"],
                        "content": refined,
                        "weight": p["weight"]
                    })
                except Exception:
                    new_proposals.append(p)
            current_proposals = new_proposals
        return current_proposals

    def _weighted_vote(self, proposals: List[Dict[str, Any]]) -> str:
        if not proposals:
            return "Consensus failed: No proposals."
            
        # For simplicity in this implementation, we pick the one with highest weight.
        # In a real system, we'd use semantic similarity to group proposals and sum weights.
        best_proposal = max(proposals, key=lambda x: x["weight"])
        logging.info(f"Consensus reached. Winner: {best_proposal['agent']} with weight {best_proposal['weight']}")
        return best_proposal["content"]

    def update_reputation(self, agent_name: str, feedback_score: float) -> None:
        """
        Updates agent reputation based on external feedback (0.0 to 1.0).
        """
        current = self.reputation_scores.get(agent_name, 0.5)
        # Moving average update
        self.reputation_scores[agent_name] = (current * 0.7) + (feedback_score * 0.3)
