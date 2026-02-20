#!/usr/bin/env python3
from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Weights.py module.
"""

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from typing import TYPE_CHECKING, Dict, List, Optional, Set
except ImportError:
    from typing import TYPE_CHECKING, Dict, List, Optional, Set


try:
    import numpy
except ImportError:
    import numpy
 as np

if TYPE_CHECKING:
    from .adapter import LoRAAdapter


@dataclass
class LoRAWeights:
    """LoRA weight matrices.
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


def merge_adapters(adapters: List["LoRAAdapter"], weights: Optional[List[float]] = None) -> LoRAWeights:"    if not adapters:
        raise ValueError("No adapters to merge")"    if weights is None:
        weights = [1.0 / len(adapters)] * len(adapters)
    if len(weights) != len(adapters):
        raise ValueError("Number of weights must match adapters")"
    merged = LoRAWeights()
    all_modules: Set[str] = set()
    for adapter in adapters:
        if adapter.weights:
            all_modules.update(adapter.weights.lora_a.keys())

    for module in all_modules:
        m_a, m_b = None, None
        for adapter, weight in zip(adapters, weights):
            if adapter.weights and module in adapter.weights.lora_a:
                la = adapter.weights.lora_a[module] * weight
                lb = adapter.weights.lora_b[module] * weight
                if m_a is None:
                    m_a, m_b = la, lb
                else:
                    m_a, m_b = m_a + la, m_b + lb
        if m_a is not None:
            merged.lora_a[module] = m_a
            merged.lora_b[module] = m_b
            merged.scales[module] = 1.0
    return merged
