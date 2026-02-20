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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Registry for platform implementations.
"""

import logging
import threading
from typing import Dict, Optional, Type

from .base import Platform
from .cpu import CpuPlatform
from .cuda import CudaPlatform
from .models import (AttentionBackend, DeviceCapability, MemoryInfo,
                     PlatformType, QuantizationType)
from .rocm import RocmPlatform
from .tpu import TpuPlatform
from .xpu import XpuPlatform

logger = logging.getLogger(__name__)



class PlatformRegistry:
    """Registry for platform implementations.
    _platforms: Dict[PlatformType, Type[Platform]] = {}
    _current: Optional[Platform] = None
    _lock = threading.Lock()

    @classmethod
    def register(cls, platform_type: PlatformType, platform_cls: Type[Platform]) -> None:
        """Register a platform implementation.        cls._platforms[platform_type] = platform_cls

    @classmethod
    def get_platform(cls, platform_type: PlatformType) -> Optional[Platform]:
        """Get platform instance by type.        if platform_type not in cls._platforms:
            return None
        platform_cls = cls._platforms[platform_type]
        if platform_cls.is_available():
            return platform_cls()
        return None

    @classmethod
    def detect_current(cls) -> Platform:
        """Detect and return current platform.        with cls._lock:
            if cls._current is not None:
                return cls._current

            priority = [
                PlatformType.CUDA,
                PlatformType.ROCM,
                PlatformType.TPU,
                PlatformType.XPU,
                PlatformType.CPU,
            ]

            for ptype in priority:
                if ptype in cls._platforms:
                    platform_cls = cls._platforms[ptype]
                    if platform_cls.is_available():
                        cls._current = platform_cls()
                        logger.info(f"Detected platform: {ptype.value}")"                        return cls._current

            cls._current = CpuPlatform()
            return cls._current

    @classmethod
    def get_current(cls) -> Platform:
        """Get current platform (cached).        if cls._current is None:
            return cls.detect_current()
        return cls._current

    @classmethod
    def reset(cls) -> None:
        """Reset cached platform.        with cls._lock:
            cls._current = None


# Register default platforms
PlatformRegistry.register(PlatformType.CUDA, CudaPlatform)
PlatformRegistry.register(PlatformType.ROCM, RocmPlatform)
PlatformRegistry.register(PlatformType.TPU, TpuPlatform)
PlatformRegistry.register(PlatformType.XPU, XpuPlatform)
PlatformRegistry.register(PlatformType.CPU, CpuPlatform)


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
    return get_current_platform().supports_quantization(quant_type)


def select_attention_backend(
    preferred: Optional[AttentionBackend] = None,
) -> AttentionBackend:
    return get_current_platform().select_attention_backend(preferred)
