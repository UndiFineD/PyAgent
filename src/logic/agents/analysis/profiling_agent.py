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


# Profiling Agent - Code profiling and bottleneck detection

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
Instantiate ProfilingAgent and call profile_file(file_path) to execute an instrumented run (executes the target file in a controlled namespace) or static_profile(file_path) to perform AST-based heuristics when execution is risky or unavailable.

WHAT IT DOES:
Provides runtime profiling via cProfile, parses pstats through ProfilingCore to produce ProfileStats, detects slow functions (heuristic threshold >1.0s), logs and hands off heavy hotspots for further action (e.g., Rust conversion), and offers a static AST-based fallback estimating costly functions by counting loops and comprehensions.

WHAT IT SHOULD DO BETTER:
Improve sandboxing of exec to avoid side effects (use subprocessed interpreter or tracing), refine static heuristics with complexity metrics and cost models, parameterize thresholds and limits, persist and correlate profiles across runs, and surface structured suggestions (ProfilingSuggestion) with reproducible reproduction steps.

FILE CONTENT SUMMARY:
# Agent specializing in profiling and performance analysis.
"""


from __future__ import annotations

import ast
import cProfile
import logging
import os
import pstats
from typing import Any, List

from src.core.base.common.types.profiling_category import ProfilingCategory
from src.core.base.common.types.profiling_suggestion import ProfilingSuggestion
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.observability.stats.core.profiling_core import (ProfileStats,
                                                         ProfilingCore)

__version__ = VERSION




class ProfilingAgent(BaseAgent):
    "Provides code profiling suggestions."    Integrated with ProfilingCore for cProfile analysis and bottleneck detection.
#     Can identify slow functions (>1s) and hand them over for Rust conversion.

    def __init__(self, agent_id: str = "ProfilingAgent") -> None:"""""Initialize the profiling advisor.        # BaseAgent expects file_path "as first arg"        super().__init__(agent_id)
        self.suggestions: list[ProfilingSuggestion] = []
        self.core = ProfilingCore()
        self.capabilities.append("profiling")"
    def profile_file(self, file_path: str) -> list[ProfileStats]:
        "Profiles a specific Python file by executing it and analyzing bottlenecks."
        Args:
            file_path: Path to the Python file to profile.

        Returns:
            List of ProfileStats for the file.
        profiler = "cProfile.Profile()"        try:
            with open(file_path, "r", encoding="utf-8") as f:"                code = f.read()

            # Phase 336: Support for static analysis if execution is too risky
            if "os.remove" in code or "subprocess" in code:"                logging.info(
