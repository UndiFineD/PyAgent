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

"""
IntelligenceCore: Pure logic for Swarm Collective Intelligence.
Handles weight calculation, insight distillation, and pattern matching.
"""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

__version__ = VERSION

@dataclass
class SwarmInsight:
    agent: str
    insight: str
    confidence: float
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def format_for_pool(self) -> str:
        return f"- {self.agent} ({self.confidence:.2f}): {self.insight}"

class IntelligenceCore:
    """Logic-only core for swarm intelligence synthesis."""

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = workspace_root

    def filter_relevant_insights(self, pool: list[dict[str, Any]], limit: int = 20) -> list[SwarmInsight]:
        """Filters and converts raw insight dictionaries into SwarmInsight objects."""
        insights = []
        # Sort by confidence and recency
        sorted_pool = sorted(pool, key=lambda x: (x.get('confidence', 0), x.get('timestamp', 0)), reverse=True)
        
        for item in sorted_pool[:limit]:
            insights.append(SwarmInsight(
                agent=item.get('agent', 'Unknown'),
                insight=item.get('insight', ''),
                confidence=item.get('confidence', 0.5),
                timestamp=item.get('timestamp', 0)
            ))
        return insights

    def generate_synthesis_prompt(self, insights: list[SwarmInsight], sql_lessons: list[dict[str, Any]]) -> str:
        """Constructs a prompt for AI synthesis from collected insights."""
        lines = [i.format_for_pool() for i in insights]
        for lesson in sql_lessons:
            lines.append(f"- RELATIONAL_LESSON: {lesson.get('sample_lesson')} (Category: {lesson.get('category')})")
            
        pool_text = "\n".join(lines)
        return f"Analyze these swarm insights and relational lessons. Synthesize the top 3 high-level patterns or warnings:\n{pool_text}"

    def extract_actionable_patterns(self, raw_patterns: list[str]) -> list[str]:
        """Filters raw AI output to ensure patterns are technically relevant."""
        valid_patterns = []
        keywords = ["error", "failure", "bottleneck", "missing", "security", "leak", "logic", "refactor", "quantum"]
        
        for p in raw_patterns:
            p_clean = p.strip()
            if not p_clean:
                continue
            
            # Heuristic: must contain a technical keyword or be long enough
            if any(k in p_clean.lower() for k in keywords) or len(p_clean) > 40:
                valid_patterns.append(p_clean)
                
        return valid_patterns