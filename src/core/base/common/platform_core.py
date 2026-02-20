#!/usr/bin/env python3
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


"""Unified platform and hardware detection core."""
import logging
import os
import platform
import sys
from typing import Any, Optional

logger = logging.getLogger("pyagent.platform")


class PlatformCore:
    """Standardized detector for environment, OS, and hardware capabilities."""
    _instance: Optional["PlatformCore"] = None

    def __new__(cls) -> "PlatformCore":
        if cls._instance is None:
            cls._instance = super(PlatformCore, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def __init__(self) -> None:
        # Attributes are initialized in _initialize for singleton consistency
        self.system: str = ""
        self.release: str = ""
        self.machine: str = ""
        self.python_version: str = ""
        self._is_windows: bool = False
        self._is_linux: bool = False
        self._is_darwin: bool = False

    def _initialize(self) -> None:
        """Initializes platform attributes."""
        self.system = platform.system()
        self.release = platform.release()
        self.machine = platform.machine()
        self.python_version = sys.version.split()[0]
        self._is_windows = self.system == "Windows"
        self._is_linux = self.system == "Linux"
        self._is_darwin = self.system == "Darwin"

    @property
    def is_windows(self) -> bool:
        """Returns True if the current OS is Windows."""
        return self._is_windows

    @property
    def is_linux(self) -> bool:
        """Returns True if the current OS is Linux."""
        return self._is_linux

    @property
    def is_macos(self) -> bool:
        """Returns True if the current OS is macOS."""
        return self._is_darwin

    def get_info(self) -> dict[str, Any]:
        """Get comprehensive platform information."""
        return {
            "os": self.system,
            "release": self.release,
            "machine": self.machine,
            "python": self.python_version,
            "win32": self._is_windows,
            "linux": self._is_linux,
            "macos": self._is_darwin,
            "pid": os.getpid(),
        }

    def get_resource_usage(self) -> dict[str, Any]:
        """Basic resource usage without full psutil dependency requirement."""
        try:
            import psutil  # pylint: disable=import-outside-toplevel

            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()._asdict()
            return {"cpu_percent": cpu, "memory": mem}
        except ImportError:
            return {"error": "psutil not installed"}

    def is_gpu_available(self) -> bool:
        """Heuristic for GPU availability."""
        # Check for CUDA explicitly disabled
        if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1":
            return False

        try:
            import torch  # pylint: disable=import-outside-toplevel

            return torch.cuda.is_available()
        except ImportError:
            try:
                import tensorflow as tf  # pylint: disable=import-outside-toplevel

                return len(tf.config.list_physical_devices("GPU")) > 0
            except ImportError:
                return False
