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

"""
Versioning logic for ChangesAgent.
"""

from __future__ import annotations
import logging
import re
from datetime import datetime
from ..VersioningStrategy import VersioningStrategy

class ChangesVersioningMixin:
    """Mixin for managing versioning strategies."""

    def set_versioning_strategy(self, strategy: VersioningStrategy) -> None:
        """Set the versioning strategy."""
        self._versioning_strategy = strategy
        logging.info(f"Using versioning strategy: {strategy.value}")

    def generate_next_version(self, bump_type: str = "patch") -> str:
        """Generate the next version based on the current strategy.

        Args:
            bump_type: For SemVer: 'major', 'minor', 'patch'. For CalVer: ignored.
        """
        if self._versioning_strategy == VersioningStrategy.CALVER:
            return datetime.now().strftime("%Y.%m.%d")

        # SemVer: Try to extract current version and bump it
        current_version = self._extract_latest_version()
        if current_version:
            parts = current_version.split(".")
            if len(parts) >= 3:
                try:
                    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
                    if bump_type == "major":
                        return f"{major + 1}.0.0"
                    elif bump_type == "minor":
                        return f"{major}.{minor + 1}.0"
                    else:
                        # patch
                        return f"{major}.{minor}.{patch + 1}"
                except ValueError:
                    pass
        return "0.1.0"  # Default starting version

    def _extract_latest_version(self) -> str | None:
        """Extract the latest version from the changelog."""
        if not hasattr(self, "previous_content") or not self.previous_content:
            return None
        pattern = r"##\s*\[?(\d+\.\d+\.\d+)\]?"
        matches = re.findall(pattern, self.previous_content)
        if matches:
            return matches[0]
        return None
