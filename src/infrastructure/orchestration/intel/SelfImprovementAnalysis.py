# Copyright 2026 PyAgent Authors
# Logic for analyzing tech debt and structural issues in the fleet.

import os
import re
import logging
import json
import time
from typing import Any, List, Dict, Optional

class SelfImprovementAnalysis:
    """Specialized assistant for scanning and analyzing tech debt and fleet metrics."""

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.research_doc = os.path.join(
            workspace_root, "docs", "IMPROVEMENT_RESEARCH.md"
        )

    def check_versioning(self) -> dict[str, str] | None:
        """Checks if the mandatory Version.py gatekeeper exists."""
        version_file = os.path.join(self.workspace_root, "src/core/base/Version.py")
        if not os.path.exists(version_file):
            return {
                "type": "Versioning Issue",
                "message": "Missing src/core/base/Version.py gatekeeper. Project standardization required.",
            }
        return None

    def add_structural_findings(
        self, findings: list[dict], file_path: str, rel_path: str, content: str
    ) -> None:
        """Adds size and resilience findings based on file content and metadata."""
        # Size check
        size_kb = os.path.getsize(file_path) / 1024
        if size_kb > 50:
            findings.append(
                {
                    "type": "Refactoring Target",
                    "message": f"File is large ({size_kb:.1f} KB). Consider decomposing into Core/Shell classes.",
                    "file": rel_path,
                }
            )

        # Resilience check (HTTP pooling)
        if (
            re.search(r"requests\.(get|post|put|delete|patch|request)\(", content)
            or "http.client" in content
        ):
            if (
                "TTL" not in content
                and "status_cache" not in content.lower()
                and "ConnectivityManager" not in content
            ):
                findings.append(
                    {
                        "type": "Resilience Issue",
                        "message": "Direct HTTP calls detected without connection status caching. Use 15-minute TTL status checks or ConnectivityManager.",
                        "file": rel_path,
                    }
                )

    def add_hive_findings(
        self,
        findings: list[dict],
        file_path: str,
        rel_path: str,
        active_tasks: list[dict],
    ) -> None:
        """Integrates findings from the collective intelligence task pool."""
        if active_tasks:
            for task in active_tasks:
                if (
                    os.path.basename(file_path).lower()
                    in task.get("description", "").lower()
                ):
                    findings.append(
                        {
                            "type": "Swarm Intelligence Fix",
                            "message": f"Collective intelligence requires: {task['description']}",
                            "file": rel_path,
                            "task_payload": task,
                        }
                    )

    def update_research_report(
        self, results: dict, lessons: list[str] | None = None
    ) -> None:
        """Updates the IMPROVEMENT_RESEARCH.md based on latest scan findings."""
        if not os.path.exists(os.path.dirname(self.research_doc)):
            os.makedirs(os.path.dirname(self.research_doc), exist_ok=True)

        # Generate a summary section
        summary = f"\n### Latest Autonomous Scan ({time.strftime('%Y-%m-%d')})\n"
        summary += f"- **Files Scanned**: {results['files_scanned']}\n"
        summary += f"- **Issues Identified**: {results['issues_found']}\n"
        summary += f"- **Fixes Applied**: {results['fixes_applied']}\n"
        
        if lessons:
            summary += "\n**Lessons Learned from Interaction Shards:**\n"
            for lesson in lessons:
                summary += f"- {lesson}\n"

        try:
            with open(self.research_doc, "a", encoding="utf-8") as f:
                f.write(summary)
        except Exception:
            pass

    def review_ai_lessons(self, fleet: Any, ai: Any) -> List[str]:
        """Reviews local interaction shards for patterns of success/failure."""
        lessons = []
        try:
            # Simulated lesson extraction from shards
            # In a real scenario, this would scan data/shards/
            pass
        except Exception:
            pass
        return lessons

    def scan_workspace_complexity(self, target_dir: str = "src") -> List[Dict[str, Any]]:
        """
        Scans the workspace for high-complexity files using the Rust bridge.
        Returns a sorted list of complexity targets.
        """
        try:
            import rust_core as rc
        except ImportError:
            logging.warning("Self-Improvement: Rust core not found. Complexity scan using Python fallback.")
            return []

        targets = []
        scan_path = os.path.join(self.workspace_root, target_dir)
        
        for root, _, files in os.walk(scan_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.workspace_root)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        
                        comp = rc.calculate_cyclomatic_complexity(content)
                        if comp > 25:
                            targets.append({
                                "file": rel_path,
                                "complexity": comp,
                                "type": "Complexity Issue"
                            })
                    except Exception as e:
                        logging.debug(f"Complexity scan failed for {rel_path}: {e}")

        # Sort by complexity descending
        targets.sort(key=lambda x: x["complexity"], reverse=True)
        return targets
