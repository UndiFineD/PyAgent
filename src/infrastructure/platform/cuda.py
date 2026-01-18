# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
NVIDIA CUDA platform implementation.
"""

from __future__ import annotations

import logging
from typing import List, Set, Optional

from .models import (
    PlatformType,
    DeviceCapability,
    MemoryInfo,
    DeviceFeature,
    AttentionBackend,
    QuantizationType,
)
from .base import Platform

logger = logging.getLogger(__name__)


class CudaPlatform(Platform):
    """NVIDIA CUDA platform implementation."""

    _torch = None

    @classmethod
    def get_platform_type(cls) -> PlatformType:
        return PlatformType.CUDA

    @classmethod
    def is_available(cls) -> bool:
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def _get_torch(self):
        if self._torch is None:
            import torch
            self._torch = torch
        return self._torch

    def get_device_count(self) -> int:
        torch = self._get_torch()
        return torch.cuda.device_count()

    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        torch = self._get_torch()
        cap = torch.cuda.get_device_capability(device_id)
        return DeviceCapability(major=cap[0], minor=cap[1])

    def get_device_name(self, device_id: int = 0) -> str:
        torch = self._get_torch()
        return torch.cuda.get_device_name(device_id)

    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        torch = self._get_torch()
        props = torch.cuda.get_device_properties(device_id)
        total = props.total_memory
        reserved = torch.cuda.memory_reserved(device_id)
        allocated = torch.cuda.memory_allocated(device_id)
        free = total - reserved
        return MemoryInfo(
            total_bytes=total,
            free_bytes=free,
            used_bytes=allocated,
            reserved_bytes=reserved,
        )

    def get_device_features(self, device_id: int = 0) -> DeviceFeature:
        cap = self.get_device_capability(device_id)
        features = DeviceFeature.NONE

        if cap >= DeviceCapability(5, 3):
            features |= DeviceFeature.FP16
        if cap >= DeviceCapability(7, 0):
            features |= DeviceFeature.TENSOR_CORES
            features |= DeviceFeature.INT8
        if cap >= DeviceCapability(8, 0):
            features |= DeviceFeature.BF16
            features |= DeviceFeature.FLASH_ATTENTION
            features |= DeviceFeature.CUDA_GRAPHS
            features |= DeviceFeature.ASYNC_COPY
        if cap >= DeviceCapability(8, 9):
            features |= DeviceFeature.FP8
            features |= DeviceFeature.INT4
            features |= DeviceFeature.SPARSE_OPS
        if self.get_device_count() > 1:
            features |= DeviceFeature.MULTI_GPU

        return features

    def get_driver_version(self) -> str:
        torch = self._get_torch()
        try:
            return torch.version.cuda or "unknown"
        except Exception:
            return "unknown"

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        cap = self.get_device_capability()
        quants = {QuantizationType.NONE, QuantizationType.INT8}

        if cap >= DeviceCapability(7, 5):
            quants |= {QuantizationType.GPTQ, QuantizationType.AWQ, QuantizationType.INT4}
        if cap >= DeviceCapability(8, 0):
            quants |= {
                QuantizationType.MARLIN,
                QuantizationType.EXLLAMA,
                QuantizationType.EXLLAMA_V2,
                QuantizationType.NF4,
                QuantizationType.BITSANDBYTES,
            }
        if cap >= DeviceCapability(8, 9):
            quants |= {
                QuantizationType.FP8,
                QuantizationType.FP8_E4M3,
                QuantizationType.FP8_E5M2,
            }

        return quants

    def get_attention_backends(self) -> List[AttentionBackend]:
        cap = self.get_device_capability()
        backends = []

        if cap >= DeviceCapability(8, 0):
            backends.append(AttentionBackend.FLASH_ATTN_V2)
            try:
                import flash_attn
                if hasattr(flash_attn, "__version__") and flash_attn.__version__.startswith("3."):
                    backends.insert(0, AttentionBackend.FLASH_ATTN_V3)
            except ImportError:
                pass

        if cap >= DeviceCapability(9, 0):
            backends.insert(0, AttentionBackend.FLASHINFER)

        backends.extend([
            AttentionBackend.XFORMERS,
            AttentionBackend.TORCH_SDPA,
            AttentionBackend.PAGED_ATTENTION,
            AttentionBackend.DEFAULT,
        ])
        return backends

    def empty_cache(self) -> None:
        torch = self._get_torch()
        torch.cuda.empty_cache()

    def synchronize(self, device_id: int = 0) -> None:
        torch = self._get_torch()
        with torch.cuda.device(device_id):
            torch.cuda.synchronize()

    def set_device(self, device_id: int) -> None:
        torch = self._get_torch()
        torch.cuda.set_device(device_id)

    def get_current_device(self) -> int:
        torch = self._get_torch()
        return torch.cuda.current_device()
