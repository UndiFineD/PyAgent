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

from __future__ import annotations
from src.core.base.version import VERSION
import os
import json
import logging
import time
import re
from pathlib import Path
from typing import Any
from src.core.base.BaseAgent import BaseAgent
from src.infrastructure.orchestration.core.SelfImprovementCore import SelfImprovementCore
from src.infrastructure.backend.LLMClient import LLMClient
from src.core.base.version import is_gate_open

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
        self.improvement_log = os.path.join(self.workspace_root, "data/logs", "self_improvement_audit.jsonl")
        self.research_doc = os.path.join(self.workspace_root, "docs", "IMPROVEMENT_RESEARCH.md")
        os.makedirs(os.path.dirname(self.improvement_log), exist_ok=True)

        # Phase 107: AI-assisted refactoring
        import requests
        self.ai = LLMClient(requests, workspace_root=self.workspace_root)
        self.core = SelfImprovementCore(workspace_root=self.workspace_root)

    def run_improvement_cycle(self, target_dir: str = "src") -> dict[str, Any]:
        """Runs a full scan and fix cycle across the specified directory."""
        # Gatekeeping Check (Phase 108)
        from src.core.base.version import STABILITY_SCORE
        if not is_gate_open(100) or STABILITY_SCORE < 0.8:
            logging.error(f"Self-Improvement: System stability too low ({STABILITY_SCORE}) for autonomous code modification.")
            return {"error": "Stability gate closed - system requires manual stabilization"}

        logging.info(f"Self-Improvement: Starting cycle for {target_dir}...")

        # Phase 108: Ingest actionable tasks from Collective Intelligence
        self.active_tasks = []
        if hasattr(self.fleet, 'intelligence'):
            try:
                self.active_tasks = self.fleet.intelligence.get_actionable_improvement_tasks()
                if self.active_tasks:
                    logging.info(f"Self-Improvement: Hive mind provided {len(self.active_tasks)} actionable tasks.")
            except Exception as e:
                logging.debug(f"Hive task ingestion failed: {e}")

        results = {
            "files_scanned": 0,
            "issues_found": 0,
            "fixes_applied": 0,
            "details": []
        }

        # Find all python files (Phase 135: Supported file targets)
        src_path = os.path.join(self.workspace_root, target_dir)

        target_files: list[Any] = []
        if os.path.isfile(src_path) and src_path.endswith(".py"):
            target_files = [(os.path.dirname(src_path), [], [os.path.basename(src_path)])]
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
                        for issue in file_issues:
                            if issue.get("fixed"):
                                results["fixes_applied"] += 1
                            # Record Debt to Relational Overlay (Phase 107)
                            try:
                                self.fleet.sql_metadata.record_debt(
                                    file_path=os.path.relpath(file_path, self.workspace_root),
                                    issue_type=issue.get("type", "General"),
                                    message=issue.get("message", ""),
                                    fixed=issue.get("fixed", False)
                                )
                            except Exception as e:
                                logging.error(f"Failed to record debt to SQL: {e}")

                        results["details"].append({
                            "file": os.path.relpath(file_path, self.workspace_root),
                            "issues": file_issues
                        })

        # Log completion
        self._log_results(results)

        # Intelligence: Review local interaction shards for "Lessons" (Phase 108)
        try:
            logging.info("Self-Improvement: Reviewing local interaction shards for AI lessons...")
            lessons = self._review_ai_lessons()
            if lessons:
                results["lessons_learned"] = len(lessons)
                logging.info(f"Self-Improvement: Extracted {len(lessons)} new lessons from local training shards.")

            # Fetch summary for research document
            intelligence_summary = self.fleet.sql_metadata.get_intelligence_summary()
            results["intelligence_summary"] = intelligence_summary
        except Exception as e:
            logging.error(f"Intelligence: Lessons review failed: {e}")

        # Phase 108: Relational Maintenance (Aggressive optimization for trillion-param scale)
        try:
            logging.info("Self-Improvement: Optimizing relational metadata indices...")
            self.fleet.sql_metadata.optimize_db()
        except Exception as e:
            logging.error(f"Maintenance: Database optimization failed: {e}")

        # Self-Research: Update the roadmap (Phase 104)
        self.update_research_report(results, lessons=lessons)

        return results

    def update_research_report(self, results: dict[str, Any], lessons: list[str] | None = None) -> str:
        """Updates the IMPROVEMENT_RESEARCH.md and FLEET_AUTO_DOC.md based on latest scan findings."""
        if not os.path.exists(self.research_doc):
            return

        with open(self.research_doc, encoding="utf-8") as f:
            content = f.read()

        # Generate a summary section
        summary = f"\n### Latest Autonomous Scan ({time.strftime('%Y-%m-%d')})\n"
        summary += f"- **Files Scanned**: {results['files_scanned']}\n"
        summary += f"- **Issues Identified**: {results['issues_found']}\n"
        summary += f"- **Autonomous Fixes**: {results['fixes_applied']}\n"
        summary += f"- **Stability Gate Status**: {'OPEN (Green)' if is_gate_open(100) else 'CLOSED (Red)'}\n"

        if results.get('details'):
            summary += "\n#### Top Issues Discovered\n"
            # Sort by issue count
            sorted_details = sorted(results['details'], key=lambda x: len(x['issues']), reverse=True)
            for item in sorted_details[:3]:
                summary += f"- `{item['file']}`: {len(item['issues'])} issues found.\n"

        if lessons:
            summary += "\n### 🧠 AI Lessons Derived from Deep Shard Analysis\n"
            for lesson in lessons:
                summary += f"- {lesson}\n"

        # Phase 108: Update FLEET_AUTO_DOC.md as well
        auto_doc = os.path.join(self.workspace_root, "docs", "FLEET_AUTO_DOC.md")
        if os.path.exists(auto_doc):
            with open(auto_doc, "a", encoding="utf-8") as f:
                f.write(f"\n## {time.strftime('%Y-%m-%d')} - Maintenance Cycle Summary\n")
                f.write(f"The fleet's SelfImprovementOrchestrator completed a cycle over {results['files_scanned']} files. Re-stabilization phase engaged.\n")

        # Update Recent Autonomous Findings (Phase 120: Avoid duplicates)
        header = "## 🚀 Recent Autonomous Findings"
        if header in content:
            # Keep everything BEFORE the header plus the header itself, discard the rest of the findings
            # to prevent infinite bloat.
            base_content = content.split(header)[0]
            new_content = base_content + header + "\n" + summary
        else:
            new_content = content + "\n\n" + header + "\n" + summary

        with open(self.research_doc, "w", encoding="utf-8") as f:
            f.write(new_content)

        logging.info("Self-Improvement: Updated IMPROVEMENT_RESEARCH.md")

    def _analyze_and_fix(self, file_path: str) -> list[dict[str, Any]]:
        """Uses specialized agents to analyze and potentially fix a file."""
        # 0. Versioning Gatekeeping (Phase 106)
        version_file = os.path.join(self.workspace_root, "version.py")
        if not os.path.exists(version_file):
            return [{
                "type": "Versioning Issue",
                "message": "Missing version.py gatekeeper. Project standardization required.",
                "file": file_path
            }]

        with open(file_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        rel_path = os.path.relpath(file_path, self.workspace_root)
        findings = self.core.analyze_content(content, rel_path)

        # Add shell-specific findings (Large file)
        size_kb = os.path.getsize(file_path) / 1024
        if size_kb > 50:
            findings.append({
                "type": "Refactoring Target",
                "message": f"File is large ({size_kb:.1f} KB). Consider decomposing into Core/Shell classes.",
                "file": rel_path
            })

        # Add intelligence-specific findings (Connectivity/Hivemind)
        # Robustness: HTTP Connection Pooling (Phase 108)
        if (re.search(r"requests\.(get|post|put|delete|patch|request)\(", content) or "http.client" in content):
            if "TTL" not in content and "status_cache" not in content.lower() and "ConnectivityManager" not in content:
                findings.append({
                    "type": "Resilience Issue",
                    "message": "Direct HTTP calls detected without connection status caching. Use 15-minute TTL status checks or ConnectivityManager.",
                    "file": rel_path
                })

        if hasattr(self, 'active_tasks') and self.active_tasks:
            for task in self.active_tasks:
                if os.path.basename(file_path).lower() in task['description'].lower():
                    findings.append({
                        "type": "Swarm Intelligence Fix",
                        "message": f"Collective intelligence requires: {task['description']}",
                        "file": rel_path,
                        "task_payload": task
                    })

        # Autonomous Fixes (Self-Healing)
        fixed_count = 0
        new_content = content
        lines = content.split('\n')

        for issue in findings:
            issue["fixed"] = False

            # Simple Core Fixes
            simple_fix = self.core.generate_simple_fix(issue["type"], new_content)
            if simple_fix:
                new_content = simple_fix
                issue["fixed"] = True
                fixed_count += 1
                continue

            # Shell-side fixes (Resilience injection)
            if issue["type"] == "Resilience Issue":
                if "import requests" in new_content and "ConnectivityManager" not in new_content:
                    if "class " in new_content:
                        new_content = new_content.replace("import logging", "import logging\nfrom src.core.base.ConnectivityManager import ConnectivityManager")
                        logging.info(f"Self-Healing: Injected ConnectivityManager into {file_path}")
                        issue["fixed"] = True
                        fixed_count += 1

            if issue["type"] == "Performance Target" and "lru_cache" not in new_content:
                if "import " in new_content and "functools" not in new_content:
                    new_content = new_content.replace("import ", "from functools import lru_cache\nimport ", 1)
                    if "def " in new_content:
                        new_content = re.sub(r"def (\w+)\(([^)]*)\):", r"@lru_cache(maxsize=128)\ndef \1(\2):", new_content, count=1)
                        issue["fixed"] = True
                        fixed_count += 1
                        logging.info(f"Self-Healing: Added @lru_cache to {file_path}")

            # AI-Assisted Fixes (Shell only)
            if not issue["fixed"] and issue["type"] in ["Security Risk", "Speed Issue"]:
                prompt = f"Fix the following {issue['type']} in this Python code:\nIssue: {issue['message']}\nCode Snippet around line {issue.get('line', 'unknown')}:\n"
                context_start = max(0, issue.get('line', 0) - 5)
                context_end = min(len(lines), issue.get('line', 0) + 5)
                prompt += "\n".join(lines[context_start:context_end])
                prompt += "\n\nProvide ONLY the replacement code for the affected lines."

                fix_suggestion = self.ai.smart_chat(prompt, system_prompt="You are a senior Python security and performance engineer. Provide concise code fixes.")
                if fix_suggestion and "```" not in fix_suggestion and len(fix_suggestion) < 200:
                    old_line = lines[issue.get('line', 1)-1]
                    if old_line.strip() in fix_suggestion or fix_suggestion.strip() in old_line:
                        new_content = new_content.replace(old_line, fix_suggestion)
                        issue["fixed"] = True
                        fixed_count += 1
                        logging.info(f"Self-Healing: AI fixed {issue['type']} in {file_path}")

            # Rust Readiness: AI Type Inference
            if issue["type"] == "Rust Readiness Task":
                if not issue["fixed"] and "Found" in issue["message"]:
                    prompt = f"Add comprehensive Python type hints (return types and arguments) to ALL untyped functions in the following code for Rust FFI stability. Return ONLY the modified code:\n\n{new_content[:8000]}"
                    try:
                        ai_typed_code = self.ai.smart_chat(prompt, system_prompt="You are a senior Rust/Python integration expert. Your task is to add perfect type hints to make Python code ready for binding with Rust.")
                        if ai_typed_code and "def " in ai_typed_code and "->" in ai_typed_code:
                                if "```python" in ai_typed_code:
                                    ai_typed_code = ai_typed_code.split("```python")[1].split("```")[0].strip()
                                elif "```" in ai_typed_code:
                                    ai_typed_code = ai_typed_code.split("```")[1].split("```")[0].strip()
                                new_content = ai_typed_code
                                issue["fixed"] = True
                                fixed_count += 1
                                logging.info(f"Self-Healing: AI performed mass-scale type inference in {file_path}")
                    except Exception as e:
                        logging.error(f"AI Typing failed for {file_path}: {e}")

                if not issue["fixed"] and "def __init__" in new_content and "def __init__(self" in new_content and "-> None" not in new_content:
                    new_content = re.sub(r"def __init__\((self[^)]*)\):", r"def __init__(\1) -> None:", new_content)
                    issue["fixed"] = True
                    fixed_count += 1

            # Hivemind Logic Fix
            if issue["type"] == "Swarm Intelligence Fix" and not issue["fixed"]:
                task_payload = issue.get("task_payload", {})
                prompt = f"Collective Intelligence identified an issue: '{task_payload.get('description')}' based on pattern '{task_payload.get('origin_pattern')}'.\nApply the requested fix to the following code and return ONLY the full updated code:\n\n{new_content[:8000]}"
                try:
                    hive_fixed_code = self.ai.smart_chat(prompt, system_prompt="You are an expert AI software architect. Apply specialized swarm intelligence lessons to source code.")
                    if hive_fixed_code and ("def " in hive_fixed_code or "class " in hive_fixed_code):
                        if "```python" in hive_fixed_code:
                                hive_fixed_code = hive_fixed_code.split("```python")[1].split("```")[0].strip()
                        elif "```" in hive_fixed_code:
                                hive_fixed_code = hive_fixed_code.split("```")[1].split("```")[0].strip()
                        new_content = hive_fixed_code
                        issue["fixed"] = True
                        fixed_count += 1
                        logging.info(f"Self-Healing: Applied Swarm Intelligence Fix to {file_path}")
                except Exception as e:
                    logging.error(f"Hive Fix failed for {file_path}: {e}")

        if fixed_count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            logging.info(f"Self-Healing: Applied {fixed_count} fixes to {file_path}")

        return findings

    def _log_results(self, results: dict[str, Any]) -> None:
        """Persists the improvement result to a log file."""
        entry = {
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "summary": {
                "scanned": results["files_scanned"],
                "found": results["issues_found"],
                "fixed": results["fixes_applied"]
            }
        }
        with open(self.improvement_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def _review_ai_lessons(self) -> list[str]:
        """
        Scans sharded interaction history for patterns and failures.
        Extracts 'deep lessons' by reading the actual shard content (Phase 108).
        """
        import gzip
        import json
        lessons = []

        # 1. Query SQL metadata for recent failed tasks
        try:
            failed_tasks = self.fleet.sql_metadata.query_interactions("success = 0 LIMIT 10")
            shards_dir = os.path.join(self.workspace_root, "data/logs", "external_ai_learning")

            for task in failed_tasks:
                shard_id = task.get('shard_id', -1)
                interaction_id = task.get('id', 'unknown')

                # Try to find the shard file
                shard_pattern = f"shard_*_{shard_id:03d}.jsonl.gz"
                import glob
                matching_shards = glob.glob(os.path.join(shards_dir, shard_pattern))

                if not matching_shards:
                    continue

                # Read the shard to get the prompt/result
                deep_reason = "Unknown failure"
                try:
                    with gzip.open(matching_shards[0], "rt", encoding="utf-8") as f:
                        for line in f:
                            data = json.loads(line)
                            if data.get("meta", {}).get("id") == interaction_id or data.get("prompt_hash") == interaction_id:
                                # Found the record!
                                prompt_start = data.get("prompt", "")[:200]
                                result_err = data.get("result", "")[:200]

                                # Use AI to diagnose if possible
                                diag_prompt = f"Analyze this failed interaction and provide a one-sentence lesson:\nPrompt: {prompt_start}\nResult/Error: {result_err}"
                                deep_reason = self.ai.smart_chat(diag_prompt, system_prompt="You are a Meta-Cognitive Analyzer. Summarize the intelligence lesson.")
                                break
                except Exception:
                    deep_reason = f"Failure in task {task['task_type']} (Agent: {task['agent_name']})"

                lesson_text = f"Intelligence Shard {shard_id}: {deep_reason}"
                lessons.append(lesson_text)

                # Persist to Relational Intelligence Table
                try:
                    self.fleet.sql_metadata.record_lesson(
                        interaction_id=interaction_id,
                        text=lesson_text,
                        category="Recursive Improvement"
                    )
                except Exception as db_e:
                    logging.warning(f"SelfImprovement: Failed to persist lesson to SQL: {db_e}")

        except Exception as e:
            logging.debug(f"Intelligence lesson recovery failed: {e}")

        return lessons
