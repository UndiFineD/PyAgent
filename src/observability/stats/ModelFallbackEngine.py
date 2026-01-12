#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.



import logging
from typing import List, Optional, Dict, Any
from src.observability.stats.TokenCostEngine import TokenCostEngine
from .ModelFallbackCore import ModelFallbackCore



































class ModelFallbackEngine:
    """
    Manages model redundancy and fallback strategies.
    Shell for ModelFallbackCore.
    """

    def __init__(self, cost_engine: Optional[TokenCostEngine] = None, fleet: Optional[Any] = None) -> None:
        if fleet and hasattr(fleet, "telemetry") and not cost_engine:
            self.cost_engine = fleet.telemetry.cost_engine
        else:
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
