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
from pathlib import Path
import sqlite3
import logging
import numpy as np
from typing import Dict, Any, Union, List

__version__ = VERSION

class FleetEconomyAgent:
    """
    Manages internal agent "wallets", credits, and resource bidding mechanisms.
    Phase 284: Implemented persistent SQLite backend and Second-Price auctions.
    """
    def __init__(self, workspace_path: str | Path = ".") -> None:
        self.workspace_path = Path(workspace_path)
        self.db_path = self.workspace_path / "data/db/swarm_economy.db"
        self._init_db()

    def _init_db(self) -> None:
        """Initializes the persistent fleet ledger (Phase 284)."""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS wallets (agent_id TEXT PRIMARY KEY, balance REAL)")
                conn.execute("CREATE TABLE IF NOT EXISTS bids (task_id TEXT, agent_id TEXT, bid REAL, priority INTEGER, status TEXT)")
                conn.commit()
            logging.info(f"FleetEconomyAgent: Persistent ledger initialized at {self.db_path}")
        except Exception as e:
            logging.error(f"FleetEconomyAgent: DB initialization failed: {e}")

    def deposit_credits(self, agent_id: str, amount: float) -> dict[str, Any]:
        """Funds an agent's wallet or deducts if negative (Phase 284)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO wallets (agent_id, balance) VALUES (?, ?) "
                "ON CONFLICT(agent_id) DO UPDATE SET balance = balance + ?",
                (agent_id, amount, amount)
            )
            cursor = conn.execute("SELECT balance FROM wallets WHERE agent_id = ?", (agent_id,))
            balance = cursor.fetchone()[0]
            conn.commit()
        return {"agent": agent_id, "balance": balance}

    def place_bid(self, agent_id: str, task_id: str, bid_amount: float, priority: int = 1) -> dict[str, Any]:
        """Places a bid for compute resources (Phase 284)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT balance FROM wallets WHERE agent_id = ?", (agent_id,))
            row = cursor.fetchone()
            balance = row[0] if row else 0.0
            
            if balance < bid_amount:
                return {"status": "failed", "reason": "Insufficient credits"}
            
            conn.execute("INSERT INTO bids (task_id, agent_id, bid, priority, status) VALUES (?, ?, ?, ?, 'active')",
                         (task_id, agent_id, bid_amount, priority))
            # Lock funds
            conn.execute("UPDATE wallets SET balance = balance - ? WHERE agent_id = ?", (bid_amount, agent_id))
            conn.commit()
            
        return {"status": "bid_placed", "task_id": task_id, "remaining_balance": balance - bid_amount}

    def resolve_auction(self, task_id: str) -> dict[str, Any]:
        """Implement Second-Price (Vickrey) auction for task allocation (Phase 284)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT agent_id, bid FROM bids WHERE task_id = ? ORDER BY bid DESC", (task_id,))
            bids = cursor.fetchall()
            
            if not bids:
                return {"status": "failed", "reason": "No bids for task"}
            
            winner_id, highest_bid = bids[0]
            # Second bid or half of highest if only one bidder
            second_bid = bids[1][1] if len(bids) > 1 else (highest_bid * 0.5)
            
            # Refund the difference (Winner pays second price)
            refund = highest_bid - second_bid
            conn.execute("UPDATE wallets SET balance = balance + ? WHERE agent_id = ?", (refund, winner_id))
            
            # Close all bids for this task
            conn.execute("UPDATE bids SET status = 'closed' WHERE task_id = ?", (task_id,))
            conn.commit()
            
        return {
            "winner": winner_id,
            "paid": second_bid,
            "savings": refund,
            "task": task_id
        }

    def get_wallet_summary(self) -> dict[str, float]:
        return self.wallets