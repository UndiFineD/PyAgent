#!/usr/bin/env python3

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from .Improvement import Improvement
from .ImprovementStatus import ImprovementStatus
from .ProgressReport import ProgressReport

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
import hashlib
import json
import logging
import re
import subprocess
import time

class ProgressDashboard:
    """Generates progress reports and dashboards for improvements.

    Tracks completion rates, velocity, and generates burndown data.

    Attributes:
        reports: List of generated reports.
    """

    def __init__(self) -> None:
        """Initialize the dashboard."""
        self.reports: List[ProgressReport] = []
        self.velocity_history: List[float] = []

    def generate_report(
        self, improvements: List[Improvement]
    ) -> ProgressReport:
        """Generate a progress report.

        Args:
            improvements: List of all improvements.

        Returns:
            ProgressReport with current metrics.
        """
        completed = len([i for i in improvements
                        if i.status == ImprovementStatus.COMPLETED])
        in_progress = len([i for i in improvements
                           if i.status == ImprovementStatus.IN_PROGRESS])
        blocked = len([i for i in improvements
                      if i.status == ImprovementStatus.DEFERRED])

        # Calculate velocity (avg completions per week)
        velocity = self._calculate_velocity()

        report = ProgressReport(
            report_date=datetime.now().isoformat()[:10],
            completed_count=completed,
            in_progress_count=in_progress,
            blocked_count=blocked,
            velocity=velocity
        )

        self.reports.append(report)
        return report

    def _calculate_velocity(self) -> float:
        """Calculate velocity from recent reports."""
        if len(self.reports) < 2:
            return 0.0
        recent = self.reports[-4:]  # Last 4 reports
        if len(recent) < 2:
            return 0.0
        completions = [
            recent[i].completed_count - recent[i - 1].completed_count
            for i in range(1, len(recent))
        ]
        return sum(completions) / len(completions) if completions else 0.0

    def generate_burndown(
        self, improvements: List[Improvement]
    ) -> List[Tuple[str, int]]:
        """Generate burndown chart data."""
        remaining = len([i for i in improvements
                        if i.status not in [ImprovementStatus.COMPLETED,
                                            ImprovementStatus.REJECTED]])
        return [(datetime.now().isoformat()[:10], remaining)]

    def get_completion_rate(
        self, improvements: List[Improvement]
    ) -> float:
        """Calculate completion rate."""
        total = len(improvements)
        if total == 0:
            return 0.0
        completed = len([i for i in improvements
                        if i.status == ImprovementStatus.COMPLETED])
        return (completed / total) * 100

    def export_dashboard(self, improvements: List[Improvement]) -> str:
        """Export dashboard as markdown."""
        report = self.generate_report(improvements)
        lines = [
            "# Improvements Dashboard",
            f"\nGenerated: {report.report_date}",
            "\n## Summary",
            f"- Completed: {report.completed_count}",
            f"- In Progress: {report.in_progress_count}",
            f"- Blocked: {report.blocked_count}",
            f"- Velocity: {report.velocity:.1f} per week",
            f"- Completion Rate: {self.get_completion_rate(improvements):.1f}%"
        ]
        return '\n'.join(lines)
