from __future__ import annotations
import threading
import time
from typing import Dict, List, Optional, Any
from .config import AdapterSlot

class LoRASlotManager:
    """Manages GPU slots for LoRA adapters."""
    def __init__(self, num_slots: int = 8):
        self.num_slots = num_slots
        self._slots = [AdapterSlot(i) for i in range(num_slots)]
        self._adapter_to_slot: Dict[str, int] = {}
        self._lock = threading.Lock()

    def allocate(self, adapter_name: str, memory_required: int = 0) -> Optional[int]:
        with self._lock:
            if adapter_name in self._adapter_to_slot:
                sid = self._adapter_to_slot[adapter_name]
                self._slots[sid].is_active = True
                return sid
            for s in self._slots:
                if s.is_free:
                    self._fill_slot(s, adapter_name, memory_required)
                    return s.slot_id
            oldest = None
            otime = float('inf')
            for s in self._slots:
                if not s.is_active and s.assigned_at < otime:
                    oldest, otime = s, s.assigned_at
            if oldest:
                if oldest.adapter_name: del self._adapter_to_slot[oldest.adapter_name]
                self._fill_slot(oldest, adapter_name, memory_required)
                return oldest.slot_id
            return None

    def _fill_slot(self, slot: AdapterSlot, name: str, mem: int):
        slot.adapter_name, slot.is_active, slot.memory_allocated, slot.assigned_at = name, True, mem, time.time()
        self._adapter_to_slot[name] = slot.slot_id

    def release(self, name: str):
        with self._lock:
            if name in self._adapter_to_slot: self._slots[self._adapter_to_slot[name]].is_active = False

    def evict(self, name: str) -> bool:
        with self._lock:
            if name in self._adapter_to_slot:
                s = self._slots[self._adapter_to_slot[name]]
                s.adapter_name, s.is_active, s.memory_allocated = None, False, 0
                del self._adapter_to_slot[name]
                return True
            return False

    def get_slot(self, name: str) -> Optional[AdapterSlot]:
        with self._lock:
            if name in self._adapter_to_slot:
                return self._slots[self._adapter_to_slot[name]]
            return None

    def get_active_adapters(self) -> List[str]:
        with self._lock: return [s.adapter_name for s in self._slots if s.adapter_name and s.is_active]

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            return {"total_slots": self.num_slots, "free_slots": sum(s.is_free for s in self._slots),
                    "active_slots": sum(s.is_active for s in self._slots),
                    "loaded_adapters": len(self._adapter_to_slot)}
