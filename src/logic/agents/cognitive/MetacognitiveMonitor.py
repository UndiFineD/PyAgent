#!/usr/bin/env python3

"""Shell for MetacognitiveMonitor, handling logging and alerting."""

import logging
from typing import Dict, Any, List, Optional

from src.logic.cognitive.MetacognitiveCore import MetacognitiveCore

class MetacognitiveMonitor:
    """Evaluates the internal consistency and certainty of agent reasoning.
    
    Acts as the I/O Shell for MetacognitiveCore.
    """

    def __init__(self) -> None:
        self.uncertainty_log: List[Dict[str, Any]] = []
        self.core = MetacognitiveCore()

    def evaluate_reasoning(self, agent_name: str, task: str, reasoning_chain: str) -> Dict[str, Any]:
        """Analyzes a reasoning chain via core and handles alerts."""
        evaluation_base = self.core.calculate_confidence(reasoning_chain)
        
        evaluation = {
            "agent": agent_name,
            "task": task,
            **evaluation_base
        }
        
        self.uncertainty_log.append(evaluation)
        
        # Shell-specific side effect: Logging/Alerting
        if evaluation["confidence"] < 0.5:
            logging.warning(f"Metacognitive Alert: {agent_name} is highly uncertain about task '{task}'")
            
        return evaluation

    def get_summary(self) -> Dict[str, Any]:
        """Aggregates log via Core."""
        return self.core.aggregate_summary(self.uncertainty_log)
