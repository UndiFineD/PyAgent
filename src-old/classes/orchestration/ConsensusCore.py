#!/usr/bin/env python3

"""
ConsensusCore logic for multi-agent voting.
Contains pure logic for tallying votes, handling ties, and selecting winners.
"""

from typing import List, Dict, Any, Optional

class ConsensusCore:
    """Pure logic core for consensus protocols."""
    
    def __init__(self, mode: str = "plurality") -> None:
        self.mode = mode

    def calculate_winner(self, proposals: List[str]) -> str:
        """Determines the winning proposal based on voting rules."""
        if not proposals:
            return ""
            
        # Count identical proposals
        counts: Dict[str, int] = {}
        for p in proposals:
            counts[p] = counts.get(p, 0) + 1
            
        # Strategy: Most frequent, then longest as tie-breaker
        # In the future, this logic could be replaced by a Rust library 
        # for high-performance string hashing and comparison.
        winner = sorted(
            proposals, 
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
