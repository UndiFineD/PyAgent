#!/usr/bin/env python3

"""Manager for dynamic scaling of the agent fleet.
Monitors system load and spawns new agent instances as needed.
"""

import logging
import time
from typing import Dict, List, Any, Optional, Type
from .ScalingCore import ScalingCore

class ScalingManager:
    """
    Shell for ScalingManager.
    Handles fleet orchestration while delegating logic to ScalingCore.
    """
    
    def __init__(self, fleet_manager) -> None:
        self.fleet = fleet_manager
        self.core = ScalingCore(scale_threshold=5.0, window_size=10)
        
    def record_metric(self, agent_name: str, latency: float) -> None:
        """Records the latency and checks if scaling is required."""
        self.core.add_metric(agent_name, latency)
        
        if self.core.should_scale(agent_name):
            self._execute_scale_out(agent_name)

    def _execute_scale_out(self, agent_name: str) -> None:
        """Spawns a new instance of an agent if latency is too high."""
        avg_latency = self.core.get_avg_latency(agent_name)
        logging.warning(f"SCALING: High latency ({avg_latency:.2f}s) detected for {agent_name}. Spawning replica.")
        
        # Replica naming logic
        replica_name = f"{agent_name}_replica_{int(time.time())}"
        # Implementation depends on FleetManager dynamic registration
        if hasattr(self.fleet, 'register_agent_runtime'):
            self.fleet.register_agent_runtime(replica_name, agent_name)
            
    def get_scaling_status(self) -> str:
        """Returns the current scaling status."""
        return f"Scaling Manager: Monitoring {len(self.core.load_metrics)} agent types."
