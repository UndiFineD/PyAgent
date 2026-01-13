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

from __future__ import annotations
from src.core.base.version import VERSION
import time
import uuid
from typing import Dict, List, Any
from src.logic.agents.swarm.core.AuctionCore import AuctionCore

__version__ = VERSION

class SwarmArbitratorAgent:
    """
    Phase 285: Swarm Arbitration with PBFT (Practical Byzantine Fault Tolerance).
    Manages consensus across multiple agents and tracks behavioral reputation.
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = workspace_path
        self.reputation_scores = {}
        self.consensus_threshold = 0.66  # 2n/3 for PBFT
        self.conflicts = []
        self.core = AuctionCore()
        
    async def arbitrate_consensus(self, votes: list[dict[str, Any]]) -> dict[str, Any]:
        """
        PBFT-inspired consensus logic.
        Requires at least 2/3 agreement to finalize a state change.
        """
        if not votes:
            return {"status": "error", "message": "No votes provided"}

        # Calculate frequency of each content hash
        vote_counts = {}
        for v in votes:
            h = v.get("hash", "unknown")
            vote_counts[h] = vote_counts.get(h, 0) + 1

        # Check for consensus (2f + 1)
        total_votes = len(votes)
        for h, count in vote_counts.items():
            if count / total_votes >= self.consensus_threshold:
                # Reward agents who voted with majority
                for v in votes:
                    agent_id = v.get("agent_id")
                    if v.get("hash") == h:
                        self._update_reputation(agent_id, 0.1)
                    else:
                        self._update_reputation(agent_id, -0.2)
                
                return {
                    "status": "success", 
                    "winner_hash": h, 
                    "confidence": round(count/total_votes, 2),
                    "voters": total_votes
                }

        # No consensus - trigger audit
        self.conflicts.append(votes)
        return {
            "status": "conflict", 
            "message": "PBFT Threshold not met. Consensus failed.",
            "distribution": vote_counts
        }

    def _update_reputation(self, agent_id: str, delta: float):
        if not agent_id: return
        self.reputation_scores[agent_id] = self.reputation_scores.get(agent_id, 1.0) + delta
        # Clamp between 0.0 (Malicious/Incompetent) and 2.0 (Highly Trusted)
        self.reputation_scores[agent_id] = max(0.0, min(2.0, self.reputation_scores[agent_id]))

    def get_reputation_report(self) -> dict[str, float]:
        """Returns the current reputation scores for all known agents."""
        return self.reputation_scores


        preempted = []
        for tid, entry in self.resource_ledger.items():
            if entry["status"] == "allocated" and entry["bid_price"] < min_bid:
                entry["status"] = "preempted"
                preempted.append(tid)
        return {"preempted_tasks": preempted, "count": len(preempted)}