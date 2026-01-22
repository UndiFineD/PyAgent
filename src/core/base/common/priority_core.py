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

<<<<<<< HEAD
<<<<<<< HEAD
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
"""
Core logic for file priority and task ordering.
"""

from __future__ import annotations
<<<<<<< HEAD
<<<<<<< HEAD

import fnmatch
from pathlib import Path
from typing import List, Optional

from .base_core import BaseCore
from .models import FilePriority, FilePriorityConfig


=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
import fnmatch
from pathlib import Path
from typing import List, Optional
from .base_core import BaseCore
from .models import FilePriority, FilePriorityConfig

<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
<<<<<<< HEAD
<<<<<<< HEAD
        """
        Determines the priority level for a given file path.
        """
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        path_str = str(path)
        for pattern, priority in self.config.path_patterns.items():
            if fnmatch.fnmatch(path_str, pattern):
                return priority
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        ext = path.suffix.lower()
        if ext in self.config.extension_priorities:
            return self.config.extension_priorities[ext]
        if ext in self._default_extensions:
            return self._default_extensions[ext]

        return self.config.default_priority

    def sort_by_priority(self, paths: List[Path]) -> List[Path]:
<<<<<<< HEAD
<<<<<<< HEAD
        """
        Sorts a list of file paths by their priority level in descending order.
        """
=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return sorted(paths, key=lambda p: self.get_priority(p).value, reverse=True)
