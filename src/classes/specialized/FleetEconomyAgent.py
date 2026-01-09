import json
from pathlib import Path

class FleetEconomyAgent:
    """
    Manages internal agent "wallets", credits, and resource bidding mechanisms
    to prioritize compute-heavy tasks within the fleet.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = Path(workspace_path)
        self.wallets = {} # agent_id -> credits
        self.current_bids = {} # task_id -> bid_info

    def deposit_credits(self, agent_id, amount):
        """Funds an agent's wallet."""
        self.wallets[agent_id] = self.wallets.get(agent_id, 0.0) + amount
        return {"agent": agent_id, "balance": self.wallets[agent_id]}

    def place_bid(self, agent_id, task_id, bid_amount, priority=1):
        """Places a bid for compute resources."""
        balance = self.wallets.get(agent_id, 0.0)
        if balance < bid_amount:
            return {"status": "failed", "reason": "Insufficient credits"}
            
        self.wallets[agent_id] -= bid_amount
        self.current_bids[task_id] = {
            "agent": agent_id,
            "bid": bid_amount,
            "priority": priority,
            "status": "active"
        }
        return {"status": "bid_placed", "task_id": task_id, "remaining_balance": self.wallets[agent_id]}

    def resolve_bids(self):
        """
        Highest bidders and priority tasks get allocated first.
        """
        sorted_bids = sorted(
            self.current_bids.items(),
            key=lambda x: (x[1]["priority"], x[1]["bid"]),
            reverse=True
        )
        
        allocation = []
        for tid, info in sorted_bids:
            if info["status"] == "active":
                info["status"] = "allocated"
                allocation.append(tid)
        
        return {"allocated_tasks": allocation, "total": len(allocation)}

    def get_wallet_summary(self):
        return self.wallets
