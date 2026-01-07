#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .DependencyNode import DependencyNode
from .DependencyType import DependencyType

from base_agent import BaseAgent
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile

class DependencyAnalyzer:
    """Analyzes code dependencies.

    Builds a dependency graph and provides analysis capabilities.

    Attributes:
        nodes: Dictionary of dependency nodes.

    Example:
        >>> analyzer=DependencyAnalyzer()
        >>> graph=analyzer.analyze("from os import path")
    """

    def __init__(self) -> None:
        """Initialize the dependency analyzer."""
        self.nodes: Dict[str, DependencyNode] = {}

    def analyze(self, content: str, file_path: str = "") -> Dict[str, DependencyNode]:
        """Analyze code dependencies.

        Args:
            content: Source code to analyze.
            file_path: Path to the source file.

        Returns:
            Dictionary of dependency nodes.
        """
        self.nodes = {}

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self.nodes
        # Analyze imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._add_dependency(alias.name, DependencyType.IMPORT, file_path)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                self._add_dependency(module, DependencyType.IMPORT, file_path)
        # Analyze class inheritance
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        self._add_dependency(
                            base.id,
                            DependencyType.CLASS_INHERITANCE,
                            file_path
                        )
        return self.nodes

    def _add_dependency(self, name: str, dep_type: DependencyType, file_path: str) -> None:
        """Add a dependency to the graph.

        Args:
            name: Name of the dependency.
            dep_type: Type of dependency.
            file_path: Path where the dependency is used.
        """
        if name not in self.nodes:
            self.nodes[name] = DependencyNode(
                name=name,
                type=dep_type,
                file_path=file_path
            )
        else:
            self.nodes[name].depended_by.append(file_path)

    def get_external_dependencies(self) -> List[str]:
        """Get list of external (non-local) dependencies.

        Returns:
            List of external dependency names.
        """
        stdlib_modules = {
            'os', 'sys', 're', 'json', 'ast', 'hashlib', 'logging',
            'pathlib', 'typing', 'dataclasses', 'enum', 'subprocess',
            'tempfile', 'shutil', 'math', 'collections', 'functools'
        }
        external: List[str] = []
        for name, node in self.nodes.items():
            if node.type == DependencyType.IMPORT:
                base_module = name.split('.')[0]
                if base_module not in stdlib_modules:
                    external.append(name)
        return external
