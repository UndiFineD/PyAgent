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


"""Core logic for Hardware Acceleration and NPU interaction.
"""
from __future__ import annotations

import logging
from typing import Optional

from .base_core import BaseCore

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.hardware")



class HardwareCore(BaseCore):
    """Standard interface for hardware-specific optimizations (NPU, GPU).
    """
    def __init__(self, name: str = "HardwareCore", repo_root: Optional[str] = None) -> None:
        super().__init__(name=name, repo_root=repo_root)
        self._npu_status = False

    def initialize_npu(self) -> bool:
        """Attempts to initialize NPU acceleration via Rust core."""
        if rc and hasattr(rc, "initialize_npu"):  # pylint: disable=no-member
            # pylint: disable=no-member
            result = rc.initialize_npu()
            self._npu_status = result == 0
            return self._npu_status
        return False

    def run_npu_model(self, model_path: str) -> bool:
        if rc and hasattr(rc, "run_npu_model") and self._npu_status:  # pylint: disable=no-member
            # pylint: disable=no-member
            result = rc.run_npu_model(model_path)
            return result == 0
        return False
