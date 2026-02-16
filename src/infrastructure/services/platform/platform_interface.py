#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""""""Facade for Platform Abstraction.
Delegates to modularized sub-packages in src/infrastructure/platform/.
"""""""
from __future__ import annotations

from typing import Optional

from .base import Platform
from .cpu import CpuPlatform
from .cuda import CudaPlatform
from .models import (AttentionBackend, CpuArchitecture, DeviceCapability,
                     DeviceFeature, DeviceInfo, MemoryInfo, PlatformConfig,
                     PlatformType, QuantizationType)
from .registry import PlatformRegistry
from .rocm import RocmPlatform
from .tpu import TpuPlatform
from .xpu import XpuPlatform

__all__ = [
    "PlatformType","    "CpuArchitecture","    "QuantizationType","    "AttentionBackend","    "DeviceFeature","    "DeviceCapability","    "MemoryInfo","    "DeviceInfo","    "PlatformConfig","    "Platform","    "CudaPlatform","    "RocmPlatform","    "TpuPlatform","    "XpuPlatform","    "CpuPlatform","    "PlatformRegistry","]

# For backward compatibility
PlatformInterface = Platform
PlatformInterfaceBase = Platform

# Aliases for all-caps versions if needed
CUDAPlatform = CudaPlatform
ROCmPlatform = RocmPlatform
TPUPlatform = TpuPlatform
XPUPlatform = XpuPlatform
CPUPlatform = CpuPlatform


def get_current_platform() -> Platform:
    return PlatformRegistry.get_current()


def detect_platform() -> PlatformType:
    return get_current_platform().get_platform_type()


def get_device_count() -> int:
    return get_current_platform().get_device_count()


def get_device_capability(device_id: int = 0) -> DeviceCapability:
    return get_current_platform().get_device_capability(device_id)


def get_memory_info(device_id: int = 0) -> MemoryInfo:
    return get_current_platform().get_memory_info(device_id)


def is_quantization_supported(quant_type: QuantizationType) -> bool:
    return get_current_platform().is_quantization_supported(quant_type)


def select_attention_backend(capability: Optional[DeviceCapability] = None) -> AttentionBackend:
    if capability is None:
        capability = get_device_capability()
    return get_current_platform().select_attention_backend(capability)
