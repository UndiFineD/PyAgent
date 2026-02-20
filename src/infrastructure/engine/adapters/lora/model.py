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


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""LoRA model container.

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from .config import LoRAConfig
from .weights import LoRALayerWeights

try:
    from numpy.typing import NDArray
except ImportError:
    NDArray = Any


@dataclass
class LoRAModel:
    """Complete LoRA model with all adapter weights.
    model_id: str
    config: LoRAConfig
    layers: dict[str, LoRALayerWeights] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_layer(self, layer: LoRALayerWeights) -> None:
        """Add a layer to the model.        self.layers[layer.module_name] = layer

    def get_layer(self, module_name: str) -> LoRALayerWeights | None:
        """Get layer weights by module name.        return self.layers.get(module_name)

    def forward(
        self,
        module_name: str,
        x: NDArray[np.float32],
        apply_dropout: bool = False,
    ) -> NDArray[np.float32] | None:
        """Compute LoRA output for a module.        layer = self.layers.get(module_name)
        if layer is None:
            return None
        return layer.forward(x, apply_dropout)

    def get_memory_bytes(self) -> int:
        """Total memory usage in bytes.        return sum(layer.get_memory_bytes() for layer in self.layers.values())

    @property
    def num_parameters(self) -> int:
        """Total number of LoRA parameters.        return sum(layer.lora_a.size + layer.lora_b.size for layer in self.layers.values())
