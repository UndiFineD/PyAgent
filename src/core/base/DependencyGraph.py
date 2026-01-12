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
        self._resources: Dict[str, Set[str]] = {} # node -> set of resource URIs

    def add_node(self, name: str, resources: Optional[List[str]] = None) -> None:
        """Add a node.

        Args:
            name: Node name.
            resources: Optional list of resource URIs this node requires.
        """
        self._nodes.add(name)
        if name not in self._edges:
            self._edges[name] = set()
        if resources:
            if name not in self._resources:
                self._resources[name] = set()
            self._resources[name].update(resources)

    def add_dependency(self, node: str, depends_on: str) -> None:
        """Add a dependency.

        Args:
            node: Node that has the dependency.
            depends_on: Node that must run first.
        """
        self.add_node(node)
        self.add_node(depends_on)
        self._edges[node].add(depends_on)

    def resolve(self) -> List[List[str]]:
        """Resolve execution order into parallel batches.

        Each inner list contains nodes that can be executed simultaneously.
        Example: [["coder"], ["tests", "linter"], ["docs"]]

        Returns:
            List of batches, where each batch is a list of node names.
        Raises:
            ValueError: If circular dependency detected.
        """
        # Node -> count of remaining dependencies it has
        in_degree = {n: len(self._edges.get(n, set())) for n in self._nodes}
        
        # Build reverse graph: node -> nodes that depend on it
        reverse: Dict[str, Set[str]] = {n: set() for n in self._nodes}
        for node, deps in self._edges.items():
            for dep in deps:
                reverse[dep].add(node)

        batches: List[List[str]] = []
        visited_count = 0

        while True:
            # Nodes with no dependencies are ready for next batch
            current_batch = [n for n in self._nodes if in_degree[n] == 0 and n not in [item for sublist in batches for item in sublist]]
            
            if not current_batch:
                break
                
            # Phase 242: Refine batch based on resource collisions
            refined_batches = self._refine_batch_by_resources(current_batch)
            for rb in refined_batches:
                batches.append(rb)
                visited_count += len(rb)
                
                # Reduce in-degree for all nodes that depend on this batch
                for node in rb:
                    for dependent in reverse[node]:
                        in_degree[dependent] -= 1

        if visited_count != len(self._nodes):
            raise ValueError("Circular dependency detected or inaccessible nodes in graph.")

        return batches

    def _refine_batch_by_resources(self, batch: List[str]) -> List[List[str]]:
        """Splits a batch into multiple sequential sub-batches to avoid resource collisions."""
        refined: List[List[str]] = []
        
        for node in batch:
            node_resources = self._resources.get(node, set())
            
            # Find the first batch where this node doesn't collide
            placed = False
            for sub_batch in refined:
                # Check for collision with any node in this sub_batch
                collision = False
                for other_node in sub_batch:
                    other_resources = self._resources.get(other_node, set())
                    if node_resources.intersection(other_resources):
                        collision = True
                        break
                
                if not collision:
                    sub_batch.append(node)
                    placed = True
                    break
            
            if not placed:
                refined.append([node])
                
        return refined
