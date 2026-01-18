# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
AttentionBackendRegistry - Dynamic attention backend selection.

Implements vLLM's AttentionImpls registry pattern for attention backends:
- AttentionBackendEnum: Available backend types
- AttentionBackend: Abstract base for backends
- AttentionBackendRegistry: Registration and capability-based lookup

Beyond vLLM: Runtime backend hot-swap without restart.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Generic, TypeVar
from functools import lru_cache

import numpy as np

logger = logging.getLogger(__name__)

# Try to import torch
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore


class AttentionBackendEnum(Enum):
    """Enumeration of available attention backends."""
    FLASH_ATTN = "flash_attn"          # FlashAttention-2
    FLASHINFER = "flashinfer"          # FlashInfer
    TRITON = "triton"                  # Triton-based attention
    XFORMERS = "xformers"              # xFormers memory efficient
    TORCH_SDPA = "torch_sdpa"          # PyTorch SDPA
    NAIVE = "naive"                    # Simple reference implementation
    PAGED = "paged"                    # PagedAttention (vLLM native)


class AttentionType(Enum):
    """Types of attention computation."""
    PREFILL = auto()      # Full attention during prefill
    DECODE = auto()       # Incremental attention during decode
    ENCODER = auto()      # Encoder-side attention
    CROSS = auto()        # Cross-attention (decoder to encoder)


@dataclass
class AttentionCapabilities:
    """Capabilities of an attention backend."""
    # Supported attention types
    supports_prefill: bool = True
    supports_decode: bool = True
    supports_encoder: bool = True
    supports_cross: bool = False
    
    # Feature support
    supports_sliding_window: bool = False
    supports_alibi: bool = False
    supports_gqa: bool = True  # Grouped query attention
    supports_mqa: bool = True  # Multi-query attention
    supports_prefix_caching: bool = False
    supports_cuda_graphs: bool = True
    supports_fp8: bool = False
    
    # Hardware requirements
    requires_cuda: bool = True
    requires_bf16: bool = False
    min_sm_version: int = 70  # Volta+
    
    # Performance hints
    best_for_short_seqs: bool = False
    best_for_long_seqs: bool = False
    memory_efficient: bool = True


@dataclass
class AttentionMetadata:
    """Metadata for attention computation."""
    # Sequence lengths
    seq_lens: list[int] = field(default_factory=list)
    max_seq_len: int = 0
    context_lens: list[int] | None = None
    
    # Paged attention
    block_tables: Any | None = None  # [batch, max_blocks]
    slot_mapping: Any | None = None  # [total_tokens]
    
    # KV cache info
    kv_cache_dtype: str = "auto"
    num_kv_heads: int = 0
    head_size: int = 0
    
    # Attention type
    attn_type: AttentionType = AttentionType.DECODE
    
    # Sliding window
    sliding_window: int | None = None
    
    # Misc
    use_cuda_graph: bool = False
    prefix_cache_hit: bool = False


# Type variable for backend implementations
T = TypeVar("T")


class AttentionBackend(ABC, Generic[T]):
    """
    Abstract base class for attention backends.
    
    Each backend implements specific attention algorithms
    optimized for different scenarios.
    """
    
    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """Get the backend name."""
        ...
    
    @staticmethod
    @abstractmethod
    def get_capabilities() -> AttentionCapabilities:
        """Get backend capabilities."""
        ...
    
    @abstractmethod
    def forward(
        self,
        query: Any,       # [batch*seq, num_heads, head_dim]
        key: Any,         # [batch*seq, num_kv_heads, head_dim]
        value: Any,       # [batch*seq, num_kv_heads, head_dim]
        kv_cache: tuple[Any, Any] | None,  # (key_cache, value_cache)
        metadata: AttentionMetadata,
        scale: float | None = None,
    ) -> Any:
        """
        Compute attention.
        
        Args:
            query: Query tensor
            key: Key tensor
            value: Value tensor
            kv_cache: Optional KV cache tensors
            metadata: Attention metadata
            scale: Attention scale (defaults to 1/sqrt(head_dim))
            
        Returns:
            Attention output [batch*seq, num_heads, head_dim]
        """
        ...
    
    def supports(self, attn_type: AttentionType) -> bool:
        """Check if backend supports attention type."""
        caps = self.get_capabilities()
        mapping = {
            AttentionType.PREFILL: caps.supports_prefill,
            AttentionType.DECODE: caps.supports_decode,
            AttentionType.ENCODER: caps.supports_encoder,
            AttentionType.CROSS: caps.supports_cross,
        }
        return mapping.get(attn_type, False)


