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
Platform abstraction package.
"""

from .base import Platform  # noqa: F401
from .cpu import CpuPlatform  # noqa: F401
from .cuda import CudaPlatform  # noqa: F401
from .models import (AttentionBackend, CpuArchitecture, DeviceCapability,  # noqa: F401
                     DeviceFeature, DeviceInfo, MemoryInfo, PlatformConfig,
                     PlatformType, QuantizationType)
from .registry import (PlatformRegistry, detect_platform, get_current_platform,  # noqa: F401
                       get_device_capability, get_device_count,
                       get_memory_info, is_quantization_supported,
                       select_attention_backend)
from .rocm import RocmPlatform  # noqa: F401
from .tpu import TpuPlatform  # noqa: F401
from .xpu import XpuPlatform  # noqa: F401

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
