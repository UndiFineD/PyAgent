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
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.core.base.types.DependencyNode import DependencyNode
from src.core.base.types.DependencyType import DependencyType
from src.logic.agents.development.DependencyCore import DependencyCore

__version__ = VERSION


class DependencyAgent:
    """Analyzes code dependencies.

    Builds a dependency graph and provides analysis capabilities.

    Attributes:
        nodes: Dictionary of dependency nodes.
    """

    def __init__(self) -> None:
        """Initialize the dependency analyzer."""
        self.nodes: dict[str, DependencyNode] = {}
        self.core = DependencyCore()

    def analyze(self, content: str, file_path: str = "") -> dict[str, DependencyNode]:
        """Analyze code dependencies."""
        self.nodes = self.core.parse_dependencies(content, file_path)
        return self.nodes

    def get_external_dependencies(self) -> list[str]:
        """Get list of external (non-local) dependencies.

        Returns:
            List of external dependency names.
        """
        stdlib_modules = {
            "os",
            "sys",
            "re",
            "json",
            "ast",
            "hashlib",
            "logging",
            "pathlib",
            "typing",
            "dataclasses",
            "enum",
            "subprocess",
            "tempfile",
            "shutil",
            "math",
            "collections",
            "functools",
        }
        external: list[str] = []
        for name, node in self.nodes.items():
            if node.type == DependencyType.IMPORT:
                base_module = name.split(".")[0]
                if base_module not in stdlib_modules:
                    external.append(name)
        return external
