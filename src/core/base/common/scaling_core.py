# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Unified Scaling Core for PyAgent.
Handles resource calculation, fleet expansion logic, and anti-flapping protocols.
"""

from __future__ import annotations
import math
import time
from typing import Any, Dict, List, Optional
from src.core.base.common.base_core import BaseCore

try:
    import rust_core as rc
except ImportError:
    rc = None

class ScalingCore(BaseCore):
    """
    Core implementation for computing scaling decisions.
    Optimized for high-frequency resource monitoring.
    """
    
    def __init__(self):
        super().__init__()
        self.load_history: List[float] = []

    def compute_moving_average(self, current_load: float, window_size: int = 10) -> float:
        """Compute the SMA for load balancing."""
        if rc and hasattr(rc, "compute_ma_rust"):
            return rc.compute_ma_rust(self.load_history, current_load, window_size)
            
        self.load_history.append(current_load)
        if len(self.load_history) > window_size:
            self.load_history.pop(0)
        return sum(self.load_history) / len(self.load_history)

    def calculate_required_replicas(self, avg_load: float, target_load: float, current_replicas: int) -> int:
        """Calculate the target replica count."""
        if avg_load <= 0: return current_replicas
        return math.ceil(current_replicas * (avg_load / target_load))
