# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: LoRA Manager - Dynamic Adapter Management

"""
LoRA adapter management with dynamic loading and multi-adapter serving.

Inspired by vLLM's lora patterns, this module provides:
- LoRA adapter loading and caching
- Multi-adapter serving (Punica batching)
- GPU slot management
- Adapter composition

Beyond vLLM:
- Runtime adapter composition/merging
- rsLoRA scaling support
- DoRA integration
- Memory-efficient adapter pooling
"""

from __future__ import annotations

import hashlib
import os
import threading
import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

import numpy as np


# =============================================================================
# Enums
# =============================================================================

class LoRAMethod(Enum):
    """LoRA method variants."""
    LORA = auto()                 # Standard LoRA
    QLORA = auto()                # Quantized LoRA
    DORA = auto()                 # Weight-Decomposed LoRA
    RSLORA = auto()               # Rank-Stabilized LoRA
    ADALORA = auto()              # Adaptive LoRA
    VERA = auto()                 # Vector-based Random LoRA
    LORA_PLUS = auto()            # LoRA+ (different LR for A/B)


class AdapterStatus(Enum):
    """Adapter lifecycle status."""
    LOADING = auto()              # Being loaded
    READY = auto()                # Ready to serve
    ACTIVE = auto()               # Currently in use
    INACTIVE = auto()             # Loaded but not active
    EVICTING = auto()             # Being evicted
    ERROR = auto()                # Load error


class TargetModule(Enum):
    """Common LoRA target modules."""
    Q_PROJ = "q_proj"
    K_PROJ = "k_proj"
    V_PROJ = "v_proj"
    O_PROJ = "o_proj"
    GATE_PROJ = "gate_proj"
    UP_PROJ = "up_proj"
    DOWN_PROJ = "down_proj"
    LM_HEAD = "lm_head"
    EMBED_TOKENS = "embed_tokens"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class LoRAConfig:
    """LoRA adapter configuration."""
    adapter_name: str                                  # Unique adapter identifier
    adapter_path: str                                  # Path to adapter files
    rank: int = 8                                      # LoRA rank (r)
    alpha: float = 16.0                                # LoRA alpha (scaling)
    dropout: float = 0.0                               # Dropout rate
    method: LoRAMethod = LoRAMethod.LORA
    target_modules: List[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj"
    ])
    modules_to_save: List[str] = field(default_factory=list)
    use_rslora: bool = False                           # Use rsLoRA scaling
    use_dora: bool = False                             # Use DoRA decomposition
    scaling: Optional[float] = None                    # Override scaling
    bias: str = "none"                                 # "none", "all", "lora_only"
    extra_config: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def computed_scaling(self) -> float:
        """Compute LoRA scaling factor."""
        if self.scaling is not None:
            return self.scaling
        if self.use_rslora:
            # rsLoRA: alpha / sqrt(rank)
            return self.alpha / (self.rank ** 0.5)
        # Standard LoRA: alpha / rank
        return self.alpha / self.rank
    
    def __hash__(self) -> int:
        return hash((self.adapter_name, self.adapter_path, self.rank))


@dataclass
class LoRARequest:
    """Request to serve with a LoRA adapter."""
    request_id: str
    adapter_name: str
    adapter_config: Optional[LoRAConfig] = None
    priority: int = 0                                  # Higher = more priority
    
    def __hash__(self) -> int:
        return hash((self.request_id, self.adapter_name))


@dataclass
class LoRAInfo:
    """Information about a loaded adapter."""
    adapter_name: str
    rank: int
    alpha: float
    method: LoRAMethod
    target_modules: List[str]
    num_parameters: int
    memory_bytes: int
    status: AdapterStatus
    load_time_ms: float = 0.0
    last_used: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "adapter_name": self.adapter_name,
            "rank": self.rank,
            "alpha": self.alpha,
            "method": self.method.name,
            "target_modules": self.target_modules,
            "num_parameters": self.num_parameters,
            "memory_mb": self.memory_bytes / (1024 * 1024),
            "status": self.status.name,
        }


@dataclass
class AdapterSlot:
    """GPU slot for a LoRA adapter."""
    slot_id: int
    adapter_name: Optional[str] = None
    is_active: bool = False
    memory_allocated: int = 0
    assigned_at: float = field(default_factory=time.time)
    
    @property
    def is_free(self) -> bool:
        return self.adapter_name is None


