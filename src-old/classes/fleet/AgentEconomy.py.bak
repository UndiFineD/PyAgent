#!/usr/bin/env python3

"""Agent economy and accounting engine.
Manages credits, bidding, and automated payments between agents.
"""

import logging
import time
import hashlib
from typing import Dict, List, Any, Optional

class AgentEconomy:
    """Manages internal marketplace credits and task bidding."""

    def __init__(self) -> None:
        self.balances: Dict[str, float] = {}
        self.blockchain: List[Dict[str, Any]] = []
        self._initialize_genesis_block()

    def _initialize_genesis_block(self) -> bool:
        genesis = {
            "index": 0,
            "timestamp": time.time(),
            "transactions": [],
            "previous_hash": "0",
            "hash": self._hash_block({"index": 0, "transactions": [], "previous_hash": "0"})
        }
        self.blockchain.append(genesis)

    def _hash_block(self, block: Dict[str, Any]) -> str:
        block_string: bytes = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_balance(self, agent_id: str) -> float:
        return self.balances.get(agent_id, 1000.0) # Default starting credits

    def transfer_credits(self, sender: str, receiver: str, amount: float, reason: str) -> bool:
        """Executes a secure transfer of credits between agents."""
        s_bal: float = self.get_balance(sender)
        if s_bal < amount:
            logging.warning(f"Transfer failed: {sender} has insufficient funds ({s_bal} < {amount})")
            return False
            
        self.balances[sender] = s_bal - amount
        self.balances[receiver] = self.get_balance(receiver) + amount
        
        # Record to immutable log
        self._record_transaction(sender, receiver, amount, reason)
        return True

    def _record_transaction(self, sender: str, receiver: str, amount: float, reason: str) -> None:
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "reason": reason,
            "timestamp": time.time()
        }
        
        prev_block: Dict[str, Any] = self.blockchain[-1]
        new_block = {
            "index": len(self.blockchain),
            "timestamp": time.time(),
            "transactions": [transaction],
            "previous_hash": prev_block["hash"]
        }
        new_block["hash"] = self._hash_block(new_block)
        self.blockchain.append(new_block)
        logging.info(f"Transaction recorded: {sender} -> {receiver} ({amount} credits)")

    def place_bid(self, agent_id: str, task_id: str, bid_amount: float) -> Dict[str, Any]:
        """Submits a bid for a task."""
        return {
            "agent_id": agent_id,
            "task_id": task_id,
            "bid": bid_amount,
            "timestamp": time.time()
        }

import json
