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

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .Improvement import Improvement
from .ImprovementStatus import ImprovementStatus
from .ProgressReport import ProgressReport
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

__version__ = VERSION

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

    def generate_bmad_strategic_grid(self, root_path: Path) -> str:
        """Generates a 3x3 strategic grid inspired by the BMAD Method.
        
        Checks for project artifacts and quality indicators.
        """
        # Planning Indicators
        has_prd = any((root_path / p).exists() for p in ["docs/PRD.md", "prd.md", "docs/stories"])
        has_arch = any((root_path / p).exists() for p in ["docs/architecture.md", "architecture.md", "docs/CODE_OF_CONDUCT.md"])
        has_backlog = (root_path / "improvements.txt").exists()
        
        # Development Indicators
        has_git = (root_path / ".git").exists()
        has_readme = (root_path / "README.md").exists()
        
        # Quality Indicators
        has_tests = (root_path / "tests").exists()
        has_results = (root_path / "test_results.txt").exists()
        has_errors = (root_path / "errors.txt").exists() and (root_path / "errors.txt").stat().st_size > 0

        # Mapping to Grid
        p_prd = "✅" if has_prd else "❌"
        p_arch = "✅" if has_arch else "❌"
        p_backlog = "✅" if has_backlog else "❌"
        
        d_code = "✅" if has_readme else "⏳"
        d_git = "✅" if has_git else "❌"
        d_stories = "⏳" # Placeholder for story-level tracking

        q_tests = "✅" if has_tests else "❌"
        q_results = "✅" if has_results else "⏳"
        q_health = "❌" if has_errors else "✅"

        grid = [
            "## 🗺️ Strategic Development Grid (BMAD Pattern)",
            "| Phase | Planning | Development | Quality |",
            "| :--- | :---: | :---: | :---: |",
            f"| **Strategy** | {p_backlog} Backlog | {d_git} Repo | {q_health} Health |",
            f"| **Definition** | {p_prd} PRD/Stories | {d_code} Codebase | {q_results} Results |",
            f"| **Structure** | {p_arch} Architecture | {d_stories} Flows | {q_tests} Tests |",
            "\n"
        ]
        return "\n".join(grid)
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