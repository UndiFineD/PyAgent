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


Linear.py module.
"""

try:
    from typing import TYPE_CHECKING
except ImportError:
    from typing import TYPE_CHECKING


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .base import Quantizer
except ImportError:
    from .base import Quantizer

try:
    from .config import QuantStrategy
except ImportError:
    from .config import QuantStrategy

try:
    from .tensor import QuantizedTensor
except ImportError:
    from .tensor import QuantizedTensor


if TYPE_CHECKING:
    from numpy.typing import NDArray



class LinearQuantizer(Quantizer):
    """Linear (uniform) quantization.
    def quantize(
        self,
        weight: NDArray[np.float32],
    ) -> QuantizedTensor:
        """Quantizes a float matrix into the configured bit-depth.        from .utils import pack_int4

        original_shape = weight.shape

        if self.config.strategy == QuantStrategy.TENSOR:
            scale, zp = self.compute_tensor_params(weight)
            qweight = self.quantize_linear(weight, scale, zp)
        elif self.config.strategy == QuantStrategy.CHANNEL:
            scale, zp = self.compute_channel_params(weight)
            qweight = self.quantize_per_channel(weight, scale, zp)
        else:
            scale, zp = self.compute_group_params(weight)
            qweight = self.quantize_per_group(weight, scale, zp)

        if self.config.bits == 4:
            qweight = pack_int4(qweight)

        return QuantizedTensor(
            data=qweight,
            scale=scale,
            zero_point=zp,
            shape=original_shape,
            config=self.config,
        )

    def dequantize(
        self,
        qtensor: QuantizedTensor,
    ) -> NDArray[np.float32]:
        """Restores a float matrix from the quantized representation.        return qtensor.dequantize()

    def compute_tensor_params(
        self,
        weight: NDArray[np.float32],
    ) -> tuple[NDArray[np.float32], NDArray[np.int32] | None]:
        """Computes quantization parameters for the entire tensor.        if self.config.symmetric:
            max_val = np.max(np.abs(weight))
            scale = max_val / self.config.qmax if max_val > 0 else 1.0
            return np.array([scale], dtype=np.float32), None

        min_val = np.min(weight)
        max_val = np.max(weight)
        scale = (max_val - min_val) / (self.config.qmax - self.config.qmin)
        scale = max(scale, 1e-8)
        zp = int(round(-min_val / scale)) + self.config.qmin
        zp = np.clip(zp, self.config.qmin, self.config.qmax)
        return np.array([scale], dtype=np.float32), np.array([zp], dtype=np.int32)

    def compute_channel_params(
        self,
        weight: NDArray[np.float32],
    ) -> tuple[NDArray[np.float32], NDArray[np.int32] | None]:
        """Computes quantization parameters per output channel.        num_channels = weight.shape[0]
        weight_flat = weight.reshape(num_channels, -1)

        if self.config.symmetric:
            max_vals = np.max(np.abs(weight_flat), axis=1)
            scales = np.where(max_vals > 0, max_vals / self.config.qmax, 1.0)
            return scales.astype(np.float32), None

        min_vals = np.min(weight_flat, axis=1)
        max_vals = np.max(weight_flat, axis=1)
        scales = (max_vals - min_vals) / (self.config.qmax - self.config.qmin)
        scales = np.maximum(scales, 1e-8)
        zps = np.round(-min_vals / scales).astype(np.int32) + self.config.qmin
        zps = np.clip(zps, self.config.qmin, self.config.qmax)
        return scales.astype(np.float32), zps.astype(np.int32)

    def compute_group_params(
        self,
        weight: NDArray[np.float32],
    ) -> tuple[NDArray[np.float32], NDArray[np.int32] | None]:
        """Computes quantization parameters per group of weights.        out_features, in_features = weight.shape[:2] if weight.ndim >= 2 else (weight.shape[0], 1)
        flat = weight.reshape(out_features, -1)
        in_features = flat.shape[1]

        num_groups = (in_features + self.config.group_size - 1) // self.config.group_size

        scales = []
        zps = [] if not self.config.symmetric else None

        for g in range(num_groups):
            start = g * self.config.group_size
            end = min(start + self.config.group_size, in_features)
            group = flat[:, start:end]

            if self.config.symmetric:
                max_val = np.max(np.abs(group), axis=1)
                scale = np.where(max_val > 0, max_val / self.config.qmax, 1.0)
                scales.append(scale)
            else:
                min_val = np.min(group, axis=1)
                max_val = np.max(group, axis=1)
                scale = (max_val - min_val) / (self.config.qmax - self.config.qmin)
                scale = np.maximum(scale, 1e-8)
                zp = np.round(-min_val / scale).astype(np.int32) + self.config.qmin
                zp = np.clip(zp, self.config.qmin, self.config.qmax)
                scales.append(scale)
                zps.append(zp)

        scales = np.stack(scales, axis=1).astype(np.float32)
        zps = np.stack(zps, axis=1).astype(np.int32) if zps else None
        return scales, zps

    def quantize_linear(
        self,
        weight: NDArray[np.float32],
        scale: NDArray[np.float32],
        zp: NDArray[np.int32] | None,
    ) -> NDArray[np.int8]:
        """Quantizes the entire tensor using a single scale/zero-point.        scaled = weight / scale[0]
        if zp is not None:
            scaled = scaled + zp[0]
        clipped = np.clip(scaled, self.config.qmin, self.config.qmax)
        return np.round(clipped).astype(np.int8)

    def quantize_per_channel(
        self,
        weight: NDArray[np.float32],
        scale: NDArray[np.float32],
        zp: NDArray[np.int32] | None,
    ) -> NDArray[np.int8]:
        """Quantizes the tensor per output channel.        num_channels = weight.shape[0]
        weight_flat = weight.reshape(num_channels, -1)

        scaled = weight_flat / scale[:, None]
        if zp is not None:
            scaled = scaled + zp[:, None]
        clipped = np.clip(scaled, self.config.qmin, self.config.qmax)
        return np.round(clipped).reshape(weight.shape).astype(np.int8)

    def quantize_per_group(
        self,
        weight: NDArray[np.float32],
        scale: NDArray[np.float32],
        zp: NDArray[np.int32] | None,
    ) -> NDArray[np.int8]:
        """Quantizes the tensor in grouped blocks.        original_shape = weight.shape
        out_features = weight.shape[0]
        flat = weight.reshape(out_features, -1)
        in_features = flat.shape[1]

        qweight = np.zeros_like(flat, dtype=np.int8)

        for g in range(scale.shape[1]):
            start = g * self.config.group_size
            end = min(start + self.config.group_size, in_features)
            group = flat[:, start:end]

            scaled = group / scale[:, g : g + 1]
            if zp is not None:
                scaled = scaled + zp[:, g : g + 1]
            qweight[:, start:end] = np.clip(np.round(scaled), self.config.qmin, self.config.qmax).astype(np.int8)

        return qweight.reshape(original_shape).astype(np.int8)
