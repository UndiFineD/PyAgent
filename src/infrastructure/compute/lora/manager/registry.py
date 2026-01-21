from __future__ import annotations
import threading
from collections import OrderedDict
from typing import Any, Dict, List, Optional
from .config import LoRAConfig
from .adapter import LoRAAdapter

class LoRARegistry:
    """Registry for LoRA adapters with caching."""
    def __init__(self, max_cached: int = 32):
        self._adapters: OrderedDict[str, LoRAAdapter] = OrderedDict()
        self._max_cached = max_cached
        self._lock = threading.RLock()
        self._stats = {"loads": 0, "cache_hits": 0, "evictions": 0}

    def register(self, config: LoRAConfig) -> LoRAAdapter:
        with self._lock:
            if config.adapter_name in self._adapters:
                self._stats["cache_hits"] += 1
                self._adapters.move_to_end(config.adapter_name)
                return self._adapters[config.adapter_name]
            while len(self._adapters) >= self._max_cached:
                self._adapters.popitem(last=False)
                self._stats["evictions"] += 1
            adapter = LoRAAdapter(config)
            adapter.load()
            self._adapters[config.adapter_name] = adapter
            self._stats["loads"] += 1
            return adapter

    def get(self, adapter_name: str) -> Optional[LoRAAdapter]:
        with self._lock:
            if adapter_name in self._adapters:
                self._adapters.move_to_end(adapter_name)
                return self._adapters[adapter_name]
            return None

    def unregister(self, adapter_name: str) -> bool:
        with self._lock:
            if adapter_name in self._adapters:
                del self._adapters[adapter_name]
                return True
            return False

    def list_adapters(self) -> List[str]:
        with self._lock: return list(self._adapters.keys())

    def get_stats(self) -> Dict[str, Any]:
        with self._lock: return {**self._stats, "cached": len(self._adapters), "max_cached": self._max_cached}
