#!/usr/bin/env python3
from __future__ import annotations
"""Utility for calculating token usage costs across different models.
Inspired by tokencost and other cost tracking tools.
"""

import logging
from typing import Dict, Any, Optional

# Constants for common models (Jan 2026 estimates)
from .TokenCostCore import TokenCostCore, MODEL_COSTS


































from src.core.base.version import VERSION
__version__ = VERSION

class TokenCostEngine:
    """
    Calculates estimated costs for LLM tokens based on model variety.
    Shell for TokenCostCore.
    """
    
    def __init__(self) -> None:
        self.core = TokenCostCore()
        # Keep global reference for backward compatibility if needed
        self.MODEL_COSTS = MODEL_COSTS

    def calculate_cost(self, model: str, input_tokens: int = 0, output_tokens: int = 0) -> float:
        """Returns the estimated cost in USD for the given token counts."""
        return self.core.compute_usd(model, input_tokens, output_tokens)

    def get_supported_models(self) -> list:
        """Returns list of models with explicit pricing."""
        return self.core.list_models()
