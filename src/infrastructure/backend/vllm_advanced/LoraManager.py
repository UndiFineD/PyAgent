#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
LoRA Adapter Manager for vLLM.

Provides efficient management of LoRA (Low-Rank Adaptation) adapters,
enabling dynamic switching between fine-tuned model variants without
reloading the base model.

Inspired by vLLM's v1/engine/core.py LoRA handling patterns.
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

# Check vLLM availability
try:
    from vllm.lora.request import LoRARequest
    
    HAS_LORA = True
except ImportError:
    HAS_LORA = False
    LoRARequest = None


class AdapterState(Enum):
    """State of a LoRA adapter."""
    UNLOADED = auto()
    LOADING = auto()
    LOADED = auto()
    ACTIVE = auto()
    ERROR = auto()


@dataclass
class LoraConfig:
    """Configuration for LoRA loading and management."""
    
    # Model settings
    max_lora_rank: int = 64
    max_loras: int = 4  # Max concurrent adapters
    max_cpu_loras: Optional[int] = None
    
    # Memory management
    lora_dtype: str = "auto"
    enable_lora_bias: bool = False
    
    # Caching
    cache_enabled: bool = True
    cache_max_adapters: int = 10
    
    # Loading behavior
    lazy_load: bool = True
    preload_adapters: List[str] = field(default_factory=list)


@dataclass
class LoraAdapter:
    """
    Represents a LoRA adapter.
    
    Attributes:
        adapter_id: Unique integer ID for vLLM
        name: Human-readable name
        path: Path to adapter weights
        state: Current loading state
    """
    
    adapter_id: int
    name: str
    path: str
    state: AdapterState = AdapterState.UNLOADED
    
    # Metadata
    base_model: Optional[str] = None
    rank: Optional[int] = None
    alpha: Optional[float] = None
    target_modules: List[str] = field(default_factory=list)
    
    # Stats
    load_count: int = 0
    last_used: Optional[float] = None
    load_time_ms: Optional[float] = None
    
    # Computed
    _hash: Optional[str] = None
    
    @property
    def hash(self) -> str:
        """Get unique hash for this adapter."""
        if self._hash is None:
            content = f"{self.name}:{self.path}:{self.rank}:{self.alpha}"
            self._hash = hashlib.md5(content.encode()).hexdigest()[:12]
        return self._hash
    
    def to_lora_request(self) -> "LoRARequest":
        """Convert to vLLM LoRARequest."""
        if not HAS_LORA:
            raise RuntimeError("LoRA support not available")
        
        return LoRARequest(
            lora_name=self.name,
            lora_int_id=self.adapter_id,
            lora_path=self.path,
        )
    
    def mark_used(self) -> None:
        """Mark adapter as recently used."""
        self.last_used = time.time()
        self.load_count += 1


class LoraRegistry:
    """
    Registry for tracking available LoRA adapters.
    
    Maintains a catalog of adapters that can be loaded on demand.
    """
    
    def __init__(self):
        self._adapters: Dict[str, LoraAdapter] = {}
        self._id_counter = 1
        self._name_to_id: Dict[str, int] = {}
    
    def register(
        self,
        name: str,
        path: str,
        base_model: Optional[str] = None,
        rank: Optional[int] = None,
        alpha: Optional[float] = None,
        target_modules: Optional[List[str]] = None,
    ) -> LoraAdapter:
        """
        Register a new LoRA adapter.
        
        Args:
            name: Unique name for the adapter
            path: Path to adapter weights (local or HuggingFace)
            base_model: Base model the adapter was trained on
            rank: LoRA rank
            alpha: LoRA alpha scaling
            target_modules: Modules the adapter modifies
            
        Returns:
            The registered LoraAdapter
        """
        if name in self._adapters:
            logging.warning(f"Adapter '{name}' already registered, updating")
            adapter = self._adapters[name]
            adapter.path = path
            adapter.base_model = base_model
            adapter.rank = rank
            adapter.alpha = alpha
            if target_modules:
                adapter.target_modules = target_modules
            return adapter
        
        adapter_id = self._id_counter
        self._id_counter += 1
        
        adapter = LoraAdapter(
            adapter_id=adapter_id,
            name=name,
            path=path,
            base_model=base_model,
            rank=rank,
            alpha=alpha,
            target_modules=target_modules or [],
        )
        
        self._adapters[name] = adapter
        self._name_to_id[name] = adapter_id
        
        logging.info(f"Registered LoRA adapter: {name} (ID: {adapter_id})")
        return adapter
    
    def unregister(self, name: str) -> bool:
        """Remove an adapter from the registry."""
        if name not in self._adapters:
            return False
        
        adapter = self._adapters.pop(name)
        self._name_to_id.pop(name, None)
        
        logging.info(f"Unregistered LoRA adapter: {name}")
        return True
    
    def get(self, name: str) -> Optional[LoraAdapter]:
        """Get adapter by name."""
        return self._adapters.get(name)
    
    def get_by_id(self, adapter_id: int) -> Optional[LoraAdapter]:
        """Get adapter by ID."""
        for adapter in self._adapters.values():
            if adapter.adapter_id == adapter_id:
                return adapter
        return None
    
    def list_adapters(self) -> List[LoraAdapter]:
        """List all registered adapters."""
        return list(self._adapters.values())
    
    def list_loaded(self) -> List[LoraAdapter]:
        """List adapters that are currently loaded."""
        return [
            a for a in self._adapters.values()
            if a.state in (AdapterState.LOADED, AdapterState.ACTIVE)
        ]
    
    def find_by_base_model(self, base_model: str) -> List[LoraAdapter]:
        """Find adapters compatible with a base model."""
        return [
            a for a in self._adapters.values()
            if a.base_model == base_model
        ]


