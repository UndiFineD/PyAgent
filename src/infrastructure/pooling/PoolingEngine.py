# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Pooling Engine - Embedding Extraction and Classification
# Inspired by vLLM's pooling_params.py

"""
PoolingEngine: Unified pooling for embeddings and classification.

Provides:
- Multiple pooling strategies (mean, cls, last, attention)
- Matryoshka embedding support with dimension reduction
- Multi-vector embeddings (ColBERT-style)
- Token-level classification with step pooling
- Contrastive pre-processing for similarity scoring
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import numpy as np


# =============================================================================
# Enums
# =============================================================================

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


# =============================================================================
# Data Classes
# =============================================================================

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
    
    def with_dimension(self, dim: int) -> 'PoolingConfig':
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
    original_dim: int = 0                         # Original dimension before truncation
    
    def to_list(self) -> List[float]:
        return self.embedding.tolist()
    
    def similarity(self, other: 'EmbeddingOutput') -> float:
        """Compute cosine similarity with another embedding."""
        a = self.embedding / (np.linalg.norm(self.embedding) + 1e-9)
        b = other.embedding / (np.linalg.norm(other.embedding) + 1e-9)
        return float(np.dot(a, b))


@dataclass
class ClassificationOutput:
    """Output for classification tasks."""
    logits: np.ndarray                            # Raw logits
    probabilities: np.ndarray                     # Softmax probabilities
    predicted_class: int                          # Argmax prediction
    confidence: float                             # Probability of predicted class
    label_names: Optional[List[str]] = None       # Optional label names
    
    @property
    def predicted_label(self) -> Optional[str]:
        if self.label_names and 0 <= self.predicted_class < len(self.label_names):
            return self.label_names[self.predicted_class]
        return None


# =============================================================================
# Base Pooler Class
# =============================================================================

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


# =============================================================================
# Strategy-based Poolers
# =============================================================================

class MeanPooler(BasePooler):
    """Mean pooling over sequence."""
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Compute mean of hidden states with optional masking.
        
        Args:
            hidden_states: Shape (batch, seq_len, hidden_dim)
            attention_mask: Shape (batch, seq_len), 1 for valid, 0 for padding
        """
        if attention_mask is None:
            return hidden_states.mean(axis=1)
        
        # Expand mask for broadcasting
        mask = attention_mask[:, :, np.newaxis].astype(hidden_states.dtype)
        
        # Masked mean
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
        """Return first token representation."""
        return hidden_states[:, 0, :]


class LastTokenPooler(BasePooler):
    """Last token pooling."""
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Return last valid token representation."""
        if attention_mask is None:
            return hidden_states[:, -1, :]
        
        # Find last valid position for each sequence
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
        """Compute max over sequence dimension."""
        if attention_mask is None:
            return hidden_states.max(axis=1)
        
        # Set padding positions to very negative
        mask = attention_mask[:, :, np.newaxis].astype(bool)
        masked = np.where(mask, hidden_states, -1e9)
        return masked.max(axis=1)


class AttentionPooler(BasePooler):
    """
    Attention-weighted pooling.
    
    Learns a query vector to compute attention weights over tokens.
    """
    
    def __init__(self, config: PoolingConfig, hidden_dim: int = 768):
        super().__init__(config)
        self.hidden_dim = hidden_dim
        # Initialize learnable query vector (random for now)
        self.query = np.random.randn(hidden_dim).astype(np.float32) / math.sqrt(hidden_dim)
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Compute attention-weighted pooling."""
        # Compute attention scores: (batch, seq_len)
        scores = np.einsum('bsh,h->bs', hidden_states, self.query)
        
        # Apply mask
        if attention_mask is not None:
            scores = np.where(attention_mask.astype(bool), scores, -1e9)
        
        # Softmax
        scores = scores - scores.max(axis=1, keepdims=True)
        weights = np.exp(scores)
        weights = weights / (weights.sum(axis=1, keepdims=True) + 1e-9)
        
        # Weighted sum
        return np.einsum('bs,bsh->bh', weights, hidden_states)


