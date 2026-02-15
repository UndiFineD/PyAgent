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


"""
Reading the repository to find governance_agent.py so the full file can be included verbatim in the module description.

governance_agent.py - GovernanceAgent for proposal deliberation, voting, and policy management

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate: agent = GovernanceAgent(__file__)
- Submit a proposal: agent.submit_proposal(title, description, creator, options=None)
- Cast a vote: agent.cast_vote(proposal_id, voter, choice, rationale="")
- Close a proposal and get results: agent.close_proposal(proposal_id)
- Lightweight async helper: await agent.improve_content(prompt, target_file=None)

WHAT IT DOES:
- Provides tools to submit proposals, record them to disk, and log metadata via the agent _record pipeline.
- Allows agents to cast votes with rationale, enforces one-vote-per-agent, persists votes, and records vote events.
- Closes proposals, tallies votes, determines a winner, and writes results back to the proposal artifact.
- Supplies a small async placeholder improve_content method and CLI entrypoint integration via create_main_function.

WHAT IT SHOULD DO BETTER:
- Add authentication/authorization and stronger identity verification for proposers and voters to prevent spoofing.
- Support quorum rules, weighted voting, vote delegation, and configurable voting windows/expiration times.
- Improve concurrency handling (file locks or transactional StateTransaction) to prevent race conditions on proposal files.
- Add unit tests for edge cases (tie handling, invalid inputs), and a policy migration/validation mechanism for policies.json.
- Replace bare filesystem persistence with the project's transactional StateTransaction abstraction and add schema validation for proposal artifacts.

FILE CONTENT SUMMARY:
GovernanceAgent for PyAgent.
Specializes in multi-agent proposal deliberation, voting, and fleet-wide policy management.
Follows Decentralized Autonomous Organization (DAO) principles for agent swarms.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class GovernanceAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Manages proposals, voting cycles, and governance policies for the fleet."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.proposals_dir = Path(self._workspace_root) / "data/memory/agent_store/governance/proposals"
        self.proposals_dir.mkdir(parents=True, exist_ok=True)
        self.policies_path = Path(self._workspace_root) / "data/memory/agent_store/governance/policies.json"
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

        proposal["votes"][choice].append({"agent": voter, "rationale": rationale, "timestamp": time.time()})

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

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        _ = (prompt, target_file)
        return "Decentralized governance ensures fleet resilience and alignment."


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(GovernanceAgent, "Governance Agent", "Swarm DAO Management")
    main()
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any

from src.core.base.common.base_utilities import as_tool
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class GovernanceAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """Manages proposals, voting cycles, and governance policies for the fleet."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.proposals_dir = Path(self._workspace_root) / "data/memory/agent_store/governance/proposals"
        self.proposals_dir.mkdir(parents=True, exist_ok=True)
        self.policies_path = Path(self._workspace_root) / "data/memory/agent_store/governance/policies.json"
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

        proposal["votes"][choice].append({"agent": voter, "rationale": rationale, "timestamp": time.time()})

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

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        _ = (prompt, target_file)
        return "Decentralized governance ensures fleet resilience and alignment."


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(GovernanceAgent, "Governance Agent", "Swarm DAO Management")
    main()
