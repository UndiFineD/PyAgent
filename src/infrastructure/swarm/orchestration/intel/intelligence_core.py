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


"""
IntelligenceCore: Pure logic for Swarm Collective Intelligence.
Handles weight calculation, insight distillation, and pattern matching.
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

from src.core.base.lifecycle.version import VERSION
from src.core.base.common.models.core_enums import FailureClassification

try:
    import rust_core as rc
except (ImportError, AttributeError):
    rc = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

__version__ = VERSION


@dataclass
class SwarmInsight:
    """Data class representing a derived insight from the swarm."""

    agent: str
    insight: str
    confidence: float

    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())

    def format_for_pool(self) -> str:
        """Format the insight for the synthesis prompt."""
        return f"- {self.agent} ({self.confidence:.2f}): {self.insight}"


class IntelligenceCore:
    """Logic-only core for swarm intelligence synthesis."""

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = workspace_root
        self._unclassified_tracker: Counter = Counter()

        # Circuit Breaker for Meta-Stability
        self._healing_depth = 0
        self._last_healing_timestamp = 0.0
        self._max_recursion_depth = 3
        self._healing_cooldown = 300.0  # 5 minutes

        self._taxonomy_map: Dict[str, FailureClassification] = {
            "hallucination": FailureClassification.AI_ERROR,
            "timeout": FailureClassification.NETWORK_FAILURE,
            "connection_refused": FailureClassification.NETWORK_FAILURE,
            "file_not_found": FailureClassification.STATE_CORRUPTION,
            "lock_error": FailureClassification.STATE_CORRUPTION,
            "memory_limit": FailureClassification.RESOURCE_EXHAUSTION,
            "disk_space": FailureClassification.RESOURCE_EXHAUSTION,
            "assertion_error": FailureClassification.TEST_INFRASTRUCTURE,
            "recursion_depth": FailureClassification.RECURSION_LIMIT,
            "shard": FailureClassification.SHARD_CORRUPTION,
            "integrity": FailureClassification.SHARD_CORRUPTION,
            "corrupt": FailureClassification.SHARD_CORRUPTION,
            "distributed": FailureClassification.DISTRIBUTED_STATE_ERROR,
            "synchronization": FailureClassification.DISTRIBUTED_STATE_ERROR,
            "recursive": FailureClassification.RECURSION_LIMIT, # Map rough matches
            "self_improvement": FailureClassification.RECURSIVE_IMPROVEMENT,
            "self_healing": FailureClassification.RECURSIVE_IMPROVEMENT,
            "swarm_desynchronization": FailureClassification.DISTRIBUTED_STATE_ERROR,
        }

    def filter_relevant_insights(self, pool: list[dict[str, Any]], limit: int = 20) -> list[SwarmInsight]:
        """Filters relevant insights from the pool.

        Args:
            pool: list of insight dictionaries.
            limit: maximum number of insights to return.

        Returns:
            List of SwarmInsight objects.
        """
        if rc:
            try:
                # Optimized sort and truncate in Rust
                pool = rc.filter_relevant_insights(pool, limit)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Rust filter_relevant_insights failed: {e}")

        insights = []
        # Fallback/Process results
        for item in pool[:limit]:
            insights.append(
                SwarmInsight(
                    agent=item.get("agent", "Unknown"),
                    insight=item.get("insight", ""),
                    confidence=item.get("confidence", 0.5),
                    timestamp=item.get("timestamp", 0),
                )
            )
        return insights

    def generate_synthesis_prompt(self, insights: list[SwarmInsight], sql_lessons: list[dict[str, Any]]) -> str:
        """Constructs a prompt for AI synthesis from collected insights.

        Args:
            insights: List of SwarmInsight objects.
            sql_lessons: List of SQL lesson dictionaries.

        Returns:
            A prompt string for the AI.
        """
        lines = [i.format_for_pool() for i in insights]
        for lesson in sql_lessons:
            lines.append(f"- RELATIONAL_LESSON: {lesson.get('sample_lesson')} (Category: {lesson.get('category')})")

        pool_text = "\n".join(lines)
        return (
            "Analyze these swarm insights and relational lessons. "
            f"Synthesize the top 3 high-level patterns or warnings:\n{pool_text}"
        )

    def extract_actionable_patterns(self, raw_patterns: list[str]) -> list[str]:
        """Filters raw AI output to ensure patterns are technically relevant.

        Args:
            raw_patterns: List of raw pattern strings from the AI.

        Returns:
            List of filtered, actionable pattern strings.
        """
        valid_patterns = []
        unknown_failures = []
        keywords = [
            "error",
            "failure",
            "bottleneck",
            "missing",
            "security",
            "leak",
            "logic",
            "refactor",
            "quantum",
            "recursive_loop",
            "shard_parallelization",
            "test_infrastructure",
            "unknown",
            "improvement",
        ]

        for p in raw_patterns:
            p_clean = p.strip()
            if not p_clean:
                continue

            # Phase 336: Taxonomy Classification
            classification = FailureClassification.UNKNOWN
            lower_p = p_clean.lower()
            
            # Check map
            for keyword, cls in self._taxonomy_map.items():
                if keyword in lower_p:
                    classification = cls
                    break

            # Circuit Breaker: Prevent meta-stability loops in self-healing
            if classification == FailureClassification.RECURSIVE_IMPROVEMENT:
                current_ts = datetime.now().timestamp()
                # Reset if outside cooldown window
                if current_ts - self._last_healing_timestamp > self._healing_cooldown:
                    self._healing_depth = 0

                self._healing_depth += 1
                self._last_healing_timestamp = current_ts

                if self._healing_depth > self._max_recursion_depth:
                    logger.error(
                        f"Intelligence Circuit Breaker: Stopping recursive healing loop (Depth {self._healing_depth})"
                    )
                    valid_patterns.append("STOP_RECURSION: Meta-stability loop detected in self-healing.")
                    continue

            # If still unknown, check general keywords
            if classification == FailureClassification.UNKNOWN:
                if any(k in lower_p for k in keywords) or len(p_clean) > 40:
                    classification = FailureClassification.AI_ERROR # Default bucket if technical but unclassified specific
                else:
                    # Generic / Noise
                    unknown_failures.append(p_clean)
                    self._unclassified_tracker[p_clean[:50]] += 1 # Track frequency
                    continue
            
            valid_patterns.append(p_clean)

        # Phase 336: Surface unknown patterns for investigation if they are significant
        if unknown_failures:
            # Check for semantic clusters of unknown failures (in a real scenario we'd use embeddings)
            # For now, simply log them as "Unclassified/Emergent"
            valid_patterns.append(
                f"[Unclassified Patterns Detected]: Found {len(unknown_failures)} patterns that did not match "
                "known failure taxonomies. Investigate for emergent behaviors."
            )

        return valid_patterns
