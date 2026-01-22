# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified platform and hardware detection core."""

import platform
import sys
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("pyagent.platform")

class PlatformCore:
    """
    Standardized detector for environment, OS, and hardware capabilities.
    """
    _instance: Optional['PlatformCore'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlatformCore, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.system = platform.system()
        self.release = platform.release()
        self.machine = platform.machine()
        self.python_version = sys.version.split()[0]
        self._is_windows = (self.system == "Windows")
        self._is_linux = (self.system == "Linux")
        self._is_darwin = (self.system == "Darwin")

    @property
    def is_windows(self) -> bool:
        return self._is_windows

    @property
    def is_linux(self) -> bool:
        return self._is_linux

    @property
    def is_macos(self) -> bool:
        return self._is_darwin

    def get_info(self) -> Dict[str, Any]:
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

    def get_resource_usage(self) -> Dict[str, Any]:
        """Basic resource usage without full psutil dependency requirement."""
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()._asdict()
            return {"cpu_percent": cpu, "memory": mem}
        except ImportError:
            return {"error": "psutil not installed"}

    def is_gpu_available(self) -> bool:
        """Heuristic for GPU availability."""
        # Check for CUDA
        if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1":
            return False
            
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            try:
                import tensorflow as tf
                return len(tf.config.list_physical_devices('GPU')) > 0
            except ImportError:
                return False
