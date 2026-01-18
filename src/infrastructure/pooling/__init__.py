
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
    AttentionPooler
)
from .engine import PoolingEngine

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
    "AttentionPooler",
    "PoolingEngine",
    
    # Connection
    "ConnectionState",
    "PoolStats",
    "PooledConnection",
    "ConnectionPool",
    "AsyncConnectionPool",
    "PooledConnectionManager",
    "MultiHostPool",
]

