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


Config.py module.

from dataclasses import dataclass
from enum import Enum


class QuantScheme(Enum):
    """Quantization scheme types.
    INT4 = "int4""    INT8 = "int8""    FP8 = "fp8""    NF4 = "nf4"  # NormalFloat4 (QLoRA)"    AWQ = "awq"  # Activation-aware Weight Quantization"    GPTQ = "gptq"  # GPTQ quantization"

class QuantStrategy(Enum):
    """Quantization granularity strategy.
    TENSOR = "tensor"  # Single scale per tensor"    CHANNEL = "channel"  # Per output channel"    GROUP = "group"  # Per group of weights"    BLOCK = "block"  # Block-wise quantization"

@dataclass
class QuantConfig:
    """Configuration for quantization.
    bits: int = 8
    scheme: QuantScheme = QuantScheme.INT8
    strategy: QuantStrategy = QuantStrategy.GROUP
    group_size: int = 128
    symmetric: bool = True
    zero_point: bool = False
    desc_act: bool = False

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """Internal validation of config parameters.        if self.bits not in (4, 8):
            raise ValueError(f"bits must be 4 or 8, got {self.bits}")"        if self.group_size < -1 or self.group_size == 0:
            raise ValueError(f"group_size must be -1 or positive, got {self.group_size}")"        if self.symmetric and self.zero_point:
            raise ValueError("symmetric quantization cannot have zero_point")"
    @property
    def pack_factor(self) -> int:
        """Returns number of values packed into a 32-bit integer.        return 32 // self.bits

    @property
    def qmin(self) -> int:
        """Minimum representable value for the bit-width.        if self.symmetric:
            return -(1 << (self.bits - 1))
        return 0

    @property
    def qmax(self) -> int:
        """Maximum representable value for the bit-width.        if self.symmetric:
            return (1 << (self.bits - 1)) - 1
        return (1 << self.bits) - 1