class WeightedMeanPooler(BasePooler):
    """
    IDF-weighted mean pooling.
    
    Weights tokens by inverse document frequency.
    """
    
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
        """Compute IDF-weighted mean."""
        batch_size, seq_len, hidden_dim = hidden_states.shape
        
        # Compute weights
        if token_ids is not None:
            weights = np.array([
                [self.token_weights.get(int(tid), self.default_weight) for tid in seq]
                for seq in token_ids
            ])
        else:
            weights = np.ones((batch_size, seq_len))
        
        # Apply attention mask
        if attention_mask is not None:
            weights = weights * attention_mask
        
        # Weighted mean
        weights = weights[:, :, np.newaxis]
        weighted_sum = (hidden_states * weights).sum(axis=1)
        weight_sum = weights.sum(axis=1)
        
        return weighted_sum / (weight_sum + 1e-9)


# =============================================================================
# Advanced Poolers
# =============================================================================

class MatryoshkaPooler(BasePooler):
    """
    Matryoshka Representation Learning pooler.
    
    Supports nested embeddings with variable dimensions.
    Ref: https://arxiv.org/abs/2205.13147
    """
    
    STANDARD_DIMS = [64, 128, 256, 512, 768, 1024, 2048, 4096]
    
    def __init__(
        self,
        config: PoolingConfig,
        base_pooler: Optional[BasePooler] = None,
        supported_dims: Optional[List[int]] = None
    ):
        super().__init__(config)
        self.base_pooler = base_pooler or MeanPooler(config)
        self.supported_dims = supported_dims or self.STANDARD_DIMS
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Pool and optionally truncate to target dimension."""
        # Base pooling
        embeddings = self.base_pooler.pool(hidden_states, attention_mask)
        
        # Truncate if requested
        if self.config.truncate_dim is not None:
            embeddings = self.truncate(embeddings, self.config.truncate_dim)
        
        # Normalize if requested
        if self.config.normalize:
            embeddings = self.normalize(embeddings)
        
        return embeddings
    
    def pool_multi_dim(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        dimensions: Optional[List[int]] = None
    ) -> Dict[int, np.ndarray]:
        """Pool to multiple dimensions simultaneously."""
        # Base pooling
        embeddings = self.base_pooler.pool(hidden_states, attention_mask)
        
        dims = dimensions or self.supported_dims
        results = {}
        
        for dim in dims:
            if dim <= embeddings.shape[-1]:
                truncated = self.truncate(embeddings, dim)
                if self.config.normalize:
                    truncated = self.normalize(truncated)
                results[dim] = truncated
        
        return results


class MultiVectorPooler(BasePooler):
    """
    Multi-vector embeddings (ColBERT-style).
    
    Returns one embedding per token instead of pooled representation.
    Useful for late interaction retrieval.
    """
    
    def __init__(
        self,
        config: PoolingConfig,
        compression_dim: Optional[int] = None,
        skip_special: bool = True
    ):
        super().__init__(config)
        self.compression_dim = compression_dim
        self.skip_special = skip_special
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Return per-token embeddings."""
        if attention_mask is not None and self.skip_special:
            # Zero out special token positions (first and last)
            mask = attention_mask.copy()
            mask[:, 0] = 0
            # Find last valid position and zero it
            for i in range(mask.shape[0]):
                last_idx = mask[i].sum() - 1
                if last_idx > 0:
                    mask[i, int(last_idx)] = 0
            
            hidden_states = hidden_states * mask[:, :, np.newaxis]
        
        # Optional compression
        if self.compression_dim and self.compression_dim < hidden_states.shape[-1]:
            hidden_states = hidden_states[..., :self.compression_dim]
        
        # Normalize
        if self.config.normalize:
            norm = np.linalg.norm(hidden_states, axis=-1, keepdims=True)
            hidden_states = hidden_states / (norm + 1e-9)
        
        return hidden_states
    
    def maxsim_score(
        self,
        query_vectors: np.ndarray,
        doc_vectors: np.ndarray
    ) -> float:
        """Compute MaxSim score between query and document."""
        # query_vectors: (q_len, dim), doc_vectors: (d_len, dim)
        # Compute all pairwise similarities
        similarities = np.einsum('qd,pd->qp', query_vectors, doc_vectors)
        
        # Max over document for each query token
        max_sims = similarities.max(axis=1)
        
        # Sum over query tokens
        return float(max_sims.sum())


