import os
import math
from typing import Tuple, Optional, Any, List, Set, Dict, Union
from abc import ABC, abstractmethod

try:
    import torch
    import torch.nn as torch_nn
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from .config import RoPEConfig, RoPEVariant

class RotaryEmbeddingBase(ABC):
    """Base class for all RoPE implementations."""

    def __init__(self, config: RoPEConfig):
        self.config = config
        self.head_dim = config.head_dim
        self.rotary_dim = config.rotary_dim
        self.base = config.base

        # Cache for cos/sin values
        self._cos_cache: Optional[Any] = None
        self._sin_cache: Optional[Any] = None
        self._cache_seq_len = 0

    @abstractmethod
    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Core implementation of the rotation."""
        pass

    def forward(
        self,
        positions: Any,
        query: Any,
        key: Any,
        use_cuda: bool = True,
    ) -> Tuple[Any, Any]:
        """Apply rotary embeddings with optional hardware acceleration."""
        # Generic wrapper that handles framework dispatch
        return self.forward_native(positions, query, key)

    def _ensure_cache(self, seq_len: int) -> None:
        """Ensure the cos/sin cache is large enough."""
        if self._cache_seq_len < seq_len:
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(
                max(seq_len, 2048)
            )
            self._cache_seq_len = max(seq_len, 2048)

    @abstractmethod
    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute the cos/sin cache for the given length."""
        pass