class LoraManager:
    """
    Manager for dynamic LoRA adapter switching.
    
    Provides:
    - Registration and discovery of adapters
    - Dynamic loading/unloading
    - LRU caching for frequently used adapters
    - Request-level adapter binding
    
    Example:
        manager = LoraManager(config=LoraConfig(max_loras=4))
        
        # Register adapters
        manager.register_adapter("code-assistant", "/path/to/adapter")
        manager.register_adapter("chat-friendly", "/path/to/chat-adapter")
        
        # Generate with specific adapter
        lora_request = manager.get_lora_request("code-assistant")
        # Pass to vLLM generate()
        
        # Switch adapters dynamically
        manager.activate("chat-friendly")
    """
    
    def __init__(
        self,
        config: Optional[LoraConfig] = None,
        registry: Optional[LoraRegistry] = None,
    ):
        self.config = config or LoraConfig()
        self.registry = registry or LoraRegistry()
        
        self._active_adapters: Set[str] = set()
        self._lru_cache: List[str] = []  # Most recently used at end
        
        # Stats
        self._stats = {
            "total_loads": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "evictions": 0,
        }
    
    @property
    def is_available(self) -> bool:
        """Check if LoRA support is available."""
        return HAS_LORA
    
    def register_adapter(
        self,
        name: str,
        path: str,
        **kwargs,
    ) -> LoraAdapter:
        """Register a new adapter."""
        return self.registry.register(name, path, **kwargs)
    
    def unregister_adapter(self, name: str) -> bool:
        """Unregister an adapter."""
        # Deactivate first if active
        if name in self._active_adapters:
            self.deactivate(name)
        
        return self.registry.unregister(name)
    
    def get_adapter(self, name: str) -> Optional[LoraAdapter]:
        """Get adapter by name."""
        return self.registry.get(name)
    
    def activate(self, name: str) -> bool:
        """
        Activate a LoRA adapter for use.
        
        If max_loras limit is reached, evicts least recently used adapter.
        """
        adapter = self.registry.get(name)
        if not adapter:
            logging.error(f"Adapter not found: {name}")
            return False
        
        if name in self._active_adapters:
            # Already active, just update LRU
            self._update_lru(name)
            self._stats["cache_hits"] += 1
            return True
        
        self._stats["cache_misses"] += 1
        
        # Check capacity
        if len(self._active_adapters) >= self.config.max_loras:
            # Evict LRU
            if not self._evict_lru():
                logging.error("Failed to evict adapter for new activation")
                return False
        
        # Activate
        start_time = time.time()
        adapter.state = AdapterState.LOADING
        
        try:
            # In a real implementation, this would trigger vLLM to load weights
            adapter.state = AdapterState.ACTIVE
            adapter.load_time_ms = (time.time() - start_time) * 1000
            adapter.mark_used()
            
            self._active_adapters.add(name)
            self._update_lru(name)
            self._stats["total_loads"] += 1
            
            logging.info(f"Activated LoRA adapter: {name} ({adapter.load_time_ms:.1f}ms)")
            return True
            
        except Exception as e:
            adapter.state = AdapterState.ERROR
            logging.error(f"Failed to activate adapter {name}: {e}")
            return False
    
    def deactivate(self, name: str) -> bool:
        """Deactivate a LoRA adapter."""
        if name not in self._active_adapters:
            return False
        
        adapter = self.registry.get(name)
        if adapter:
            adapter.state = AdapterState.LOADED
        
        self._active_adapters.discard(name)
        if name in self._lru_cache:
            self._lru_cache.remove(name)
        
        logging.info(f"Deactivated LoRA adapter: {name}")
        return True
    
    def _update_lru(self, name: str) -> None:
        """Update LRU cache ordering."""
        if name in self._lru_cache:
            self._lru_cache.remove(name)
        self._lru_cache.append(name)
    
    def _evict_lru(self) -> bool:
        """Evict least recently used adapter."""
        if not self._lru_cache:
            return False
        
        lru_name = self._lru_cache[0]
        if self.deactivate(lru_name):
            self._stats["evictions"] += 1
            logging.info(f"Evicted LRU adapter: {lru_name}")
            return True
        
        return False
    
    def get_lora_request(self, name: str) -> Optional["LoRARequest"]:
        """
        Get a LoRARequest for use with vLLM generate().
        
        Automatically activates the adapter if not already active.
        """
        if not HAS_LORA:
            logging.warning("LoRA not available")
            return None
        
        adapter = self.registry.get(name)
        if not adapter:
            logging.error(f"Adapter not found: {name}")
            return None
        
        # Ensure activated
        if name not in self._active_adapters:
            if not self.activate(name):
                return None
        else:
            # Update usage
            adapter.mark_used()
            self._update_lru(name)
        
        return adapter.to_lora_request()
    
    def get_active_adapters(self) -> List[LoraAdapter]:
        """Get list of currently active adapters."""
        return [
            self.registry.get(name)
            for name in self._active_adapters
            if self.registry.get(name) is not None
        ]
    
    def list_adapters(self) -> List[Dict[str, Any]]:
        """List all registered adapters with status."""
        return [
            {
                "name": a.name,
                "path": a.path,
                "state": a.state.name,
                "is_active": a.name in self._active_adapters,
                "load_count": a.load_count,
                "last_used": a.last_used,
            }
            for a in self.registry.list_adapters()
        ]
    
    def preload_adapters(self, names: Optional[List[str]] = None) -> int:
        """
        Preload adapters for faster switching.
        
        Returns count of successfully preloaded adapters.
        """
        names = names or self.config.preload_adapters
        loaded = 0
        
        for name in names:
            if self.activate(name):
                loaded += 1
        
        return loaded
    
    def clear_cache(self) -> None:
        """Deactivate all adapters."""
        for name in list(self._active_adapters):
            self.deactivate(name)
        
        self._lru_cache.clear()
        logging.info("Cleared LoRA adapter cache")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get manager statistics."""
        return {
            **self._stats,
            "active_count": len(self._active_adapters),
            "registered_count": len(self.registry.list_adapters()),
            "max_loras": self.config.max_loras,
            "hit_rate": (
                self._stats["cache_hits"] / 
                max(1, self._stats["cache_hits"] + self._stats["cache_misses"])
            ),
        }


# Convenience functions
def create_lora_request(
    name: str,
    adapter_id: int,
    path: str,
) -> Optional["LoRARequest"]:
    """Create a LoRARequest directly."""
    if not HAS_LORA:
        return None
    
    return LoRARequest(
        lora_name=name,
        lora_int_id=adapter_id,
        lora_path=path,
    )


def discover_adapters(
    directory: Union[str, Path],
    pattern: str = "adapter_config.json",
) -> List[Dict[str, Any]]:
    """
    Discover LoRA adapters in a directory.
    
    Scans for adapter_config.json files (standard HuggingFace PEFT format).
    """
    import json
    
    directory = Path(directory)
    adapters = []
    
    for config_path in directory.rglob(pattern):
        try:
            with open(config_path) as f:
                config = json.load(f)
            
            adapters.append({
                "name": config_path.parent.name,
                "path": str(config_path.parent),
                "base_model": config.get("base_model_name_or_path"),
                "rank": config.get("r"),
                "alpha": config.get("lora_alpha"),
                "target_modules": config.get("target_modules", []),
            })
        except Exception as e:
            logging.debug(f"Failed to parse adapter config {config_path}: {e}")
    
    return adapters
