# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Platform abstraction package.
"""

from .models import (
    PlatformType,
    CpuArchitecture,
    QuantizationType,
    AttentionBackend,
    DeviceFeature,
    DeviceCapability,
    MemoryInfo,
    PlatformConfig,
    DeviceInfo,
)
from .base import Platform
from .cuda import CudaPlatform
from .rocm import RocmPlatform
from .tpu import TpuPlatform
from .xpu import XpuPlatform
from .cpu import CpuPlatform
from .registry import (
    PlatformRegistry,
    get_current_platform,
    detect_platform,
    get_device_count,
    get_device_capability,
    get_memory_info,
    is_quantization_supported,
    select_attention_backend,
)

__all__ = [
    "PlatformType",
    "CpuArchitecture",
    "QuantizationType",
    "AttentionBackend",
    "DeviceFeature",
    "DeviceCapability",
    "MemoryInfo",
    "PlatformConfig",
    "DeviceInfo",
    "Platform",
    "CudaPlatform",
    "RocmPlatform",
    "TpuPlatform",
    "XpuPlatform",
    "CpuPlatform",
    "PlatformRegistry",
    "get_current_platform",
    "detect_platform",
    "get_device_count",
    "get_device_capability",
    "get_memory_info",
    "is_quantization_supported",
    "select_attention_backend",
]

