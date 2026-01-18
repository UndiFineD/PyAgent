
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
    EmbeddingOutput
)
from .strategies import (
    BasePooler,
    MeanPooler,
    CLSPooler,
    AttentionPooler
)
from .engine import PoolingEngine

__all__ = [
    "PoolingTask",
    "PoolingStrategy",
    "PoolingConfig",
    "PoolingResult",
    "EmbeddingOutput",
    "BasePooler",
    "MeanPooler",
    "CLSPooler",
    "AttentionPooler",
    "PoolingEngine"
]

