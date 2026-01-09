#!/usr/bin/env python3

"""
ModelFallbackCore logic for redundancy and cost optimization.
Pure logic for selecting fallback models and price comparisons.
"""

from typing import List, Dict, Optional, Any

class ModelFallbackCore:
    """Pure logic core for model fallback strategies."""

    def __init__(self, fallback_chains: Optional[Dict[str, List[str]]] = None) -> None:
        self.fallback_chains = fallback_chains or {
            "high_performance": ["gpt-4o", "claude-3-5-sonnet", "gpt-4-turbo"],
            "balanced": ["claude-3-5-sonnet", "gpt-4o-mini", "gemini-1.5-pro"],
            "economy": ["gpt-4o-mini", "claude-3-haiku", "gemini-1.5-flash"]
        }

    def determine_next_model(self, current_model: str) -> Optional[str]:
        """Logic to pick the next model in a chain."""
        for chain_name, chain in self.fallback_chains.items():
            if current_model in chain:
                idx = chain.index(current_model)
                if idx + 1 < len(chain):
                    return chain[idx + 1]
        
        # Default fallback if not in a chain
        return self.fallback_chains["economy"][0]

    def rank_models_by_cost(self, models: List[str], model_price_map: Dict[str, Dict[str, float]]) -> List[str]:
        """Ranks models from cheapest to most expensive."""
        def get_cost(m: str) -> float:
            return model_price_map.get(m, {}).get("total", 999.0)
            
        return sorted(models, key=get_cost)

    def validate_retry_limit(self, current_retry: int, max_retries: int) -> bool:
        """Logic for retry boundaries."""
        return current_retry < max_retries
