#!/usr/bin/env python3

"""
DependencyCore logic for PyAgent.
Pure logic for AST-based dependency analysis.
No I/O or side effects.
"""

from __future__ import annotations

import ast
from typing import Dict, List, Set, Optional, Tuple
from src.core.base.types.DependencyType import DependencyType
from src.core.base.types.DependencyNode import DependencyNode

class DependencyCore:
    """Pure logic core for dependency analysis."""

    @staticmethod
    def parse_dependencies(content: str, file_path: str = "") -> Dict[str, DependencyNode]:
        """Parses imports and class inheritance from code content."""
        nodes: Dict[str, DependencyNode] = {}
        
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
                module = node.module or ""
                DependencyCore._add_to_nodes(nodes, module, DependencyType.IMPORT, file_path)
            elif isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        DependencyCore._add_to_nodes(nodes, base.id, DependencyType.CLASS_INHERITANCE, file_path)
        
        return nodes

    @staticmethod
    def _add_to_nodes(nodes: Dict[str, DependencyNode], name: str, dep_type: DependencyType, file_path: str) -> None:
        if name not in nodes:
            nodes[name] = DependencyNode(name=name, type=dep_type, file_path=file_path)
        else:
            if file_path not in nodes[name].depended_by:
                nodes[name].depended_by.append(file_path)

    @staticmethod
    def filter_external_deps(nodes: Dict[str, DependencyNode], stdlib_list: Set[str]) -> List[str]:
        """Filters nodes to return only non-standard library dependencies."""
        return [name for name in nodes if name not in stdlib_list]