class NaiveAttentionBackend(AttentionBackend[None]):
    """
    Naive reference implementation for testing.
    
    Simple scaled dot-product attention without optimizations.
    """
    
    @staticmethod
    def get_name() -> str:
        return "naive"
    
    @staticmethod
    def get_capabilities() -> AttentionCapabilities:
        return AttentionCapabilities(
            supports_prefill=True,
            supports_decode=True,
            supports_encoder=True,
            supports_cross=True,
            supports_sliding_window=False,
            supports_alibi=False,
            supports_gqa=True,
            supports_mqa=True,
            supports_prefix_caching=False,
            supports_cuda_graphs=False,
            supports_fp8=False,
            requires_cuda=False,
            min_sm_version=0,
            best_for_short_seqs=True,
            best_for_long_seqs=False,
            memory_efficient=False,
        )
    
    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        kv_cache: tuple[Any, Any] | None,
        metadata: AttentionMetadata,
        scale: float | None = None,
    ) -> Any:
        """Naive attention implementation."""
        if not HAS_TORCH:
            raise RuntimeError("PyTorch required for NaiveAttentionBackend")
        
        # Get dimensions
        batch_seq, num_heads, head_dim = query.shape
        _, num_kv_heads, _ = key.shape
        
        if scale is None:
            scale = 1.0 / (head_dim ** 0.5)
        
        # Handle GQA/MQA by repeating KV heads
        if num_kv_heads != num_heads:
            repeat_factor = num_heads // num_kv_heads
            key = key.repeat_interleave(repeat_factor, dim=1)
            value = value.repeat_interleave(repeat_factor, dim=1)
        
        # Compute attention
        # [batch*seq, heads, head_dim] @ [batch*seq, heads, head_dim].T
        # -> [batch*seq, heads, heads] (this is simplified, actual is different)
        
        # For decode with cache, we use cached KV
        if kv_cache is not None:
            k_cache, v_cache = kv_cache
            # Would use slot_mapping to gather cached KV
            # Simplified here
        
        # Simple attention: Q @ K.T * scale -> softmax -> @ V
        attn_weights = torch.matmul(query, key.transpose(-2, -1)) * scale
        attn_weights = torch.softmax(attn_weights, dim=-1)
        output = torch.matmul(attn_weights, value)
        
        return output


class TorchSDPABackend(AttentionBackend[None]):
    """
    PyTorch Scaled Dot-Product Attention backend.
    
    Uses torch.nn.functional.scaled_dot_product_attention.
    """
    
    @staticmethod
    def get_name() -> str:
        return "torch_sdpa"
    
    @staticmethod
    def get_capabilities() -> AttentionCapabilities:
        return AttentionCapabilities(
            supports_prefill=True,
            supports_decode=True,
            supports_encoder=True,
            supports_cross=True,
            supports_sliding_window=False,
            supports_alibi=False,
            supports_gqa=True,
            supports_mqa=True,
            supports_prefix_caching=False,
            supports_cuda_graphs=True,
            supports_fp8=False,
            requires_cuda=False,
            min_sm_version=0,
            best_for_short_seqs=True,
            best_for_long_seqs=False,
            memory_efficient=True,
        )
    
    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        kv_cache: tuple[Any, Any] | None,
        metadata: AttentionMetadata,
        scale: float | None = None,
    ) -> Any:
        """SDPA attention implementation."""
        if not HAS_TORCH:
            raise RuntimeError("PyTorch required for TorchSDPABackend")
        
        import torch.nn.functional as F
        
        batch_seq, num_heads, head_dim = query.shape
        _, num_kv_heads, _ = key.shape
        
        # Handle GQA/MQA
        if num_kv_heads != num_heads:
            repeat_factor = num_heads // num_kv_heads
            key = key.repeat_interleave(repeat_factor, dim=1)
            value = value.repeat_interleave(repeat_factor, dim=1)
        
        # SDPA expects [batch, heads, seq, head_dim]
        # We have [batch*seq, heads, head_dim] - reshape appropriately
        # For simplicity, assume batch=1 here
        q = query.unsqueeze(0).transpose(1, 2)  # [1, heads, batch*seq, dim]
        k = key.unsqueeze(0).transpose(1, 2)
        v = value.unsqueeze(0).transpose(1, 2)
        
        output = F.scaled_dot_product_attention(
            q, k, v,
            scale=scale,
            is_causal=(metadata.attn_type != AttentionType.ENCODER),
        )
        
        # Reshape back
        output = output.transpose(1, 2).squeeze(0)  # [batch*seq, heads, dim]
        return output


