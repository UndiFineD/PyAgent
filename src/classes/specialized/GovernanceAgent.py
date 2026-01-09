#!/usr/bin/env python3

"""GovernanceAgent for PyAgent.
Specializes in multi-agent proposal deliberation, voting, and fleet-wide policy management.
Follows Decentralized Autonomous Organization (DAO) principles for agent swarms.
"""

import logging
import json
import uuid
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.classes.base_agent import BaseAgent
from src.classes.base_agent.utilities import as_tool

class GovernanceAgent(BaseAgent):
    """Manages proposals, voting cycles, and governance policies for the fleet."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.proposals_dir = Path("agent_store/governance/proposals")
        self.proposals_dir.mkdir(parents=True, exist_ok=True)
        self.policies_path = Path("agent_store/governance/policies.json")
        self._system_prompt = (
            "You are the Governance Agent. Your role is to oversee the democratic processes "
            "of the fleet. You manage proposals for resource allocation, task prioritization, "
            "and model upgrades. You ensure that all votes are counted and policies are archived."
        )

    @as_tool
    def submit_proposal(self, title: str, description: str, creator: str, options: List[str] = None) -> str:
        """Submits a new governance proposal for the fleet.
        
        Args:
            title: Title of the proposal.
            description: Detailed description of the requested change/action.
            creator: Name of the agent or user submitting the proposal.
            options: List of choices for the vote (default is ['Approve', 'Reject']).
        """
        proposal_id = str(uuid.uuid4())[:8]
        proposal = {
            "id": proposal_id,
            "title": title,
            "description": description,
            "creator": creator,
            "options": options or ["Approve", "Reject"],
            "status": "active",
            "votes": {opt: [] for opt in (options or ["Approve", "Reject"])},
            "created_at": time.time()
        }
        
        path = self.proposals_dir / f"{proposal_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(proposal, f, indent=4)
        
        logging.info(f"Governance: New proposal submitted: {title} ({proposal_id})")
        return proposal_id

    @as_tool
    def cast_vote(self, proposal_id: str, voter: str, choice: str, rationale: str = "") -> str:
        """Casts a vote on an active proposal.
        
        Args:
            proposal_id: ID of the proposal to vote on.
            voter: Name of the agent casting the vote.
            choice: The selected option.
            rationale: Brief explanation for the vote.
        """
        path = self.proposals_dir / f"{proposal_id}.json"
        if not path.exists():
            return f"Error: Proposal {proposal_id} not found."
            
        with open(path, "r", encoding="utf-8") as f:
            proposal = json.load(f)
            
        if proposal["status"] != "active":
            return f"Error: Proposal {proposal_id} is no longer active."
            
        if choice not in proposal["votes"]:
            return f"Error: Invalid choice '{choice}'. Valid: {list(proposal['votes'].keys())}"
            
        # Check if already voted
        for opt in proposal["votes"]:
            for v in proposal["votes"][opt]:
                if v["agent"] == voter:
                    return f"Error: Agent {voter} has already voted on this proposal."
        
        proposal["votes"][choice].append({
            "agent": voter,
            "rationale": rationale,
            "timestamp": time.time()
        })
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(proposal, f, indent=4)
            
        return f"Vote cast by {voter} on proposal {proposal_id}."

    @as_tool
    def close_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """Closes a proposal and calculates the results."""
        path = self.proposals_dir / f"{proposal_id}.json"
        if not path.exists():
            return {"error": "Proposal not found"}
            
        with open(path, "r", encoding="utf-8") as f:
            proposal = json.load(f)
            
        proposal["status"] = "closed"
        
        # Calculate winner
        tallies = {opt: len(proposal["votes"][opt]) for opt in proposal["votes"]}
        winner = max(tallies, key=tallies.get)
        proposal["result"] = {
            "winner": winner,
            "tallies": tallies
        }
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(proposal, f, indent=4)
            
        return proposal

    def improve_content(self, input_text: str) -> str:
        return "Decentralized governance ensures fleet resilience and alignment."

if __name__ == "__main__":
    from src.classes.base_agent.utilities import create_main_function
    main = create_main_function(GovernanceAgent, "Governance Agent", "Swarm DAO Management")
    main()
