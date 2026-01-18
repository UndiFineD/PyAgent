# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Base platform abstraction.
"""

from __future__ import annotations

import logging
import threading
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any

from .models import (
    PlatformType,
    DeviceCapability,
    MemoryInfo,
    DeviceInfo,
    DeviceFeature,
    AttentionBackend,
)

logger = logging.getLogger(__name__)


class Platform(ABC):
    """
    Abstract base class for platform implementations.
    """

    _instances: Dict[PlatformType, "Platform"] = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Singleton pattern for platform instances."""
        platform_type = cls.get_platform_type()
        with cls._lock:
            if platform_type not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[platform_type] = instance
            return cls._instances[platform_type]

    @classmethod
    @abstractmethod
    def get_platform_type(cls) -> PlatformType:
        ...

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        ...

    @abstractmethod
    def get_device_count(self) -> int:
        ...

    @abstractmethod
    def get_device_name(self, device_id: int = 0) -> str:
        ...

    @abstractmethod
    def get_device_capability(self, device_id: int = 0) -> DeviceCapability:
        ...

    @abstractmethod
    def get_memory_info(self, device_id: int = 0) -> MemoryInfo:
        ...

    @abstractmethod
    def get_device_info(self, device_id: int = 0) -> DeviceInfo:
        ...

    @abstractmethod
    def select_attention_backend(
        self, capability: DeviceCapability
    ) -> AttentionBackend:
        ...

    @abstractmethod
    def is_quantization_supported(self, quant_type: str) -> bool:
        ...

    def get_all_device_info(self) -> List[DeviceInfo]:
        """Get info for all devices on this platform."""
        return [self.get_device_info(i) for i in range(self.get_device_count())]
