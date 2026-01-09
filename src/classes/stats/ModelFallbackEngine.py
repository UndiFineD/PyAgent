#!/usr/bin/env python3

import logging
from typing import List, Optional, Dict
from src.classes.stats.TokenCostEngine import TokenCostEngine
from .ModelFallbackCore import ModelFallbackCore

class ModelFallbackEngine:
    """
    Manages model redundancy and fallback strategies.
    Shell for ModelFallbackCore.
    """

    def __init__(self, cost_engine: Optional[TokenCostEngine] = None) -> None:
        self.cost_engine = cost_engine
        self.core = ModelFallbackCore()
        self.max_retries = 3

    def get_fallback_model(self, current_model: str, failure_reason: str = "") -> Optional[str]:
        """Determines the next model to use after a failure."""
        logging.warning(f"Fallback requested for {current_model}. Reason: {failure_reason}")
        next_model = self.core.determine_next_model(current_model)
        if next_model:
            logging.info(f"Stepping to next model: {next_model}")
        return next_model

    def get_cheapest_model(self, models: List[str]) -> str:
        """Returns the cheapest model from the list based on the cost engine."""
        price_map = {}
        if self.cost_engine:
            price_map = self.cost_engine.MODEL_COSTS
            
        ranked = self.core.rank_models_by_cost(models, price_map)
        return ranked[0]

if __name__ == "__main__":
    cost_engine = TokenCostEngine()
    fallback = ModelFallbackEngine(cost_engine)
    
    print(f"Fallback for gpt-4o: {fallback.get_fallback_model('gpt-4o')}")
    print(f"Cheapest of [gpt-4o, gpt-4o-mini]: {fallback.get_cheapest_model(['gpt-4o', 'gpt-4o-mini'])}")
