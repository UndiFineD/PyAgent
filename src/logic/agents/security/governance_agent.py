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


"""GovernanceAgent for PyAgent.
Specializes in multi-agent proposal deliberation, voting, and fleet-wide policy management.
Follows Decentralized Autonomous Organization (DAO) principles for agent swarms.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
import json
import uuid
import time
from pathlib import Path
from typing import Any
from src.core.base.base_agent import BaseAgent
from src.core.base.base_utilities import as_tool

__version__ = VERSION


class GovernanceAgent(BaseAgent):
    """Manages proposals, voting cycles, and governance policies for the fleet."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.proposals_dir = Path("data/memory/agent_store/governance/proposals")
        self.proposals_dir.mkdir(parents=True, exist_ok=True)
        self.policies_path = Path("data/memory/agent_store/governance/policies.json")
        self._system_prompt = (
            "You are the Governance Agent. Your role is to oversee the democratic processes "
            "of the fleet. You manage proposals for resource allocation, task prioritization, "
            "and model upgrades. You ensure that all votes are counted and policies are archived."
        )

    @as_tool
    def submit_proposal(
        self,
        title: str,
        description: str,
        creator: str,
        options: list[str] | None = None,
    ) -> str:
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
            "created_at": time.time(),
        }

        path = self.proposals_dir / f"{proposal_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(proposal, f, indent=4)

        # Phase 108: Intelligence Recording
        self._record(
            description,
            proposal_id,
            provider="Governance",
            model="ProposalSubmission",
            meta={"title": title, "creator": creator},
        )

        logging.info(f"Governance: New proposal submitted: {title} ({proposal_id})")
        return proposal_id

    @as_tool
    def cast_vote(
        self, proposal_id: str, voter: str, choice: str, rationale: str = ""
    ) -> str:
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

        with open(path, encoding="utf-8") as f:
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

        proposal["votes"][choice].append(
            {"agent": voter, "rationale": rationale, "timestamp": time.time()}
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(proposal, f, indent=4)

        # Phase 108: Intelligence Recording
        self._record(
            f"{voter} voted {choice} on {proposal_id}",
            rationale,
            provider="Governance",
            model="Vote",
            meta={"proposal_id": proposal_id},
        )

        return f"Vote cast by {voter} on proposal {proposal_id}."

    @as_tool
    def close_proposal(self, proposal_id: str) -> dict[str, Any]:
        """Closes a proposal and calculates the results."""
        path = self.proposals_dir / f"{proposal_id}.json"
        if not path.exists():
            return {"error": "Proposal not found"}

        with open(path, encoding="utf-8") as f:
            proposal = json.load(f)

        proposal["status"] = "closed"

        # Calculate winner

        tallies = {opt: len(proposal["votes"][opt]) for opt in proposal["votes"]}
        winner = max(tallies, key=tallies.get)
        proposal["result"] = {"winner": winner, "tallies": tallies}

        with open(path, "w", encoding="utf-8") as f:
            json.dump(proposal, f, indent=4)

        return proposal

    def improve_content(self, input_text: str) -> str:
        return "Decentralized governance ensures fleet resilience and alignment."


if __name__ == "__main__":
    from src.core.base.base_utilities import create_main_function

    main = create_main_function(
        GovernanceAgent, "Governance Agent", "Swarm DAO Management"
    )
    main()
