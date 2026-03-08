#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/ProfilingAdvisor.description.md

# ProfilingAdvisor

**File**: `src\classes\coder\ProfilingAdvisor.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 101  
**Complexity**: 3 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `ProfilingAgent`

Provides code profiling suggestions.
Integrated with ProfilingCore for cProfile analysis and bottleneck detection.

**Methods** (3):
- `__init__(self)`
- `analyze_pstats(self, pstats_filepath)`
- `_analyze_function(self, node)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `ast`
- `logging`
- `pstats`
- `src.core.base.types.ProfilingCategory.ProfilingCategory`
- `src.core.base.types.ProfilingSuggestion.ProfilingSuggestion`
- `src.core.base.version.VERSION`
- `src.observability.stats.core.ProfilingCore.ProfileStats`
- `src.observability.stats.core.ProfilingCore.ProfilingCore`
- `typing.Any`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/ProfilingAdvisor.improvements.md

# Improvements for ProfilingAdvisor

**File**: `src\classes\coder\ProfilingAdvisor.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 101 lines (medium)  
**Complexity**: 3 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ProfilingAdvisor_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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

from src.core.base.version import VERSION
from src.core.base.types.ProfilingCategory import ProfilingCategory
from src.core.base.types.ProfilingSuggestion import ProfilingSuggestion
from typing import Any, List
import ast
import logging
import pstats
from src.observability.stats.core.ProfilingCore import ProfilingCore, ProfileStats

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