class FlashAttentionBackend(AttentionBackend[None]):
    """
    FlashAttention-2 backend.
    
    Optimized attention using tiling and recomputation.
    """
    
    @staticmethod
    def get_name() -> str:
        return "flash_attn"
    
    @staticmethod
    def get_capabilities() -> AttentionCapabilities:
        return AttentionCapabilities(
            supports_prefill=True,
            supports_decode=True,
            supports_encoder=True,
            supports_cross=True,
            supports_sliding_window=True,
            supports_alibi=True,
            supports_gqa=True,
            supports_mqa=True,
            supports_prefix_caching=True,
            supports_cuda_graphs=True,
            supports_fp8=False,
            requires_cuda=True,
            requires_bf16=False,
            min_sm_version=80,  # Ampere+
            best_for_short_seqs=True,
            best_for_long_seqs=True,
            memory_efficient=True,
        )
    
    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        kv_cache: tuple[Any, Any] | None,
        metadata: AttentionMetadata,
        scale: float | None = None,
    ) -> Any:
        """FlashAttention implementation."""
        try:
            from flash_attn import flash_attn_func
        except ImportError:
            logger.warning("flash_attn not available, falling back to SDPA")
            return TorchSDPABackend().forward(
                query, key, value, kv_cache, metadata, scale
            )
        
        # FlashAttention expects [batch, seqlen, heads, head_dim]
        # Reshape accordingly
        batch_seq, num_heads, head_dim = query.shape
        
        q = query.unsqueeze(0)  # Add batch dim
        k = key.unsqueeze(0)
        v = value.unsqueeze(0)
        
        # Compute
        output = flash_attn_func(
            q, k, v,
            softmax_scale=scale,
            causal=(metadata.attn_type != AttentionType.ENCODER),
            window_size=(metadata.sliding_window, metadata.sliding_window)
            if metadata.sliding_window else (-1, -1),
        )
        
        return output.squeeze(0)


class FlashInferBackend(AttentionBackend[None]):
    """
    FlashInfer backend for decode-focused attention.
    
    Optimized for single-token decode with PagedAttention.
    """
    
    @staticmethod
    def get_name() -> str:
        return "flashinfer"
    
    @staticmethod
    def get_capabilities() -> AttentionCapabilities:
        return AttentionCapabilities(
            supports_prefill=True,
            supports_decode=True,
            supports_encoder=False,
            supports_cross=False,
            supports_sliding_window=True,
            supports_alibi=False,
            supports_gqa=True,
            supports_mqa=True,
            supports_prefix_caching=True,
            supports_cuda_graphs=True,
            supports_fp8=True,
            requires_cuda=True,
            min_sm_version=80,
            best_for_short_seqs=True,
            best_for_long_seqs=True,
            memory_efficient=True,
        )
    
    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        kv_cache: tuple[Any, Any] | None,
        metadata: AttentionMetadata,
        scale: float | None = None,
    ) -> Any:
        """FlashInfer implementation."""
        try:
            import flashinfer
        except ImportError:
            logger.warning("flashinfer not available, falling back to SDPA")
            return TorchSDPABackend().forward(
                query, key, value, kv_cache, metadata, scale
            )
        
        # FlashInfer-specific implementation would go here
        # For now, fall back to SDPA
        return TorchSDPABackend().forward(
            query, key, value, kv_cache, metadata, scale
        )


