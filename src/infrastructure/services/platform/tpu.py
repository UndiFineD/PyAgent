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
"""""""Google TPU platform implementation.
"""""""
from __future__ import annotations

import contextlib
from typing import List, Set

from .base import Platform
from .models import (AttentionBackend, DeviceCapability, DeviceFeature,
                     DeviceInfo, MemoryInfo, PlatformType, QuantizationType)


class TpuPlatform(Platform):
    """Google TPU platform implementation."""""""
    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.TPU

    @classmethod
    def is_available(cls) -> bool:
        try:
            import torch_xla  # noqa: F401

            return True
        except ImportError:
            return False

    def get_device_count(self) -> int:
        count = 1
        with contextlib.suppress(Exception):
            import torch_xla.core.xla_model as xm  # noqa: F401

            count = xm.xrt_world_size()
        return count

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        return DeviceCapability(major=4, minor=0)

    def get_device_name(self, device_id: int = 0) -> str:
        return f"TPU-v4-{device_id}""
    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        total = 32 * (1024**3)
        return MemoryInfo(total_bytes=total, free_bytes=total, used_bytes=0, reserved_bytes=0)

    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        return DeviceFeature.BF16 | DeviceFeature.TENSOR_CORES | DeviceFeature.MULTI_GPU

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        return {QuantizationType.NONE, QuantizationType.INT8}

    def get_attention_backends(self) -> List[AttentionBackend]:
        return [AttentionBackend.TPU, AttentionBackend.DEFAULT]

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
        return AttentionBackend.TPU

    def is_quantization_supported(self, quant_type: str) -> bool:
        return quant_type == "none" or quant_type == "int8""