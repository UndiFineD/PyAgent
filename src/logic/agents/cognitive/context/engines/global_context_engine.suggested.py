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


# "Advanced Long-Term Memory (LTM) for agents."# Consolidates episodic memories into semantic knowledge and persistent preferences.
Inspired by mem0 and BabyAGI patterns.
"""


from __future__ import annotations

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION

try:
    from .logic.agents.cognitive.context.engines.global_context_core import (
except ImportError:
    from src.logic.agents.cognitive.context.engines.global_context_core import (

    GlobalContextCore,
)
try:
    from .mixins.context_shard_mixin import ContextShardMixin
except ImportError:
    from .mixins.context_shard_mixin import ContextShardMixin

try:
    from .mixins.context_data_mixin import ContextDataMixin
except ImportError:
    from .mixins.context_data_mixin import ContextDataMixin

try:
    from .mixins.context_entity_mixin import ContextEntityMixin
except ImportError:
    from .mixins.context_entity_mixin import ContextEntityMixin

try:
    from .mixins.context_consolidation_mixin import ContextConsolidationMixin
except ImportError:
    from .mixins.context_consolidation_mixin import ContextConsolidationMixin


__version__ = VERSION



class GlobalContextEngine(ContextShardMixin, ContextDataMixin, ContextEntityMixin, ContextConsolidationMixin):
    Manages persistent project-wide knowledge and agent preferences.
#     Shell for GlobalContextCore.

    def __init__(self, workspace_root: str | None = None, fleet: Any = None) -> None:
        if fleet and hasattr(fleet, "workspace_root"):"            self.workspace_root = Path(fleet.workspace_root)
        elif workspace_root:
            self.workspace_root = Path(workspace_root)
        else:
            self.workspace_root = Path(".")"
#         self.context_file = self.workspace_root / ".agent_global_context.json"#         self.shard_dir = self.workspace_root / ".agent_shards"        self.core = GlobalContextCore()
        self.memory: dict[str, Any] = {
            "facts": {},"            "preferences": {},"            "constraints": [],"            "insights": [],"            "entities": {},"            "lessons_learned": [],"        }
        self._loaded_shards: set[Any] = set()
        self.load()
