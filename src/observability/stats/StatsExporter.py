#!/usr/bin/env python3
from __future__ import annotations
"""Auto-extracted class from agent_stats.py"""

from typing import Any, Dict, List, Optional
import json


































from src.core.base.version import VERSION
__version__ = VERSION

class StatsExporter:
    """Exports stats in various formats."""
    def __init__(self, format: str = "json") -> None:
        self.format = format

    def export(self, metrics: Dict[str, Any], format: Optional[str] = None) -> str:
        """Export metrics in specified format."""
        export_format = format or self.format
        if export_format == "json":
            return json.dumps(metrics)
        elif export_format == "prometheus":
            lines: List[str] = []
            for name, value in metrics.items():
                lines.append(f"{name} {value}")
            return "\n".join(lines)
        return ""
