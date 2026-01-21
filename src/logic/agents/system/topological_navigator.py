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


"""Agent specializing in Topological Context Navigation.
Builds a semantic map of the codebase for graph-based dependency exploration.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import os
from pathlib import Path
from .mixins.map_builder_mixin import MapBuilderMixin
from .mixins.graph_analysis_mixin import GraphAnalysisMixin
from .mixins.federation_mixin import FederationMixin
from src.core.base.base_agent import BaseAgent

__version__ = VERSION


class TopologicalNavigator(BaseAgent, MapBuilderMixin, GraphAnalysisMixin, FederationMixin):
    """
    Tier 2 (Cognitive Logic) - Topological Navigator: Maps code relationships 
    and determines the impact of changes using graph-based dependency analysis.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.graph: dict[str, set[str]] = {}
        self.reverse_graph: dict[str, set[str]] = {}
        self.root_dir = Path(os.getcwd())
        self._system_prompt = (
            "You are the Topological Context Navigator. "
            "You map relationships between code entities (classes, functions, modules) "
            "to determine the impact of changes across the codebase."
        )

    # Logic delegated to mixins
