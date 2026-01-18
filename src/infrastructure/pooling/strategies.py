# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Strategy-based poolers for sequence representations.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple, List
import numpy as np

from .models import PoolingConfig, PoolingStrategy


class BasePooler(ABC):
    """Abstract base for pooling operations."""
    
    def __init__(self, config: PoolingConfig):
        self.config = config
    
    @abstractmethod
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Pool hidden states to fixed representation."""
        pass
    
    def normalize(self, embeddings: np.ndarray) -> np.ndarray:
        """L2 normalize embeddings."""
        norm = np.linalg.norm(embeddings, axis=-1, keepdims=True)
        return embeddings / (norm + 1e-9)
    
    def truncate(self, embeddings: np.ndarray, dim: int) -> np.ndarray:
        """Truncate embeddings to specified dimension (Matryoshka)."""
        if dim >= embeddings.shape[-1]:
            return embeddings
        return embeddings[..., :dim]


class MeanPooler(BasePooler):
    """Mean pooling over sequence."""
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Compute mean of hidden states with optional masking."""
        if attention_mask is None:
            return hidden_states.mean(axis=1)
        
        mask = attention_mask[:, :, np.newaxis].astype(hidden_states.dtype)
        masked_sum = (hidden_states * mask).sum(axis=1)
        mask_sum = mask.sum(axis=1)
        return masked_sum / (mask_sum + 1e-9)


class CLSPooler(BasePooler):
    """First token ([CLS]) pooling."""
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        return hidden_states[:, 0, :]


class LastTokenPooler(BasePooler):
    """Last token pooling."""
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        if attention_mask is None:
            return hidden_states[:, -1, :]
        
        batch_size = hidden_states.shape[0]
        last_indices = attention_mask.sum(axis=1).astype(int) - 1
        last_indices = np.clip(last_indices, 0, hidden_states.shape[1] - 1)
        return hidden_states[np.arange(batch_size), last_indices]


class MaxPooler(BasePooler):
    """Max pooling over sequence."""
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        if attention_mask is None:
            return hidden_states.max(axis=1)
        
        mask = attention_mask[:, :, np.newaxis].astype(bool)
        masked = np.where(mask, hidden_states, -1e9)
        return masked.max(axis=1)


class AttentionPooler(BasePooler):
    """Attention-weighted pooling."""
    
    def __init__(self, config: PoolingConfig, hidden_dim: int = 768):
        super().__init__(config)
        self.hidden_dim = hidden_dim
        self.query = np.random.randn(hidden_dim).astype(np.float32) / math.sqrt(hidden_dim)
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        scores = np.einsum('bsh,h->bs', hidden_states, self.query)
        if attention_mask is not None:
            scores = np.where(attention_mask.astype(bool), scores, -1e9)
        
        scores = scores - scores.max(axis=1, keepdims=True)
        weights = np.exp(scores)
        weights = weights / (weights.sum(axis=1, keepdims=True) + 1e-9)
        return np.einsum('bs,bsh->bh', weights, hidden_states)


class WeightedMeanPooler(BasePooler):
    """IDF-weighted mean pooling."""
    
    def __init__(self, config: PoolingConfig, token_weights: Optional[Dict[int, float]] = None):
        super().__init__(config)
        self.token_weights = token_weights or {}
        self.default_weight = 1.0
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        token_ids: Optional[np.ndarray] = None
    ) -> np.ndarray:
        if token_ids is None or not self.token_weights:
            return MeanPooler(self.config).pool(hidden_states, attention_mask)
            
        weights = np.array([[self.token_weights.get(int(tid), self.default_weight) for tid in row] for row in token_ids])
        if attention_mask is not None:
            weights = weights * attention_mask
            
        weights = weights[:, :, np.newaxis]
        weighted_sum = (hidden_states * weights).sum(axis=1)
        weights_sum = weights.sum(axis=1)
        return weighted_sum / (weights_sum + 1e-9)
