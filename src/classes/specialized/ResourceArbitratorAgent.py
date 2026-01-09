import time
import uuid

class ResourceArbitratorAgent:
    """
    Arbitrates the allocation of compute resources (CPU, GPU, Memory)
    using a priority-based internal market system.
    """
    def __init__(self, workspace_path) -> None:
        self.workspace_path = workspace_path
        self.resource_ledger = {} # task_id -> {type, amount, bid, timestamp}
        self.available_credits = 10000.0 # Virtual credits for the swarm
        
    def submit_bid(self, agent_id, resource_type, amount, bid_price):
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

    def get_resource_usage_report(self):
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

    def preempt_low_priority_task(self, min_bid):
        """
        Reclaims resources from tasks with lower bids.
        """
        preempted = []
        for tid, entry in self.resource_ledger.items():
            if entry["status"] == "allocated" and entry["bid_price"] < min_bid:
                entry["status"] = "preempted"
                preempted.append(tid)
        return {"preempted_tasks": preempted, "count": len(preempted)}
