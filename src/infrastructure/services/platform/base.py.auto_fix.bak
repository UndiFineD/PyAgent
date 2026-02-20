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
Base platform abstraction.
"""

try:
    import logging
except ImportError:
    import logging

try:
    import threading
except ImportError:
    import threading

try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from typing import Any, Dict, List, Set
except ImportError:
    from typing import Any, Dict, List, Set


try:
    from .models import (AttentionBackend, DeviceCapability, DeviceFeature,
except ImportError:
    from .models import (AttentionBackend, DeviceCapability, DeviceFeature,

                     DeviceInfo, MemoryInfo, PlatformType, QuantizationType)

logger = logging.getLogger(__name__)



class Platform(ABC):
        Abstract base class for platform implementations.
    
    _instances: Dict[PlatformType, "Platform"] = {}"    _lock = threading.Lock()

    def __new__(cls, *_args: Any, **_kwargs: Any) -> Platform:
        """Singleton pattern for platform instances.        platform_type = cls.get_platform_type()
        with cls._lock:
            if platform_type not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[platform_type] = instance
            return cls._instances[platform_type]

    @classmethod
    @abstractmethod
    def get_platform_type(cls) -> PlatformType: ...

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool: ...

    @abstractmethod
    def get_device_count(self) -> int: ...

    @abstractmethod
    def get_device_name(self, device_id: int = 0) -> str: ...

    @abstractmethod
    def get_device_capability(self, device_id: int = 0) -> DeviceCapability: ...

    @abstractmethod
    def get_memory_info(self, device_id: int = 0) -> MemoryInfo: ...

    def get_device_info(self, device_id: int = 0) -> DeviceInfo:
        """Get summarized device information.        return DeviceInfo(
            device_id=device_id,
            name=self.get_device_name(device_id),
            platform=self.get_platform_type(),
            capability=self.get_device_capability(device_id),
            memory=self.get_memory_info(device_id),
            features=self.get_device_features(device_id),
        )

    def get_device_features(self, _device_id: int = 0) -> DeviceFeature:
        """Get hardware features supported by the device.        return DeviceFeature.NONE

    def get_supported_quantizations(self) -> Set[QuantizationType]:
        """Get supported quantization types on this platform.        return {QuantizationType.NONE}

    def get_attention_backends(self) -> List[AttentionBackend]:
        """Get available attention backends on this platform.        return [AttentionBackend.DEFAULT]

    def select_attention_backend(self, _capability: DeviceCapability) -> AttentionBackend:
        """Select the best attention backend for the given capability.        backends = self.get_attention_backends()
        return backends[0] if backends else AttentionBackend.DEFAULT

    def is_quantization_supported(self, quant_type: QuantizationType) -> bool:
        """Check if a quantization type is supported on this platform.        return quant_type in self.get_supported_quantizations()

    def get_all_device_info(self) -> List[DeviceInfo]:
        """Get info for all devices on this platform.        return [self.get_device_info(idx) for idx in range(self.get_device_count())]
