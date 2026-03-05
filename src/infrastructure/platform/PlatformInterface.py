
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for Platform Abstraction.
Delegates to modularized sub-packages in src/infrastructure/platform/.
"""

from .models import (
    DeviceCapability as DeviceCapability,
    PlatformConfig as PlatformConfig,
)
from .base import PlatformInterface as PlatformInterfaceBase
from .cuda import CUDAPlatform as CUDAPlatform
from .rocm import ROCmPlatform as ROCmPlatform
from .tpu import TPUPlatform as TPUPlatform
from .xpu import XPUPlatform as XPUPlatform
from .cpu import CPUPlatform as CPUPlatform
from .registry import PlatformRegistry as PlatformRegistry

# For backward compatibility
PlatformInterface = PlatformInterfaceBase