class AttentionBackendRegistry:
    """
    Registry for attention backends with capability-based selection.
    
    Features:
    - Backend registration and discovery
    - Capability-based lookup
    - Runtime hot-swap (beyond vLLM)
    - Fallback chains
    """
    
    _instance: AttentionBackendRegistry | None = None
    
    def __new__(cls) -> AttentionBackendRegistry:
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_registry()
        return cls._instance
    
    def _init_registry(self) -> None:
        """Initialize the registry with default backends."""
        self._backends: dict[str, type[AttentionBackend]] = {}
        self._active_backend: AttentionBackend | None = None
        self._fallback_chain: list[str] = []
        self._hot_swap_enabled: bool = True
        
        # Register default backends
        self.register(NaiveAttentionBackend)
        self.register(TorchSDPABackend)
        self.register(FlashAttentionBackend)
        self.register(FlashInferBackend)
        
        # Default fallback chain
        self._fallback_chain = [
            "flash_attn",
            "flashinfer",
            "torch_sdpa",
            "naive",
        ]
    
    def register(
        self,
        backend_cls: type[AttentionBackend],
        override: bool = False,
    ) -> None:
        """
        Register an attention backend.
        
        Args:
            backend_cls: Backend class to register
            override: Whether to override existing registration
        """
        name = backend_cls.get_name()
        
        if name in self._backends and not override:
            logger.warning(f"Backend '{name}' already registered, skipping")
            return
        
        self._backends[name] = backend_cls
        logger.debug(f"Registered attention backend: {name}")
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a backend.
        
        Args:
            name: Backend name to remove
            
        Returns:
            True if removed, False if not found
        """
        if name in self._backends:
            del self._backends[name]
            if name in self._fallback_chain:
                self._fallback_chain.remove(name)
            logger.debug(f"Unregistered attention backend: {name}")
            return True
        return False
    
    def get_backend(
        self,
        name: str | AttentionBackendEnum | None = None,
    ) -> AttentionBackend | None:
        """
        Get a backend by name.
        
        Args:
            name: Backend name or enum (uses active if None)
            
        Returns:
            Backend instance or None
        """
        if name is None:
            return self._active_backend
        
        if isinstance(name, AttentionBackendEnum):
            name = name.value
        
        backend_cls = self._backends.get(name)
        if backend_cls is not None:
            return backend_cls()
        return None
    
    def select_backend(
        self,
        capabilities: AttentionCapabilities | None = None,
        attn_type: AttentionType | None = None,
        prefer: str | None = None,
    ) -> AttentionBackend | None:
        """
        Select best backend based on requirements.
        
        Args:
            capabilities: Required capabilities
            attn_type: Required attention type
            prefer: Preferred backend name
            
        Returns:
            Best matching backend
        """
        # Try preferred first
        if prefer:
            backend = self.get_backend(prefer)
            if backend and self._check_backend(backend, capabilities, attn_type):
                return backend
        
        # Try fallback chain
        for name in self._fallback_chain:
            backend = self.get_backend(name)
            if backend and self._check_backend(backend, capabilities, attn_type):
                return backend
        
        # Try any backend
        for name in self._backends:
            backend = self.get_backend(name)
            if backend and self._check_backend(backend, capabilities, attn_type):
                return backend
        
        return None
    
    def _check_backend(
        self,
        backend: AttentionBackend,
        capabilities: AttentionCapabilities | None,
        attn_type: AttentionType | None,
    ) -> bool:
        """Check if backend meets requirements."""
        if attn_type is not None and not backend.supports(attn_type):
            return False
        
        if capabilities is not None:
            caps = backend.get_capabilities()
            # Check key capabilities
            if capabilities.supports_sliding_window and not caps.supports_sliding_window:
                return False
            if capabilities.supports_fp8 and not caps.supports_fp8:
                return False
            if capabilities.requires_cuda and not caps.requires_cuda:
                return False
        
        return True
    
    def set_active(
        self,
        backend: str | AttentionBackend | AttentionBackendEnum,
    ) -> bool:
        """
        Set the active backend.
        
        Args:
            backend: Backend name, instance, or enum
            
        Returns:
            True if set successfully
        """
        if isinstance(backend, str):
            self._active_backend = self.get_backend(backend)
        elif isinstance(backend, AttentionBackendEnum):
            self._active_backend = self.get_backend(backend.value)
        else:
            self._active_backend = backend
        
        if self._active_backend:
            logger.info(f"Active attention backend: {self._active_backend.get_name()}")
            return True
        return False
    
    def hot_swap(
        self,
        new_backend: str | AttentionBackend,
    ) -> bool:
        """
        Hot-swap to a new backend without restart.
        
        Beyond vLLM: Allows runtime backend changes.
        
        Args:
            new_backend: New backend to use
            
        Returns:
            True if swap successful
        """
        if not self._hot_swap_enabled:
            logger.warning("Hot-swap disabled")
            return False
        
        old_backend = self._active_backend
        
        if self.set_active(new_backend):
            if old_backend:
                logger.info(
                    f"Hot-swapped from {old_backend.get_name()} to "
                    f"{self._active_backend.get_name()}"  # type: ignore
                )
            return True
        
        # Restore on failure
        self._active_backend = old_backend
        return False
    
    def set_fallback_chain(self, chain: list[str]) -> None:
        """Set the backend fallback chain."""
        self._fallback_chain = chain
    
    def list_backends(self) -> list[str]:
        """List all registered backends."""
        return list(self._backends.keys())
    
    def get_capabilities(self, name: str) -> AttentionCapabilities | None:
        """Get capabilities for a backend."""
        backend_cls = self._backends.get(name)
        if backend_cls:
            return backend_cls.get_capabilities()
        return None
    
    @lru_cache(maxsize=32)
    def _check_availability(self, name: str) -> bool:
        """Check if backend is actually usable."""
        backend = self.get_backend(name)
        if backend is None:
            return False
        
        caps = backend.get_capabilities()
        
        # Check CUDA requirement
        if caps.requires_cuda and (not HAS_TORCH or not torch.cuda.is_available()):
            return False
        
        # Check SM version
        if HAS_TORCH and torch.cuda.is_available():
            major, minor = torch.cuda.get_device_capability()
            sm_version = major * 10 + minor
            if sm_version < caps.min_sm_version:
                return False
        
        return True
    
    def get_available_backends(self) -> list[str]:
        """Get list of actually usable backends."""
        return [name for name in self._backends if self._check_availability(name)]


# Convenience function
def get_attention_registry() -> AttentionBackendRegistry:
    """Get the singleton attention backend registry."""
    return AttentionBackendRegistry()
