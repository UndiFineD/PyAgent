# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
CPU-only platform implementation.
"""

from __future__ import annotations

import platform
from typing import List, Set

from .models import (
    PlatformType,
    DeviceCapability,
    MemoryInfo,
    DeviceInfo,
    DeviceFeature,
    AttentionBackend,
    QuantizationType,
)
from .base import Platform


class CpuPlatform(Platform):
    """CPU-only platform implementation."""

    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.CPU

    @classmethod
    def is_available(cls) -> bool:
        return True

    def get_device_count(self) -> int:
        return 1

    def get_device_capability(self, _device_id: int = 0) -> DeviceCapability:
        return DeviceCapability(major=0, minor=0)

    def get_device_name(self, _device_id: int = 0) -> str:
        return platform.processor() or "CPU"

    def get_memory_info(self, _device_id: int = 0) -> MemoryInfo:
        try:
            import psutil
            vm = psutil.virtual_memory()
            return MemoryInfo(
                total_bytes=vm.total,
                free_bytes=vm.available,
                used_bytes=vm.used,
                reserved_bytes=0,
            )
        except ImportError:
            return MemoryInfo(total_bytes=0, free_bytes=0, used_bytes=0, reserved_bytes=0)

    def get_device_features(self, _device_id: int = 0) -> DeviceFeature:
        features = DeviceFeature.FP16
        try:
            import cpuinfo
            info = cpuinfo.get_cpu_info()
            flags = info.get("flags", [])
            if "avx512f" in flags:
                features |= DeviceFeature.BF16
        except ImportError:
            pass
        return features

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        return {
            QuantizationType.NONE,
            QuantizationType.INT8,
            QuantizationType.GGUF,
        }

    def get_attention_backends(self) -> List[AttentionBackend]:
        return [AttentionBackend.CPU, AttentionBackend.TORCH_SDPA, AttentionBackend.DEFAULT]

    def get_device_info(self, device_id: int = 0) -> DeviceInfo:
        return DeviceInfo(
            device_id=device_id,
            name=self.get_device_name(device_id),
            platform=self.get_platform_type(),
            capability=self.get_device_capability(device_id),
            memory=self.get_memory_info(device_id),
            features=self.get_device_features(device_id),
        )

    def select_attention_backend(self, _capability: DeviceCapability) -> AttentionBackend:
        return AttentionBackend.CPU
