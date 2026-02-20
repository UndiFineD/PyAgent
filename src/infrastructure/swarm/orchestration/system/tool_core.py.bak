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

"""Tool core utilities: metadata extraction and argument filtering.

This module provides a trimmed, reliable implementation used by the
test suite to inspect tool functions and filter invocation arguments.
"""

from __future__ import annotations

import inspect
import logging
import re
from collections.abc import Callable
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel

from src.core.base.lifecycle.version import VERSION

try:
    import rust_core as rc  # optional acceleration
except (ImportError, AttributeError):
    rc = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

__version__ = VERSION


class ToolMetadata(BaseModel):
    name: str
    description: str
    parameters: Dict[str, str]
    owner: str
    category: str = "general"
    priority: int = 0
    reliability_score: float = 1.0


class ToolCore:
    """Core helpers for tooling metadata and argument handling."""

    def extract_metadata(self, owner_name: str, func: Callable, category: str = "general", priority: int = 0) -> ToolMetadata:
        name: str = getattr(func, "__name__", "<anonymous>")
        doc: str = func.__doc__ or "No description provided."

        sig = inspect.signature(func)
        params: Dict[str, str] = {}
        for p_name, param in sig.parameters.items():
            if p_name == "self":
                continue
            params[p_name] = str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any"

        calc_priority = int(priority) + (len(doc) // 100)

        return ToolMetadata(
            name=name,
            description=doc.split("\n")[0].strip(),
            parameters=params,
            owner=owner_name,
            category=category,
            priority=calc_priority,
        )

    def filter_arguments(self, func: Callable, args_dict: Dict[str, Any]) -> Dict[str, Any]:
        sig = inspect.signature(func)
        has_kwargs: bool = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())

        if has_kwargs:
            return args_dict

        return {k: v for k, v in args_dict.items() if k in sig.parameters}

    def score_tool_relevance(self, metadata: ToolMetadata, query: str) -> float:
        """Heuristic relevance scoring; defers to rust_core when available."""
        if rc:
            try:
                return rc.score_tool_relevance(metadata.name, metadata.description, query)  # type: ignore[attr-defined]
            except Exception:
                logger.warning("Rust score_tool_relevance failed; falling back to Python heuristic")

        query_lower = query.lower()
        score = 0.0

        if metadata.name.lower() in query_lower:
            score += 10.0

        desc_words = re.findall(r"\w+", metadata.description.lower())
        query_words = re.findall(r"\w+", query_lower)
        common = set(desc_words) & set(query_words)
        score += len(common) * 2.0

        score += metadata.priority * 0.1
        score *= metadata.reliability_score

        return float(score)

    def update_reliability(self, metadata: ToolMetadata, success: bool, weight: float = 0.1) -> ToolMetadata:
        if success:
            metadata.reliability_score = min(
                1.0, metadata.reliability_score + (1.0 - metadata.reliability_score) * weight
            )
        else:
            metadata.reliability_score = max(0.1, metadata.reliability_score - (metadata.reliability_score * weight))

        return metadata

    def selection_tournament(self, candidates: List[Tuple[ToolMetadata, float]], tournament_size: int = 2) -> ToolMetadata:
        import random

        if not candidates:
            raise ValueError("No candidate tools for selection.")

        sample = random.sample(candidates, min(len(candidates), tournament_size))
        winner = max(sample, key=lambda x: x[1])
        return winner[0]

