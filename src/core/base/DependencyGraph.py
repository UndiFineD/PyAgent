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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent.py"""




from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

class DependencyGraph:
    """Resolve agent dependencies for ordered execution.

    Example:
        graph=DependencyGraph()
        graph.add_dependency("tests", "coder")  # tests depends on coder
        graph.add_dependency("docs", "tests")

        order=graph.resolve()  # ["coder", "tests", "docs"]
    """

    def __init__(self) -> None:
        """Initialize dependency graph."""
        self._nodes: Set[str] = set()
        self._edges: Dict[str, Set[str]] = {}  # node -> dependencies

    def add_node(self, name: str) -> None:
        """Add a node.

        Args:
            name: Node name.
        """
        self._nodes.add(name)
        if name not in self._edges:
            self._edges[name] = set()

    def add_dependency(self, node: str, depends_on: str) -> None:
        """Add a dependency.

        Args:
            node: Node that has the dependency.
            depends_on: Node that must run first.
        """
        self.add_node(node)
        self.add_node(depends_on)
        self._edges[node].add(depends_on)

    def resolve(self) -> List[str]:
        """Resolve execution order.

        Returns:
            List of nodes in execution order.

        Raises:
            ValueError: If circular dependency detected.
        """
        in_degree = {n: 0 for n in self._nodes}

        for node, deps in self._edges.items():
            for dep in deps:
                # This is reverse - we need nodes with deps to have higher in_degree
                pass  # Actually, we track outgoing

        # Build reverse graph for topological sort
        reverse: dict[str, set[str]] = {n: set() for n in self._nodes}
        for node, deps in self._edges.items():
            for dep in deps:
                reverse[dep].add(node)

        # Calculate in - degree based on dependencies
        in_degree = {n: len(self._edges.get(n, set())) for n in self._nodes}

        # Start with nodes that have no dependencies
        queue: list[str] = [n for n in self._nodes if in_degree[n] == 0]
        result: list[str] = []

        while queue:
            node = queue.pop(0)
            result.append(node)

            for dependent in reverse[node]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(self._nodes):
            raise ValueError("Circular dependency detected")

        return result
