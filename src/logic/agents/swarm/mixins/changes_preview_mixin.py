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
Preview management logic for ChangesAgent.
"""

from __future__ import annotations
import logging
from typing import Any, Dict

class ChangesPreviewMixin:
    """Mixin for managing preview mode and changes."""

    def enable_preview_mode(self) -> None:
        """Enable preview mode - changes won't be written to file."""
        self._preview_mode = True
        logging.info("Preview mode enabled")

    def disable_preview_mode(self) -> None:
        """Disable preview mode."""
        self._preview_mode = False
        logging.info("Preview mode disabled")

    def get_preview(self) -> str:
        """Get the preview of changes without applying them."""
        return self._preview_content if getattr(self, "_preview_content", "") else getattr(self, "current_content", "")

    def preview_changes(self, content: str) -> Dict[str, Any]:
        """Preview changes and return a summary."""
        self._preview_content = content

        # Calculate diff statistics
        original_lines = getattr(self, "previous_content", "").split("\n")
        new_lines = content.split("\n")

        added = len([line for line in new_lines if line and line not in original_lines])
        removed = len(
            [line for line in original_lines if line and line not in new_lines]
        )

        return {
            "original_lines": len(original_lines),
            "new_lines": len(new_lines),
            "lines_added": added,
            "lines_removed": removed,
            "preview": content[:500] + "..." if len(content) > 500 else content,
        }