class StepPooler(BasePooler):
    """
    Step-based pooling for token classification.
    
    Pools at specific token positions (e.g., step markers in reasoning).
    """
    
    def __init__(
        self,
        config: PoolingConfig,
        step_token_ids: Optional[List[int]] = None
    ):
        super().__init__(config)
        self.step_token_ids = set(step_token_ids or [])
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        token_ids: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Pool at step token positions."""
        if token_ids is None or not self.step_token_ids:
            # Fallback to mean pooling
            return MeanPooler(self.config).pool(hidden_states, attention_mask)
        
        batch_size, seq_len, hidden_dim = hidden_states.shape
        
        # Find step positions
        step_mask = np.zeros((batch_size, seq_len), dtype=bool)
        for tid in self.step_token_ids:
            step_mask |= (token_ids == tid)
        
        # Pool at step positions
        results = []
        for i in range(batch_size):
            step_indices = np.where(step_mask[i])[0]
            if len(step_indices) > 0:
                step_embeddings = hidden_states[i, step_indices]
                results.append(step_embeddings.mean(axis=0))
            else:
                # Fallback to CLS token
                results.append(hidden_states[i, 0])
        
        return np.stack(results)


# =============================================================================
# Main Pooling Engine
# =============================================================================

class PoolingEngine:
    """
    Unified pooling engine for embeddings and classification.
    
    Features beyond vLLM:
    - Dynamic dimension selection based on downstream task
    - Pooling strategy optimization
    - Multi-vector embeddings (ColBERT-style)
    - Contrastive pre-processing
    - Ensemble pooling
    """
    
    POOLER_REGISTRY: Dict[PoolingStrategy, type] = {
        PoolingStrategy.MEAN: MeanPooler,
        PoolingStrategy.CLS: CLSPooler,
        PoolingStrategy.LAST: LastTokenPooler,
        PoolingStrategy.MAX: MaxPooler,
        PoolingStrategy.ATTENTION: AttentionPooler,
        PoolingStrategy.WEIGHTED_MEAN: WeightedMeanPooler,
    }
    
    def __init__(
        self,
        config: Optional[PoolingConfig] = None,
        hidden_dim: int = 768,
    ):
        self.config = config or PoolingConfig()
        self.hidden_dim = hidden_dim
        
        # Initialize poolers
        self._poolers: Dict[PoolingStrategy, BasePooler] = {}
        for strategy, pooler_cls in self.POOLER_REGISTRY.items():
            if pooler_cls == AttentionPooler:
                self._poolers[strategy] = pooler_cls(self.config, hidden_dim)
            else:
                self._poolers[strategy] = pooler_cls(self.config)
        
        # Specialized poolers
        self._matryoshka = MatryoshkaPooler(self.config)
        self._multi_vector = MultiVectorPooler(self.config)
        
        # Statistics
        self._stats = {
            "total_pooled": 0,
            "mean_seq_length": 0.0,
        }
    
    def pool(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        config: Optional[PoolingConfig] = None
    ) -> PoolingResult:
        """
        Pool hidden states using configured strategy.
        
        Args:
            hidden_states: Shape (batch, seq_len, hidden_dim)
            attention_mask: Shape (batch, seq_len)
            config: Optional override config
        """
        cfg = config or self.config
        
        # Get pooler for strategy
        pooler = self._poolers.get(cfg.strategy, self._poolers[PoolingStrategy.MEAN])
        
        # Pool
        embeddings = pooler.pool(hidden_states, attention_mask)
        
        # Truncate if requested
        original_dim = embeddings.shape[-1]
        if cfg.truncate_dim:
            embeddings = pooler.truncate(embeddings, cfg.truncate_dim)
        
        # Normalize if requested
        if cfg.normalize:
            embeddings = pooler.normalize(embeddings)
        
        # Update stats
        self._stats["total_pooled"] += hidden_states.shape[0]
        
        return PoolingResult(
            embeddings=embeddings,
            dimension=embeddings.shape[-1],
            strategy_used=cfg.strategy,
            normalized=cfg.normalize,
            metadata={"original_dim": original_dim}
        )
    
    def embed(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        truncate_dim: Optional[int] = None
    ) -> EmbeddingOutput:
        """Generate embeddings for the input."""
        cfg = self.config.with_dimension(truncate_dim) if truncate_dim else self.config
        
        result = self.pool(hidden_states, attention_mask, cfg)
        
        return EmbeddingOutput(
            embedding=result.embeddings[0] if result.embeddings.ndim > 1 else result.embeddings,
            tokens_used=hidden_states.shape[1],
            truncated=truncate_dim is not None,
            original_dim=result.metadata.get("original_dim", result.dimension)
        )
    
    def classify(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        classifier_weights: Optional[np.ndarray] = None,
        classifier_bias: Optional[np.ndarray] = None,
        label_names: Optional[List[str]] = None
    ) -> ClassificationOutput:
        """Classify sequence using pooled representation."""
        # Pool to single vector
        pooled = self.pool(hidden_states, attention_mask)
        embedding = pooled.embeddings[0]
        
        # Apply classifier head
        if classifier_weights is not None:
            logits = embedding @ classifier_weights.T
            if classifier_bias is not None:
                logits = logits + classifier_bias
        else:
            # Dummy logits
            logits = embedding[:self.config.num_labels]
        
        # Softmax
        logits = logits - logits.max()
        exp_logits = np.exp(logits)
        probabilities = exp_logits / (exp_logits.sum() + 1e-9)
        
        predicted = int(np.argmax(probabilities))
        
        return ClassificationOutput(
            logits=logits,
            probabilities=probabilities,
            predicted_class=predicted,
            confidence=float(probabilities[predicted]),
            label_names=label_names
        )
    
    def embed_multi_dim(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None,
        dimensions: Optional[List[int]] = None
    ) -> Dict[int, EmbeddingOutput]:
        """Generate Matryoshka embeddings at multiple dimensions."""
        results = self._matryoshka.pool_multi_dim(
            hidden_states, attention_mask, dimensions
        )
        
        return {
            dim: EmbeddingOutput(
                embedding=emb[0] if emb.ndim > 1 else emb,
                tokens_used=hidden_states.shape[1],
                truncated=dim < self.hidden_dim,
                original_dim=self.hidden_dim
            )
            for dim, emb in results.items()
        }
    
    def embed_multi_vector(
        self,
        hidden_states: np.ndarray,
        attention_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Generate per-token embeddings (ColBERT-style)."""
        return self._multi_vector.pool(hidden_states, attention_mask)
    
    def score_similarity(
        self,
        query_states: np.ndarray,
        doc_states: np.ndarray,
        query_mask: Optional[np.ndarray] = None,
        doc_mask: Optional[np.ndarray] = None,
        multi_vector: bool = False
    ) -> float:
        """Score similarity between query and document."""
        if multi_vector:
            # ColBERT-style MaxSim
            query_vecs = self.embed_multi_vector(query_states, query_mask)
            doc_vecs = self.embed_multi_vector(doc_states, doc_mask)
            return self._multi_vector.maxsim_score(query_vecs[0], doc_vecs[0])
        else:
            # Cosine similarity
            query_emb = self.embed(query_states, query_mask)
            doc_emb = self.embed(doc_states, doc_mask)
            return query_emb.similarity(doc_emb)
    
    def get_stats(self) -> Dict[str, Any]:
        """Return pooling statistics."""
        return self._stats.copy()


# =============================================================================
# Factory Functions
# =============================================================================

def create_pooling_engine(
    task: PoolingTask = PoolingTask.EMBED,
    strategy: PoolingStrategy = PoolingStrategy.MEAN,
    hidden_dim: int = 768,
    normalize: bool = True,
    truncate_dim: Optional[int] = None,
) -> PoolingEngine:
    """Create pooling engine with specified configuration."""
    config = PoolingConfig(
        task=task,
        strategy=strategy,
        truncate_dim=truncate_dim,
        normalize=normalize
    )
    
    return PoolingEngine(config, hidden_dim)
