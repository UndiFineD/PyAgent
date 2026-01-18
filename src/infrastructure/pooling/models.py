# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Data models and Enums for the Pooling Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Dict, List, Any, Tuple
import numpy as np

class PoolingTask(Enum):
    """Supported pooling tasks."""
    EMBED = auto()             # Sentence/document embedding
    CLASSIFY = auto()          # Sequence classification
    SCORE = auto()             # Similarity/relevance scoring
    TOKEN_EMBED = auto()       # Token-level embeddings
    TOKEN_CLASSIFY = auto()    # Token-level classification (NER, etc.)
    RERANK = auto()            # Cross-encoder reranking


class PoolingStrategy(Enum):
    """Pooling strategies for sequence representations."""
    MEAN = auto()              # Mean of all tokens
    CLS = auto()               # First token ([CLS])
    LAST = auto()              # Last token
    MAX = auto()               # Max pooling
    ATTENTION = auto()         # Attention-weighted pooling
    WEIGHTED_MEAN = auto()     # IDF-weighted mean
    FIRST_LAST_AVG = auto()    # Average of first and last hidden states


@dataclass
class PoolingConfig:
    """Configuration for pooling operations."""
    task: PoolingTask = PoolingTask.EMBED
    strategy: PoolingStrategy = PoolingStrategy.MEAN
    truncate_dim: Optional[int] = None           # Matryoshka dimension
    normalize: bool = True                        # L2 normalize output
    return_all_layers: bool = False               # Return all hidden layers
    step_tag_ids: Optional[List[int]] = None     # Token IDs for step pooling
    classifier_head: bool = False                 # Use classification head
    num_labels: int = 2                           # Number of classification labels
    
    def with_dimension(self, dim: int) -> "PoolingConfig":
        """Create copy with different truncation dimension."""
        return PoolingConfig(
            task=self.task,
            strategy=self.strategy,
            truncate_dim=dim,
            normalize=self.normalize,
            return_all_layers=self.return_all_layers,
            step_tag_ids=self.step_tag_ids,
            classifier_head=self.classifier_head,
            num_labels=self.num_labels
        )


@dataclass
class PoolingResult:
    """Result from pooling operation."""
    embeddings: np.ndarray                        # Pooled embeddings
    dimension: int                                # Embedding dimension
    strategy_used: PoolingStrategy = PoolingStrategy.MEAN
    normalized: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def shape(self) -> Tuple[int, ...]:
        return self.embeddings.shape


@dataclass
class EmbeddingOutput:
    """Output for embedding tasks."""
    embedding: np.ndarray                         # Single embedding vector
    tokens_used: int                              # Number of tokens pooled
    truncated: bool = False                       # Was dimension truncated

