
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for the Pooling Engine (AI-specific).
"""

from .models import (
    PoolingTask,
    PoolingStrategy,
    PoolingConfig,
    PoolingResult,
    EmbeddingOutput,
    ClassificationOutput
)
from .strategies import (
    BasePooler,
    MeanPooler,
    CLSPooler,
    LastTokenPooler,
    MaxPooler,
    AttentionPooler,
    WeightedMeanPooler,
    MatryoshkaPooler,
    MultiVectorPooler,
    StepPooler
)
from .engine import PoolingEngine, create_pooling_engine

__all__ = [
    "PoolingTask",
    "PoolingStrategy",
    "PoolingConfig",
    "PoolingResult",
    "EmbeddingOutput",
    "ClassificationOutput",
    "BasePooler",
    "MeanPooler",
    "CLSPooler",
    "LastTokenPooler",
    "MaxPooler",
    "AttentionPooler",
    "WeightedMeanPooler",
    "MatryoshkaPooler",
    "MultiVectorPooler",
    "StepPooler",
    "PoolingEngine",
    "create_pooling_engine"
]


