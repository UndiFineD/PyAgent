#!/usr/bin/env python3

"""
ConsensusCore logic for multi-agent voting.
Contains pure logic for tallying votes, handling ties, and selecting winners.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional

class ConsensusCore:
    """Pure logic core for consensus protocols."""
    
    def __init__(self, mode: str = "plurality") -> None:
        self.mode = mode

    def calculate_winner(self, proposals: List[str], weights: Optional[List[float]] = None) -> str:
        """
        Determines the winning proposal based on voting rules.
        Phase 119: Supports weighted voting based on agent reliability.
        """
        if not proposals:
            return ""
            
        if weights and len(weights) != len(proposals):
            weights = None # Fallback to unweighted if mismatch

        # Count identical proposals with weights
        counts: Dict[str, float] = {}
        for idx, p in enumerate(proposals):
            weight = weights[idx] if weights else 1.0
            counts[p] = counts.get(p, 0) + weight
            
        # Strategy: Most weighted, then longest as tie-breaker
        winner = sorted(
            counts.keys(), 
            key=lambda x: (counts[x], len(x)), 
            reverse=True
        )[0]
        
        return winner

    def get_agreement_score(self, proposals: List[str], winner: str) -> float:
        """Calculates the percentage of agents that agreed with the winner."""
        if not proposals:
            return 0.0
        match_count = sum(1 for p in proposals if p == winner)
        return match_count / len(proposals)
