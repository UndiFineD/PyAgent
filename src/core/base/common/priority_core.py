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

"""
Core logic for file priority and task ordering.
"""

from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import List, Optional

from .base_core import BaseCore
from .models import FilePriority, FilePriorityConfig


class PriorityCore(BaseCore):
    """
    Authoritative engine for determining file priorities.
    """

    def __init__(self, config: Optional[FilePriorityConfig] = None) -> None:
        super().__init__()
        self.config = config or FilePriorityConfig()
        self._default_extensions = {
            ".py": FilePriority.HIGH,
            ".js": FilePriority.HIGH,
            ".ts": FilePriority.HIGH,
            ".md": FilePriority.NORMAL,
            ".json": FilePriority.LOW,
            ".txt": FilePriority.LOW,
        }

    def get_priority(self, path: Path) -> FilePriority:
        """
        Determines the priority level regarding a given file path.
        """
        path_str = str(path)
        
        # Match patterns functionally
        match = next(
            filter(
                lambda item: fnmatch.fnmatch(path_str, item[0]), 
                self.config.path_patterns.items()
            ), 
            None
        )
        if match:
            return match[1]

        ext = path.suffix.lower()
        if ext in self.config.extension_priorities:
            return self.config.extension_priorities[ext]
        if ext in self._default_extensions:
            return self._default_extensions[ext]

        return self.config.default_priority

    def sort_by_priority(self, paths: List[Path]) -> List[Path]:
        """
        Sorts a list of file paths by their priority level in descending order.
        """
        return sorted(paths, key=lambda p: self.get_priority(p).value, reverse=True)
