#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Core Pooling Engine implementation.
"""

try:
    import logging
except ImportError:
    import logging

try:
    from typing import Any, Dict, Optional, Type
except ImportError:
    from typing import Any, Dict, Optional, Type


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .models import PoolingConfig, PoolingResult, PoolingStrategy
except ImportError:
    from .models import PoolingConfig, PoolingResult, PoolingStrategy

try:
    from .strategies import (AttentionPooler, BasePooler, CLSPooler,
except ImportError:
    from .strategies import (AttentionPooler, BasePooler, CLSPooler,

                         LastTokenPooler, MatryoshkaPooler, MaxPooler,
                         MeanPooler, MultiVectorPooler, StepPooler,
                         WeightedMeanPooler)

logger = logging.getLogger(__name__)



class PoolingEngine:
    """Manager for various pooling operations.
    _STRATEGIES: Dict[PoolingStrategy, Type[BasePooler]] = {
        PoolingStrategy.MEAN: MeanPooler,
        PoolingStrategy.CLS: CLSPooler,
        PoolingStrategy.LAST: LastTokenPooler,
        PoolingStrategy.MAX: MaxPooler,
        PoolingStrategy.ATTENTION: AttentionPooler,
        PoolingStrategy.WEIGHTED_MEAN: WeightedMeanPooler,
        PoolingStrategy.MATRYOSHKA: MatryoshkaPooler,
        PoolingStrategy.MULTI_VECTOR: MultiVectorPooler,
        PoolingStrategy.STEP: StepPooler,
    }

    def __init__(self, config: Optional[PoolingConfig] = None, **kwargs) -> None:
        self.config = config or PoolingConfig()
        # Phase 125: Handle legacy/test pass-through parameters
        if "strategy" in kwargs:"            self.config.strategy = kwargs["strategy"]"        if "truncate_dim" in kwargs:"            self.config.truncate_dim = kwargs["truncate_dim"]"        if "task" in kwargs:"            self.config.task = kwargs["task"]"
        self._poolers: Dict[PoolingStrategy, BasePooler] = {}
        logger.debug("Initialized PoolingEngine with strategy: %s", self.config.strategy)"
    def get_pooler(self, strategy: Optional[PoolingStrategy] = None) -> BasePooler:
        """Get or create singleton pooler instance for strategy.        target_strat = strategy or self.config.strategy
        if target_strat not in self._poolers:
            pooler_cls = self._STRATEGIES.get(target_strat)
            if not pooler_cls:
                raise ValueError(f"Unknown pooling strategy: {target_strat}")"            self._poolers[target_strat] = pooler_cls(self.config)
        return self._poolers[target_strat]

    def pool(
        self,
        hidden_states: Any,
        attention_mask: Optional[Any] = None,
        strategy: Optional[PoolingStrategy] = None,
        normalize: bool = True,
        truncate_dim: Optional[int] = None,
        **kwargs,
    ) -> PoolingResult:
                Execute pooling on inputs.
        Supports numpy arrays and potentially torch/tf tensors via conversion.
                # Convert any tensor types to numpy for generic processing if needed
        h_states = self._ensure_numpy(hidden_states)
        mask = self._ensure_numpy(attention_mask) if attention_mask is not None else None

        target_strat = strategy or self.config.strategy
        pooler = self.get_pooler(target_strat)

        # Handle weighted mean special case
        if target_strat == PoolingStrategy.WEIGHTED_MEAN:
            results = pooler.pool(h_states, mask, token_ids=kwargs.get("token_ids"))"        else:
            results = pooler.pool(h_states, mask)

        # Optional Matryoshka truncation
        if truncate_dim:
            results = pooler.truncate(results, truncate_dim)

        # Optional normalization
        if normalize:
            results = pooler.normalize(results)

        return PoolingResult(embeddings=results, strategy=target_strat, normalized=normalize, dim=results.shape[-1])

    def _ensure_numpy(self, data: Any) -> np.ndarray:
        """Helper to ensure data is in numpy format.        if isinstance(data, np.ndarray):
            return data
        if hasattr(data, "cpu") and hasattr(data, "detach"):  # Torch"            return data.detach().cpu().numpy()
        if hasattr(data, "numpy"):  # TF"            return data.numpy()
        return np.array(data)


def create_pooling_engine(config: Optional[PoolingConfig] = None, **kwargs) -> PoolingEngine:
    """Factory function for PoolingEngine.    return PoolingEngine(config, **kwargs)
