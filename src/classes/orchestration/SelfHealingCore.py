#!/usr/bin/env python3

"""
SelfHealingCore logic for fleet resilience.
Contains pure logic for health threshold calculation, anomaly detection,
and recovery strategy selection.
"""

import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class HealthStatus:
    agent_name: str
    is_alive: bool
    last_seen: float
    error_count: int = 0
    latency_ms: float = 0.0
    status_msg: str = "ok"

class SelfHealingCore:
    """Pure logic core for the SelfHealing orchestrator."""
    
    def __init__(self, timeout_seconds: float = 30.0, max_errors: int = 5) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_errors = max_errors
        self.health_registry: Dict[str, HealthStatus] = {}

    def update_health(self, agent_name: str, latency: float = 0.0, error: bool = False) -> bool:
        """Updates internal status for an agent."""
        now = time.time()
        if agent_name not in self.health_registry:
            self.health_registry[agent_name] = HealthStatus(agent_name, True, now)
        
        status = self.health_registry[agent_name]
        status.last_seen = now
        status.latency_ms = latency
        if error:
            status.error_count += 1
        else:
            # Gradually decay error count on success
            status.error_count = max(0, status.error_count - 1)
        
        status.is_alive = (status.error_count < self.max_errors)
        return status.is_alive

    def detect_failures(self) -> List[str]:
        """Returns a list of agent names that are considered failed."""
        now = time.time()
        failed = []
        for name, status in self.health_registry.items():
            # Time-based failure
            if now - status.last_seen > self.timeout_seconds:
                status.is_alive = False
                status.status_msg = "timeout"
                failed.append(name)
            # Error-based failure
            elif status.error_count >= self.max_errors:
                status.is_alive = False
                status.status_msg = "error_threshold_exceeded"
                failed.append(name)
        return failed

    def get_recovery_action(self, agent_name: str) -> str:
        """Determines the best strategy for a failed agent."""
        status = self.health_registry.get(agent_name)
        if not status:
            return "reinitialize"
            
        if status.status_msg == "timeout":
            return "restart_process"
        if status.error_count > self.max_errors * 2:
            return "apoptosis" # Clean kill if beyond help
            
        return "reinitialize"

    def validate_plugin_version(self, plugin_version: str, required_version: str) -> bool:
        """
        Semantic version comparison logic.
        v1.2.3 vs v1.2.0
        """
        try:
            p_parts = [int(x) for x in plugin_version.lstrip('v').split('.')]
            r_parts = [int(x) for x in required_version.lstrip('v').split('.')]
            
            # Pad with zeros if necessary
            p_parts += [0] * (3 - len(p_parts))
            r_parts += [0] * (3 - len(r_parts))
            
            # Major must match exactly, Minor must be >=, Patch ignored for now
            if p_parts[0] != r_parts[0]: return False
            if p_parts[1] < r_parts[1]: return False
            return True
        except Exception:
            return False
