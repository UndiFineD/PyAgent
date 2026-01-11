#!/usr/bin/env python3
from __future__ import annotations
"""
ObservabilityCore logic for metric aggregation and auditing.
Pure logic for summarizing agent performance and costs.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional


































from src.core.base.version import VERSION
__version__ = VERSION

@dataclass
class AgentMetric:
    agent_name: str
    operation: str
    duration_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "success"
    token_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    model: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

class ObservabilityCore:
    """Pure logic for processing agent telemetry data."""
    
    def __init__(self) -> None:
        self.metrics_history: List[AgentMetric] = []

    def process_metric(self, metric: AgentMetric) -> None:
        """Standardizes a metric entry."""
        self.metrics_history.append(metric)

    def summarize_performance(self) -> Dict[str, Any]:
        """Calculates aggregate stats from history."""
        if not self.metrics_history:
            return {"count": 0, "avg_duration": 0, "total_cost": 0}
            
        total_duration = sum(m.duration_ms for m in self.metrics_history)
        total_cost = sum(m.estimated_cost for m in self.metrics_history)
        count = len(self.metrics_history)
        
        # Breakdown by agent
        by_agent = {}
        for m in self.metrics_history:
            if m.agent_name not in by_agent:
                by_agent[m.agent_name] = {"count": 0, "total_cost": 0, "avg_duration": 0}
            stats = by_agent[m.agent_name]
            stats["count"] += 1
            stats["total_cost"] += m.estimated_cost
            
        return {
            "total_count": count,
            "avg_duration_ms": total_duration / count,
            "total_cost_usd": round(total_cost, 6),
            "agents": by_agent
        }

    def filter_by_time(self, start_iso: str, end_iso: str) -> List[AgentMetric]:
        """Filters metrics within a time range."""
        results = []
        for m in self.metrics_history:
            if start_iso <= m.timestamp <= end_iso:
                results.append(m)
        return results

    def calculate_reliability_scores(self, agent_names: List[str]) -> List[float]:
        """
        Calculates normalized reliability scores (0.0 to 1.0) for a list of agents.
        Reliability = success_count / total_attempts.
        If no history, defaults to 0.5 (neutral).
        """
        scores: List[float] = []
        
        # Aggregate history per agent
        stats: Dict[str, Dict[str, int]] = {}
        for m in self.metrics_history:
            if m.agent_name not in stats:
                stats[m.agent_name] = {"success": 0, "total": 0}
            stats[m.agent_name]["total"] += 1
            if m.status == "success":
                stats[m.agent_name]["success"] += 1
                
        for name in agent_names:
            if name in stats and stats[name]["total"] > 0:
                score = stats[name]["success"] / stats[name]["total"]
                scores.append(score)
            else:
                # Neutral default for new/unknown agents
                scores.append(0.5)
                
        return scores
