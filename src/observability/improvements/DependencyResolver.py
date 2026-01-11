#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_improvements.py"""

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time


































from src.core.base.version import VERSION
__version__ = VERSION

class DependencyResolver:
    """Resolves improvement dependencies."""

    def __init__(self) -> None:
        self.dependencies: Dict[str, List[str]] = {}

    def add_dependency(self, improvement_id: str, depends_on_id: str) -> None:
        self.dependencies.setdefault(improvement_id, []).append(depends_on_id)

    def get_dependencies(self, improvement_id: str) -> List[str]:
        return list(self.dependencies.get(improvement_id, []))

    def resolve_order(self, improvement_ids: List[str]) -> List[str]:
        """Topologically sort the given ids so dependencies come first."""
        visited: set[str] = set()
        temp: set[str] = set()
        ordered: List[str] = []

        def visit(node: str) -> None:
            if node in visited:
                return
            if node in temp:
                return
            temp.add(node)
            for dep in self.dependencies.get(node, []):
                if dep in improvement_ids:
                    visit(dep)
            temp.remove(node)
            visited.add(node)
            ordered.append(node)

        for node in improvement_ids:
            visit(node)
        return ordered
