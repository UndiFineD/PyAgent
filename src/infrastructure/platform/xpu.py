# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Intel XPU (GPU/Accelerator) platform implementation.
"""

from __future__ import annotations

from typing import List, Set

from .models import (
    PlatformType,
    DeviceCapability,
    MemoryInfo,
    DeviceFeature,
    AttentionBackend,
    QuantizationType,
    DeviceInfo,
)
from .base import Platform


class XpuPlatform(Platform):
    """Intel XPU (GPU/Accelerator) platform implementation."""

    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.XPU

    @classmethod
    def is_available(cls) -> bool:
        try:
            import torch
            import intel_extension_for_pytorch
            return hasattr(torch, "xpu") and torch.xpu.is_available()
        except ImportError:
            return False

    def get_device_count(self) -> int:
        try:
            import torch
            return torch.xpu.device_count()
        except Exception:
            return 0

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        return DeviceCapability(major=1, minor=0)

    def get_device_name(self, device_id: int = 0) -> str:
        try:
            import torch
            return torch.xpu.get_device_name(device_id)
        except Exception:
            return f"Intel-XPU-{device_id}"

    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        try:
            import torch
            props = torch.xpu.get_device_properties(device_id)
            total = props.total_memory
            return MemoryInfo(total_bytes=total, free_bytes=total, used_bytes=0, reserved_bytes=0)
        except Exception:
            return MemoryInfo(total_bytes=0, free_bytes=0, used_bytes=0, reserved_bytes=0)

    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        return DeviceFeature.FP16 | DeviceFeature.BF16

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        return {QuantizationType.NONE}

    def get_attention_backends(self) -> List[AttentionBackend]:
        return [AttentionBackend.TRITON, AttentionBackend.DEFAULT]

    def get_device_info(self, device_id: int = 0) -> DeviceInfo:
        return DeviceInfo(
            device_id=device_id,
            name=self.get_device_name(device_id),
            platform=self.get_platform_type(),
            capability=self.get_device_capability(device_id),
            memory=self.get_memory_info(device_id),
            features=self.get_device_features(device_id),
        )

    def select_attention_backend(self, capability: DeviceCapability) -> AttentionBackend:
        return AttentionBackend.TRITON

    def is_quantization_supported(self, quant_type: str) -> bool:
        return quant_type == "none"
