#!/usr/bin/env python3
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
Unified pooling infrastructure (AI and Connections).

# Connection Pooling
try:
    from .connection_pool import (AsyncConnectionPool, ConnectionPool,  # noqa: F401
except ImportError:
    from .connection_pool import (AsyncConnectionPool, ConnectionPool, # noqa: F401

                              ConnectionState, MultiHostPool, PooledConnection,
                              PooledConnectionManager, PoolStats)
try:
    from .engine import PoolingEngine, create_pooling_engine  # noqa: F401
except ImportError:
    from .engine import PoolingEngine, create_pooling_engine # noqa: F401

# AI Pooling
try:
    from .models import (EmbeddingOutput, PoolingConfig, PoolingResult,  # noqa: F401
except ImportError:
    from .models import (EmbeddingOutput, PoolingConfig, PoolingResult, # noqa: F401

                     PoolingStrategy, PoolingTask)
try:
    from .strategies import (AttentionPooler, BasePooler, CLSPooler,  # noqa: F401
except ImportError:
    from .strategies import (AttentionPooler, BasePooler, CLSPooler, # noqa: F401

                         LastTokenPooler, MatryoshkaPooler, MaxPooler,
                         MeanPooler, MultiVectorPooler, StepPooler,
                         WeightedMeanPooler)

__all__ = [
    # AI
    "PoolingTask","    "PoolingStrategy","    "PoolingConfig","    "PoolingResult","    "EmbeddingOutput","    "BasePooler","    "MeanPooler","    "CLSPooler","    "LastTokenPooler","    "MaxPooler","    "AttentionPooler","    "WeightedMeanPooler","    "MatryoshkaPooler","    "MultiVectorPooler","    "StepPooler","    "PoolingEngine","    "create_pooling_engine","    # Connection
    "ConnectionState","    "PoolStats","    "PooledConnection","    "ConnectionPool","    "AsyncConnectionPool","    "PooledConnectionManager","    "MultiHostPool","]
