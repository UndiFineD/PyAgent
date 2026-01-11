#!/usr/bin/env python3

from __future__ import annotations

import logging
import time
from typing import Dict, List, Any, Optional

class EmotionalRegulationOrchestrator:
    """
    Phase 36: Synthetic Emotional Regulation.
    Manages fleet 'patience' and 'urgency' to balance speed vs accuracy.
    """
    
    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.urgency = 0.5 # 0.0 to 1.0 (1.0 = immediate response needed)
        self.patience = 0.5 # 0.0 to 1.0 (1.0 = deep reasoning preferred)
        self.vibe_history: List[Dict[str, float]] = []

    def set_vibe(self, urgency: Optional[float] = None, patience: Optional[float] = None) -> None:
        """Adjusts the fleet's emotional state."""
        if urgency is not None:
            self.urgency = max(0.0, min(1.0, urgency))
        if patience is not None:
            self.patience = max(0.0, min(1.0, patience))
        
        logging.info(f"EmotionalRegulation: Vibe updated - Urgency: {self.urgency:.2f}, Patience: {self.patience:.2f}")
        self.vibe_history.append({"urgency": self.urgency, "patience": self.patience, "timestamp": time.time()})

    def determine_execution_path(self, task_context: str) -> str:
        """Determines if the task should take the 'fast' or 'deep' path."""
        # Simple heuristic: high urgency -> fast path; high patience -> deep path
        if self.urgency > 0.8:
            return "FAST_PATH"
        if self.patience > 0.7:
            return "DEEP_REASONING_PATH"
            
        # Contextual check
        if "emergency" in task_context.lower() or "critical" in task_context.lower():
            self.urgency = min(1.0, self.urgency + 0.2)
            return "FAST_PATH"
            
        return "BALANCED_PATH"

    def get_token_budget_multiplier(self) -> float:
        """Adjusts token budget based on patience."""
        return 0.5 + self.patience # 0.5x to 1.5x budget
