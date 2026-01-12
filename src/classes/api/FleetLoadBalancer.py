#!/usr/bin/env python3

import logging
import random
from typing import Dict, List, Any, Optional
from src.infrastructure.api.core.GatewayCore import GatewayCore
from src.infrastructure.fleet.core.LoadBalancerCore import LoadBalancerCore, AgentMetrics

class FleetLoadBalancer:
    """
    GUI Improvements: Load Balancer for multi-interface traffic.
    Integrated with LoadBalancerCore for cognitive pressure distribution.
    """
    
    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.gateway_core = GatewayCore()
        self.lb_core = LoadBalancerCore()
        self.request_queue: List[Dict[str, Any]] = []
        self.agent_metrics: Dict[str, AgentMetrics] = {}

    def balance_request(self, interface: str, command: str) -> Dict[str, Any]:
        """
        Routes the request to the most available resource or queues it.
        Assigns model based on Interface Affinity.
        """
        logging.info(f"LoadBalancer: Incoming request from {interface}: {command[:30]}...")
        
        assigned_model = self.core.resolve_model_by_affinity(interface)
        
        # Simple simulation: If queue is large, increase latency or reject
        if len(self.request_queue) > 100:
            return {"status": "REJECTED", "reason": "High Traffic Load"}
            
        self.request_queue.append({
            "interface": interface,
            "command": command,
            "model": assigned_model
        })
        
        return {
            "status": "ACCEPTED",
            "interface": interface,
            "assigned_model": assigned_model,
            "estimated_wait_ms": len(self.request_queue) * 10
        }

    def get_stats(self) -> Dict[str, Any]:
        return {
            "queue_depth": len(self.request_queue),
            "interface_diversity": list(set(r["interface"] for r in self.request_queue))
        }