@dataclass
class LoRAWeights:
    """LoRA weight matrices."""
    lora_a: Dict[str, np.ndarray] = field(default_factory=dict)  # Down projection
    lora_b: Dict[str, np.ndarray] = field(default_factory=dict)  # Up projection
    scales: Dict[str, float] = field(default_factory=dict)       # Per-module scales
    dora_magnitudes: Optional[Dict[str, np.ndarray]] = None      # DoRA magnitudes
    
    @property
    def num_parameters(self) -> int:
        total = 0
        for module in self.lora_a:
            total += self.lora_a[module].size
            total += self.lora_b[module].size
        return total
    
    @property
    def memory_bytes(self) -> int:
        total = 0
        for module in self.lora_a:
            total += self.lora_a[module].nbytes
            total += self.lora_b[module].nbytes
        return total


# =============================================================================
# LoRA Adapter
# =============================================================================

class LoRAAdapter:
    """
    Represents a loaded LoRA adapter.
    
    Handles:
    - Weight loading from various formats
    - Scaling computation
    - Weight application
    """
    
    def __init__(self, config: LoRAConfig):
        self.config = config
        self.weights: Optional[LoRAWeights] = None
        self.info: Optional[LoRAInfo] = None
        self._status = AdapterStatus.LOADING
        self._load_time_ms = 0.0
    
    @property
    def name(self) -> str:
        return self.config.adapter_name
    
    @property
    def status(self) -> AdapterStatus:
        return self._status
    
    def load(self) -> bool:
        """Load adapter weights from disk."""
        start = time.perf_counter()
        
        try:
            path = Path(self.config.adapter_path)
            
            if path.is_dir():
                self.weights = self._load_from_directory(path)
            elif path.suffix == ".safetensors":
                self.weights = self._load_safetensors(path)
            elif path.suffix in (".pt", ".pth", ".bin"):
                self.weights = self._load_pytorch(path)
            else:
                raise ValueError(f"Unsupported adapter format: {path}")
            
            self._load_time_ms = (time.perf_counter() - start) * 1000
            self._status = AdapterStatus.READY
            
            self.info = LoRAInfo(
                adapter_name=self.config.adapter_name,
                rank=self.config.rank,
                alpha=self.config.alpha,
                method=self.config.method,
                target_modules=self.config.target_modules,
                num_parameters=self.weights.num_parameters,
                memory_bytes=self.weights.memory_bytes,
                status=self._status,
                load_time_ms=self._load_time_ms,
            )
            
            return True
            
        except Exception as e:
            self._status = AdapterStatus.ERROR
            return False
    
    def _load_from_directory(self, path: Path) -> LoRAWeights:
        """Load from HuggingFace PEFT directory."""
        weights = LoRAWeights()
        
        # Try safetensors first
        adapter_file = path / "adapter_model.safetensors"
        if adapter_file.exists():
            return self._load_safetensors(adapter_file)
        
        # Try PyTorch
        adapter_file = path / "adapter_model.bin"
        if adapter_file.exists():
            return self._load_pytorch(adapter_file)
        
        raise FileNotFoundError(f"No adapter weights found in {path}")
    
    def _load_safetensors(self, path: Path) -> LoRAWeights:
        """Load from SafeTensors format."""
        try:
            from safetensors import safe_open
            
            weights = LoRAWeights()
            
            with safe_open(str(path), framework="numpy") as f:
                for key in f.keys():
                    tensor = f.get_tensor(key)
                    
                    if ".lora_A." in key or ".lora_a." in key:
                        module = self._extract_module_name(key)
                        weights.lora_a[module] = tensor
                    elif ".lora_B." in key or ".lora_b." in key:
                        module = self._extract_module_name(key)
                        weights.lora_b[module] = tensor
            
            # Set scales
            for module in weights.lora_a:
                weights.scales[module] = self.config.computed_scaling
            
            return weights
            
        except ImportError:
            raise ImportError("safetensors required for loading .safetensors files")
    
    def _load_pytorch(self, path: Path) -> LoRAWeights:
        """Load from PyTorch format."""
        try:
            import torch
            
            weights = LoRAWeights()
            state_dict = torch.load(str(path), map_location="cpu")
            
            for key, tensor in state_dict.items():
                array = tensor.numpy()
                
                if ".lora_A." in key or ".lora_a." in key:
                    module = self._extract_module_name(key)
                    weights.lora_a[module] = array
                elif ".lora_B." in key or ".lora_b." in key:
                    module = self._extract_module_name(key)
                    weights.lora_b[module] = array
            
            for module in weights.lora_a:
                weights.scales[module] = self.config.computed_scaling
            
            return weights
            
        except ImportError:
            raise ImportError("PyTorch required for loading .pt/.bin files")
    
    def _extract_module_name(self, key: str) -> str:
        """Extract module name from weight key."""
        # Handle various naming conventions
        parts = key.split(".")
        
        # Find the target module name
        for target in self.config.target_modules:
            if target in key:
                return target
        
        # Fallback: return last meaningful part
        for part in reversed(parts):
            if part not in ("lora_A", "lora_B", "lora_a", "lora_b", "weight", "default"):
                return part
        
        return key
    
    def apply_to_linear(
        self,
        module_name: str,
        hidden_states: np.ndarray,
    ) -> np.ndarray:
        """Apply LoRA to a linear layer's output."""
        if self.weights is None:
            raise RuntimeError("Adapter weights not loaded")
        
        if module_name not in self.weights.lora_a:
            return np.zeros_like(hidden_states)
        
        # LoRA: h + scale * (x @ A.T @ B.T)
        lora_a = self.weights.lora_a[module_name]
        lora_b = self.weights.lora_b[module_name]
        scale = self.weights.scales.get(module_name, self.config.computed_scaling)
        
        # x @ A.T @ B.T
        intermediate = hidden_states @ lora_a.T
        lora_output = intermediate @ lora_b.T
        
        return scale * lora_output
    
    def merge_into_weights(
        self,
        original_weights: Dict[str, np.ndarray],
    ) -> Dict[str, np.ndarray]:
        """Merge LoRA into base model weights."""
        if self.weights is None:
            raise RuntimeError("Adapter weights not loaded")
        
        merged = {}
        
        for name, weight in original_weights.items():
            merged[name] = weight.copy()
            
            # Check if this module has LoRA
            for target in self.config.target_modules:
                if target in name:
                    if target in self.weights.lora_a:
                        lora_a = self.weights.lora_a[target]
                        lora_b = self.weights.lora_b[target]
                        scale = self.weights.scales.get(target, self.config.computed_scaling)
                        
                        # W' = W + scale * B @ A
                        delta = scale * (lora_b @ lora_a)
                        merged[name] = weight + delta
        
        return merged


