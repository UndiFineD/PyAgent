#!/usr/bin/env python3
# Refactored by copilot-placeholder
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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class EnvironmentDetector:
    """Detects and reports test environment information."""

    def detect(self) -> dict[str, Any]:
        """Detect environment information."""
        import os
        import platform

        is_ci = any(env in os.environ for env in ["CI", "CONTINUOUS_INTEGRATION", "BUILD_ID", "GITHUB_ACTIONS"])
        system = platform.system().lower()
        if system == "windows":
            os_name = "windows"
        elif system == "darwin":
            os_name = "darwin"
        elif system == "linux":
            os_name = "linux"
        else:
            os_name = "unknown"
        return {
            "is_ci": is_ci,
            "os": os_name,
            "python_version": platform.python_version(),
            "platform": system,
        }
