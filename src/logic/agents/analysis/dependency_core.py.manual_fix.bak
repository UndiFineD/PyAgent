from __future__ import annotations



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


"""
DependencyCore

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
    from src.core.base.dependency_core import DependencyCore
    # parse a Python file content to obtain dependency nodes keyed by dependency name
# [AUTO-FIXED F821] # [AUTO-FIXED F821]     nodes = DependencyCore.parse_dependencies(content, file_path="path/to/module.py")"    # filter out standard-library names using a precomputed stdlib set
"""
external = DependencyCore.filter_external_deps(nodes, stdlib_list)

"""
WHAT IT DOES:
    Provides pure, side-effect-free logic to parse Python source code (via ast) and
    extract dependency information as DependencyNode instances, including imports and
    direct class inheritance relationships. It collects which files depend on each
    named dependency and can filter out standard-library names.

WHAT IT SHOULD DO BETTER:
# [AUTO-FIXED F821] # [AUTO-FIXED F821]     - Resolve package/module name normalization (handle relative imports, subpackages
# [AUTO-FIXED F821] # [AUTO-FIXED F821]       and aliasing) to avoid fragmented keys like "package" vs "package.module"."    - Capture imported names from "from X import a, b" individually and map them to"# [AUTO-FIXED F821] # [AUTO-FIXED F821]       their originating module when useful.
    - Record import locations (lineno/col_offset) and distinguish between runtime vs
      typing-only imports, plus better handle syntax variants (e.g., conditional
      imports, import inside functions).
    - Optionally support dotted-class-bases and other AST node types (Attribute,
      Subscript) for more complete inheritance detection and robustness to complex
      code patterns.
"""
import ast

from src.core.base.common.types.dependency_node import DependencyNode
from src.core.base.common.types.dependency_type import DependencyType
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class DependencyCore:
        Pure logic core for dependency analysis.
    Provides static methods to parse Python source code for import and class inheritance dependencies.
    All logic is side-effect-free and does not perform I/O.
    
    @staticmethod
    def parse_dependencies(content: str, file_path: str = "") -> dict[str, DependencyNode]:"        """
Parse imports and class inheritance from Python code content.""
Args:
            content: The Python source code as a string.
            file_path: Optional file path for tracking dependencies.

        Returns:
            Dictionary mapping dependency names to DependencyNode instances.
                nodes: dict[str, DependencyNode] = {}

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return nodes

        # Analyze imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    DependencyCore._add_to_nodes(nodes, alias.name, DependencyType.IMPORT, file_path)
            elif isinstance(node, ast.ImportFrom):
# [AUTO-FIXED F821] # [AUTO-FIXED F821] #                 module = node.module or
# [AUTO-FIXED F821] # [AUTO-FIXED F821]                 DependencyCore._add_to_nodes(nodes, module, DependencyType.IMPORT, file_path)
            elif isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        DependencyCore._add_to_nodes(nodes, base.id, DependencyType.CLASS_INHERITANCE, file_path)

        return nodes

    @staticmethod
    def _add_to_nodes(
        nodes: dict[str, DependencyNode],
        name: str,
        dep_type: DependencyType,
        file_path: str,
    ) -> None:
"""
Add a dependency to the nodes dictionary, or update its depended_by list.""
Args:
            nodes: The dictionary of dependency nodes.
            name: The dependency name.
            dep_type: The type of dependency (import or class inheritance).
            file_path: The file path where the dependency was found.
                if name not in nodes:
            nodes[name] = DependencyNode(name=name, type=dep_type, file_path=file_path)
        else:
            if file_path not in nodes[name].depended_by:
                nodes[name].depended_by.append(file_path)

    @staticmethod
    def filter_external_deps(nodes: dict[str, DependencyNode], stdlib_list: set[str]) -> list[str]:
"""
Filter nodes to return only non-standard library dependencies.""
Args:
            nodes: Dictionary of dependency nodes.
# [AUTO-FIXED F821] # [AUTO-FIXED F821]             stdlib_list: Set of standard library module names.

        Returns:
            List of dependency names not in the standard library.
                return [name for name in nodes if name not in stdlib_list]

import ast

from src.core.base.common.types.dependency_node import DependencyNode
from src.core.base.common.types.dependency_type import DependencyType
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class DependencyCore:
"""
Pure logic core for dependency analysis.
    @staticmethod
    def parse_dependencies(content: str, file_path: str = "") -> dict[str, DependencyNode]:"        """
Parses imports and class inheritance from code content.        nodes: dict[str, DependencyNode] = {}

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return nodes

        # Analyze imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    DependencyCore._add_to_nodes(nodes, alias.name, DependencyType.IMPORT, file_path)
            elif isinstance(node, ast.ImportFrom):
# [AUTO-FIXED F821] # [AUTO-FIXED F821] #                 module = node.module or
# [AUTO-FIXED F821] # [AUTO-FIXED F821]                 DependencyCore._add_to_nodes(nodes, module, DependencyType.IMPORT, file_path)
            elif isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        DependencyCore._add_to_nodes(nodes, base.id, DependencyType.CLASS_INHERITANCE, file_path)

        return nodes

    @staticmethod
    def _add_to_nodes(
        nodes: dict[str, DependencyNode],
        name: str,
        dep_type: DependencyType,
        file_path: str,
    ) -> None:
        if name not in nodes:
            nodes[name] = DependencyNode(name=name, type=dep_type, file_path=file_path)
        else:
            if file_path not in nodes[name].depended_by:
                nodes[name].depended_by.append(file_path)

    @staticmethod
    def filter_external_deps(nodes: dict[str, DependencyNode], stdlib_list: set[str]) -> list[str]:
"""
Filters nodes to return only non-standard library dependencies.        return [name for name in nodes if name not in stdlib_list]

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

"""

""