# =============================================================================
# LoRA Registry
# =============================================================================

class LoRARegistry:
    """
    Registry for LoRA adapters.
    
    Features:
    - Adapter caching with LRU eviction
    - Thread-safe access
    - Lazy loading
    """
    
    def __init__(self, max_cached: int = 32):
        self._adapters: OrderedDict[str, LoRAAdapter] = OrderedDict()
        self._max_cached = max_cached
        self._lock = threading.RLock()
        self._stats = {
            "loads": 0,
            "cache_hits": 0,
            "evictions": 0,
        }
    
    def register(self, config: LoRAConfig) -> LoRAAdapter:
        """Register and load a LoRA adapter."""
        with self._lock:
            # Check cache
            if config.adapter_name in self._adapters:
                self._stats["cache_hits"] += 1
                self._adapters.move_to_end(config.adapter_name)
                return self._adapters[config.adapter_name]
            
            # Evict if necessary
            while len(self._adapters) >= self._max_cached:
                evicted_name, _ = self._adapters.popitem(last=False)
                self._stats["evictions"] += 1
            
            # Load adapter
            adapter = LoRAAdapter(config)
            adapter.load()
            
            self._adapters[config.adapter_name] = adapter
            self._stats["loads"] += 1
            
            return adapter
    
    def get(self, adapter_name: str) -> Optional[LoRAAdapter]:
        """Get a registered adapter."""
        with self._lock:
            if adapter_name in self._adapters:
                self._adapters.move_to_end(adapter_name)
                return self._adapters[adapter_name]
            return None
    
    def unregister(self, adapter_name: str) -> bool:
        """Unregister an adapter."""
        with self._lock:
            if adapter_name in self._adapters:
                del self._adapters[adapter_name]
                return True
            return False
    
    def list_adapters(self) -> List[str]:
        """List all registered adapter names."""
        with self._lock:
            return list(self._adapters.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        with self._lock:
            return {
                **self._stats,
                "cached": len(self._adapters),
                "max_cached": self._max_cached,
            }


# =============================================================================
# LoRA Slot Manager
# =============================================================================

class LoRASlotManager:
    """
    Manages GPU slots for LoRA adapters.
    
    Features:
    - Fixed number of GPU slots
    - LRU eviction when full
    - Slot allocation tracking
    """
    
    def __init__(self, num_slots: int = 8):
        self.num_slots = num_slots
        self._slots: List[AdapterSlot] = [
            AdapterSlot(slot_id=i) for i in range(num_slots)
        ]
        self._adapter_to_slot: Dict[str, int] = {}
        self._lock = threading.Lock()
    
    def allocate(self, adapter_name: str, memory_required: int = 0) -> Optional[int]:
        """Allocate a slot for an adapter."""
        with self._lock:
            # Check if already allocated
            if adapter_name in self._adapter_to_slot:
                slot_id = self._adapter_to_slot[adapter_name]
                self._slots[slot_id].is_active = True
                return slot_id
            
            # Find free slot
            for slot in self._slots:
                if slot.is_free:
                    slot.adapter_name = adapter_name
                    slot.is_active = True
                    slot.memory_allocated = memory_required
                    slot.assigned_at = time.time()
                    self._adapter_to_slot[adapter_name] = slot.slot_id
                    return slot.slot_id
            
            # Evict LRU inactive slot
            oldest_slot = None
            oldest_time = float('inf')
            
            for slot in self._slots:
                if not slot.is_active and slot.assigned_at < oldest_time:
                    oldest_slot = slot
                    oldest_time = slot.assigned_at
            
            if oldest_slot:
                # Evict
                if oldest_slot.adapter_name:
                    del self._adapter_to_slot[oldest_slot.adapter_name]
                
                oldest_slot.adapter_name = adapter_name
                oldest_slot.is_active = True
                oldest_slot.memory_allocated = memory_required
                oldest_slot.assigned_at = time.time()
                self._adapter_to_slot[adapter_name] = oldest_slot.slot_id
                return oldest_slot.slot_id
            
            return None  # All slots active
    
    def release(self, adapter_name: str):
        """Release a slot (mark as inactive, but keep loaded)."""
        with self._lock:
            if adapter_name in self._adapter_to_slot:
                slot_id = self._adapter_to_slot[adapter_name]
                self._slots[slot_id].is_active = False
    
    def evict(self, adapter_name: str) -> bool:
        """Evict an adapter from its slot."""
        with self._lock:
            if adapter_name in self._adapter_to_slot:
                slot_id = self._adapter_to_slot[adapter_name]
                slot = self._slots[slot_id]
                slot.adapter_name = None
                slot.is_active = False
                slot.memory_allocated = 0
                del self._adapter_to_slot[adapter_name]
                return True
            return False
    
    def get_slot(self, adapter_name: str) -> Optional[int]:
        """Get slot ID for an adapter."""
        return self._adapter_to_slot.get(adapter_name)
    
    def get_active_adapters(self) -> List[str]:
        """Get list of active adapter names."""
        with self._lock:
            return [
                slot.adapter_name
                for slot in self._slots
                if slot.adapter_name and slot.is_active
            ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get slot statistics."""
        with self._lock:
            free_slots = sum(1 for s in self._slots if s.is_free)
            active_slots = sum(1 for s in self._slots if s.is_active)
            total_memory = sum(s.memory_allocated for s in self._slots)
            
            return {
                "total_slots": self.num_slots,
                "free_slots": free_slots,
                "active_slots": active_slots,
                "loaded_adapters": len(self._adapter_to_slot),
                "total_memory_mb": total_memory / (1024 * 1024),
            }


# =============================================================================
# LoRA Manager
# =============================================================================

class LoRAManager:
    """
    High-level LoRA management.
    
    Features:
    - Adapter lifecycle management
    - Multi-adapter serving
    - Request routing
    - Punica-style batching
    """
    
    def __init__(
        self,
        max_loras: int = 16,
        max_gpu_slots: int = 8,
        max_rank: int = 64,
    ):
        self.max_loras = max_loras
        self.max_rank = max_rank
        
        self._registry = LoRARegistry(max_cached=max_loras)
        self._slot_manager = LoRASlotManager(num_slots=max_gpu_slots)
        self._active_requests: Dict[str, LoRARequest] = {}
        self._lock = threading.Lock()
    
    def load_adapter(self, config: LoRAConfig) -> LoRAInfo:
        """Load a LoRA adapter."""
        if config.rank > self.max_rank:
            raise ValueError(f"Rank {config.rank} exceeds max_rank {self.max_rank}")
        
        adapter = self._registry.register(config)
        
        if adapter.info:
            return adapter.info
        
        raise RuntimeError(f"Failed to load adapter: {config.adapter_name}")
    
    def unload_adapter(self, adapter_name: str) -> bool:
        """Unload a LoRA adapter."""
        self._slot_manager.evict(adapter_name)
        return self._registry.unregister(adapter_name)
    
    def add_request(self, request: LoRARequest) -> bool:
        """Add a request that uses a LoRA adapter."""
        adapter = self._registry.get(request.adapter_name)
        if adapter is None:
            return False
        
        # Allocate GPU slot
        memory = adapter.weights.memory_bytes if adapter.weights else 0
        slot_id = self._slot_manager.allocate(request.adapter_name, memory)
        
        if slot_id is None:
            return False
        
        with self._lock:
            self._active_requests[request.request_id] = request
        
        return True
    
    def remove_request(self, request_id: str):
        """Remove a completed request."""
        with self._lock:
            if request_id in self._active_requests:
                request = self._active_requests.pop(request_id)
                
                # Check if adapter still needed
                still_needed = any(
                    r.adapter_name == request.adapter_name
                    for r in self._active_requests.values()
                )
                
                if not still_needed:
                    self._slot_manager.release(request.adapter_name)
    
    def get_adapter(self, adapter_name: str) -> Optional[LoRAAdapter]:
        """Get a loaded adapter."""
        return self._registry.get(adapter_name)
    
    def list_loaded_adapters(self) -> List[str]:
        """List all loaded adapter names."""
        return self._registry.list_adapters()
    
    def get_active_adapters(self) -> List[str]:
        """Get adapters currently in GPU slots."""
        return self._slot_manager.get_active_adapters()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        with self._lock:
            return {
                "registry": self._registry.get_stats(),
                "slots": self._slot_manager.get_stats(),
                "active_requests": len(self._active_requests),
            }


# =============================================================================
# Utility Functions
# =============================================================================

def load_lora_adapter(
    adapter_path: str,
    adapter_name: Optional[str] = None,
    rank: int = 8,
    alpha: float = 16.0,
    **kwargs,
) -> LoRAAdapter:
    """Load a LoRA adapter from path."""
    if adapter_name is None:
        adapter_name = Path(adapter_path).stem
    
    config = LoRAConfig(
        adapter_name=adapter_name,
        adapter_path=adapter_path,
        rank=rank,
        alpha=alpha,
        **kwargs,
    )
    
    adapter = LoRAAdapter(config)
    adapter.load()
    return adapter


def merge_adapters(
    adapters: List[LoRAAdapter],
    weights: Optional[List[float]] = None,
) -> LoRAWeights:
    """
    Merge multiple LoRA adapters.
    
    Beyond vLLM:
    - Weighted combination of multiple adapters
    - Runtime composition without re-training
    """
    if not adapters:
        raise ValueError("No adapters to merge")
    
    if weights is None:
        weights = [1.0 / len(adapters)] * len(adapters)
    
    if len(weights) != len(adapters):
        raise ValueError("Number of weights must match number of adapters")
    
    merged = LoRAWeights()
    
    # Get all modules from all adapters
    all_modules: Set[str] = set()
    for adapter in adapters:
        if adapter.weights:
            all_modules.update(adapter.weights.lora_a.keys())
    
    # Merge each module
    for module in all_modules:
        merged_a = None
        merged_b = None
        
        for adapter, weight in zip(adapters, weights):
            if adapter.weights and module in adapter.weights.lora_a:
                lora_a = adapter.weights.lora_a[module] * weight
                lora_b = adapter.weights.lora_b[module] * weight
                
                if merged_a is None:
                    merged_a = lora_a
                    merged_b = lora_b
                else:
                    merged_a = merged_a + lora_a
                    merged_b = merged_b + lora_b
        
        if merged_a is not None:
            merged.lora_a[module] = merged_a
            merged.lora_b[module] = merged_b
            merged.scales[module] = 1.0  # Already scaled by weights
    
    return merged


def get_lora_info(adapter_path: str) -> Optional[LoRAInfo]:
    """Get information about a LoRA adapter without fully loading it."""
    path = Path(adapter_path)
    
    if path.is_dir():
        config_path = path / "adapter_config.json"
        if config_path.exists():
            import json
            with open(config_path) as f:
                config = json.load(f)
            
            return LoRAInfo(
                adapter_name=path.stem,
                rank=config.get("r", 8),
                alpha=config.get("lora_alpha", 16),
                method=LoRAMethod.LORA,
                target_modules=config.get("target_modules", []),
                num_parameters=0,  # Would need to load weights
                memory_bytes=0,
                status=AdapterStatus.INACTIVE,
            )
    
    return None
