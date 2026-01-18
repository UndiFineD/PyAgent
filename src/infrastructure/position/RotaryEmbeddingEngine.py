# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
Rotary Position Embedding Engine - Unified RoPE implementation with multiple variants.

Provides a unified interface for various rotary position embedding methods
discovered in vLLM's model_executor/layers/rotary_embedding.py.

Key patterns from vLLM:
- RotaryEmbedding base with forward_native/forward_cuda
- MRotaryEmbedding for multimodal (3D: temporal/height/width)
- XDRotaryEmbedding with dynamic NTK alpha scaling
- DualChunkRotaryEmbedding for dual chunk attention
- DeepseekScalingRotaryEmbedding with FlashInfer integration

Beyond vLLM:
- Automatic variant detection from model configuration
- Unified interface for all variants
- Runtime variant switching
- Precomputed frequency caching
"""

from __future__ import annotations

import logging
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

# Try to import PyTorch, but allow graceful fallback
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    nn = None

# Try to import numpy for CPU fallback
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None


class RoPEVariant(Enum):
    """Supported rotary position embedding variants.
    
    Based on vLLM's rotary_embedding.py implementations.
    """
    NEOX = auto()           # Standard NeoX-style RoPE
    GPTJ = auto()           # GPT-J style (interleaved)
    MROPE = auto()          # Multimodal RoPE (3D sections)
    XDROPE = auto()         # Extended Dynamic RoPE (NTK scaling)
    DUAL_CHUNK = auto()     # Dual chunk attention RoPE
    DEEPSEEK = auto()       # Deepseek scaling with FlashInfer
    LINEAR = auto()         # Linear position scaling
    YARN = auto()           # YaRN (Yet another RoPE extensioN)
    LONGROPE = auto()       # LongRoPE with multi-scale
    

class RoPEScalingType(Enum):
    """Scaling types for extended context."""
    NONE = auto()
    LINEAR = auto()         # Linear interpolation
    DYNAMIC = auto()        # Dynamic NTK
    YARN = auto()           # YaRN scaling
    LONGROPE = auto()       # LongRoPE scaling


@dataclass
class RoPEConfig:
    """Configuration for rotary position embeddings.
    
    Inspired by vLLM's RoPE configuration patterns.
    """
    head_dim: int = 64
    rotary_dim: Optional[int] = None  # Defaults to head_dim
    max_position_embeddings: int = 2048
    base: float = 10000.0
    is_neox_style: bool = True  # True for NeoX, False for GPT-J
    
    # Scaling configuration
    scaling_type: RoPEScalingType = RoPEScalingType.NONE
    scaling_factor: float = 1.0
    
    # Dynamic NTK configuration
    dynamic_scaling: bool = False
    original_max_position: int = 2048
    
    # YaRN configuration
    yarn_beta_fast: float = 32.0
    yarn_beta_slow: float = 1.0
    yarn_mscale: float = 1.0
    yarn_mscale_all_dim: float = 0.0
    
    # Multimodal RoPE configuration
    mrope_sections: Optional[List[int]] = None  # [temporal, height, width]
    
    # LongRoPE configuration
    longrope_short_mscale: float = 1.0
    longrope_long_mscale: float = 1.0
    longrope_short_factor: Optional[List[float]] = None
    longrope_long_factor: Optional[List[float]] = None
    
    # Device configuration
    dtype: Optional[Any] = None  # torch.dtype
    device: Optional[str] = None
    
    def __post_init__(self):
        if self.rotary_dim is None:
            self.rotary_dim = self.head_dim
    
    @property
    def variant(self) -> RoPEVariant:
        """Detect RoPE variant from configuration."""
        if self.mrope_sections is not None:
            return RoPEVariant.MROPE
        if self.scaling_type == RoPEScalingType.YARN:
            return RoPEVariant.YARN
        if self.scaling_type == RoPEScalingType.LONGROPE:
            return RoPEVariant.LONGROPE
        if self.dynamic_scaling:
            return RoPEVariant.XDROPE
        if self.scaling_type == RoPEScalingType.LINEAR:
            return RoPEVariant.LINEAR
        if self.is_neox_style:
            return RoPEVariant.NEOX
        return RoPEVariant.GPTJ


class RotaryEmbeddingBase(ABC):
    """Abstract base class for rotary position embeddings.
    
    Inspired by vLLM's RotaryEmbedding class structure.
    """
    
    def __init__(self, config: RoPEConfig):
        self.config = config
        self.head_dim = config.head_dim
        self.rotary_dim = config.rotary_dim or config.head_dim
        self.max_position = config.max_position_embeddings
        self.base = config.base
        self.is_neox_style = config.is_neox_style
        
        # Frequency cache
        self._cos_cache: Optional[Any] = None
        self._sin_cache: Optional[Any] = None
        self._cache_seq_len: int = 0
        
    @abstractmethod
    def _compute_inv_freq(self) -> Any:
        """Compute inverse frequencies for the embedding."""
        ...
    
    @abstractmethod
    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute cos/sin cache for positions up to max_len."""
        ...
    
    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply rotary embeddings using native (CPU/numpy) implementation.
        
        Args:
            positions: Position indices [batch, seq_len] or [seq_len]
            query: Query tensor [batch, seq_len, num_heads, head_dim]
            key: Key tensor [batch, seq_len, num_kv_heads, head_dim]
            
        Returns:
            Tuple of (rotated_query, rotated_key)
        """
        raise NotImplementedError("Subclass must implement forward_native")
    
    def forward_cuda(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply rotary embeddings using CUDA-optimized implementation.
        
        Args:
            positions: Position indices
            query: Query tensor
            key: Key tensor
            
        Returns:
            Tuple of (rotated_query, rotated_key)
        """
        # Default to native implementation
        return self.forward_native(positions, query, key)
    
    def forward(
        self,
        positions: Any,
        query: Any,
        key: Any,
        use_cuda: bool = True,
    ) -> Tuple[Any, Any]:
        """Apply rotary embeddings with automatic backend selection.
        
        Args:
            positions: Position indices
            query: Query tensor
            key: Key tensor
            use_cuda: Whether to prefer CUDA implementation
            
        Returns:
            Tuple of (rotated_query, rotated_key)
        """
        if use_cuda and TORCH_AVAILABLE and torch.cuda.is_available():
            return self.forward_cuda(positions, query, key)
        return self.forward_native(positions, query, key)


