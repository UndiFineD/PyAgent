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


"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

import ast
import logging
import pstats
from typing import Any

from src.core.base.common.types.profiling_category import ProfilingCategory
from src.core.base.common.types.profiling_suggestion import ProfilingSuggestion
from src.core.base.lifecycle.version import VERSION
from src.observability.stats.core.profiling_core import (ProfileStats,
                                                         ProfilingCore)

__version__ = VERSION


class ProfilingAgent:
    """Provides code profiling suggestions.
    Integrated with ProfilingCore for cProfile analysis and bottleneck detection.
    """

    def __init__(self) -> None:
        """Initialize the profiling advisor."""
        self.suggestions: list[ProfilingSuggestion] = []
        self.core = ProfilingCore()

    def analyze_pstats(self, pstats_filepath: str) -> list[ProfileStats]:
        """Analyzes a binary pstats file and returns optimization priorities."""
        stats = pstats.Stats(pstats_filepath)
        results = self.core.analyze_stats(stats)

        bottlenecks = self.core.identify_bottlenecks(results)
        if bottlenecks:
            logging.warning(f"ProfilingAgent: Detected {len(bottlenecks)} bottlenecks.")

        return results

    def _analyze_function(self, node: Any) -> None:
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
                    if name in ("read", "write", "open", "close"):
                        has_io = True
                    if name in ("get", "post", "request", "connect"):
                        has_network = True
        if has_loop:
            self.suggestions.append(
                ProfilingSuggestion(
                    category=ProfilingCategory.CPU_BOUND,
                    function_name=node.name,
                    reason="Contains loops that may be CPU-intensive",
                    estimated_impact="medium",
                    profiling_approach="Use cProfile or line_profiler",
                )
            )
        if has_io:
            self.suggestions.append(
                ProfilingSuggestion(
                    category=ProfilingCategory.IO_BOUND,
                    function_name=node.name,
                    reason="Contains I / O operations that may block",
                    estimated_impact="high",
                    profiling_approach="Use async profiling or io tracing",
                )
            )
        if has_network:
            self.suggestions.append(
                ProfilingSuggestion(
                    category=ProfilingCategory.NETWORK_BOUND,
                    function_name=node.name,
                    reason="Contains network operations",
                    estimated_impact="high",
                    profiling_approach="Monitor network latency and throughput",
                )
            )
