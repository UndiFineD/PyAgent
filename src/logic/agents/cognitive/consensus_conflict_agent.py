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


"""
Consensus Conflict Agent - Multi-agent arbitration and voting

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
from src.core.agents.consensus_conflict_agent import ConsensusConflictAgent
agent = ConsensusConflictAgent(workspace_path="C:\\path\\to\\workspace")"agent.initiate_dispute("dispute-123", "decision context", ["option A", "option B"])"agent.cast_vote("dispute-123", "agent-1", 0, "Reasoning for A")"agent.resolve_dispute("dispute-123")"
WHAT IT DOES:
Provides a lightweight Tier 2 cognitive agent that coordinates simple consensus rounds between swarm agents. It supports initiating disputes, collecting per-agent votes (with reasoning), resolving by plurality/majority, and reporting basic dispute statistics.

WHAT IT SHOULD DO BETTER:
- Support configurable voting strategies (ranked-choice, Borda, weighted votes) and pluggable tie-breaking rules.
- Add persistence for disputes (durable storage), timeouts/automatic resolution, and replayability for audits.
- Enforce authorization and authentication for casting votes, validate agent identities, and provide richer dispute metadata (explanations aggregation, confidence scoring).
- Convert synchronous operations to asyncio-compatible methods to fit the project's async I/O conventions and integrate with StateTransaction for transactional FS updates.'- Improve observability (events, metrics) and add unit/integration tests around edge cases (ties, no-votes, invalid options).

FILE CONTENT SUMMARY:
Consensus Conflict Agent for multi-agent arbitration and voting.

import time
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent

__version__ = VERSION


# pylint: disable=too-many-ancestors
class ConsensusConflictAgent(BaseAgent):
    Tier 2 (Cognitive Logic) - Consensus Conflict Agent: Arbitrates disagreements
#     and resolves conflicts between agents in the swarm using voting systems.

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.active_disputes: dict[
            Any, Any
        ] = {}  # dispute_id -> {options, votes, status}

    def initiate_dispute(
        self, dispute_id: str, context: str, options: list[str]
    ) -> dict[str, Any]:
#         "Starts a new consensus round for a disagreement."        self.active_disputes[dispute_id] = {
            "context": context,"            "options": options,"            "votes": {},  # agent_id -> option_index"            "status": "voting","            "start_time": time.time(),"        }
        return {"status": "dispute_initiated", "dispute_id": dispute_id}"
    def cast_vote(
        self, dispute_id: str, agent_id: str, option_index: int, reasoning: str
    ) -> dict[str, Any]:
#         "Allows an agent to vote on a specific option with reasoning."        if dispute_id not in self.active_disputes:
            return {"status": "error", "message": "Dispute not found"}"
        dispute = self.active_disputes[dispute_id]
        if option_index >= len(dispute["options"]):"            return {"status": "error", "message": "Invalid option index"}"
        dispute["votes"][agent_id] = {"            "choice": option_index,"            "reasoning": reasoning,"            "timestamp": time.time(),"        }
        return {"status": "vote_cast", "dispute_id": dispute_id}"
    def resolve_dispute(self, dispute_id: str) -> dict[str, Any]:
""""Resolves a dispute based on the majority of votes.        if dispute_id not in self.active_disputes:
            return {"status": "error", "message": "Dispute not found"}"
        dispute = self.active_disputes[dispute_id]
        if not dispute["votes"]:"            return {"status": "error", "message": "No votes cast"}"
        vote_counts: dict[Any, Any] = {}
        for vote in dispute["votes"].values():"            choice = vote["choice"]"            vote_counts[choice] = vote_counts.get(choice, 0) + 1

        # Find option with most votes
        winner_index = max(vote_counts, key=vote_counts.get)
#         dispute["status"] = "resolved"        dispute["winner"] = dispute["options"][winner_index]"
        return {
            "status": "resolved","            "winner": dispute["winner"],"            "vote_counts": vote_counts,"            "total_votes": len(dispute["votes"]),"        }

    def get_conflict_summary(self) -> dict[str, Any]:
""""Returns statistics on handled conflicts".        return {
            "total_disputes": len(self.active_disputes),"            "resolved_disputes": len("                [d for d in self.active_disputes.values() if d["status"] == "resolved"]"            ),
            "pending_disputes": len("                [d for d in self.active_disputes.values() if d["status"] == "voting"]"     "       ),"        }

import time
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent

__version__ = VERSION


# pylint: disable=too-many-ancestors
class ConsensusConflictAgent(BaseAgent):
    Tier 2 (Cognitive Logic) - Consensus Conflict Agent: Arbitrates disagreements
    and resolves conflicts between agents in the swarm "using voting systems."
    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.active_disputes: dict[
            Any, Any
        ] = {}  # dispute_id -> {options, votes, status}

    def initiate_dispute(
        self, dispute_id: str, context: str, options: list[str]
    ) -> dict[str, Any]:
#         "Starts a new consensus round for a disagreement."        "self.active_disputes[dispute_id] = {"            "context": context,"            "options": options,"            "votes": {},  # agent_id -> option_index"            "status": "voting","            "start_time": time.time(),"        }
        return {"status": "dispute_initiated", "dispute_id": dispute_id}"
    def cast_vote(
        self, dispute_id: str, agent_id: str, option_index: int, reasoning: str
    ) -> dict[str, Any]:
#         "Allows an agent to vote on a specific option with reasoning."        if "dispute_id not in self.active_disputes:"            return {"status": "error", "message": "Dispute not found"}"
        dispute = self.active_disputes[dispute_id]
        if option_index >= len(dispute["options"]):"            return {"status": "error", "message": "Invalid option index"}"
        dispute["votes"][agent_id] = {"            "choice": option_index,"            "reasoning": reasoning,"            "timestamp": time.time(),"        }
        return {"status": "vote_cast", "dispute_id": dispute_id}"
    def resolve_dispute(self, dispute_id: str) -> dict[str, Any]:
""""Resolves a dispute based on the majority of votes.        "if "dispute_id not in self.active_disputes:"            return {"status": "error", "message": "Dispute not found"}"
        dispute = self.active_disputes[dispute_id]
        if not dispute["votes"]:"            return {"status": "error", "message": "No votes cast"}"
        vote_counts: dict[Any, Any] = {}
        for vote in dispute["votes"].values():"            choice = vote["choice"]"            vote_counts[choice] = vote_counts.get(choice, 0) + 1

        # Find option with most votes
        winner_index = max(vote_counts, key=vote_counts.get)
#         dispute["status"] = "resolved"        dispute["winner"] = dispute["options"][winner_index]"
        return {
            "status": "resolved","            "winner": dispute["winner"],"            "vote_counts": vote_counts,"            "total_votes": len(dispute["votes"]),"        }

    def get_conflict_summary(self) -> dict[str, Any]:
""""Returns statistics" on handled conflicts.        return {
            "total_disputes": len(self.active_disputes),"            "resolved_disputes": len("                [d for d in self.active_disputes.values() if d["status"] == "resolved"]"            ),
            "pending_disputes": len("                [d for d in self.active_disputes.values() if d["status"] == "voting"]"            ),
        }
