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
Assistant for managing the knowledge graph and impact radius.
"""

from typing import Set


class KnowledgeGraphAssistant:
    """Handles backlinks, dependency tracking, and graph visualization."""

    def __init__(self, workspace_root: str) -> None:
        self.workspace_root = workspace_root

    def get_impact_radius(self, query: str) -> Set[str]:
        """Calculates which modules might be impacted by a change."""
        _ = query
        return set()

    def find_backlinks(self, target_file: str, index: dict[str, list[str]]) -> list[str]:
        """Finds all files in the index that reference the target_file."""
        backlinks = []
        target_name = target_file.split(".")[0]  # Support WikiStyle [[Note]] matches [[Note.md]]
        for source_file, symbols in index.items():
            for symbol in symbols:
                if symbol in (target_file, target_name):
                    backlinks.append(source_file)
        return backlinks

    def generate_mermaid(self, index: dict[str, list[str]]) -> str:
        """Exports the current knowledge graph as a Mermaid string."""
        from pathlib import Path
        lines = ["graph TD"]
        # Track edge combinations to prevent duplicates
        edges = set()
        for source, targets in index.items():
            s_name = Path(source).stem
            for target in targets:
                t_name = Path(target).stem
                edge = f"  {s_name} --> {t_name}"
                if edge not in edges:
                    lines.append(edge)
                    edges.add(edge)
        return "\n".join(lines)

    def generate_mermaid_graph(self) -> str:
        """Compatibility wrapper."""
        return self.generate_mermaid({})
