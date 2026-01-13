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

class ResourceArbitratorAgent:
    """
    Arbitrates the allocation of compute resources (CPU, GPU, Memory)
    using a priority-based internal market system (Phase 184 VCG).
    """
    def __init__(self, workspace_path: str) -> None:
        self.workspace_path = workspace_path
        self.resource_ledger: Dict[str, Any] = {} # task_id -> {type, amount, bid, timestamp}
        self.available_credits = 10000.0 # Virtual credits for the swarm
        self.core = AuctionCore()
        self.vram_total = 80.0 # GB (e.g., A100)
        
    def submit_vcg_bid(self, bids: List[Dict[str, Any]], slots: int = 1) -> List[Dict[str, Any]]:
        """Executes a VCG auction for the provided bids."""
        return self.core.calculate_vcg_auction(bids, slots)

    def check_vram_limit(self, agent_request_gb: float) -> bool:
        """Enforces VRAM quotas (Phase 184)."""
        return self.core.enforce_vram_quota(agent_request_gb, self.vram_total)

    def submit_bid(self, agent_id: str, resource_type: str, amount: float, bid_price: float) -> Dict[str, Any]:
        """
        Allows an agent to bid for a slice of the resource pool.
        """
        task_id = str(uuid.uuid4())[:8]
        entry = {
            "agent_id": agent_id,
            "resource_type": resource_type,
            "amount": amount,
            "bid_price": bid_price,
            "timestamp": time.time(),
            "status": "pending"
        }
        self.resource_ledger[task_id] = entry
        
        # Simple arbitration: If bid is above threshold, auto-approve for simulation
        if bid_price > 50:
            entry["status"] = "allocated"
            return {"task_id": task_id, "status": "allocated", "credits_reserved": bid_price}
        else:
            entry["status"] = "queued"
            return {"task_id": task_id, "status": "queued", "message": "Bid too low, waiting for lower demand."}

    def get_resource_usage_report(self) -> Dict[str, Any]:
        """
        Returns a summary of resource allocation across the fleet.
        """
        allocated = [v for v in self.resource_ledger.values() if v["status"] == "allocated"]
        queued = [v for v in self.resource_ledger.values() if v["status"] == "queued"]
        return {
            "total_credits_locked": sum(v["bid_price"] for v in allocated),
            "allocation_count": len(allocated),
            "backlog": len(queued)
        }

    def preempt_low_priority_task(self, min_bid: float) -> Dict[str, Any]:
        """
        Reclaims resources from tasks with lower bids.
        """
        preempted = []
        for tid, entry in self.resource_ledger.items():
            if entry["status"] == "allocated" and entry["bid_price"] < min_bid:
                entry["status"] = "preempted"
                preempted.append(tid)
        return {"preempted_tasks": preempted, "count": len(preempted)}