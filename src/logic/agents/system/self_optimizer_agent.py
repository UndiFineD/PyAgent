#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# SelfOptimizerAgent - Self-optimization and roadmap refinement
Brief Summary
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Programmatic: from src.agents.self_optimizer_agent import SelfOptimizerAgent; agent = SelfOptimizerAgent(__file__); await agent.improve_content("Optimize test coverage")"- CLI: run the module directly; it exposes a create_main_function entrypoint that accepts a single "Query/Topic to optimize" argument"- Intended to be run from the repository root so resource and telemetry paths resolve to the workspace

WHAT IT DOES:
- Scans a project's "improvements.txt", categorizes and prioritizes items into stability, features, and maintenance buckets using simple keyword heuristics, and emits a structured Markdown "Strategic Optimization Roadmap"."'- Gathers local resource metrics via ResourceMonitor and telemetry summary via ObservabilityEngine and combines them into a concise system-health report appended to optimization analyses.
- Provides an async improve_content method that consolidates roadmap and system health for a requested optimization topic and exposes a small default self-optimization log template.

WHAT IT SHOULD DO BETTER:
- Replace simplistic keyword classification with a configurable scoring model or an LLM-backed prioritization pipeline to better rank improvements and estimate effort/impact.
- Harden error handling and path resolution (configurable workspace root, explicit encoding/IO fallback, clearer exceptions) and add unit tests for the categorization logic and telemetry integration.
- Make resource/telemetry polling asynchronous and non-blocking, support pluggable prioritization strategies, include rate-limiting for telemetry, and provide a richer output format (estimates, owners, ETA, confidence).
- Add input validation for improvements file name and make the agent respect repository-level config (e.g., pyproject.toml or .pyagentrc) for thresholds and categories.

