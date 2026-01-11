#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from src.core.base.types.DependencyNode import DependencyNode
from src.core.base.types.DependencyType import DependencyType
from src.logic.agents.development.DependencyCore import DependencyCore

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import logging

class DependencyAgent:
    """Analyzes code dependencies.

    Builds a dependency graph and provides analysis capabilities.

    Attributes:
        nodes: Dictionary of dependency nodes.
    """

    def __init__(self) -> None:
        """Initialize the dependency analyzer."""
        self.nodes: Dict[str, DependencyNode] = {}
        self.core = DependencyCore()

    def analyze(self, content: str, file_path: str = "") -> Dict[str, DependencyNode]:
        """Analyze code dependencies."""
        self.nodes = self.core.parse_dependencies(content, file_path)
        return self.nodes

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
