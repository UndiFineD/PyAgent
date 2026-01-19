# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Core Pooling Engine implementation.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional, Any, Type, List
import numpy as np

from .models import PoolingConfig, PoolingStrategy, PoolingResult
from .strategies import (
    BasePooler, MeanPooler, CLSPooler, LastTokenPooler, 
    MaxPooler, AttentionPooler, WeightedMeanPooler
)

logger = logging.getLogger(__name__)

class PoolingEngine:
    """Manager for various pooling operations."""
    
    _STRATEGIES: Dict[PoolingStrategy, Type[BasePooler]] = {
        PoolingStrategy.MEAN: MeanPooler,
        PoolingStrategy.CLS: CLSPooler,
        PoolingStrategy.LAST: LastTokenPooler,
        PoolingStrategy.MAX: MaxPooler,
        PoolingStrategy.ATTENTION: AttentionPooler,
        PoolingStrategy.WEIGHTED_MEAN: WeightedMeanPooler
    }
    
    def __init__(self, config: Optional[PoolingConfig] = None, **kwargs):
        self.config = config or PoolingConfig()
        # Phase 125: Handle legacy/test pass-through parameters
        if "strategy" in kwargs:
            self.config.strategy = kwargs["strategy"]
        if "truncate_dim" in kwargs:
            self.config.truncate_dim = kwargs["truncate_dim"]
        if "task" in kwargs:
            self.config.task = kwargs["task"]

        self._poolers: Dict[PoolingStrategy, BasePooler] = {}
        logger.debug("Initialized PoolingEngine with strategy: %s", self.config.strategy)

    def get_pooler(self, strategy: Optional[PoolingStrategy] = None) -> BasePooler:
        """Get or create singleton pooler instance for strategy."""
        target_strat = strategy or self.config.strategy
        if target_strat not in self._poolers:
            pooler_cls = self._STRATEGIES.get(target_strat)
            if not pooler_cls:
                raise ValueError(f"Unknown pooling strategy: {target_strat}")
            self._poolers[target_strat] = pooler_cls(self.config)
        return self._poolers[target_strat]

    def pool(
        self,
        hidden_states: Any,
        attention_mask: Optional[Any] = None,
        strategy: Optional[PoolingStrategy] = None,
        normalize: bool = True,
        truncate_dim: Optional[int] = None,
        **kwargs
    ) -> PoolingResult:
        """
        Execute pooling on inputs.
        Supports numpy arrays and potentially torch/tf tensors via conversion.
        """
        # Convert any tensor types to numpy for generic processing if needed
        h_states = self._ensure_numpy(hidden_states)
        mask = self._ensure_numpy(attention_mask) if attention_mask is not None else None
        
        target_strat = strategy or self.config.strategy
        pooler = self.get_pooler(target_strat)
        
        # Handle weighted mean special case
        if target_strat == PoolingStrategy.WEIGHTED_MEAN:
            results = pooler.pool(h_states, mask, token_ids=kwargs.get("token_ids"))
        else:
            results = pooler.pool(h_states, mask)
            
        # Optional Matryoshka truncation
        if truncate_dim:
            results = pooler.truncate(results, truncate_dim)
            
        # Optional normalization
        if normalize:
            results = pooler.normalize(results)
            
        return PoolingResult(
            embeddings=results,
            strategy=target_strat,
            normalized=normalize,
            dim=results.shape[-1]
        )

    def _ensure_numpy(self, data: Any) -> np.ndarray:
        """Helper to ensure data is in numpy format."""
        if isinstance(data, np.ndarray):
            return data
        if hasattr(data, "cpu") and hasattr(data, "detach"): # Torch
            return data.detach().cpu().numpy()
        if hasattr(data, "numpy"): # TF
            return data.numpy()
        return np.array(data)


def create_pooling_engine(config: Optional[PoolingConfig] = None, **kwargs) -> PoolingEngine:
    """Factory function for PoolingEngine."""
    return PoolingEngine(config, **kwargs)

