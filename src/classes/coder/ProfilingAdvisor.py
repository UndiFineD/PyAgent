#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .ProfilingCategory import ProfilingCategory
from .ProfilingSuggestion import ProfilingSuggestion

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

class ProfilingAdvisor:
    """Provides code profiling suggestions.

    Analyzes code to identify functions that would benefit
    from profiling.

    Attributes:
        suggestions: List of profiling suggestions.

    Example:
        >>> advisor=ProfilingAdvisor()
        >>> # suggestions=advisor.analyze("def slow_func(): asyncio.sleep(10)")
    """

    def __init__(self) -> None:
        """Initialize the profiling advisor."""
        self.suggestions: List[ProfilingSuggestion] = []

    def analyze(self, content: str) -> List[ProfilingSuggestion]:
        """Analyze code for profiling opportunities.

        Args:
            content: Source code to analyze.

        Returns:
            List of profiling suggestions.
        """
        self.suggestions = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self.suggestions
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._analyze_function(node)
        return self.suggestions

    def _analyze_function(
        self,
        node: Any
    ) -> None:
        """Analyze a function for profiling needs.

        Args:
            node: AST node of the function.
        """
        has_loop = False
        has_io = False
        has_network = False
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                has_loop = True
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    name = child.func.attr
                    if name in ('read', 'write', 'open', 'close'):
                        has_io = True
                    if name in ('get', 'post', 'request', 'connect'):
                        has_network = True
        if has_loop:
            self.suggestions.append(ProfilingSuggestion(
                category=ProfilingCategory.CPU_BOUND,
                function_name=node.name,
                reason="Contains loops that may be CPU-intensive",
                estimated_impact="medium",
                profiling_approach="Use cProfile or line_profiler"
            ))
        if has_io:
            self.suggestions.append(ProfilingSuggestion(
                category=ProfilingCategory.IO_BOUND,
                function_name=node.name,
                reason="Contains I / O operations that may block",
                estimated_impact="high",
                profiling_approach="Use async profiling or io tracing"
            ))
        if has_network:
            self.suggestions.append(ProfilingSuggestion(
                category=ProfilingCategory.NETWORK_BOUND,
                function_name=node.name,
                reason="Contains network operations",
                estimated_impact="high",
                profiling_approach="Monitor network latency and throughput"
            ))
