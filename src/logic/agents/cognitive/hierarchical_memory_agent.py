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


"""Agent specializing in Multi-Resolution Hierarchical Memory.
Manages Short-term (Episodic), Mid-term (Working), Long-term (Semantic), and Archival storage tiers.
"""

from src.core.base.lifecycle.version import VERSION
from src.core.base.lifecycle.base_agent import BaseAgent
from .mixins.memory_storage_mixin import MemoryStorageMixin
from .mixins.memory_query_mixin import MemoryQueryMixin

__version__ = VERSION


# pylint: disable=too-many-ancestors
class HierarchicalMemoryAgent(BaseAgent, MemoryStorageMixin, MemoryQueryMixin):
    """Manages memory across multiple temporal and semantic resolutions.
    Phase 290: Integrated with 3-layer system (ShortTerm, Working, LongTerm).
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.memory_root = self._workspace_root / "data" / "logs" / "memory_hierarchical"
        # Phase 290: Standardized 3-layer tiers + Archival
        self.tiers = ["ShortTerm", "Working", "LongTerm", "Archival"]
        for tier in self.tiers:
            (self.memory_root / tier).mkdir(parents=True, exist_ok=True)

        self._system_prompt = (
            "You are the Hierarchical Memory Agent. "
            "Your role is to categorize and move information between different memory tiers. "
            "ShortTerm memory: Recent raw telemetry and episodic events. "
            "Working memory: Task-specific context and scratchpad data. "
            "LongTerm memory: Distilled semantic knowledge and reusable patterns. "
            "Archival memory: Highly compressed historical logs for auditing."
        )

    # Logic delegated to mixins


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(
        HierarchicalMemoryAgent,
        "Hierarchical Memory Agent",
        "Multi-resolution memory management",
    )
    main()
