#!/usr/bin/env python3

"""
MetacognitiveCore logic for PyAgent.
Pure logic for evaluating reasoning certainty and consistency.
No I/O or side effects.
"""

from typing import Dict, Any, List

class MetacognitiveCore:
    """Pure logic core for metacognitive evaluation."""

    @staticmethod
    def calculate_confidence(reasoning_chain: str) -> Dict[str, Any]:
        """Analyzes a reasoning chain for hedge words and length patterns."""
        hedge_words = ["maybe", "perhaps", "i think", "not sure", "unclear", "likely"]
        count = sum(1 for word in hedge_words if word in reasoning_chain.lower())
        
        uncertainty_score = min(1.0, count / 5.0)
        confidence = 1.0 - uncertainty_score
        
        return {
            "confidence": confidence,
            "uncertainty_score": uncertainty_score,
            "hedges_detected": count,
            "status": "high_confidence" if confidence > 0.7 else "uncertain"
        }

    @staticmethod
    def aggregate_summary(uncertainty_log: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates average confidence and totals."""
        if not uncertainty_log:
            return {"avg_confidence": 1.0, "total_evaluations": 0}
            
        avg = sum(e.get("confidence", 0.0) for e in uncertainty_log) / len(uncertainty_log)
        return {
            "avg_confidence": round(avg, 2),
            "total_evaluations": len(uncertainty_log)
        }
