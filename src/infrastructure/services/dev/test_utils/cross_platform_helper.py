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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from pathlib import Path
import sys
import tempfile

__version__ = VERSION

class CrossPlatformHelper:
    """Helpers for cross-platform testing.

    Provides utilities to handle platform differences in tests.

    Example:
        helper=CrossPlatformHelper()
        path=helper.normalize_path("/some / path")
        if helper.is_windows():
            # Windows - specific test code
    """

    def __init__(self) -> None:
        """Initialize helper."""
        self._platform = sys.platform

    def is_windows(self) -> bool:
        """Check if running on Windows."""
        return self._platform.startswith("win")

    def is_linux(self) -> bool:
        """Check if running on Linux."""
        return self._platform.startswith("linux")

    def is_macos(self) -> bool:
        """Check if running on macOS."""
        return self._platform == "darwin"

    def normalize_path(self, path: str) -> Path:
        """Normalize path for current platform.

        Args:
            path: Path string.

        Returns:
            Normalized Path object.
        """
        return Path(path).resolve()

    def normalize_line_endings(self, content: str) -> str:
        """Normalize line endings to platform default.

        Args:
            content: Text content.

        Returns:
            Content with normalized line endings.
        """
        # First normalize to \n, then to platform default
        normalized = content.replace("\r\n", "\n").replace("\r", "\n")
        if self.is_windows():
            return normalized.replace("\n", "\r\n")
        return normalized

    def get_temp_dir(self) -> Path:
        """Get platform-appropriate temp directory."""
        return Path(tempfile.gettempdir())

    def skip_on_platform(self, *platforms: str) -> bool:
        """Check if test should be skipped on current platform.

        Args:
            platforms: Platform names to skip ("windows", "linux", "macos").

        Returns:
            True if should skip.
        """
        platform_map = {
            "windows": self.is_windows(),
            "linux": self.is_linux(),
            "macos": self.is_macos(),
        }
        return any(platform_map.get(p, False) for p in platforms)