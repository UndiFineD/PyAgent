
"""
Orchestrator scan mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import logging
import os
import time
from typing import Any


class OrchestratorScanMixin:
    """Methods for scanning files and analyzing contents."""

    def _scan_and_repair_files(
        self, target_dir: str, results: dict[str, Any], allow_triton_check: bool = True
    ) -> list[tuple[str, str, str, int, float]]:
        """Iterates through files, analyzes them, and applies fixes."""
        debt_records: list[tuple[str, str, str, int, float]] = []
        current_time = time.time()
        src_path = os.path.join(self.workspace_root, target_dir)

        if os.path.isfile(src_path) and src_path.endswith(".py"):
            target_files: Any = [(os.path.dirname(src_path), [], [os.path.basename(src_path)])]
        elif os.path.isdir(src_path):
            target_files = os.walk(src_path)
        else:
            return []

        for root, _, files in target_files:
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    results["files_scanned"] += 1
                    file_issues = self._analyze_and_fix(file_path, allow_triton_check=allow_triton_check)

                    if file_issues:
                        results["issues_found"] += len(file_issues)
                        rel_path = os.path.relpath(file_path, self.workspace_root)
                        for issue in file_issues:
                            if issue.get("fixed"):
                                results["fixes_applied"] += 1
                            debt_records.append(
                                (
                                    rel_path,
                                    issue.get("type", "General"),
                                    issue.get("message", ""),
                                    1 if issue.get("fixed", False) else 0,
                                    current_time,
                                )
                            )
                        results["details"].append({"file": rel_path, "issues": file_issues})
        return debt_records

    def _record_debt_to_sql(self, debt_records: list[tuple]) -> None:
        """Batch records technical debt to the SQL metadata store."""
        if debt_records:
            try:
                if self.fleet and hasattr(self.fleet, "sql_metadata"):
                    self.fleet.sql_metadata.bulk_record_debt(debt_records)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.error(f"Failed to bulk record debt to SQL: {e}")

    def _analyze_and_fix(self, file_path: str, allow_triton_check: bool = True) -> list[dict[str, Any]]:
        """Uses specialized assistant classes to analyze and fix a file."""
        # 0. Delegate Analysis tasks
        versioning_issue = self.analysis.check_versioning()
        if versioning_issue:
            return [versioning_issue | {"file": file_path}]

        try:
            with open(file_path, encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            return []

        rel_path = os.path.relpath(file_path, self.workspace_root)
        findings = self.core.analyze_content(content, rel_path, allow_triton_check=allow_triton_check)

        # 1. Structural and Hive Analysis
        self.analysis.add_structural_findings(findings, file_path, rel_path, content)
        self.analysis.add_hive_findings(findings, file_path, rel_path, getattr(self, "active_tasks", []))

        # 2. Autonomous Fixes (Self-Healing Delegation)
        self.fixer.apply_autonomous_fixes(file_path, rel_path, content, findings)

        return findings
