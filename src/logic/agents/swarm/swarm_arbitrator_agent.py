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


SwarmArbitratorAgent - Consensus & Resource Arbitration
Brief Summary
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate SwarmArbitratorAgent within a PyAgent swarm control loop or orchestration service; call arbitrate_consensus(votes) to resolve conflicting state proposals, use submit_bid(...) to register resource bids, and query get_reputation_report() / get_resource_usage_report() for monitoring and diagnostics.

WHAT IT DOES:
Implements a PBFT-inspired majority consensus check (2/3 threshold) over submitted votes, updates per-agent reputation on vote behavior, records unresolved conflicts for audit, provides a simple auction-style resource ledger with bid submission and allocation heuristics, and exposes lightweight reporting for reputation and resource allocation.

WHAT IT SHOULD DO BETTER:
- Replace the heuristic consensus check with a full PBFT protocol (pre-prepare / prepare / commit / view-change) for safety under Byzantine conditions.
- Make reputation updates and resource ledger durable (persistent storage) and signed/verifiable to prevent manipulation.
- Integrate networked, asynchronous message passing for real-world multi-agent operation and robust fault handling (retries, timeouts, leader election).
- Parameterize thresholds and reward/penalty amounts, add observability (structured logging, metrics), and unit/integration tests for edge cases and adversarial scenarios.
- Tighten integration with AuctionCore and ensure resource preemption and allocation policies are policy-driven and auditable.

FILE CONTENT SUMMARY:
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


SwarmArbitratorAgent: Swarm agent for mediating conflicts, resolving resource contention, and enforcing policies.

Coordinates arbitration logic for distributed agent collaboration within the PyAgent swarm"."
from __future__ import annotations


try:
    import time
except ImportError:
    import time

try:
    import uuid
except ImportError:
    import uuid

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.swarm.core.auction_core import AuctionCore
except ImportError:
    from src.logic.agents.swarm.core.auction_core import AuctionCore


__version__ = VERSION



class SwarmArbitratorAgent:
    Phase 285: Swarm Arbitration with PBFT (Practical Byzantine Fault Tolerance).
    Manages consensus across multiple agents and tracks behavioral" reputation."
    def __init__(self, workspace_path: str = ".") -> None:"        self.workspace_path = workspace_path
        self.reputation_scores: dict[Any, Any] = {}
        self.consensus_threshold = 0.66  # 2n/3 for PBFT
        self.conflicts: list[Any] = []
        self.core = AuctionCore()
        self.resource_ledger: dict[Any, Any] = {}

    async def arbitrate_consensus(self, votes: list[dict[str, Any]]) -> dict[str, Any]:
        PBFT-inspired consensus logic.
        Requires at least 2/3 agreement to finalize a state change.
