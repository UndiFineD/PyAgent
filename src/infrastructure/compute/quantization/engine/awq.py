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
Awq.py module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .base import Quantizer
from .config import QuantConfig
from .linear import LinearQuantizer
from .tensor import QuantizedTensor

if TYPE_CHECKING:
    from numpy.typing import NDArray


class AWQQuantizer(Quantizer):
    """Activation-Aware Weight Quantization (AWQ)."""

    def __init__(
        self,
        config: QuantConfig,
        calibration_data: NDArray[np.float32] | None = None,
    ):
        super().__init__(config)
        self.calibration_data = calibration_data
        self._importance_cache: dict[tuple[int, ...], NDArray[np.float32]] = {}

    def quantize(
        self,
        weight: NDArray[np.float32],
        activations: NDArray[np.float32] | None = None,
    ) -> QuantizedTensor:
        """Quantizes weights using activation-aware scaling to protect salient weights."""
        activations = activations if activations is not None else self.calibration_data

        if activations is not None:
            importance = self._compute_importance(activations, weight)
            scaled_weight = weight * importance
        else:
            scaled_weight = weight

        linear_quant = LinearQuantizer(self.config)
        qtensor = linear_quant.quantize(scaled_weight)

        if activations is not None:
            self._importance_cache[weight.shape] = importance

        return qtensor

    def dequantize(
        self,
        qtensor: QuantizedTensor,
    ) -> NDArray[np.float32]:
        """Dequantizes the tensor and reverses AWQ scaling if applicable."""
        result = qtensor.dequantize()
        if qtensor.shape in self._importance_cache:
            importance = self._importance_cache[qtensor.shape]
            result = result / importance
        return result

    def _compute_importance(
        self,
        activations: NDArray[np.float32],
        weight: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Calculates weight importance scores from calibration activations."""
        act_importance = np.mean(np.abs(activations), axis=0)
        weight_importance = np.max(np.abs(weight), axis=0)
        importance = act_importance * weight_importance
        importance = importance / (np.max(importance) + 1e-8)
        scales = 1.0 + importance * 0.5
        return scales.astype(np.float32)
