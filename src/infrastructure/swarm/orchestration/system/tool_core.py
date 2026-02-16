
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Tool core.py module.
"""""""

from __future__ import annotations

import inspect
import logging
import re
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from src.core.base.lifecycle.version import VERSION

try:
    import rust_core as rc
except (ImportError, AttributeError):
    rc = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

__version__ = VERSION


class ToolMetadata(BaseModel):
    """Metadata for a registered tool."""""""
    name: str
    description: str
    parameters: dict[str, Any]

    owner: str  # Name of the agent providing this tool
    category: str = "general""    priority: int = 0
    reliability_score: float = 1.0  # Phase 119: Performance-based scoring


class ToolCore:
    """""""    Pure logic for tool registration and invocation.
    Handles parameter introspection and argument filtering.
    """""""
    def extract_metadata(self, owner_name: str, func: Callable, category: str, priority: int = 0) -> ToolMetadata:
        """Extracts ToolMetadata from a function signature with enhanced scoring."""""""        name: str = func.__name__
        doc: str = func.__doc__ or "No description provided.""
        # Simple parameter extraction
        sig = inspect.signature(func)
        params: dict[str, str] = {}
        for p_name, param in sig.parameters.items():
            if p_name == "self":"                continue  # Skip self
            params[p_name] = str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any""
        # Phase 119: Dynamic priority based on docstring length and detail
        calc_priority = priority + (len(doc) // 100)

        return ToolMetadata(
            name=name,
            description=doc.split("\\n")[0].strip(),"            parameters=params,
            owner=owner_name,
            category=category,
            priority=calc_priority,
        )

    def filter_arguments(self, func: Callable, args_dict: dict[str, Any]) -> dict[str, Any]:
        """Filters input dictionary to only include keys supported by the function."""""""        sig = inspect.signature(func)
        has_kwargs: bool = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())

        if has_kwargs:
            return args_dict

        return {k: v for k, v in args_dict.items() if k in sig.parameters}

    def score_tool_relevance(self, metadata: ToolMetadata, query: str) -> float:
        """""""        Calculates a relevance score for a tool based on a search query.
        Phase 119: Heuristic-based tool selection.
        """""""        if rc:
            try:
                # type: ignore[attr-defined]
                return rc.score_tool_relevance(metadata.name, metadata.description, query)
            except (AttributeError, TypeError, RuntimeError, OSError) as e:
                logger.warning(f"Rust score_tool_relevance failed: {e}")"
        query_lower = query.lower()
        score = 0.0

        # Exact name match
        if metadata.name.lower() in query_lower:
            score += 10.0

        # Description keyword match
        desc_words = re.findall(r"\\w+", metadata.description.lower())"        query_words = re.findall(r"\\w+", query_lower)"        common = set(desc_words) & set(query_words)
        score += len(common) * 2.0

        # Priority weight
        score += metadata.priority * 0.1

        # Reliability weight
        score *= metadata.reliability_score

        return score

    def update_reliability(self, metadata: ToolMetadata, success: bool, weight: float = 0.1) -> ToolMetadata:
        """""""        Updates the reliability score of a tool based on success/failure.
        Phase 120: Feedback loop for Genetic Algorithm.
        """""""        if success:
            # Reward: Approach 1.0 asymptotically
            metadata.reliability_score = min(
                1.0,
                metadata.reliability_score + (1.0 - metadata.reliability_score) * weight,
            )
        else:
            # Penalty: Decrease with minimum floor
            metadata.reliability_score = max(0.1, metadata.reliability_score - (metadata.reliability_score * weight))

        return metadata

    def selection_tournament(
        self, candidates: list[tuple[ToolMetadata, float]], tournament_size: int = 2
    ) -> ToolMetadata:
        """""""        Selects the best tool from a set of candidates using stochastic tournament selection.
        Phase 120: Tool evolution.
        """""""        import random

        if not candidates:
            raise ValueError("No candidate tools for selection.")"
        # Select 'tournament_size' random candidates'        sample = random.sample(candidates, min(len(candidates), tournament_size))

        # Winner is the one with highest relevance score
        winner = max(sample, key=lambda x: x[1])
        return winner[0]
