#!/usr/bin/env python3

"""
IntelligenceCore: Pure logic for Swarm Collective Intelligence.
Handles weight calculation, insight distillation, and pattern matching.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

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

    def __init__(self, workspace_root: Optional[str] = None) -> None:
        self.workspace_root = workspace_root

    def filter_relevant_insights(self, pool: List[Dict[str, Any]], limit: int = 20) -> List[SwarmInsight]:
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

    def generate_synthesis_prompt(self, insights: List[SwarmInsight], sql_lessons: List[Dict[str, Any]]) -> str:
        """Constructs a prompt for AI synthesis from collected insights."""
        lines = [i.format_for_pool() for i in insights]
        for lesson in sql_lessons:
            lines.append(f"- RELATIONAL_LESSON: {lesson.get('sample_lesson')} (Category: {lesson.get('category')})")
            
        pool_text = "\n".join(lines)
        return f"Analyze these swarm insights and relational lessons. Synthesize the top 3 high-level patterns or warnings:\n{pool_text}"

    def extract_actionable_patterns(self, raw_patterns: List[str]) -> List[str]:
        """Filters raw AI output to ensure patterns are technically relevant."""
        valid_patterns = []
        keywords = ["error", "failure", "bottleneck", "missing", "security", "leak", "logic", "refactor", "quantum"]
        
        for p in raw_patterns:
            p_clean = p.strip()
            if not p_clean: continue
            
            # Heuristic: must contain a technical keyword or be long enough
            if any(k in p_clean.lower() for k in keywords) or len(p_clean) > 40:
                valid_patterns.append(p_clean)
                
        return valid_patterns
