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


Tensor.py module.
"""


from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .config import QuantConfig

if TYPE_CHECKING:
    from numpy.typing import NDArray




class QuantizedTensor:
    """Quantized tensor representation.
    def __init__(
        self,
        data: NDArray[np.int8] | NDArray[np.int32],
        scale: NDArray[np.float32],
        zero_point: NDArray[np.int32] | None,
        shape: tuple[int, ...],
        config: QuantConfig,
    ) -> None:
        """Initializes a quantized tensor with data and calibration parameters.        self.data: (
            np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._8Bit]]]
            | np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._32Bit]]]
        ) = data
        self.scale = scale
        self.zero_point: (
            np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._32Bit]]] | None
        ) = zero_point
        self.shape: tuple[int, ...] = shape
        self.config: QuantConfig = config

    def dequantize(self) -> NDArray[np.float32]:
        """Reconstructs float32 values from the quantized data.        from .utils import unpack_int4

        if self.config.bits == 4:
            unpacked: np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._8Bit]]] = (
                unpack_int4(self.data)
            )
        else:
            unpacked: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = (
                self.data.astype(np.float32)
            )

        unpacked_reshaped: (
            np.ndarray[tuple[int, ...], np.dtype[np.signedinteger[np._8Bit]]]
            | np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]]
        ) = unpacked.reshape(self.shape)

        if self.scale.size == 1:
            if self.zero_point is not None:
                result = (unpacked_reshaped - self.zero_point.item()) * self.scale.item()
            else:
                result = unpacked_reshaped * self.scale.item()
        elif self.scale.ndim == 1 and self.scale.shape[0] == self.shape[0]:
            if self.zero_point is not None:
                result = (unpacked_reshaped - self.zero_point[:, None]) * self.scale[:, None]
            else:
                result = unpacked_reshaped * self.scale[:, None]
        elif self.scale.ndim == 2:
            out_features: int = self.shape[0]
            in_features: int = self.shape[1] if len(self.shape) > 1 else 1
            num_groups: int = self.scale.shape[1]
            group_size: int = (in_features + num_groups - 1) // num_groups

            result: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = (
                np.zeros(self.shape, dtype=np.float32)
            )
            flat: (
                np.ndarray[tuple[int, int], np.dtype[np.signedinteger[np._8Bit]]]
                | np.ndarray[tuple[int, int], np.dtype[np.floating[np._32Bit]]]
            ) = unpacked_reshaped.reshape(out_features, -1)

            for g in range(num_groups):
                start: int = g * group_size
                end: int = min(start + group_size, in_features)
                if self.zero_point is not None:
                    result[:, start:end] = (flat[:, start:end] - self.zero_point[:, g : g + 1]) * self.scale[
                        :, g : g + 1
                    ]
                else:
                    result[:, start:end] = flat[:, start:end] * self.scale[:, g : g + 1]
        else:
            if self.zero_point is not None:
                result = (unpacked_reshaped - self.zero_point) * self.scale
            else:
                result = unpacked_reshaped * self.scale

        return result.reshape(self.shape).astype(np.float32)

    @property
    def memory_bytes(self) -> int:
        """Calculates total memory footprint of the quantized tensor (bytes).        data_bytes: int = self.data.nbytes
        scale_bytes: int = self.scale.nbytes
        zp_bytes: int = self.zero_point.nbytes if self.zero_point is not None else 0
        return data_bytes + scale_bytes + zp_bytes

    @property
    def compression_ratio(self) -> float:
        """Returns the ratio between FP32 size and current memory usage.        original_bytes: np.signedinteger[np._64Bit] = np.prod(self.shape) * 4  # FP32
        return original_bytes / self.memory_bytes
