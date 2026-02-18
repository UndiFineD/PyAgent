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


"""Storage base.py module.
"""

from __future__ import annotations


try:
    from abc import ABC, abstractmethod
except ImportError:
    from abc import ABC, abstractmethod

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.common.memory_core import MemoryCore
except ImportError:
    from src.core.base.common.memory_core import MemoryCore

try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class KnowledgeStore(ABC):
    """Base interface for all knowledge storage types."""
    def __init__(self, agent_id: str, storage_path: Path) -> None:
        self.agent_id = agent_id
        self.storage_path = storage_path
        self._memory_core = MemoryCore()
        # Initialize paths via standard core
        self.storage_path.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def store(self, key: str, value: Any, metadata: dict[str, Any] | None = None) -> bool:
        """Store a piece of knowledge."""raise NotImplementedError()

    @abstractmethod
    def retrieve(self, query: Any, limit: int = 5) -> list[Any]:
        """Retrieve knowledge based on a query."""raise NotImplementedError()

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a piece of knowledge by key."""raise NotImplementedError()
