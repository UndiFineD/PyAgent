#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .ContextRecommendation import ContextRecommendation

from src.classes.base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

class ContextRecommender:
    """Recommends context improvements based on similar files.

    Analyzes similar files to suggest context improvements.

    Example:
        >>> recommender=ContextRecommender()
        >>> recommendations=recommender.recommend("auth.py", similar_contexts)
    """

    def __init__(self) -> None:
        self.reference_files: Dict[str, str] = {}

    def add_reference(self, file_name: str, content: str) -> None:
        """Add a reference context file used for recommendations."""
        self.reference_files[file_name] = content

    def find_similar(self, query: str) -> List[str]:
        """Find reference files that look similar to the query."""
        query_words = set(query.lower().split())
        matches: List[str] = []
        for name, content in self.reference_files.items():
            content_words = set(content.lower().split())
            if query_words & content_words:
                matches.append(name)
        return matches

    def recommend(
        self,
        content_or_target_file: str,
        similar_contexts: Optional[Dict[str, str]] = None
    ) -> List[ContextRecommendation]:
        """Generate context recommendations.

        Compatibility behavior:
        - If similar_contexts is provided, it is treated as the corpus.
        - Otherwise, content_or_target_file is treated as the target content
          and reference_files are used as the corpus.
        """
        corpus = similar_contexts if similar_contexts is not None else self.reference_files
        target_content = content_or_target_file

        recommendations: List[ContextRecommendation] = []
        if not corpus:
            return recommendations

        target_sections = set(re.findall(r"##\s+(\w+)", target_content))

        section_counts: Dict[str, int] = {}
        for _, content in corpus.items():
            sections = re.findall(r"##\s+(\w+)", content)
            for section in sections:
                section_counts[section] = section_counts.get(section, 0) + 1

        common_sections: List[Tuple[str, int]] = sorted(section_counts.items(), key=lambda x: x[1], reverse=True)
        suggested = [name for name, _ in common_sections if name not in target_sections][:5]
        if suggested:
            recommendations.append(ContextRecommendation(
                source_file=list(corpus.keys())[0],
                suggested_sections=suggested,
                reason="Common sections in similar files",
                confidence=0.8
            ))

        return recommendations
