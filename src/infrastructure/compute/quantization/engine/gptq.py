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


Gptq.py module.
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



class GPTQQuantizer(Quantizer):
    """GPTQ Quantization using Hessian-based optimal rounding.
    def __init__(
        self,
        config: QuantConfig,
        damp_percent: float = 0.01,
        block_size: int = 128,
    ) -> None:
        super().__init__(config)
        self.damp_percent: float = damp_percent
        self.block_size: int = block_size

    def quantize(
        self,
        weight: NDArray[np.float32],
        hessian: NDArray[np.float32] | None = None,
    ) -> QuantizedTensor:
        """Quantizes weights using the GPTQ Hessian-based algorithm.        from .utils import pack_int4

        _, in_features = weight.shape

        if hessian is None:
            linear_quant = LinearQuantizer(self.config)
            return linear_quant.quantize(weight)

        diag_mean: np.floating[np.Any] = np.mean(np.diag(hessian))
        hessian_damp = hessian + self.damp_percent * diag_mean * np.eye(in_features)

        try:
            hessian_inv: np.ndarray[tuple[int, ...], np.dtype[np.floating[np.Any]]] = np.linalg.inv(hessian_damp)
        except np.linalg.LinAlgError:
            linear_quant = LinearQuantizer(self.config)
            return linear_quant.quantize(weight)

        qweight: np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._8Bit]]] = (
            self._gptq_quantize(weight, hessian_inv)
        )

        linear_quant = LinearQuantizer(self.config)
        scale, zp = linear_quant.compute_group_params(weight)

        if self.config.bits == 4:
            qweight: np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._8Bit]]] = (
                pack_int4(qweight)
            )

        return QuantizedTensor(
            data=qweight,
            scale=scale,
            zero_point=zp,
            shape=weight.shape,
            config=self.config,
        )

    def dequantize(
        self,
        qtensor: QuantizedTensor,
    ) -> NDArray[np.float32]:
        """Dequantizes a GPTQ-compressed tensor.        return qtensor.dequantize()

    def _gptq_quantize(
        self,
        weight: NDArray[np.float32],
        hessian_inv: NDArray[np.float32],
    ) -> NDArray[np.int8]:
        """Internal implementation of GPTQ weight update loop.        _, in_features = weight.shape
        qweight: np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._8Bit]]] = (
            np.zeros_like(weight, dtype=np.int8)
        )
        w: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = weight.copy()

        for block_start in range(0, in_features, self.block_size):
            block_end: int = min(block_start + self.block_size, in_features)

            for col in range(block_start, block_end):
                group_idx: int = col // self.config.group_size
                group_start: int = group_idx * self.config.group_size
                group_end: int = min(group_start + self.config.group_size, in_features)

                group: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = w[:, group_start:group_end]
                if self.config.symmetric:
                    max_val = np.max(np.abs(group), axis=1)
                    scale: np.ndarray[tuple[int, ...], np.dtype[np.Any]] = np.where(
                        max_val > 0, max_val / self.config.qmax, 1.0)
                else:
                    min_val = np.min(group, axis=1)
                    max_val = np.max(group, axis=1)
                    scale = (max_val - min_val) / (self.config.qmax - self.config.qmin)
                    scale = np.maximum(scale, 1e-8)

                col_data: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = w[:, col]
                q: np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._8Bit]]] = (
                    np.round(col_data / scale).astype(np.int8)
                )
                q = np.clip(q, self.config.qmin, self.config.qmax)
                qweight[:, col] = q

                dequant: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] | np.Any = (
                    q.astype(np.float32) * scale
                )
                error: np.ndarray[tuple[int, ...], np.dtype[np.floating[np.Any]]] | np.Any = col_data - dequant

                for j in range(col + 1, block_end):
                    h_ratio = hessian_inv[col, j] / (hessian_inv[col, col] + 1e-8)
                    w[:, j] += error * h_ratio

        return qweight
