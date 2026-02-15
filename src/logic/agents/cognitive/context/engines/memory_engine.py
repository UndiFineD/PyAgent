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


"""Engine for persistent episodic memory of agent actions and outcomes."""

from __future__ import annotations
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.context.engines.memory_core import MemoryCore
from .memory_mixins.memory_storage_mixin import MemoryStorageMixin
from .memory_mixins.memory_episode_mixin import MemoryEpisodeMixin
from .memory_mixins.memory_search_mixin import MemorySearchMixin

__version__ = VERSION


class MemoryEngine(MemoryStorageMixin, MemoryEpisodeMixin, MemorySearchMixin):
    """Stores and retrieves historical agent contexts and lessons learned."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = Path(workspace_root)
        self.memory_file = self.workspace_root / ".agent_memory.json"
        self.db_path = self.workspace_root / "data/db/.agent_memory_db"
        self.episodes: list[dict[str, Any]] = []
        self._collection = None
        self.core = MemoryCore()
        self.load()