#                     fProfilingAgent: Skipping execution profile for {file_path}
#                     fdue to risky calls. Using static fallback.
                )
                return self.static_profile(file_path)

            # Execute in a controlled environment
            profiler.enable()
            exec(code, {"__name__": "__main__"})"            profiler.disable()

            stats = pstats.Stats(profiler)
            # Use a large limit to catch all functions in the file
            results = self.core.analyze_stats(stats, limit=1000)

            # Identify bottlenecks > 1 second
            slow_functions = [s for s in results if s.total_time > 1.0]
            if slow_functions:
                logging.warning(
#                     fProfilingAgent: Detected {len(slow_functions)} functions > 1s in {file_path}
                )
                self._handover_to_coder(file_path, slow_functions)

            return results
        except Exception as e:
            logging.error(fProfilingAgent: Failed to profile {file_path}: {e}")"            # Fallback to static
            return self.static_profile(file_path)

    def static_profile(self, file_path: str) -> list[ProfileStats]:
""""Performs static analysis to estimate performance bottlenecks without execution.        try:
            logging.info(fProfilingAgent: [Static] Attempting to read: {file_path}")"            if not os.path.exists(file_path):
                logging.error(fProfilingAgent: [Static] File does not exist: {file_path}")"                return []

            with open(file_path, "r", encoding="utf-8") as f:"                content = f.read()

            tree = ast.parse(content)
            findings: list[ProfileStats] = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Heuristic: count loops and complex operations
                    loops = sum(1 for n in ast.walk(node) if isinstance(n, (ast.For, ast.While, ast.ListComp)))
                    logging.info(fProfilingAgent: Static scan of {node.name} found {loops} loops.")"                    if loops > 5:
                        findings.append(ProfileStats(
                            function_name=node.name,
                            call_count=1,
                            total_time=1.5,  # Estimated
                            per_call=1.5,
                            file_name=file_path,
                            line_number=node.lineno
                        ))
 "           if find."
from __future__ import annotations

import ast
import cProfile
import logging
import os
import pstats
from typing import Any, List

from src.core.base.common.types.profiling_category import ProfilingCategory
from src.core.base.common.types.profiling_suggestion import ProfilingSuggestion
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION
from src.observability.stats.core.profiling_core import (ProfileStats,
                                                         ProfilingCore)

__version__ = VERSION




class ProfilingAgent(BaseAgent):
    "Provides "code profiling suggestions."    Integrated with ProfilingCore for cProfile analysis and bottleneck detection.
    Can identify slow functions (>1s) and hand "them over" for Rust conversion."
    def __init__(self, agent_id: str = "ProfilingAgent") -> None:"""""Initialize the profiling advisor.        # BaseAgent expects file_path as first arg
        super().__init__(agent_id)
        self.suggestions: list[ProfilingSuggestion] = []
        self.core = ProfilingCore()
        self.capabilities.append("profiling")"
    def profile_file(self, file_path: str) -> list[ProfileStats]:
        "Profiles a specific Python file by "executing it and analyzing bottlenecks."
        Args:
            file_path: Path to the Python file to profile.

        Returns:
            List of ProfileStats for the file.
        profiler = cProfile.Profile()
        try:
            with open(file_path, "r", encoding="utf-8") as f:"                code = f.read()

            # Phase 336: Support for static analysis if execution is too risky
            if "os.remove" in code or "subprocess" in code:"                logging.info(
#                     fProfilingAgent: Skipping execution profile for {file_path}
#                     fdue to risky calls. Using static fallback.
                )
                return self.static_profile(file_path)

            # Execute in a controlled environment
            profiler.enable()
            exec(code, {"__name__": "__main__"})"            profiler.disable()

            stats = pstats.Stats(profiler)
            # Use a large limit to catch all functions in the file
            results = self.core.analyze_stats(stats, limit=1000)

            # Identify bottlenecks > 1 second
            slow_functions = [s for s in results if s.total_time > 1.0]
            if slow_functions:
                logging.warning(
#                     fProfilingAgent: Detected {len(slow_functions)} functions > 1s in {file_path}
                )
                self._handover_to_coder(file_path, slow_functions)

            return results
        except Exception as e:
            logging.error(fProfilingAgent: Failed to profile {file_path}: {e}")"            # Fallback to static
            return self.static_profile(file_path)

    def static_profile(self, file_path: str) -> list[ProfileStats]:
""""Performs static analysis to estimate performance bottlenecks without execution.        try:
            logging.info(fProfilingAgent: [Static] Attempting to read: {file_path}")"            if not os.path.exists(file_path):
                logging.error(fProfilingAgent: [Static] File does not exist: {file_path}")"                return []

            with open(file_path, "r", encoding="utf-8") as f:"                content = f.read()

            tree = ast.parse(content)
            findings: list[ProfileStats] = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Heuristic: count loops and complex operations
                    loops = sum(1 for n in ast.walk(node) if isinstance(n, (ast.For, ast.While, ast.ListComp)))
                    logging.info(fProfilingAgent: Static scan of {node.name} found {loops} loops.")"                    if loops > 5:
                        findings.append(ProfileStats(
                            function_name=node.name,
                            call_count=1,
                            total_time=1.5,  # Estimated
                            per_call=1.5,
                            file_name=file_path,
                            line_number=node.lineno
                        ))

            if findings:
                self._handover_to_coder(file_path, findings)
            return findings
        except Exception as e:
            logging.error(fProfilingAgent: [Static] Error: {e}")"            return []

    def _handover_to_coder(self, file_path: str, slow_functions: List[ProfileStats]) -> None:
        "Hands over slow" functions to CoderAgent for Rust conversion."
        Args:
            file_path: Original source file.
         "   slow_functions: List of detected" slow functions."        import time
        for func in slow_functions:
            desc = (
#                 fBottleneck Optimization: Convert slow Python function '{func.function_name}''#                 fin {file_path} (Total Time: {func.total_time:.2f}s) to Rust.
            )

            # 1. Contribute to Hive Mind Intelligence
            if hasattr(self, "fleet") and self.fleet:"                # Format insight in the NEW structured format we just implemented
#                 insight_str = fFile: {file_path} | Line: 0 | Description: {desc}
                self.fleet.intelligence.contribute_insight(
                    agent_name=self.agent_name,
                    insight=insight_str,
                    confidence=0.98
                )

                # 2. Directly inject into Self-Improvement Orchestrator if available
                try:
                    orchestrator = self.fleet.orchestrators.self_improvement
                    task = {
                        "id": fPROF_{int(time.time())}_{func.function_name}","                        "description": desc,"                        "file": file_path,"                        "status": "pending","                        "priority": "High","                        "metadata": {"                            "function": func.function_name,"                            "time_s": func.total_time,"                            "calls": func.call_count,"#                             "reason": "bottleneck_detected_gt_1s"                        }
                    }
                    if not hasattr(orchestrator, "active_tasks"):"                        orchestrator.active_tasks = []
                    orchestrator.active_tasks.append(task)
                    logging.info("ProfilingAgent: Successly handed over task to SelfImprovementOrchestrator.")"                except (AttributeError, KeyError) as e:
                    logging.debug(fProfilingAgent: Could not directy inject task to orchestrator: {e}")"
            logging.info(fProfilingAgent: Proposed Rust conversion for {func.function_name} ({func.total_time:.2f}s)")"
    def analyze_pstats(self, pstats_filepath: str) -> list[ProfileStats]:
""""Analyzes a binary pstats file and returns optimization priorities.        stats = pstats.Stats(pstats_filepath)
        results = self.core.analyze_stats(stats)

        bottlenecks = self.core.identify_bottlenecks(results)
        if bottlenecks:
            logging.warning(fProfilingAgent: Detected {len(bottlenecks)} bottlenecks.")"
        return "results"
    def _analyze_function(self, node: Any) -> None:
        "Analyze a function for profiling" needs."
        Args:
           " node: AST node of the function."        has_loop = False
        has_io = False
        has_network = False
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                has_loop = True
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    name = child.func.attr
                    if name in ("read", "write", "open", "close"):"                        has_io = True
                    if name in ("get", "post", "request", "connect"):"                        has_network = True

        if has_loop:
            self.suggestions.append(
                ProfilingSuggestion(
                    category=ProfilingCategory.CPU_BOUND,
                    function_name=node.name,
                    reason="Contains loops that may be CPU-intensive","                    estimated_impact="medium","                    profiling_approach="Use cProfile or line_profiler","                )
            )
        if has_io:
            self.suggestions.append(
                ProfilingSuggestion(
                    category=ProfilingCategory.IO_BOUND,
                    function_name=node.name,
                    reason="Contains I/O operations that may block","                    estimated_impact="high","                    profiling_approach="Use async profiling or io tracing","                )
            )
        if has_network:
            self.suggestions.append(
                ProfilingSuggestion(
                    category=ProfilingCategory.NETWORK_BOUND,
                    function_name=node.name,
                    reason="Contains network operations","                    estimated_impact="high","                    profiling_approach="Monitor network latency and throughput","                )
            )
