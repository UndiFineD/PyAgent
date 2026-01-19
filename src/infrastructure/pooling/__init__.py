
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Unified pooling infrastructure (AI and Connections).
"""

# AI Pooling
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
    LastTokenPooler,
    MaxPooler,
    AttentionPooler,
    WeightedMeanPooler,
    MatryoshkaPooler,
    MultiVectorPooler,
    StepPooler
)
from .engine import PoolingEngine, create_pooling_engine

# Connection Pooling
from .ConnectionPool import (
    ConnectionState,
    PoolStats,
    PooledConnection,
    ConnectionPool,
    AsyncConnectionPool,
    PooledConnectionManager,
    MultiHostPool,
)

__all__ = [
    # AI
    "PoolingTask",
    "PoolingStrategy",
    "PoolingConfig",
    "PoolingResult",
    "EmbeddingOutput",
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
    "create_pooling_engine",
    
    # Connection
    "ConnectionState",
    "PoolStats",
    "PooledConnection",
    "ConnectionPool",
    "AsyncConnectionPool",
    "PooledConnectionManager",
    "MultiHostPool",
]

