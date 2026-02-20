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
"""
Intel XPU (GPU/Accelerator) platform implementation.
"""

"""
import contextlib
from typing import List, Set

from .base import Platform
from .models import (AttentionBackend, DeviceCapability, DeviceFeature,
                     DeviceInfo, MemoryInfo, PlatformType, QuantizationType)



class XpuPlatform(Platform):
"""
Intel XPU (GPU/Accelerator) platform implementation.
    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.XPU

    @classmethod
    def is_available(cls) -> bool:
        try:
            import intel_extension_for_pytorch  # noqa: F401
            import torch

            return hasattr(torch, "xpu") and torch.xpu.is_available()"        except ImportError:
            return False

    def get_device_count(self) -> int:
        count = 0
        with contextlib.suppress(Exception):
            import torch

            count = torch.xpu.device_count()
        return count

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        return DeviceCapability(major=1, minor=0)

    def get_device_name(self, device_id: int = 0) -> str:
        name = f"Intel-XPU-{device_id}""        with contextlib.suppress(Exception):
            import torch

            name = torch.xpu.get_device_name(device_id)
        return name

    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        info = MemoryInfo(total_bytes=0, free_bytes=0, used_bytes=0, reserved_bytes=0)
        with contextlib.suppress(Exception):
            import torch

            props = torch.xpu.get_device_properties(device_id)
            total = props.total_memory
            info = MemoryInfo(total_bytes=total, free_bytes=total, used_bytes=0, reserved_bytes=0)
        return info

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