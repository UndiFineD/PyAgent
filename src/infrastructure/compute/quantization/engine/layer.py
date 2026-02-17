#!/usr/bin/env python3
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


Layer.py module.

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .tensor import QuantizedTensor

if TYPE_CHECKING:
    from numpy.typing import NDArray


class DequantizedLinear:
    """Dequantized linear layer for inference.
    def __init__(
        self,
        qweight: QuantizedTensor,
        bias: NDArray[np.float32] | None = None,
    ) -> None:
        """Initializes a layer with quantized weights and optional bias.        self.qweight: QuantizedTensor = qweight
        self.bias: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] | None = bias
        self._dequant_cache: NDArray[np.float32] | None = None

    def forward(
        self,
        x: NDArray[np.float32],
        use_cache: bool = True,
    ) -> NDArray[np.float32]:
        """Performs a forward pass, dequantizing the weights on-the-fly.        if use_cache and self._dequant_cache is not None:
            weight = self._dequant_cache
        else:
            weight: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = self.qweight.dequantize()
            if use_cache:
                self._dequant_cache = weight

        output = x @ weight.T

        if self.bias is not None:
            output = output + self.bias

        return output

    def clear_cache(self) -> None:
        """Flushes the dequantized weight cache to save memory.        self._dequant_cache = None

    @property
    def in_features(self) -> int:
        """Returns the number of input features.        return self.qweight.shape[1] if len(self.qweight.shape) >= 2 else self.qweight.shape[0]

    @property
    def out_features(self) -> int:
        """Returns the number of output features.        return self.qweight.shape[0]
