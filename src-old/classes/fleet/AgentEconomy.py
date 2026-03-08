#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/fleet/AgentEconomy.description.md

# AgentEconomy

**File**: `src\classes\fleet\AgentEconomy.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 80  
**Complexity**: 7 (moderate)

## Overview

Agent economy and accounting engine.
Manages credits, bidding, and automated payments between agents.

## Classes (1)

### `AgentEconomy`

Manages internal marketplace credits and task bidding.

**Methods** (7):
- `__init__(self)`
- `_initialize_genesis_block(self)`
- `_hash_block(self, block)`
- `get_balance(self, agent_id)`
- `transfer_credits(self, sender, receiver, amount, reason)`
- `_record_transaction(self, sender, receiver, amount, reason)`
- `place_bid(self, agent_id, task_id, bid_amount)`

## Dependencies

**Imports** (8):
- `hashlib`
- `json`
- `logging`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/fleet/AgentEconomy.improvements.md

# Improvements for AgentEconomy

**File**: `src\classes\fleet\AgentEconomy.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 80 lines (small)  
**Complexity**: 7 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentEconomy_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

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
            "hash": self._hash_block(
                {"index": 0, "transactions": [], "previous_hash": "0"}
            ),
        }
        self.blockchain.append(genesis)

    def _hash_block(self, block: Dict[str, Any]) -> str:
        block_string: bytes = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_balance(self, agent_id: str) -> float:
        return self.balances.get(agent_id, 1000.0)  # Default starting credits

    def transfer_credits(
        self, sender: str, receiver: str, amount: float, reason: str
    ) -> bool:
        """Executes a secure transfer of credits between agents."""
        s_bal: float = self.get_balance(sender)
        if s_bal < amount:
            logging.warning(
                f"Transfer failed: {sender} has insufficient funds ({s_bal} < {amount})"
            )
            return False

        self.balances[sender] = s_bal - amount
        self.balances[receiver] = self.get_balance(receiver) + amount

        # Record to immutable log
        self._record_transaction(sender, receiver, amount, reason)
        return True

    def _record_transaction(
        self, sender: str, receiver: str, amount: float, reason: str
    ) -> None:
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "reason": reason,
            "timestamp": time.time(),
        }

        prev_block: Dict[str, Any] = self.blockchain[-1]
        new_block = {
            "index": len(self.blockchain),
            "timestamp": time.time(),
            "transactions": [transaction],
            "previous_hash": prev_block["hash"],
        }
        new_block["hash"] = self._hash_block(new_block)
        self.blockchain.append(new_block)
        logging.info(f"Transaction recorded: {sender} -> {receiver} ({amount} credits)")

    def place_bid(
        self, agent_id: str, task_id: str, bid_amount: float
    ) -> Dict[str, Any]:
        """Submits a bid for a task."""
        return {
            "agent_id": agent_id,
            "task_id": task_id,
            "bid": bid_amount,
            "timestamp": time.time(),
        }

        import json
