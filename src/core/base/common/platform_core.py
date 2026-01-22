<<<<<<< HEAD
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Unified platform and hardware detection core."""

import logging
import os
import platform
import sys
from typing import Any, Dict, Optional

logger = logging.getLogger("pyagent.platform")


=======
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified platform and hardware detection core."""

import platform
import sys
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("pyagent.platform")

>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class PlatformCore:
    """
    Standardized detector for environment, OS, and hardware capabilities.
    """
<<<<<<< HEAD

    _instance: Optional["PlatformCore"] = None

    def __new__(cls) -> "PlatformCore":
=======
    _instance: Optional['PlatformCore'] = None

    def __new__(cls):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        if cls._instance is None:
            cls._instance = super(PlatformCore, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

<<<<<<< HEAD
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
=======
    def _initialize(self):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.system = platform.system()
        self.release = platform.release()
        self.machine = platform.machine()
        self.python_version = sys.version.split()[0]
<<<<<<< HEAD
        self._is_windows = self.system == "Windows"
        self._is_linux = self.system == "Linux"
        self._is_darwin = self.system == "Darwin"

    @property
    def is_windows(self) -> bool:
        """Returns True if the current OS is Windows."""
=======
        self._is_windows = (self.system == "Windows")
        self._is_linux = (self.system == "Linux")
        self._is_darwin = (self.system == "Darwin")

    @property
    def is_windows(self) -> bool:
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return self._is_windows

    @property
    def is_linux(self) -> bool:
<<<<<<< HEAD
        """Returns True if the current OS is Linux."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return self._is_linux

    @property
    def is_macos(self) -> bool:
<<<<<<< HEAD
        """Returns True if the current OS is macOS."""
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
<<<<<<< HEAD
            import psutil  # pylint: disable=import-outside-toplevel

=======
            import psutil
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
<<<<<<< HEAD

        try:
            import torch  # pylint: disable=import-outside-toplevel

            return torch.cuda.is_available()
        except ImportError:
            try:
                import tensorflow as tf  # pylint: disable=import-outside-toplevel

                return len(tf.config.list_physical_devices("GPU")) > 0
=======
            
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            try:
                import tensorflow as tf
                return len(tf.config.list_physical_devices('GPU')) > 0
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            except ImportError:
                return False
