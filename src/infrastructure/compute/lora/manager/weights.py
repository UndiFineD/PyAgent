from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import numpy as np

@dataclass
class LoRAWeights:
    """LoRA weight matrices."""
    lora_a: Dict[str, np.ndarray] = field(default_factory=dict)
    lora_b: Dict[str, np.ndarray] = field(default_factory=dict)
    scales: Dict[str, float] = field(default_factory=dict)
    dora_magnitudes: Optional[Dict[str, np.ndarray]] = None

    @property
    def num_parameters(self) -> int:
        total = 0
        for m in self.lora_a:
            total += self.lora_a[m].size + self.lora_b[m].size
        return total

    @property
    def memory_bytes(self) -> int:
        total = 0
        for m in self.lora_a:
            total += self.lora_a[m].nbytes + self.lora_b[m].nbytes
        return total

def merge_adapters(adapters: List["LoRAAdapter"], weights: Optional[List[float]] = None) -> LoRAWeights:
    if not adapters: raise ValueError("No adapters to merge")
    if weights is None: weights = [1.0 / len(adapters)] * len(adapters)
    if len(weights) != len(adapters):
        raise ValueError("Number of weights must match adapters")

    merged = LoRAWeights()
    all_modules: Set[str] = set()
    for adapter in adapters:
        if adapter.weights: all_modules.update(adapter.weights.lora_a.keys())

    for module in all_modules:
        m_a, m_b = None, None
        for adapter, weight in zip(adapters, weights):
            if adapter.weights and module in adapter.weights.lora_a:
                la = adapter.weights.lora_a[module] * weight
                lb = adapter.weights.lora_b[module] * weight
                if m_a is None: m_a, m_b = la, lb
                else: m_a, m_b = m_a + la, m_b + lb
        if m_a is not None:
            merged.lora_a[module], merged.lora_b[module] = m_a, m_b
            merged.scales[module] = 1.0
    return merged