class NeoxRotaryEmbedding(RotaryEmbeddingBase):
    """NeoX-style rotary position embedding.
    
    Standard RoPE implementation where rotation is applied to
    first and second halves of the head dimension separately.
    
    Inspired by vLLM's RotaryEmbedding with is_neox_style=True.
    """
    
    def __init__(self, config: RoPEConfig):
        config.is_neox_style = True
        super().__init__(config)
        self.inv_freq = self._compute_inv_freq()
    
    def _compute_inv_freq(self) -> Any:
        """Compute inverse frequencies."""
        if TORCH_AVAILABLE:
            inv_freq = 1.0 / (
                self.base ** (
                    torch.arange(0, self.rotary_dim, 2, dtype=torch.float32) 
                    / self.rotary_dim
                )
            )
            return inv_freq
        elif NUMPY_AVAILABLE:
            inv_freq = 1.0 / (
                self.base ** (
                    np.arange(0, self.rotary_dim, 2, dtype=np.float32) 
                    / self.rotary_dim
                )
            )
            return inv_freq
        else:
            # Pure Python fallback
            inv_freq = []
            for i in range(0, self.rotary_dim, 2):
                inv_freq.append(1.0 / (self.base ** (i / self.rotary_dim)))
            return inv_freq
    
    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute cos/sin cache for positions."""
        if TORCH_AVAILABLE:
            t = torch.arange(max_len, dtype=torch.float32)
            freqs = torch.outer(t, self.inv_freq)
            cos_cache = torch.cos(freqs)
            sin_cache = torch.sin(freqs)
            return cos_cache, sin_cache
        elif NUMPY_AVAILABLE:
            t = np.arange(max_len, dtype=np.float32)
            freqs = np.outer(t, self.inv_freq)
            cos_cache = np.cos(freqs)
            sin_cache = np.sin(freqs)
            return cos_cache, sin_cache
        else:
            raise RuntimeError("No numerical backend available")
    
    def _ensure_cache(self, seq_len: int) -> None:
        """Ensure cos/sin cache is large enough."""
        if seq_len > self._cache_seq_len:
            new_len = max(seq_len, self._cache_seq_len * 2, 2048)
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(new_len)
            self._cache_seq_len = new_len
    
    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply NeoX-style rotary embeddings."""
        if TORCH_AVAILABLE and isinstance(positions, torch.Tensor):
            return self._forward_torch(positions, query, key)
        elif NUMPY_AVAILABLE:
            return self._forward_numpy(positions, query, key)
        else:
            raise RuntimeError("No numerical backend available")
    
    def _forward_torch(
        self,
        positions: "torch.Tensor",
        query: "torch.Tensor",
        key: "torch.Tensor",
    ) -> Tuple["torch.Tensor", "torch.Tensor"]:
        """PyTorch implementation of NeoX RoPE."""
        seq_len = int(positions.max().item()) + 1
        self._ensure_cache(seq_len)
        
        # Get cos/sin for positions
        cos = self._cos_cache[positions]  # [batch, seq, rotary_dim//2]
        sin = self._sin_cache[positions]
        
        # Apply rotation to query and key
        def rotate_half(x: "torch.Tensor") -> "torch.Tensor":
            x1 = x[..., : x.shape[-1] // 2]
            x2 = x[..., x.shape[-1] // 2 :]
            return torch.cat((-x2, x1), dim=-1)
        
        # Apply to query
        q_rotary = query[..., :self.rotary_dim]
        q_pass = query[..., self.rotary_dim:]
        
        cos_q = cos.unsqueeze(-2)  # Add head dimension
        sin_q = sin.unsqueeze(-2)
        
        q_rotated = q_rotary * cos_q + rotate_half(q_rotary) * sin_q
        query_out = torch.cat([q_rotated, q_pass], dim=-1) if q_pass.numel() > 0 else q_rotated
        
        # Apply to key
        k_rotary = key[..., :self.rotary_dim]
        k_pass = key[..., self.rotary_dim:]
        
        k_rotated = k_rotary * cos_q + rotate_half(k_rotary) * sin_q
        key_out = torch.cat([k_rotated, k_pass], dim=-1) if k_pass.numel() > 0 else k_rotated
        
        return query_out, key_out
    
    def _forward_numpy(
        self,
        positions: "np.ndarray",
        query: "np.ndarray",
        key: "np.ndarray",
    ) -> Tuple["np.ndarray", "np.ndarray"]:
        """NumPy implementation of NeoX RoPE."""
        seq_len = int(positions.max()) + 1
        self._ensure_cache(seq_len)
        
        cos = self._cos_cache[positions]
        sin = self._sin_cache[positions]
        
        def rotate_half(x: "np.ndarray") -> "np.ndarray":
            x1 = x[..., : x.shape[-1] // 2]
            x2 = x[..., x.shape[-1] // 2 :]
            return np.concatenate((-x2, x1), axis=-1)
        
        q_rotary = query[..., :self.rotary_dim]
        cos_q = np.expand_dims(cos, axis=-2)
        sin_q = np.expand_dims(sin, axis=-2)
        
        q_rotated = q_rotary * cos_q + rotate_half(q_rotary) * sin_q
        k_rotary = key[..., :self.rotary_dim]
        k_rotated = k_rotary * cos_q + rotate_half(k_rotary) * sin_q
        
        return q_rotated, k_rotated


class GptJRotaryEmbedding(RotaryEmbeddingBase):
    """GPT-J style rotary position embedding.
    
    Interleaved rotation pattern where pairs of dimensions
    are rotated together.
    
    Inspired by vLLM's RotaryEmbedding with is_neox_style=False.
    """
    
    def __init__(self, config: RoPEConfig):
        config.is_neox_style = False
        super().__init__(config)
        self.inv_freq = self._compute_inv_freq()
    
    def _compute_inv_freq(self) -> Any:
        """Compute inverse frequencies."""
        if TORCH_AVAILABLE:
            return 1.0 / (
                self.base ** (
                    torch.arange(0, self.rotary_dim, 2, dtype=torch.float32)
                    / self.rotary_dim
                )
            )
        elif NUMPY_AVAILABLE:
            return 1.0 / (
                self.base ** (
                    np.arange(0, self.rotary_dim, 2, dtype=np.float32)
                    / self.rotary_dim
                )
            )
        raise RuntimeError("No numerical backend available")
    
    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute cos/sin cache."""
        if TORCH_AVAILABLE:
            t = torch.arange(max_len, dtype=torch.float32)
            freqs = torch.outer(t, self.inv_freq)
            # Interleaved pattern: [cos0, cos0, cos1, cos1, ...]
            cos_cache = torch.cos(freqs).repeat_interleave(2, dim=-1)
            sin_cache = torch.sin(freqs).repeat_interleave(2, dim=-1)
            return cos_cache, sin_cache
        elif NUMPY_AVAILABLE:
            t = np.arange(max_len, dtype=np.float32)
            freqs = np.outer(t, self.inv_freq)
            cos_cache = np.repeat(np.cos(freqs), 2, axis=-1)
            sin_cache = np.repeat(np.sin(freqs), 2, axis=-1)
            return cos_cache, sin_cache
        raise RuntimeError("No numerical backend available")
    
    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply GPT-J style rotary embeddings."""
        # Similar to NeoX but with interleaved rotation
        seq_len = int(positions.max()) + 1 if NUMPY_AVAILABLE else positions.max().item() + 1
        
        if self._cache_seq_len < seq_len:
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(
                max(seq_len, 2048)
            )
            self._cache_seq_len = max(seq_len, 2048)
        
        if TORCH_AVAILABLE and isinstance(positions, torch.Tensor):
            cos = self._cos_cache[positions].unsqueeze(-2)
            sin = self._sin_cache[positions].unsqueeze(-2)
            
            def rotate_interleaved(x: "torch.Tensor") -> "torch.Tensor":
                x1 = x[..., ::2]
                x2 = x[..., 1::2]
                rotated = torch.stack((-x2, x1), dim=-1).flatten(-2)
                return rotated
            
            q_rotated = query * cos + rotate_interleaved(query) * sin
            k_rotated = key * cos + rotate_interleaved(key) * sin
            return q_rotated, k_rotated
        
        raise RuntimeError("GPT-J RoPE requires PyTorch")


class MRotaryEmbedding(RotaryEmbeddingBase):
    """Multimodal Rotary Position Embedding.
    
    Applies separate rotary embeddings for different modality sections:
    - Temporal (time/frame index)
    - Height (spatial y)
    - Width (spatial x)
    
    Inspired by vLLM's MRotaryEmbedding for vision-language models.
    """
    
    def __init__(self, config: RoPEConfig):
        super().__init__(config)
        self.mrope_sections = config.mrope_sections or [8, 8, 8]
        assert len(self.mrope_sections) == 3, "Need 3 sections: temporal, height, width"
        assert sum(self.mrope_sections) * 2 <= self.rotary_dim
        
        self.inv_freq = self._compute_inv_freq()
    
    def _compute_inv_freq(self) -> Any:
        """Compute inverse frequencies for each section."""
        if not TORCH_AVAILABLE:
            raise RuntimeError("MRotaryEmbedding requires PyTorch")
        
        inv_freqs = []
        for section_size in self.mrope_sections:
            inv_freq = 1.0 / (
                self.base ** (
                    torch.arange(0, section_size * 2, 2, dtype=torch.float32)
                    / (section_size * 2)
                )
            )
            inv_freqs.append(inv_freq)
        return inv_freqs
    
    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute cos/sin cache for each section."""
        if not TORCH_AVAILABLE:
            raise RuntimeError("MRotaryEmbedding requires PyTorch")
        
        t = torch.arange(max_len, dtype=torch.float32)
        
        cos_caches = []
        sin_caches = []
        
        for inv_freq in self.inv_freq:
            freqs = torch.outer(t, inv_freq)
            cos_caches.append(torch.cos(freqs))
            sin_caches.append(torch.sin(freqs))
        
        return cos_caches, sin_caches
    
    def forward_native(
        self,
        positions: Any,  # [3, seq_len] for temporal, height, width
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply multimodal rotary embeddings.
        
        Args:
            positions: 3D position tensor [3, seq_len] with temporal, height, width
            query: Query tensor
            key: Key tensor
        """
        if not TORCH_AVAILABLE:
            raise RuntimeError("MRotaryEmbedding requires PyTorch")
        
        if positions.dim() == 1:
            # Fallback to single positions
            positions = positions.unsqueeze(0).expand(3, -1)
        
        seq_len = int(positions.max().item()) + 1
        if self._cache_seq_len < seq_len:
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(
                max(seq_len, 2048)
            )
            self._cache_seq_len = max(seq_len, 2048)
        
        # Apply rotation for each section
        q_parts = []
        k_parts = []
        
        dim_offset = 0
        for i, section_size in enumerate(self.mrope_sections):
            section_dim = section_size * 2
            pos_i = positions[i]  # [seq_len]
            
            cos = self._cos_cache[i][pos_i]  # [seq_len, section_size]
            sin = self._sin_cache[i][pos_i]
            
            q_section = query[..., dim_offset:dim_offset + section_dim]
            k_section = key[..., dim_offset:dim_offset + section_dim]
            
            # Apply rotation
            q_rot, k_rot = self._apply_rotation(q_section, k_section, cos, sin)
            q_parts.append(q_rot)
            k_parts.append(k_rot)
            
            dim_offset += section_dim
        
        # Passthrough for remaining dimensions
        if dim_offset < query.shape[-1]:
            q_parts.append(query[..., dim_offset:])
            k_parts.append(key[..., dim_offset:])
        
        return torch.cat(q_parts, dim=-1), torch.cat(k_parts, dim=-1)
    
    def _apply_rotation(
        self,
        q: "torch.Tensor",
        k: "torch.Tensor",
        cos: "torch.Tensor",
        sin: "torch.Tensor",
    ) -> Tuple["torch.Tensor", "torch.Tensor"]:
        """Apply rotation to a section."""
        def rotate_half(x: "torch.Tensor") -> "torch.Tensor":
            x1 = x[..., : x.shape[-1] // 2]
            x2 = x[..., x.shape[-1] // 2 :]
            return torch.cat((-x2, x1), dim=-1)
        
        cos = cos.unsqueeze(-2)
        sin = sin.unsqueeze(-2)
        
        q_rot = q * cos + rotate_half(q) * sin
        k_rot = k * cos + rotate_half(k) * sin
        
        return q_rot, k_rot


class XDRotaryEmbedding(RotaryEmbeddingBase):
    """Extended Dynamic Rotary Position Embedding.
    
    Implements dynamic NTK-aware scaling for extended context lengths.
    The base frequency is dynamically adjusted based on sequence length.
    
    Inspired by vLLM's DynamicNTKScalingRotaryEmbedding.
    """
    
    def __init__(self, config: RoPEConfig):
        super().__init__(config)
        self.scaling_factor = config.scaling_factor
        self.original_max_position = config.original_max_position
        
        # Alpha calculation for dynamic NTK
        self._current_seq_len = 0
        self._current_base = self.base
        self.inv_freq = self._compute_inv_freq()
    
    def _compute_inv_freq(self, base: Optional[float] = None) -> Any:
        """Compute inverse frequencies with optional custom base."""
        base = base or self.base
        if TORCH_AVAILABLE:
            return 1.0 / (
                base ** (
                    torch.arange(0, self.rotary_dim, 2, dtype=torch.float32)
                    / self.rotary_dim
                )
            )
        elif NUMPY_AVAILABLE:
            return 1.0 / (
                base ** (
                    np.arange(0, self.rotary_dim, 2, dtype=np.float32)
                    / self.rotary_dim
                )
            )
        raise RuntimeError("No numerical backend available")
    
    def _compute_dynamic_base(self, seq_len: int) -> float:
        """Compute dynamically scaled base for sequence length."""
        if seq_len <= self.original_max_position:
            return self.base
        
        # NTK-aware scaling
        alpha = (seq_len / self.original_max_position) ** (
            self.rotary_dim / (self.rotary_dim - 2)
        )
        return self.base * alpha
    
    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute cos/sin cache with dynamic scaling."""
        # Update base if sequence length increased
        new_base = self._compute_dynamic_base(max_len)
        
        if new_base != self._current_base:
            self._current_base = new_base
            self.inv_freq = self._compute_inv_freq(new_base)
        
        if TORCH_AVAILABLE:
            t = torch.arange(max_len, dtype=torch.float32)
            freqs = torch.outer(t, self.inv_freq)
            return torch.cos(freqs), torch.sin(freqs)
        elif NUMPY_AVAILABLE:
            t = np.arange(max_len, dtype=np.float32)
            freqs = np.outer(t, self.inv_freq)
            return np.cos(freqs), np.sin(freqs)
        raise RuntimeError("No numerical backend available")
    
    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply XD rotary embeddings with dynamic scaling."""
        if TORCH_AVAILABLE and isinstance(positions, torch.Tensor):
            seq_len = int(positions.max().item()) + 1
        else:
            seq_len = int(positions.max()) + 1
        
        # Recompute cache if sequence length changed significantly
        if seq_len > self._cache_seq_len:
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(seq_len)
            self._cache_seq_len = seq_len
        
        # Apply rotation (same as NeoX)
        if TORCH_AVAILABLE and isinstance(positions, torch.Tensor):
            cos = self._cos_cache[positions].unsqueeze(-2)
            sin = self._sin_cache[positions].unsqueeze(-2)
            
            def rotate_half(x: "torch.Tensor") -> "torch.Tensor":
                x1 = x[..., : x.shape[-1] // 2]
                x2 = x[..., x.shape[-1] // 2 :]
                return torch.cat((-x2, x1), dim=-1)
            
            q_rot = query * cos + rotate_half(query) * sin
            k_rot = key * cos + rotate_half(key) * sin
            return q_rot, k_rot
        
        raise RuntimeError("XDRotaryEmbedding requires PyTorch")


class RotaryEmbeddingEngine:
    """Unified engine for rotary position embeddings.
    
    Provides automatic variant detection and unified interface
    for all RoPE implementations.
    
    Beyond vLLM:
    - Automatic variant detection from model configuration
    - Runtime variant switching
    - Lazy initialization with caching
    """
    
    _VARIANT_MAP: Dict[RoPEVariant, type] = {
        RoPEVariant.NEOX: NeoxRotaryEmbedding,
        RoPEVariant.GPTJ: GptJRotaryEmbedding,
        RoPEVariant.MROPE: MRotaryEmbedding,
        RoPEVariant.XDROPE: XDRotaryEmbedding,
    }
    
    def __init__(self, config: Optional[RoPEConfig] = None):
        """Initialize the RoPE engine.
        
        Args:
            config: RoPE configuration. If None, uses defaults.
        """
        self.config = config or RoPEConfig()
        self._embeddings: Dict[RoPEVariant, RotaryEmbeddingBase] = {}
        self._current_variant = self.config.variant
        self._current_embedding: Optional[RotaryEmbeddingBase] = None
    
    def _get_or_create_embedding(self, variant: RoPEVariant) -> RotaryEmbeddingBase:
        """Get or create an embedding instance for the variant."""
        if variant not in self._embeddings:
            if variant not in self._VARIANT_MAP:
                raise ValueError(f"Unsupported RoPE variant: {variant}")
            
            embedding_cls = self._VARIANT_MAP[variant]
            self._embeddings[variant] = embedding_cls(self.config)
        
        return self._embeddings[variant]
    
    def set_variant(self, variant: RoPEVariant) -> None:
        """Set the current RoPE variant.
        
        Args:
            variant: Variant to use
        """
        self._current_variant = variant
        self._current_embedding = self._get_or_create_embedding(variant)
    
    @property
    def embedding(self) -> RotaryEmbeddingBase:
        """Get the current embedding instance."""
        if self._current_embedding is None:
            self._current_embedding = self._get_or_create_embedding(self._current_variant)
        return self._current_embedding
    
    def forward(
        self,
        positions: Any,
        query: Any,
        key: Any,
        use_cuda: bool = True,
    ) -> Tuple[Any, Any]:
        """Apply rotary embeddings.
        
        Args:
            positions: Position indices
            query: Query tensor
            key: Key tensor
            use_cuda: Whether to prefer CUDA implementation
            
        Returns:
            Tuple of (rotated_query, rotated_key)
        """
        return self.embedding.forward(positions, query, key, use_cuda)
    
    @classmethod
    def from_model_config(
        cls,
        model_config: Dict[str, Any],
    ) -> "RotaryEmbeddingEngine":
        """Create engine from model configuration.
        
        Beyond vLLM: Automatic variant detection.
        
        Args:
            model_config: Model configuration dictionary
            
        Returns:
            Configured engine instance
        """
        config = RoPEConfig(
            head_dim=model_config.get("head_dim", 64),
            rotary_dim=model_config.get("rotary_dim"),
            max_position_embeddings=model_config.get("max_position_embeddings", 2048),
            base=model_config.get("rope_theta", 10000.0),
            is_neox_style=model_config.get("is_neox_style", True),
        )
        
        # Detect scaling type
        rope_scaling = model_config.get("rope_scaling", {})
        if rope_scaling:
            scaling_type = rope_scaling.get("type", "none").lower()
            if scaling_type == "linear":
                config.scaling_type = RoPEScalingType.LINEAR
                config.scaling_factor = rope_scaling.get("factor", 1.0)
            elif scaling_type == "dynamic":
                config.dynamic_scaling = True
            elif scaling_type == "yarn":
                config.scaling_type = RoPEScalingType.YARN
                config.yarn_beta_fast = rope_scaling.get("beta_fast", 32.0)
                config.yarn_beta_slow = rope_scaling.get("beta_slow", 1.0)
        
        # Detect multimodal sections
        if "mrope_section" in model_config:
            config.mrope_sections = model_config["mrope_section"]
        
        return cls(config)
    
    @classmethod
    def list_variants(cls) -> List[str]:
        """List all supported RoPE variants."""
        return [v.name for v in RoPEVariant]


# Convenience functions
def create_rope_embedding(
    head_dim: int = 64,
    max_position: int = 2048,
    base: float = 10000.0,
    variant: Union[str, RoPEVariant] = RoPEVariant.NEOX,
    **kwargs: Any,
) -> RotaryEmbeddingBase:
    """Create a RoPE embedding instance.
    
    Args:
        head_dim: Head dimension
        max_position: Maximum position
        base: Base for frequency calculation
        variant: RoPE variant to use
        **kwargs: Additional configuration
        
    Returns:
        Configured embedding instance
    """
    if isinstance(variant, str):
        variant = RoPEVariant[variant.upper()]
    
    config = RoPEConfig(
        head_dim=head_dim,
        max_position_embeddings=max_position,
        base=base,
        **kwargs,
    )
    
    engine = RotaryEmbeddingEngine(config)
    engine.set_variant(variant)
    return engine.embedding