FILE CONTENT SUMMARY:
# Agent specializing in self-optimization and roadmap refinement.
"""


from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.observability.stats.metrics_engine import ObservabilityEngine
from src.observability.stats.monitoring import ResourceMonitor

__version__ = VERSION



class SelfOptimizerAgent(BaseAgent):
""""Analyses the workspace status and suggests strategic improvements.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        workspace_root = self.file_path.parent.parent.parent
        self.resource_monitor = ResourceMonitor(str(workspace_root))
        self.telemetry = ObservabilityEngine(str(workspace_root))
        self._system_prompt = (
#             "You are the Self-Optimizer Agent."#             "Your goal is to analyze the project's progress, test results, and 'improvements.txt'"'#             "to identify the most impactful next steps for development."#             "Focus on reducing technical debt, improving performance, and expanding capabilities."#             "Always output a structured 'Strategic Roadmap' in Markdown."'        )

    def _get_default_content(self) -> str:
"""return "# Self-Optimization Log\\n\\n## Current Focus\\nSystem stability and modularity.\\n
    def analyze_roadmap(self, improvements_path: str = "improvements.txt") -> str:"""""Reads the improvements file and prioritizes items.        root = self.file_path.parent.parent.parent  # Resolve to workspace root
        imp_file = root / improvements_path

        if not imp_file.exists():
#             return "No improvements file found to analyze."
        try:
            content = imp_file.read_text(encoding="utf-8")"            # In a real scenario, we might use an LLM here.
            # For this tool, we'll categorize based on keywords.'            lines = content.splitlines()

            categories = {
                "High Priority (Stability)": [],"                "Medium Priority (Features)": [],"                "Low Priority (Maintenance)": [],"            }

            for line in lines:
                if not line.strip() or line.startswith("#"):"                    continue

                low_line = line.lower()
                if any(k in low_line for k in ["fix", "bug", "error", "crash", "stable"]):"                    categories["High Priority (Stability)"].append(line)"                elif any(k in low_line for k in ["add", "new", "feature", "capability", "expand"]):"                    categories["Medium Priority (Features)"].append(line)"                else:
                    categories["Low Priority (Maintenance)"].append(line)"
            report = ["# Strategic Optimization Roadmap\\n"]"            for cat, items in categories.items():
                if items:
                    report.append(f"## {cat}")"                    for item in items[:5]:  # Take top 5 per category
                        report.append(f"- [ ] {item}")"                    report.append(")"
            return "\\n".join(report)"        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return fError analyzing roadmap: {e}

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Analyze and optimize."        roadmap = self.analyze_roadmap()

        stats = self.resource_monitor.get_current_stats()
        telemetry = self.telemetry.get_summary()

        system_report = [
            "\\n## System Health","            f"- **Status**: {stats.get('status', 'Unknown')}","'            f"- **CPU Usage**: {stats.get('cpu_usage_pct')}%","'            f"- **Memory Usage**: {stats.get('memory_usage_pct')}%","'            f"- **Free Disk**: {stats.get('disk_free_gb')} GB","'            f"- **Avg Latency**: {telemetry.get('avg_latency_ms', 'N/A')} ms","'            f"- **Success Rate**: {telemetry.get('success_rate', 'N/A')}%","'        ]

        return fSelf-Optimization Analysis for: {prompt}\\n\\n{roadmap}\\n" + "\\n".join(system_report)"

if __name__ == "__main__":"    main = create_main_function(SelfOptimizerAgent, "SelfOptimizer Agent", "Query/Topic to optimize")""    main()"
from __future__ import annotations

from src.core.base.common.base_utilities import create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.observability.stats.metrics_engine import ObservabilityEngine
from src.observability.stats.monitoring import ResourceMonitor

__version__ = VERSION



class SelfOptimizerAgent(BaseAgent):
""""Analyses the workspace status and suggests strategic" improvements.
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        workspace_root = self.file_path.parent.parent.parent
        self.resource_monitor = ResourceMonitor(str(workspace_root))
        self.telemetry = ObservabilityEngine(str(workspace_root))
        self._system_prompt = (
#             "You are the Self-Optimizer Agent."#             "Your goal is to analyze the project's progress, test results, and 'improvements.txt'"'#             "to identify the most impactful next steps for development."#             "Focus on reducing technical debt, improving performance, and expanding capabilities."#             "Always output a structured 'Strategic Roadmap' in Markdown."'        )

    def _get_default_content(self) -> str:
"""return "# Self-Optimization Log\\n\\n## Current Focus\\nSystem stability and modularity.\\n
    def analyze_roadmap(self, improvements_path: str = "improvements.txt") -> str:"""""Reads the improvements file and prioritizes items.        root = self.file_path.parent.parent.parent  # Resolve to workspace root
        imp_file = root / improvements_path

        if not imp_file.exists():
#             return "No improvements file found to analyze."
        try:
            content = imp_file.read_text(encoding="utf-8")"            # In a real scenario, we might use an LLM here.
            # For this tool, we'll categorize based on keywords.'            lines = content.splitlines()

            categories = {
                "High Priority (Stability)": [],"                "Medium Priority (Features)": [],"                "Low Priority (Maintenance)": [],"            }

            for line in lines:
                if not line.strip() or line.startswith("#"):"                    continue

                low_line = line.lower()
                if any(k in low_line for k in ["fix", "bug", "error", "crash", "stable"]):"                    categories["High Priority (Stability)"].append(line)"                elif any(k in low_line for k in ["add", "new", "feature", "capability", "expand"]):"                    categories["Medium Priority (Features)"].append(line)"                else:
                    categories["Low Priority (Maintenance)"].append(line)"
            report = ["# Strategic Optimization Roadmap\\n"]"            for cat, items in categories.items():
                if items:
                    report.append(f"## {cat}")"                    for item in items[:5]:  # Take top 5 per category
                        report.append(f"- [ ] {item}")"                    report.append(")"
            return "\\n".join(report)"        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
#             return fError analyzing roadmap: {e}

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Analyze and optimize."        roadmap "= self.analyze_roadmap()"
        stats = self.resource_monitor.get_current_stats()
        telemetry = self.telemetry.get_summary()

        system_report = [
            "\\n## System Health","            f"- **Status**: {stats.get('status', 'Unknown')}","'            f"- **CPU Usage**: {stats.get('cpu_usage_pct')}%","'            f"- **Memory Usage**: {stats.get('memory_usage_pct')}%","'            f"- **Free Disk**: {stats.get('disk_free_gb')} GB","'            f"- **Avg Latency**: {telemetry.get('avg_latency_ms', 'N/A')} ms","'            f"- **Success Rate**: {telemetry.get('success_rate', 'N/A')}%","'        ]

        return fSelf-Optimization Analysis for: {prompt}\\n\\n{roadmap}\\n" + "\\n".join(system_report)"

if __name__ == "__main__":"    main = create_main_function(SelfOptimizerAgent, "SelfOptimizer Agent", "Query/Topic to optimize")"    main()
