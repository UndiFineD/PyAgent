#!/usr/bin/env python3
# Refactored by copilot-placeholder
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

"""
Orchestrator scan mixin.py module.
"""
# Licensed under the Apache License, Version 2.0 (the "License");

import logging
import os
import time
from typing import Any


class OrchestratorScanMixin:
    """Methods for scanning files and analyzing contents."""

    workspace_root: str
    fleet: Any
    analysis: Any
    core: Any
    fixer: Any

    def _scan_and_repair_files(
        self, target_dir: str, results: dict[str, Any], allow_triton_check: bool = True
    ) -> list[tuple[str, str, str, int, float]]:
        """Iterates through files, analyzes them, and applies fixes. Stops on first error and triggers coding swarm."""
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
                if not file.endswith(".py"):
                    continue
                file_path = os.path.join(root, file)
                result = self._process_single_file(file_path, results, debt_records, current_time, allow_triton_check)
                if result is not None:
                    return result
        return debt_records

    def _process_single_file(
        self, file_path: str, results: dict[str, Any], debt_records: list, current_time: float, allow_triton_check: bool
    ) -> list[tuple[str, str, str, int, float]] | None:
        """Process a single Python file and return early if swarm is triggered."""
        results["files_scanned"] += 1
        file_issues = self._analyze_and_fix(file_path, allow_triton_check=allow_triton_check)

        if not file_issues:
            return None

        results["issues_found"] += len(file_issues)
        rel_path = os.path.relpath(file_path, self.workspace_root)

        unfixed_issues = [issue for issue in file_issues if not issue.get("fixed", False)]
        if unfixed_issues:
            # Stop on first error and trigger coding swarm
            logging.info(f"Self-Improvement: Found {len(unfixed_issues)} unfixed issues in {rel_path}. Stopping scan and triggering coding swarm.")
            self._trigger_coding_swarm(file_path, rel_path, unfixed_issues)
            self._record_file_issues(rel_path, file_issues, results, debt_records, current_time)
            results["details"].append({"file": rel_path, "issues": file_issues, "swarm_triggered": True})
            return debt_records

        # If all issues were fixed, continue normally
        self._record_file_issues(rel_path, file_issues, results, debt_records, current_time)
        results["details"].append({"file": rel_path, "issues": file_issues})
        return None

    def _record_file_issues(self, rel_path: str, file_issues: list, results: dict, debt_records: list, current_time: float) -> None:
        """Record file issues to debt records and update results."""
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

    def _trigger_coding_swarm(self, file_path: str, rel_path: str, unfixed_issues: list[dict[str, Any]]) -> None:
        """Triggers a coding swarm to fix unfixed issues in a file."""
        # Format the issues for the coding task
        issues_description = "\n".join([
            f"- {issue.get('type', 'Issue')}: {issue.get('message', 'No description')}"
            for issue in unfixed_issues
        ])
        
        prompt = f"""Fix the following issues in file {rel_path}:

{issues_description}

Please analyze the file and apply appropriate fixes for these issues. Focus on code quality, security, and best practices."""

        try:
            if self.fleet:
                # Use fleet delegation if available
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    self.fleet.delegate_to("CoderAgent", prompt, file_path)
                )
                loop.close()
                logging.info(f"Self-Improvement: Coding swarm triggered via fleet for {rel_path}. Result: {result}")
            else:
                # Fallback: Create CoderAgent directly
                import os
                import asyncio
                from src.logic.agents.development.coder_agent import CoderAgent
                coder_path = os.path.join(self.workspace_root, "src/logic/agents/development/coder_agent.py")
                # Configure to use Grok Code Fast 1 instead of default model
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    # Attempt to initialize with specific inference engine
                    coder_agent = CoderAgent(coder_path, inference_engine="grok-code-fast-1")
                except TypeError:
                    # Fallback if kwargs are not supported by the constructor MRO
                    logging.warning("Self-Improvement: CoderAgent validation failed for custom kwargs using fallback.")
                    coder_agent = CoderAgent(coder_path)

                result = loop.run_until_complete(coder_agent.improve_content(prompt, target_file=file_path))
                loop.close()
                logging.info(f"Self-Improvement: Coding swarm triggered for {rel_path}. Result: {result}")
        except Exception as e:
            logging.error(f"Self-Improvement: Failed to trigger coding swarm for {rel_path}: {e}")

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
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            return []

        rel_path = os.path.relpath(file_path, self.workspace_root)
        findings = self.core.analyze_content(content, rel_path, allow_triton_check=allow_triton_check)

        # 1. Structural and Hive Analysis
        self.analysis.add_structural_findings(findings, file_path, rel_path, content)
        self.analysis.add_hive_findings(findings, file_path, rel_path, getattr(self, "active_tasks", []))
        self.analysis.add_profiling_findings(findings, file_path, rel_path, content)

        # 2. Autonomous Fixes (Self-Healing Delegation)
        self.fixer.apply_autonomous_fixes(file_path, rel_path, content, findings)

        return findings
