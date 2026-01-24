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
Utils.py module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .awq import AWQQuantizer
from .config import QuantConfig, QuantScheme, QuantStrategy
from .gptq import GPTQQuantizer
from .linear import LinearQuantizer
from .tensor import QuantizedTensor

if TYPE_CHECKING:
    from numpy.typing import NDArray


def pack_int4(data: NDArray[np.int8]) -> NDArray[np.int8]:
    flat = data.flatten()
    if len(flat) % 2 != 0:
        flat = np.pad(flat, (0, 1), constant_values=0)

    evens = flat[0::2].astype(np.int8)
    odds = flat[1::2].astype(np.int8)

    packed = (evens & 0x0F) | ((odds & 0x0F) << 4)
    return packed.astype(np.int8)


def unpack_int4(packed: NDArray[np.int8]) -> NDArray[np.int8]:
    flat = packed.flatten()
    lower = flat & 0x0F
    upper = (flat >> 4) & 0x0F

    lower = np.where(lower > 7, lower - 16, lower)
    upper = np.where(upper > 7, upper - 16, upper)

    unpacked = np.empty(len(flat) * 2, dtype=np.int8)
    unpacked[0::2] = lower
    unpacked[1::2] = upper

    return unpacked


def compute_scales_minmax(
    weight: NDArray[np.float32],
    bits: int = 8,
    symmetric: bool = True,
) -> tuple[NDArray[np.float32], NDArray[np.int32] | None]:
    qmax = (1 << (bits - 1)) - 1 if symmetric else (1 << bits) - 1
    qmin = -(1 << (bits - 1)) if symmetric else 0

    if symmetric:
        max_val = np.max(np.abs(weight))
        scale = max_val / qmax if max_val > 0 else 1.0
        return np.array([scale], dtype=np.float32), None
    else:
        min_val = np.min(weight)
        max_val = np.max(weight)
        scale = (max_val - min_val) / (qmax - qmin)
        scale = max(scale, 1e-8)
        zp = int(round(-min_val / scale)) + qmin
        zp = np.clip(zp, qmin, qmax)
        return np.array([scale], dtype=np.float32), np.array([zp], dtype=np.int32)


def quantize_tensor(
    tensor: NDArray[np.float32],
    bits: int = 8,
    group_size: int = 128,
    symmetric: bool = True,
    scheme: str = "linear",
) -> QuantizedTensor:
    config = QuantConfig(
        bits=bits,
        scheme=QuantScheme[scheme.upper()] if scheme.upper() in QuantScheme.__members__ else QuantScheme.INT8,
        strategy=QuantStrategy.GROUP if group_size > 0 else QuantStrategy.TENSOR,
        group_size=group_size,
        symmetric=symmetric,
    )

    if scheme.lower() == "awq":
        quantizer = AWQQuantizer(config)
    elif scheme.lower() == "gptq":
        quantizer = GPTQQuantizer(config)
    else:
        quantizer = LinearQuantizer(config)

    return quantizer.quantize(tensor)


def get_quantization_error(
    original: NDArray[np.float32],
    qtensor: QuantizedTensor,
) -> dict[str, float]:
    dequant = qtensor.dequantize()

    mse = np.mean((original - dequant) ** 2)
    mae = np.mean(np.abs(original - dequant))
    max_error = np.max(np.abs(original - dequant))

    signal_power = np.mean(original**2)
    noise_power = mse
    snr = 10 * np.log10(signal_power / (noise_power + 1e-10))

    return {
        "mse": float(mse),
        "mae": float(mae),
        "max_error": float(max_error),
        "snr_db": float(snr),
        "compression_ratio": float(qtensor.compression_ratio),
    }
