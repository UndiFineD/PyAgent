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
MarketPricingEngine and AgentEconomy 
- Dynamic pricing and internal credit system for PyAgent Swarm.
Agent economy and accounting engine.
Manages credits, bidding, and automated payments between agents.
"""


from __future__ import annotations


try:
    import hashlib
except ImportError:
    import hashlib

try:
    import json
except ImportError:
    import json

try:
    import logging
except ImportError:
    import logging

try:
    import time
except ImportError:
    import time

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .infrastructure.swarm.fleet.core.economy_core import EconomyCore
except ImportError:
    from src.infrastructure.swarm.fleet.core.economy_core import EconomyCore




class MarketPricingEngine:
    """Calculates dynamic pricing based on system load, hardware specs, and model types.
    # PRICING (USD per 1K tokens) - migrated from benchmark_glm47.py
    MODEL_PRICING = {
        "gpt-4.1": {"input": 0.02, "output": 0.15},"        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},"        "glm-4": {"input": 0.01, "output": 0.05},"        "glm-4v": {"input": 0.02, "output": 0.10},"        "claude-3-5-sonnet": {"input": 0.003, "output": 0.015},"    }

    @staticmethod
    def calculate_price(base_price: float, resource_stats: dict[str, Any]) -> float:
        """Applies multipliers based on CPU/GPU demand.
        multiplier = 1.0

        # Load-based surcharge
        if resource_stats.get("status") == "CRITICAL":"            multiplier *= 2.5

        elif resource_stats.get("status") == "WARNING":"            multiplier *= 1.5

        # Hardware-based premium
        gpu = resource_stats.get("gpu", {})"
        if gpu.get("available"):"            multiplier *= 2.0  # GPU turns are premium

        return base_price * multiplier



class AgentEconomy:
    """Manages internal marketplace credits and task bidding.
    def __init__(self) -> None:
        self.balances: dict[str, float] = {}
        self.blockchain: list[dict[str, Any]] = []
        self.pricing_engine = MarketPricingEngine()
        self._initialize_genesis_block()

    def _initialize_genesis_block(self) -> bool:
        genesis = {
            "index": 0,"            "timestamp": time.time(),"            "transactions": [],"            "previous_hash": "0","            "hash": self._hash_block({"index": 0, "transactions": [], "previous_hash": "0"}),"        }
        self.blockchain.append(genesis)

    def _hash_block(self, block: dict[str, Any]) -> str:
        block_string: bytes = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_balance(self, agent_id: str) -> float:
        """Retrieves the current credit balance of an agent.        return self.balances.get(agent_id, 1000.0)  # Default starting credits

    def transfer_credits(self, sender: str, receiver: str, amount: float, reason: str) -> bool:
        """Executes a secure transfer of credits between agents.        s_bal: float = self.get_balance(sender)
        if s_bal < amount:
            logging.warning(f"Transfer failed: {sender} has insufficient funds ({s_bal} < {amount})")"            return False

        self.balances[sender] = s_bal - amount
        self.balances[receiver] = self.get_balance(receiver) + amount

        # Record to immutable log
        self._record_transaction(sender, receiver, amount, reason)
        return True

    def request_gpu_priority(self, agent_id: str, bid_amount: float, importance: float) -> bool:
        """Process a bid for high-priority GPU access (Phase 179).        balance = self.get_balance(agent_id)
        if bid_amount > balance:
            return False

        priority = EconomyCore.calculate_bid_priority(bid_amount, importance, 0.5)
        logging.info(f"AgentEconomy: Agent {agent_id} bidding {bid_amount} credits. Priority: {priority:.2f}")"
        # Threshold for high priority
        if priority > 100.0:
            self.transfer_credits(agent_id, "SYSTEM_GPU_POOL", bid_amount, "GPU_PRIORITY_BID")"            return True
        return False

    def _record_transaction(self, sender: str, receiver: str, amount: float, reason: str) -> None:
        transaction = {
            "sender": sender,"            "receiver": receiver,"            "amount": amount,"            "reason": reason,"            "timestamp": time.time(),"        }

        prev_block: dict[str, Any] = self.blockchain[-1]
        new_block = {
            "index": len(self.blockchain),"            "timestamp": time.time(),"            "transactions": [transaction],"            "previous_hash": prev_block["hash"],"        }
        new_block["hash"] = self._hash_block(new_block)"        self.blockchain.append(new_block)
        logging.info(f"Transaction recorded: {sender} -> {receiver} ({amount} credits)")"
    def place_bid(self, agent_id: str, task_id: str, bid_amount: float) -> dict[str, Any]:
        """Submits a bid for a task.        return {
            "agent_id": agent_id,"            "task_id": task_id,"            "bid": bid_amount,"            "timestamp": time.time(),"        }



class AuctionOrchestrator:
    """Orchestrates auctions for task allocation across the swarm.
    def __init__(self, economy: AgentEconomy) -> None:
        self.economy = economy
        self.active_auctions: dict[str, dict[str, Any]] = {}

    def start_auction(
        self,
        task_id: str,
        requirements: dict[str, Any],
        reserve_price: float = 10.0,
        auction_type: str = "vickrey","    ) -> str:
        """Starts a new auction (Vickrey or Dutch) for a task.        self.active_auctions[task_id] = {
            "requirements": requirements,"            "bids": [],"            "reserve_price": reserve_price,"            "start_time": time.time(),"            "status": "active","            "type": auction_type,"            "initial_price": reserve_price * 10 if auction_type == "dutch" else None,"        }
        return f"{auction_type.capitalize()} auction started for task {task_id}""
    def get_current_dutch_price(self, task_id: str) -> float:
        """Calculates current price for a Dutch auction based on elapsed time.        auction = self.active_auctions.get(task_id)
        if not auction or auction["type"] != "dutch":"            return 0.0

        elapsed = time.time() - auction["start_time"]"
        decay_rate = 0.1  # Price drops by 10% per second
        current_price = auction["initial_price"] * (1.0 - (elapsed * decay_rate))"        return max(auction["reserve_price"], current_price)"
    def submit_bid(
        self,
        task_id: str,
        agent_id: str,
        bid_amount: float,
        capability_score: float = 1.0,
    ) -> bool:
        """Submits a bid to an active auction.        if task_id not in self.active_auctions or self.active_auctions[task_id]["status"] != "active":"            return False

        auction = self.active_auctions[task_id]

        # Dutch auction special handling
        if auction["type"] == "dutch":"            current_price = self.get_current_dutch_price(task_id)
            if bid_amount >= current_price:
                # First bidder wins immediately in Dutch auction
                auction["bids"].append("                    {
                        "agent_id": agent_id,"                        "amount": current_price,"                        "score": capability_score,"                        "effective_bid": current_price,"                    }
                )
                self.resolve_auction(task_id)
                return True
            return False

        # Verify balance for sealed-bid
        if self.economy.get_balance(agent_id) < bid_amount:
            return False

        auction["bids"].append("            {
                "agent_id": agent_id,"                "amount": bid_amount,"                "score": capability_score,"                "effective_bid": bid_amount * capability_score,"            }
        )
        return True

    def start_bundle_auction(self, items: list[str], requirements: dict[str, Any]) -> str:
        """Starts a combinatorial auction for a bundle of items/tasks.        bundle_id = f"bundle_{int(time.time())}""        self.active_auctions[bundle_id] = {
            "items": items,"            "requirements": requirements,"            "bids": [],"            "status": "active","            "type": "bundle","        }
        return bundle_id

    def resolve_auction(self, task_id: str) -> dict[str, Any] | None:
        """Resolves the auction and returns the winner and the price to pay.        if task_id not in self.active_auctions:
            return None

        auction = self.active_auctions[task_id]
        if not auction["bids"]:"            auction["status"] = "failed""            return None

        # Sort by effective bid
        sorted_bids = sorted(auction["bids"], key=lambda x: x["effective_bid"], reverse=True)"
        winner = sorted_bids[0]

        # In a Vickrey auction, winner pays the second-highest bid price
        payment_price = sorted_bids[1]["amount"] if len(sorted_bids) > 1 else auction["reserve_price"]"
        auction["status"] = "closed""        auction["winner"] = winner["agent_id"]"        auction["final_price"] = payment_price"
        return {
            "task_id": task_id,"            "winner": winner["agent_id"],"            "payment": payment_price,"        }


__version__ = VERSION
