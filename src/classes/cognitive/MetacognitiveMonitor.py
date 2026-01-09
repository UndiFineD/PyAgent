#!/usr/bin/env python3

"""Metacognitive monitoring for agent reasoning assessment.
Allows agents to track and report their own certainty and reasoning uncertainty.
"""

import logging
from typing import Dict, Any, List

class MetacognitiveMonitor:
    """Evaluates the internal consistency and certainty of agent reasoning."""

    def __init__(self) -> None:
        self.uncertainty_log: List[Dict[str, Any]] = []

    def evaluate_reasoning(self, agent_name: str, task: str, reasoning_chain: str) -> Dict[str, Any]:
        """Analyzes a reasoning chain for potential 'hallucination' or low confidence tokens."""
        # In a real scenario, this would analyze logprobs or use a cross-checking model
        # For simulation, we'll scan for hedge words and length patterns
        hedge_words = ["maybe", "perhaps", "i think", "not sure", "unclear", "likely"]
        count = sum(1 for word in hedge_words if word in reasoning_chain.lower())
        
        uncertainty_score = min(1.0, count / 5.0)
        confidence = 1.0 - uncertainty_score
        
        evaluation = {
            "agent": agent_name,
            "task": task,
            "confidence": confidence,
            "uncertainty_score": uncertainty_score,
            "hedges_detected": count,
            "status": "high_confidence" if confidence > 0.7 else "uncertain"
        }
        
        self.uncertainty_log.append(evaluation)
        if confidence < 0.5:
            logging.warning(f"Metacognitive Alert: {agent_name} is highly uncertain about task '{task}'")
            
        return evaluation

    def get_summary(self) -> Dict[str, Any]:
        if not self.uncertainty_log:
            return {"avg_confidence": 1.0}
            
        avg = sum(e["confidence"] for e in self.uncertainty_log) / len(self.uncertainty_log)
        return {
            "avg_confidence": round(avg, 2),
            "total_evaluations": len(self.uncertainty_log)
        }
