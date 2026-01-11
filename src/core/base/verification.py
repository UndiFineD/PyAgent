"""
Verification logic for agent outputs.
Implements Stanford Reseach 'Anchoring Strength' and Keio University 'Self-Verification' paths.
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List

class AgentVerifier:
    """Handles quality and anchoring verification of agent responses."""

    @staticmethod
    def calculate_anchoring_strength(result: str, context_pool: Dict[str, Any]) -> float:
        """
        Calculates the 'Anchoring Strength' metric.
        Measures how well the output is anchored to the provided context/grounding.
        """
        if not context_pool:
            return 0.5
            
        context_text = " ".join([str(v) for v in context_pool.values()])
        if not context_text:
            return 0.5
            
        context_words = set(context_text.lower().split())
        result_words = result.lower().split()
        if not result_words:
            return 0.0
            
        overlap = [word in context_words for word in result_words]
        score = sum(overlap) / len(result_words)
        
        if len(result_words) < 5:
            score *= 0.5
            
        return min(1.0, score * 1.5)

    @staticmethod
    def verify_self(result: str, anchoring_score: float) -> tuple[bool, str]:
        """Self-verification layer output check."""
        if not result:
            return False, "Empty result"
            
        hallucination_threshold = 0.3
        if anchoring_score < hallucination_threshold:
            return False, f"Low anchoring strength ({anchoring_score:.2f})"
            
        return True, "Verified"
