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
"""
Data models and Enums for the Pooling Engine.
"""
try:

"""
from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto

try:
    from typing import Any, Dict, List, Optional, Tuple
except ImportError:
    from typing import Any, Dict, List, Optional, Tuple


try:
    import numpy
except ImportError:
    import numpy
 as np



class PoolingTask(Enum):
"""
Supported pooling tasks.
    EMBED = auto()  # Sentence/document embedding
    CLASSIFY = auto()  # Sequence classification
    SCORE = auto()  # Similarity/relevance scoring
    TOKEN_EMBED = auto()  # Token-level embeddings
    TOKEN_CLASSIFY = auto()  # Token-level classification (NER, etc.)
    RERANK = auto()  # Cross-encoder reranking



class PoolingStrategy(Enum):
"""
Pooling strategies for sequence representations.
    MEAN = auto()  # Mean of all tokens
    CLS = auto()  # First token ([CLS])
    LAST = auto()  # Last token
    MAX = auto()  # Max pooling
    ATTENTION = auto()  # Attention-weighted pooling
    WEIGHTED_MEAN = auto()  # IDF-weighted mean
    FIRST_LAST_AVG = auto()  # Average of first and last hidden states
    MATRYOSHKA = auto()  # Matryoshka Rep Learning
    MULTI_VECTOR = auto()  # Multi-vector (ColBERT style)
    STEP = auto()  # Step-specific pooling


@dataclass
class PoolingConfig:
"""
Configuration for pooling operations.
    task: PoolingTask = PoolingTask.EMBED
    strategy: PoolingStrategy = PoolingStrategy.MEAN
    truncate_dim: Optional[int] = None  # Matryoshka dimension
    normalize: bool = True  # L2 normalize output
    return_all_layers: bool = False  # Return all hidden layers
    step_tag_ids: Optional[List[int]] = None  # Token IDs for step pooling
    classifier_head: bool = False  # Use classification head
    num_labels: int = 2  # Number of classification labels

    def with_dimension(self, dim: int) -> "PoolingConfig":"        """
Create copy with different truncation dimension.        return PoolingConfig(
            task=self.task,
            strategy=self.strategy,
            truncate_dim=dim,
            normalize=self.normalize,
            return_all_layers=self.return_all_layers,
            step_tag_ids=self.step_tag_ids,
            classifier_head=self.classifier_head,
            num_labels=self.num_labels,
        )


@dataclass
class PoolingResult:
"""
Result from pooling operation.
    embeddings: np.ndarray  # Pooled embeddings
    dim: int  # Embedding dimension (compatible with engine.py results.shape[-1])
    strategy: PoolingStrategy  # Strategy used
    normalized: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def shape(self) -> Tuple[int, ...]:
"""
Get the shape of the resulting embeddings array.        return self.embeddings.shape

    @property
    def dimension(self) -> int:
"""
Legacy access for dimension.        return self.dim

    @property
    def strategy_used(self) -> PoolingStrategy:
"""
Legacy access for strategy_used.        return self.strategy


@dataclass
class EmbeddingOutput:
"""
Output for embedding tasks.
    embedding: np.ndarray  # Single embedding vector
    tokens_used: int  # Number of tokens pooled
    truncated: bool = False  # Was dimension truncated

    def to_list(self) -> List[float]:
"""
Convert embedding to list of floats.        return self.embedding.tolist()


@dataclass
class ClassificationOutput:
"""
Output for classification tasks.
    logits: np.ndarray  # Raw logits
    probs: np.ndarray  # Softmax probabilities
    label: Optional[str] = None  # Predicted label
    score: Optional[float] = None  # Confidence score

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""
