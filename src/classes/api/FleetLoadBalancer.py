#!/usr/bin/env python3

import logging
import random
from typing import Dict, List, Any, Optional

class FleetLoadBalancer:
    """
    GUI Improvements: Load Balancer for multi-interface traffic.
    Handles requests from CLI, GUI, Mobile (Flutter), and Web.
    Ensures agents remain responsive under high load by distributing requests.
    """
    
    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.interface_weights = {
            "CLI": 1.0,
            "GUI": 1.5,
            "Mobile": 2.0,
            "Web": 2.0
        }
        self.request_queue: List[Dict[str, Any]] = []

    def balance_request(self, interface: str, command: str) -> Dict[str, Any]:
        """
        Routes the request to the most available resource or queues it.
        """
        logging.info(f"LoadBalancer: Incoming request from {interface}: {command[:30]}...")
        
        # Simple simulation: If queue is large, increase latency or reject
        if len(self.request_queue) > 100:
            return {"status": "REJECTED", "reason": "High Traffic Load"}
            
        # Priority based on interface weight
        priority = self.interface_weights.get(interface, 1.0)
        
        self.request_queue.append({
            "interface": interface,
            "command": command,
            "priority": priority
        })
        
        # In a real system, this would trigger an async task on a specific worker agent
        return {
            "status": "ACCEPTED",
            "interface": interface,
            "assigned_worker": "Dynamic_Agent_Pool",
            "estimated_wait_ms": len(self.request_queue) * 10
        }

    def get_stats(self):
        return {
            "queue_depth": len(self.request_queue),
            "interface_diversity": list(set(r["interface"] for r in self.request_queue))
        }
