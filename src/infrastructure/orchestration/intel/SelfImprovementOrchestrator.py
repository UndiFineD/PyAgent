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

from __future__ import annotations
from src.core.base.Version import VERSION
import os
import json
import logging
import time
import re
from pathlib import Path
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.infrastructure.orchestration.core.SelfImprovementCore import (
    SelfImprovementCore,
)
from src.infrastructure.orchestration.intel.SelfImprovementAnalysis import (
    SelfImprovementAnalysis,
)
from src.infrastructure.orchestration.intel.SelfImprovementFixer import (
    SelfImprovementFixer,
)
from src.infrastructure.backend.LLMClient import LLMClient
from src.core.base.Version import is_gate_open

__version__ = VERSION


class SelfImprovementOrchestrator(BaseAgent):
    """
    Orchestrates the fleet's self-improvement cycle: scanning for tech debt,
    security leaks, and quality issues, and applying autonomous fixes.
    """

    def __init__(self, fleet_manager=None) -> None:
        # Phase 125: Handle polymorphic initialization (Fleet or Path string)
        if not fleet_manager:
            # Fallback to current working directory
            self.workspace_root = os.getcwd()
            self.fleet = None
        elif isinstance(fleet_manager, str) or isinstance(fleet_manager, Path):
            self.workspace_root = str(fleet_manager)
            self.fleet = None  # Will be set by registry if possible
        else:
            self.workspace_root = str(fleet_manager.workspace_root)
            self.fleet = fleet_manager

        # We pass workspace_root as the file_path for BaseAgent context
        super().__init__(self.workspace_root)
        self.improvement_log = os.path.join(
            self.workspace_root, "data/logs", "self_improvement_audit.jsonl"
        )
        self.research_doc = os.path.join(
            self.workspace_root, "docs", "IMPROVEMENT_RESEARCH.md"
        )
        os.makedirs(os.path.dirname(self.improvement_log), exist_ok=True)

        # Phase 107: AI-assisted refactoring
        import requests

        self.ai = LLMClient(requests, workspace_root=self.workspace_root)
        self.core = SelfImprovementCore(workspace_root=self.workspace_root)
        self.analysis = SelfImprovementAnalysis(workspace_root=self.workspace_root)
        self.fixer = SelfImprovementFixer(
            ai=self.ai, core=self.core, workspace_root=self.workspace_root
        )

    def run_improvement_cycle(self, target_dir: str = "src") -> dict[str, Any]:
        """Runs a full scan and fix cycle across the specified directory."""
        # Gatekeeping Check (Phase 108)
        from src.core.base.Version import STABILITY_SCORE

        if not is_gate_open(100) or STABILITY_SCORE < 0.8:
            logging.error(
                f"Self-Improvement: System stability too low ({STABILITY_SCORE}) for autonomous code modification."
            )
            return {
                "error": "Stability gate closed - system requires manual stabilization"
            }

        logging.info(f"Self-Improvement: Starting cycle for {target_dir}...")

        # Phase 108: Ingest actionable tasks from Collective Intelligence
        self.active_tasks = []
        if hasattr(self.fleet, "intelligence"):
            try:
                self.active_tasks = (
                    self.fleet.intelligence.get_actionable_improvement_tasks()
                )
                if self.active_tasks:
                    logging.info(
                        f"Self-Improvement: Hive mind provided {len(self.active_tasks)} actionable tasks."
                    )
            except Exception as e:
                logging.debug(f"Hive task ingestion failed: {e}")

        results = {
            "files_scanned": 0,
            "issues_found": 0,
            "fixes_applied": 0,
            "details": [],
        }

        # Phase 14: Start batch debt recording for performance
        debt_records: list[tuple] = []
        current_time = time.time()

        # Find all python files (Phase 135: Supported file targets)
        src_path = os.path.join(self.workspace_root, target_dir)

        target_files: list[Any] = []
        if os.path.isfile(src_path) and src_path.endswith(".py"):
            target_files = [
                (os.path.dirname(src_path), [], [os.path.basename(src_path)])
            ]
        elif os.path.isdir(src_path):
            target_files = os.walk(src_path)

        for root, _, files in target_files:
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    results["files_scanned"] += 1
                    file_issues = self._analyze_and_fix(file_path)
                    if file_issues:
                        results["issues_found"] += len(file_issues)
                        rel_path = os.path.relpath(file_path, self.workspace_root)
                        for issue in file_issues:
                            if issue.get("fixed"):
                                results["fixes_applied"] += 1
                            # Batch debt record (Phase 14: Reduce SQL overhead)
                            debt_records.append((
                                rel_path,
                                issue.get("type", "General"),
                                issue.get("message", ""),
                                1 if issue.get("fixed", False) else 0,
                                current_time,
                            ))

                        results["details"].append(
                            {
                                "file": rel_path,
                                "issues": file_issues,
                            }
                        )

        # Phase 14: Flush all debt records in one transaction
        if debt_records:
            try:
                if self.fleet and hasattr(self.fleet, "sql_metadata"):
                    self.fleet.sql_metadata.bulk_record_debt(debt_records)
            except Exception as e:
                logging.error(f"Failed to bulk record debt to SQL: {e}")

        # Log completion
        self._log_results(results)

        # Intelligence: Review local interaction shards for "Lessons" (Phase 108)
        try:
            logging.info(
                "Self-Improvement: Reviewing local interaction shards for AI lessons..."
            )
            lessons = self.analysis.review_ai_lessons(self.fleet, self.ai)
            if lessons:
                results["lessons_learned"] = len(lessons)
                logging.info(
                    f"Self-Improvement: Extracted {len(lessons)} new lessons from local training shards."
                )

            # Fetch summary for research document
            if self.fleet and hasattr(self.fleet, "sql_metadata"):
                intelligence_summary = self.fleet.sql_metadata.get_intelligence_summary()
                results["intelligence_summary"] = intelligence_summary
        except Exception as e:
            logging.error(f"Intelligence: Lessons review failed: {e}")

        # Phase 108: Relational Maintenance (Aggressive optimization for trillion-param scale)
        try:
            if self.fleet and hasattr(self.fleet, "sql_metadata"):
                logging.info("Self-Improvement: Optimizing relational metadata indices...")
                self.fleet.sql_metadata.optimize_db()
        except Exception as e:
            logging.error(f"Maintenance: Database optimization failed: {e}")

        # Self-Research: Update the roadmap (Phase 104)
        self.analysis.update_research_report(results, lessons=lessons if 'lessons' in locals() else None)

        return results

    def _analyze_and_fix(self, file_path: str) -> list[dict[str, Any]]:
        """Uses specialized assistant classes to analyze and fix a file."""
        # 0. Delegate Analysis tasks
        versioning_issue = self.analysis.check_versioning()
        if versioning_issue:
            return [versioning_issue | {"file": file_path}]

        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return []

        rel_path = os.path.relpath(file_path, self.workspace_root)
        findings = self.core.analyze_content(content, rel_path)

        # 1. Structural and Hive Analysis
        self.analysis.add_structural_findings(findings, file_path, rel_path, content)
        self.analysis.add_hive_findings(findings, file_path, rel_path, getattr(self, "active_tasks", []))

        # 2. Autonomous Fixes (Self-Healing Delegation)
        self.fixer.apply_autonomous_fixes(file_path, rel_path, content, findings)

        return findings

    def _log_results(self, results: dict[str, Any]) -> None:
        """Persists the improvement result to a log file."""
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "scanned": results["files_scanned"],
                "found": results["issues_found"],
                "fixed": results["fixes_applied"],
            },
        }
        try:
            with open(self.improvement_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass
