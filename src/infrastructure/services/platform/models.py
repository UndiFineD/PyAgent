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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Platform-related data models and enums.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import List, NamedTuple, Optional, Set


class PlatformType(Enum):
    """Supported platform types."""

    CUDA = "cuda"
    ROCM = "rocm"
    TPU = "tpu"
    XPU = "xpu"
    CPU = "cpu"
    OOT = "out_of_tree"  # Out-of-tree custom platforms
    UNKNOWN = "unknown"


class CpuArchitecture(Enum):
    """CPU architecture types."""

    X86_64 = "x86_64"
    ARM64 = "arm64"
    AARCH64 = "aarch64"
    POWERPC = "powerpc"
    S390X = "s390x"
    RISCV = "riscv"


class QuantizationType(Enum):
    """Quantization methods."""

    NONE = "none"
    GPTQ = "gptq"
    AWQ = "awq"
    SQUEEZELLM = "squeezellm"
    FP8 = "fp8"
    FP8_E4M3 = "fp8_e4m3"
    FP8_E5M2 = "fp8_e5m2"
    INT8 = "int8"
    INT4 = "int4"
    NF4 = "nf4"
    GGUF = "gguf"
    BITSANDBYTES = "bitsandbytes"
    EXLLAMA = "exllama"
    EXLLAMA_V2 = "exllama_v2"
    MARLIN = "marlin"


class AttentionBackend(Enum):
    """Attention implementation backends."""

    FLASH_ATTN = "flash_attn"
    FLASH_ATTN_V2 = "flash_attn_v2"
    FLASH_ATTN_V3 = "flash_attn_v3"
    XFORMERS = "xformers"
    TORCH_SDPA = "torch_sdpa"
    FLASHINFER = "flashinfer"
    PAGED_ATTENTION = "paged_attention"
    TRITON = "triton"
    ROCM = "rocm"
    TPU = "tpu"
    CPU = "cpu"
    DEFAULT = "default"


class DeviceFeature(Flag):
    """Device feature flags."""

    NONE = 0
    TENSOR_CORES = auto()
    FP16 = auto()
    BF16 = auto()
    FP8 = auto()
    INT8 = auto()
    INT4 = auto()
    FLASH_ATTENTION = auto()
    PAGED_ATTENTION = auto()
    CUDA_GRAPHS = auto()
    UNIFIED_MEMORY = auto()
    MULTI_GPU = auto()
    PEER_ACCESS = auto()
    NVLINK = auto()
    INFINITY_FABRIC = auto()  # AMD
    ASYNC_COPY = auto()
    SPARSE_OPS = auto()


class DeviceCapability(NamedTuple):
    """Device compute capability."""

    major: int
    minor: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def __ge__(self, other: "DeviceCapability") -> bool:
        return (self.major, self.minor) >= (other.major, other.minor)

    def __gt__(self, other: "DeviceCapability") -> bool:
        return (self.major, self.minor) > (other.major, other.minor)

    @property
    def as_int(self) -> int:
        """Return capability as integer (e.g., 80 for 8.0)."""
        return self.major * 10 + self.minor


@dataclass
class MemoryInfo:
    """Device memory information."""

    total_bytes: int
    free_bytes: int
    used_bytes: int
    reserved_bytes: int = 0

    @property
    def total_gb(self) -> float:
        return self.total_bytes / (1024**3)

    @property
    def free_gb(self) -> float:
        return self.free_bytes / (1024**3)

    @property
    def used_gb(self) -> float:
        return self.used_bytes / (1024**3)

    @property
    def utilization(self) -> float:
        """Memory utilization as percentage."""
        if self.total_bytes == 0:
            return 0.0
        return self.used_bytes / self.total_bytes * 100


@dataclass
class DeviceInfo:
    """Complete device information."""

    device_id: int
    name: str
    platform: PlatformType
    capability: DeviceCapability
    memory: MemoryInfo
    features: DeviceFeature
    driver_version: str = ""
    compute_units: int = 0
    clock_rate_mhz: int = 0
    pcie_bandwidth_gbps: float = 0.0

    def supports_feature(self, feature: DeviceFeature) -> bool:
        """Check if device supports a feature."""
        return bool(self.features & feature)

    @property
    def is_datacenter(self) -> bool:
        """Check if device is a datacenter GPU."""
        datacenter_patterns = ["A100", "H100", "H200", "V100", "MI250", "MI300"]
        return any(p in self.name for p in datacenter_patterns)


@dataclass
class PlatformConfig:
    """Platform configuration."""

    platform_type: PlatformType
    device_ids: List[int] = field(default_factory=list)
    memory_fraction: float = 0.9
    enable_cuda_graphs: bool = True
    enable_flash_attention: bool = True
    attention_backend: Optional[AttentionBackend] = None
    quantization_types: Set[QuantizationType] = field(default_factory=set)
    custom_ops_enabled: bool = True
    compile_backend: str = "inductor"
