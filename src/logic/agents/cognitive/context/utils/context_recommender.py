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


"""Auto-extracted class from agent_context.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from src.logic.agents.cognitive.context.models.context_recommendation import (
    ContextRecommendation,
)
import re

__version__ = VERSION


class ContextRecommender:
    """Recommends context improvements based on similar files.

    Analyzes similar files to suggest context improvements.

    Example:
        >>> recommender=ContextRecommender()
        >>> recommendations=recommender.recommend("auth.py", similar_contexts)
    """

    def __init__(self) -> None:
        self.reference_files: dict[str, str] = {}

    def add_reference(self, file_name: str, content: str) -> None:
        """Add a reference context file used for recommendations."""
        self.reference_files[file_name] = content

    def find_similar(self, query: str) -> list[str]:
        """Find reference files that look similar to the query."""
        query_words = set(query.lower().split())
        matches: list[str] = []
        for name, content in self.reference_files.items():
            content_words = set(content.lower().split())
            if query_words & content_words:
                matches.append(name)
        return matches

    def recommend(
        self,
        content_or_target_file: str,
        similar_contexts: dict[str, str] | None = None,
    ) -> list[ContextRecommendation]:
        """Generate context recommendations.

        Compatibility behavior:
        - If similar_contexts is provided, it is treated as the corpus.
        - Otherwise, content_or_target_file is treated as the target content
          and reference_files are used as the corpus.
        """
        corpus = (
            similar_contexts if similar_contexts is not None else self.reference_files
        )
        target_content = content_or_target_file

        recommendations: list[ContextRecommendation] = []
        if not corpus:
            return recommendations

        target_sections = set(re.findall(r"##\s+(\w+)", target_content))

        section_counts: dict[str, int] = {}
        for _, content in corpus.items():
            sections = re.findall(r"##\s+(\w+)", content)
            for section in sections:
                section_counts[section] = section_counts.get(section, 0) + 1

        common_sections: list[tuple[str, int]] = sorted(
            section_counts.items(), key=lambda x: x[1], reverse=True
        )
        suggested = [
            name for name, _ in common_sections if name not in target_sections
        ][:5]
        if suggested:
            recommendations.append(
                ContextRecommendation(
                    source_file=list(corpus.keys())[0],
                    suggested_sections=suggested,
                    reason="Common sections in similar files",
                    confidence=0.8,
                )
            )

        return recommendations