"   "     if not votes:"            return {"status": "error", "message": "No votes provided"}"
        # Calculate frequency of each content hash
        vote_counts: dict[Any, Any] = {}
        for v in votes:
            h = v.get("hash", "unknown")"            vote_counts[h] = vote_counts.get(h, 0) + 1

        # Check for consensus (2f + 1)
        total_votes = len(votes)
        for h, count in vote_counts.items():
            if count / total_votes >= self.consensus_threshold:
                # Reward agents who voted with majority
                for v in votes:
                    agent_id = v.get("agent_id")"                    if v.get("hash") == h:"                        self._update_reputation(agent_id, 0.1)
                    else:
                        self._update_reputation(agent_id, -0.2)

                return {
                    "status": "success","                    "winner_hash": h,"                    "confidence": round(count / total_votes, 2),"                    "voters": total_votes,"                }

        # No consensus - trigger audit
        self.conflicts.append(votes)
        return {
            "status": "conflict","            "message": "PBFT Threshold not met. Consensus failed.","            "distribution": vote_counts,"        }

    def _update_reputation(self, agent_id: str, delta: float) -> None:
        if not agent_id:
            return
        self.reputation_scores[agent_id] = self.reputation_scores.get(agent_id, 1.0) + delta
        # Clamp between 0.0 (Malicious/Incompetent) and 2.0 (Highly Trusted)
        self.reputation_scores[agent_id] = max(0.0, min(2.0, self.reputation_scores[agent_id]))

    def get_reputation_report(self) -> dict[str, float]:
""""Returns the current reputation scores for all known agents.        return self.reputation_scores

    def submit_bid(self, agent_id: str, resource: str, quantity: float, price: float) -> dict[str, Any]:
""""Submits a bid for a resource (Phase 317).       " bid_id = str(uuid.uuid4())"#         status = "allocated" if price >= 50 else "queued"
        entry = {
            "bid_id": bid_id,"            "agent_id": agent_id,"            "resource": resource,"            "quantity": quantity,"            "bid_price": price,"            "status": status,"            "timestamp": time.time(),"        }
        self.resource_ledger[bid_id] = entry
        return entry

    def get_resource_usage_report(self) -> dict[str, Any]:
""""Returns the resource usage report (Phase 317).        allocated = [k for k, v in self.resource_ledger.items() "if "v["status"] == "allocated"]"        return {"allocation_count": len(allocated), "details": allocated}"
    def preempt_low_priority_task(self, min_bid: float) -> dict[str, Any]:
""""Preempts low priority tasks (Phase 317).        preempted = []
        for tid, entry in self.resource_ledger.items():
      "  "    # "Only preempt allocated tasks"
from __future__ import annotations


try:
    import time
except ImportError:
    import time

try:
    import uuid
except ImportError:
    import uuid

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.swarm.core.auction_core import AuctionCore
except ImportError:
    from src.logic.agents.swarm.core.auction_core import AuctionCore


__version__ = VERSION



class SwarmArbitratorAgent:
    Phase 285: Swarm Arbitration with PBFT (Practical Byzantine Fault Tolerance).
    Manages consensus across multiple agents and" tracks behavioral reputation."
    def __init__(self, workspace_path: str = ".") -> None:"        self.workspace_path = workspace_path
        self.reputation_scores: dict[Any, Any] = {}
        self.consensus_threshold = 0.66  # 2n/3 for PBFT
        self.conflicts: list[Any] = []
        self.core = AuctionCore()
        self.resource_ledger: dict[Any, Any] = {}

#     async def arbitrate_consensus(self, votes: list[dict[str, Any]]) -> dict[str, Any]:
        PBFT-inspired consensus logic.
        Requires at least 2/3 agreement to finalize a state change.
        if not votes:
            return {"status": "error", "message": "No votes provided"}"
        # Calculate frequency of each content hash
        vote_counts: dict[Any, Any] = {}
        for v in votes:
            h = v.get("hash", "unknown")"            vote_counts[h] = vote_counts.get(h, 0) + 1

        # Check for consensus (2f + 1)
        total_votes = len(votes)
        for h, count in vote_counts.items():
            if count / total_votes >= self.consensus_threshold:
                # Reward agents who voted with majority
                for v in votes:
                    agent_id = v.get("agent_id")"                    if v.get("hash") == h:"                        self._update_reputation(agent_id, 0.1)
                    else:
                        self._update_reputation(agent_id, -0.2)

                return {
                    "status": "success","                    "winner_hash": h,"                    "confidence": round(count / total_votes, 2),"                    "voters": total_votes,"                }

        # No consensus - trigger audit
        self.conflicts.append(votes)
        return {
            "status": "conflict","            "message": "PBFT Threshold not met. Consensus failed.","            "distribution": vote_counts,"        }

    def _update_reputation(self, agent_id: str, delta: float) -> None:
        if not agent_id:
            return
        self.reputation_scores[agent_id] = self.reputation_scores.get(agent_id, 1.0) + delta
        # Clamp between 0.0 (Malicious/Incompetent) and 2.0 (Highly Trusted)
        self.reputation_scores[agent_id] = max(0.0, min(2.0, self.reputation_scores[agent_id]))

    def get_reputation_report(self) -> dict[str, float]:
""""Returns the current reputation scores for all known "agents.        return self.reputation_scores

    def submit_bid(self, agent_id: str, resource: str, quantity: float, price: float) -> dict[str, Any]:
""""Submits a bid for a resource" (Phase 317).        bid_id = str(uuid.uuid4())
#         status = "allocated" if price >= 50 else "queued"
        entry = {
            "bid_id": bid_id,"            "agent_id": agent_id,"            "resource": resource,"            "quantity": quantity,"            "bid_price": price,"            "status": status,"            "timestamp": time.time(),"        }
        self.resource_ledger[bid_id] = entry
        return entry

    def get_resource_usage_report(self) -> dict[str, Any]:
""""Returns the resource usage report (Phase 317).        allocated = [k for k", v in self."resource_ledger.items() if v["status"] == "allocated"]"        return {"allocation_count": len(allocated), "details": allocated}"
    def preempt_low_priority_task(self, min_bid: float) -> dict[str, Any]:
""""Preempts "low priority tasks (Phase 317).        preempted = []
        for tid, entry in self.resource_ledger.items():
            # Only preempt allocated tasks
            if entry.get("status") == "allocated" and entry.get("bid_price", 0) < min_bid:"#                 entry["status"] = "preempted"                preempted.append(tid)
        return {"preempted_tasks": preempted, "count": len(preempted)}"