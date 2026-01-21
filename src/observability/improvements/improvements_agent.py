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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
from .effort_estimate import EffortEstimate
from .improvement import Improvement
from .improvement_category import ImprovementCategory
from .improvement_priority import ImprovementPriority
from .improvement_status import ImprovementStatus
from .improvement_template import ImprovementTemplate
from .improvement_manager import ImprovementManager
from src.core.base.lifecycle.base_agent import BaseAgent
from datetime import datetime
from typing import Any
import json
import logging

__version__ = VERSION


class ImprovementsAgent(BaseAgent):
    """Updates code file improvement suggestions using AI assistance.

    This agent reads .improvements.md files and uses AI to suggest better,
    more actionable improvements for the associated code file.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self._check_associated_file()

        # Improvement management delegated to ImprovementManager
        self.manager = ImprovementManager(base_file_path=str(self.file_path))
        self._analytics: dict[str, Any] = {}

    @property
    def _improvements(self) -> list[Improvement]:
        return self.manager._improvements

    @property
    def _templates(self) -> dict[str, ImprovementTemplate]:
        return self.manager._templates

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".improvements.md"):
            logging.warning(
                f"File {self.file_path.name} does not end with .improvements.md"
            )

    def _check_associated_file(self) -> None:
        """Check if the associated code file exists.

        Searches:
        1. Same directory with various extensions.
        2. Parent directory (e.g. if doc is in a subfolder).
        3. Common code directories (src, lib, app).
        """
        name = self.file_path.name
        if not name.endswith(".improvements.md"):
            return

        base_name = name[:-16]

        # Extensions to try
        extensions = [
            "",
            ".py",
            ".sh",
            ".js",
            ".ts",
            ".md",
            ".txt",
            ".yaml",
            ".yml",
            ".json",
            ".html",
            ".css",
            ".go",
            ".rs",
        ]

        # Directories to search
        search_dirs = []
        if self.file_path.parent:
            search_dirs.append(self.file_path.parent)
            if self.file_path.parent.parent:
                search_dirs.append(self.file_path.parent.parent)

        # Look for src/lib adjacent to current or parent
        for d in list(search_dirs):
            for sub in ["src", "lib", "app", "classes"]:
                cand_dir = d / sub
                if cand_dir.exists() and cand_dir.is_dir():
                    search_dirs.append(cand_dir)

        # Unique search directories
        unique_dirs = []
        seen = set()
        for d in search_dirs:
            resolved = str(d.resolve())
            if resolved not in seen:
                unique_dirs.append(d)
                seen.add(resolved)

        for directory in unique_dirs:
            for ext in extensions:
                candidate = directory / (base_name + ext)
                try:
                    if (
                        candidate.exists()
                        and candidate.is_file()
                        and candidate.resolve() != self.file_path.resolve()
                    ):
                        logging.debug(f"Found associated file: {candidate}")
                        return
                except (OSError, PermissionError):
                    continue

        logging.warning(
            f"Could not find associated code file for {self.file_path.name}"
        )

    # ========== Improvement Management ==========

    def load(self) -> None:
        """Load improvements from file."""
        if not self.file_path.exists():
            return

        content = self.file_path.read_text(encoding="utf-8")
        self.parse_markdown(content)

    def parse_markdown(self, content: str) -> None:
        """Parse improvements from markdown content.

        Supports format:
        - [ ] **Title** (Category) <!-- id: id -->
          - Description
        """
        self.manager.parse_markdown(content)

    def save(self) -> None:
        """Save improvements to file."""
        self.current_content = self.export_improvements(format="markdown")
        self.update_file()

    def add_improvement(
        self,
        title: str,
        description: str,
        file_path: str = "",
        priority: ImprovementPriority = ImprovementPriority.MEDIUM,
        category: ImprovementCategory = ImprovementCategory.OTHER,
        effort: EffortEstimate = EffortEstimate.MEDIUM,
        tags: list[str] | None = None,
        dependencies: list[str] | None = None,
    ) -> Improvement:
        """Add a new improvement."""
        return self.manager.add_improvement(
            title=title,
            description=description,
            file_path=file_path,
            priority=priority,
            category=category,
            effort=effort,
            tags=tags,
            dependencies=dependencies,
        )

    def get_improvements(self) -> list[Improvement]:
        """Get all improvements."""
        return self.manager._improvements

    def get_improvement_by_id(self, improvement_id: str) -> Improvement | None:
        """Get an improvement by ID."""
        return next(
            (i for i in self.manager._improvements if i.id == improvement_id), None
        )

    def update_status(self, improvement_id: str, status: ImprovementStatus) -> bool:
        """Update the status of an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.status = status
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def get_improvements_by_status(
        self, status: ImprovementStatus
    ) -> list[Improvement]:
        """Get improvements filtered by status."""
        return [i for i in self.manager._improvements if i.status == status]

    def get_improvements_by_category(
        self, category: ImprovementCategory
    ) -> list[Improvement]:
        """Get improvements filtered by category."""
        return [i for i in self.manager._improvements if i.category == category]

    def get_improvements_by_priority(
        self, priority: ImprovementPriority
    ) -> list[Improvement]:
        """Get improvements filtered by priority."""
        return [i for i in self.manager._improvements if i.priority == priority]

    # ========== Impact Scoring ==========
    def calculate_impact_score(self, improvement: Improvement) -> float:
        """Calculate impact score for an improvement."""
        return self.manager.calculate_impact_score(improvement)

    def prioritize_improvements(self) -> list[Improvement]:
        """Return improvements sorted by impact score."""
        return self.manager.prioritize()

    # ========== Effort Estimation ==========
    def estimate_total_effort(self) -> int:
        """Return the total effort score for non-completed improvements.

        Tests expect this to be an integer sum of `EffortEstimate` values.
        """
        return self.manager.estimate_total_effort()

    def _estimate_total_effort_breakdown(self) -> dict[str, Any]:
        """Internal analytics-friendly effort breakdown."""
        total = int(self.estimate_total_effort())
        by_category: dict[str, int] = {}
        for imp in self._improvements:
            if imp.status in (ImprovementStatus.COMPLETED, ImprovementStatus.REJECTED):
                continue
            by_category[imp.category.name] = by_category.get(
                imp.category.name, 0
            ) + int(imp.effort.value)
        return {
            "total_hours": total,
            "by_category": by_category,
            "estimated_days": total / 8,
            "estimated_weeks": total / 40,
        }

    # ========== Dependencies ==========
    def add_dependency(self, improvement_id: str, depends_on_id: str) -> bool:
        """Add a dependency between improvements."""
        improvement = self.get_improvement_by_id(improvement_id)
        depends_on = self.get_improvement_by_id(depends_on_id)

        if improvement and depends_on and depends_on_id not in improvement.dependencies:
            improvement.dependencies.append(depends_on_id)
            return True
        return False

    def get_dependencies(self, improvement_id: str) -> list[Improvement]:
        """Get all dependencies for an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if not improvement:
            return []

        dependencies: list[Improvement] = []
        for dep_id in improvement.dependencies:
            dep = self.get_improvement_by_id(dep_id)
            if dep is not None:
                dependencies.append(dep)
        return dependencies

    def get_dependents(self, improvement_id: str) -> list[Improvement]:
        """Get all improvements that depend on this one."""
        return [i for i in self._improvements if improvement_id in i.dependencies]

    def get_ready_to_implement(self) -> list[Improvement]:
        """Get improvements that have all dependencies satisfied."""
        ready: list[Improvement] = []
        for imp in self.manager._improvements:
            if imp.status == ImprovementStatus.APPROVED:
                deps_satisfied = all(
                    (dep := self.get_improvement_by_id(dep_id)) is not None
                    and dep.status == ImprovementStatus.COMPLETED
                    for dep_id in imp.dependencies
                )
                if deps_satisfied or not imp.dependencies:
                    ready.append(imp)
        return ready

    # ========== Templates ==========

    def add_template(self, template: ImprovementTemplate) -> None:
        """Add a custom template."""
        self.manager.add_template(template)  # Wait, need to add this to manager

    def get_templates(self) -> dict[str, ImprovementTemplate]:
        """Get all templates."""
        return self.manager._templates

    def create_from_template(
        self, template_name: str, variables: dict[str, str], file_path: str = ""
    ) -> Improvement | None:
        """Create an improvement from a template."""
        imp = self.manager.create_from_template(template_name, variables, file_path)
        if imp:
            # Add to list and save
            self.manager._improvements.append(imp)
            self.save_to_file()
            return imp
        return None

    # ========== Voting ==========

    def vote(self, improvement_id: str, vote: int = 1) -> bool:
        """Vote for an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.votes += vote
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def get_top_voted(self, limit: int = 10) -> list[Improvement]:
        """Get top voted improvements."""
        return sorted(self._improvements, key=lambda i: i.votes, reverse=True)[:limit]

    # ========== Assignment ==========

    def assign(self, improvement_id: str, assignee: str) -> bool:
        """Assign an improvement to someone."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.assignee = assignee
            improvement.updated_at = datetime.now().isoformat()
            if improvement.status == ImprovementStatus.PROPOSED:
                improvement.status = ImprovementStatus.IN_PROGRESS
            return True
        return False

    def unassign(self, improvement_id: str) -> bool:
        """Unassign an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.assignee = None
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def get_by_assignee(self, assignee: str) -> list[Improvement]:
        """Get improvements assigned to a specific person."""
        return [i for i in self._improvements if i.assignee == assignee]

    def approve_improvement(self, improvement_id: str) -> bool:
        """Approve an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.status = ImprovementStatus.APPROVED
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def reject_improvement(self, improvement_id: str, reason: str = "") -> bool:
        """Reject an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.status = ImprovementStatus.REJECTED
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def get_assigned_to(self, assignee: str) -> list[Improvement]:
        """Get improvements assigned to a specific person."""
        return [i for i in self._improvements if i.assignee == assignee]

    # ========== Analytics ==========

    def calculate_analytics(self) -> dict[str, Any]:
        """Calculate analytics for improvements."""
        total = len(self._improvements)
        if total == 0:
            return {"total": 0}

        by_status: dict[str, int] = {}
        for status in ImprovementStatus:
            by_status[status.name] = len(self.get_improvements_by_status(status))

        by_category: dict[str, int] = {}
        for category in ImprovementCategory:
            by_category[category.name] = len(
                self.get_improvements_by_category(category)
            )

        by_priority: dict[str, int] = {}
        for priority in ImprovementPriority:
            by_priority[priority.name] = len(
                self.get_improvements_by_priority(priority)
            )

        completed = by_status.get("COMPLETED", 0)
        completion_rate = (completed / total * 100) if total > 0 else 0

        effort = self._estimate_total_effort_breakdown()

        self._analytics = {
            "total": total,
            "by_status": by_status,
            "by_category": by_category,
            "by_priority": by_priority,
            "completion_rate": completion_rate,
            "effort_estimation": effort,
            "avg_votes": sum(i.votes for i in self._improvements) / total,
        }

        return self._analytics

    # ========== Export ==========
    def export_improvements(self, format: str = "json") -> str:
        """Export improvements to various formats."""
        if format == "json":
            data: list[dict[str, Any]] = [
                {
                    "id": i.id,
                    "title": i.title,
                    "description": i.description,
                    "priority": i.priority.name,
                    "category": i.category.name,
                    "status": i.status.name,
                    "effort": i.effort.name,
                    "impact_score": i.impact_score,
                    "votes": i.votes,
                    "assignee": i.assignee,
                    "dependencies": i.dependencies,
                    "tags": i.tags,
                }
                for i in self._improvements
            ]
            return json.dumps(data, indent=2)
        elif format == "markdown":
            lines = ["# Improvements\n"]
            for priority in sorted(
                ImprovementPriority, key=lambda p: p.value, reverse=True
            ):
                imps = self.get_improvements_by_priority(priority)
                if imps:
                    lines.append(f"\n## {priority.name}\n")
                    for i in imps:
                        status_icon = " "
                        if i.status == ImprovementStatus.COMPLETED:
                            status_icon = "x"
                        elif i.status == ImprovementStatus.IN_PROGRESS:
                            status_icon = "/"
                        elif i.status == ImprovementStatus.DEFERRED:
                            status_icon = "-"

                        lines.append(
                            f"- [{status_icon}] **{i.title}** ({i.category.value}) <!-- id: {i.id} -->"
                        )
                        if i.description:
                            # Handle multi-line descriptions
                            for desc_line in i.description.split("\n"):
                                lines.append(f"  - {desc_line}")
            return "\n".join(lines)
        elif format == "csv":
            header = "id,title,description,priority,category,status,effort"
            rows = [header]
            for i in self._improvements:
                rows.append(
                    ",".join(
                        [
                            str(i.id),
                            str(i.title).replace(",", " "),
                            str(i.description).replace("\n", " ").replace(",", " "),
                            str(i.priority.name),
                            str(i.category.name),
                            str(i.status.name),
                            str(i.effort.name),
                        ]
                    )
                )
            return "\n".join(rows)
        return ""

    # ========== Documentation Generation ==========
    def generate_documentation(self) -> str:
        """Generate documentation for all improvements."""
        analytics = self.calculate_analytics()
        docs = ["# Improvement Documentation\n"]
        docs.append("## Summary\n")
        docs.append(f"- Total Improvements: {analytics['total']}")
        docs.append(f"- Completion Rate: {analytics['completion_rate']:.1f}%")
        docs.append(
            f"- Total Effort: {analytics['effort_estimation']['estimated_days']:.1f} days\n"
        )
        docs.append("## By Status\n")
        for status, count in analytics["by_status"].items():
            if count > 0:
                docs.append(f"- {status}: {count}")
        docs.append("\n## Prioritized List\n")
        for imp in self.prioritize_improvements()[:10]:
            docs.append(
                f"- [{imp.priority.name}] {imp.title} (Score: {imp.impact_score:.1f})"
            )
        return "\n".join(docs)

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return default content for new improvement files."""
        return "# Improvements\n\nNo improvements suggested.\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
            "# Original suggestions preserved below:\n\n"
        )

    def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Use AI to improve the improvement suggestions.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids duplicated wrapper sections).
        """
        actual_path = Path(target_file) if target_file else self.file_path
        logging.info(f"Improving suggestions for {actual_path}")
        # Add guidance for structured output
        enhanced_prompt = (
            f"{prompt}\n\n"
            "Please format the improvements as a markdown list with "
            "checkboxes for actionable items:\n"
            "- [ ] Actionable item 1\n"
            "- [ ] Actionable item 2\n\n"
            "Group improvements by priority (High, Medium, Low) if applicable."
        )
        return super().improve_content(enhanced_prompt, target_file=target_file)

    def validate_improved_content(self, content: str) -> bool:
        """Validate that the improved content follows the required format.

        Checks for:
        1. Essential headers (Priority levels)
        2. Correct markdown checklist format
        """
        if not content:
            return False

        # Check for at least one priority header (case insensitive)
        content_upper = content.upper()
        has_priority = any(
            p in content_upper
            for p in ["## HIGH", "## MEDIUM", "## LOW", "## URGENT", "## BACKLOG"]
        )

        # Check for standard markdown checkboxes
        has_checkboxes = (
            "- [ ] " in content or "- [x] " in content or "- [X] " in content
        )

        if not has_priority:
            logging.warning("Improved content missing priority headers (e.g. ## HIGH)")
        if not has_checkboxes:
            logging.warning(
                "Improved content missing markdown checkboxes (e.g. - [ ] )"
            )

        return has_priority and has_checkboxes
