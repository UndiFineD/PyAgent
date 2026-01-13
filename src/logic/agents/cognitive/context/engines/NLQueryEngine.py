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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.logic.agents.cognitive.context.models.NLQueryResult import NLQueryResult
from typing import Dict, List, Optional

__version__ = VERSION

class NLQueryEngine:
    """Searches context with natural language queries.

    Provides natural language interface for searching context.

    Example:
        >>> engine=NLQueryEngine()
        >>> result=engine.query("How does authentication work?", contexts)
    """

    def __init__(self) -> None:
        """Initialize NL query engine."""
        self.contexts: dict[str, str] = {}

    def add_context(self, name: str, content: str) -> None:
        """Add context to the engine."""
        self.contexts[name] = content

    def extract_keywords(self, query: str) -> list[str]:
        """Extract keywords from query."""
        return query.lower().split()

    def query(self, question: str, contexts: dict[str, str] | None = None) -> NLQueryResult:
        """Query contexts with natural language.

        Args:
            question: Natural language question.
            contexts: Optional dictionary of context file paths to contents.
                      If omitted, uses contexts added via add_context().

        Returns:
            NLQueryResult with answer.
        """
        # Simplified NL query - in production, use LLM
        relevant: list[str] = []
        keywords = question.lower().split()
        active_contexts = contexts if contexts is not None else self.contexts
        for path, content in active_contexts.items():
            content_lower = content.lower()
            if any(kw in content_lower for kw in keywords):
                relevant.append(path)
        return NLQueryResult(
            query=question,
            answer=f"Found {len(relevant)} relevant context files",
            relevant_contexts=relevant,
            confidence=0.7 if relevant else 0.2
        )