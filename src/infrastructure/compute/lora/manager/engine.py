from __future__ import annotations
import threading
from typing import Any, Dict, List, Optional
from .config import LoRAConfig, LoRARequest, LoRAInfo
from .registry import LoRARegistry
from .slot import LoRASlotManager
from .adapter import LoRAAdapter

class LoRAManager:
    """High-level LoRA management."""
    def __init__(self, max_loras: int = 16, max_gpu_slots: int = 8, max_rank: int = 64):
        self.max_loras = max_loras
        self.max_rank = max_rank
        self._registry = LoRARegistry(max_cached=max_loras)
        self._slot_manager = LoRASlotManager(num_slots=max_gpu_slots)
        self._active_requests: Dict[str, LoRARequest] = {}
        self._lock = threading.Lock()

    def load_adapter(self, config: LoRAConfig) -> LoRAInfo:
        if config.rank > self.max_rank:
            raise ValueError(f"exceeds max_rank {self.max_rank}")
        adapter = self._registry.register(config)
        if adapter.info: return adapter.info
        raise RuntimeError(f"Failed to load {config.adapter_name}")

    def unload_adapter(self, name: str) -> bool:
        self._slot_manager.evict(name)
        return self._registry.unregister(name)

    def add_request(self, request: LoRARequest) -> bool:
        adapter = self._registry.get(request.adapter_name)
        if not adapter: return False
        mem = adapter.weights.memory_bytes if adapter.weights else 0
        sid = self._slot_manager.allocate(request.adapter_name, mem)
        if sid is None: return False
        with self._lock: self._active_requests[request.request_id] = request
        return True

    def remove_request(self, rid: str):
        with self._lock:
            if rid in self._active_requests:
                req = self._active_requests.pop(rid)
                if not any(r.adapter_name == req.adapter_name for r in self._active_requests.values()):
                    self._slot_manager.release(req.adapter_name)

    def get_adapter(self, name: str) -> Optional[LoRAAdapter]: return self._registry.get(name)
    def list_loaded_adapters(self) -> List[str]: return self._registry.list_adapters()
    def get_active_adapters(self) -> List[str]: return self._slot_manager.get_active_adapters()
    def get_stats(self) -> Dict[str, Any]:
        with self._lock: return {"registry": self._registry.get_stats(), "slots": self._slot_manager.get_stats(), "active_requests": len(self._active_requests)}
