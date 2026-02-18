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


from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any
import asyncio
from src.core.base.execution.agent_command_handler import AgentCommandHandler
from src.core.base.lifecycle.version import VERSION
from .orchestrator_features import OrchestratorFeatures

__version__ = VERSION
BaseAgent = None  # Will be imported locally to avoid circular import



class OrchestratorAgent(OrchestratorFeatures):  # pylint: disable=too-many-ancestors
    # Primary orchestrator for swarm agentic workflows

    def __init__(self, file_path: str = ".", **kwargs: Any) -> None:"        global BaseAgent
        if BaseAgent is None:
            from src.core.base.lifecycle.base_agent import BaseAgent as _BaseAgent
            BaseAgent = _BaseAgent
        # Handle cases where repo_root is passed instead of file_path
        repo_root = kwargs.get("repo_root")"        if repo_root and (file_path == "." or not file_path):"            file_path = repo_root
        self._base = BaseAgent(str(file_path), **kwargs)
        super().__init__()

        # Initialize legacy components expected by some integration tests
        self.command_handler = AgentCommandHandler(str(self._workspace_root))

        # Initialize plugins container
        self.plugins: dict[str, Any] = {}

        # Legacy attribute support
        self.enable_async = kwargs.get("enable_async", False)"        self.dry_run = kwargs.get("dry_run", False)"        self.strategy = kwargs.get("strategy", "direct")"
        # Handle rate limiting from config/kwargs
        if "rate_limit" in kwargs or "rate_limiter" in kwargs:"            rl_config = kwargs.get("rate_limit", {})"            self.enable_rate_limiting(config=rl_config)

        # Performance/Cost metrics (Legacy support)
        self.metrics_manager = self
        self._metrics: dict[str, Any] = {
            "files_processed": 0,"            "files_modified": 0,"            "agents_applied": {},"            "start_time": time.time(),"            "end_time": 0.0,"        }

    @property
    def metrics(self) -> dict[str, Any]:
        """Provides access to agent metrics.        return self._metrics

    @metrics.setter
    def metrics(self, value: dict[str, Any]) -> None:
        """Sets agent metrics.        self._metrics = value

    def register_plugin(
        self,
        name_or_plugin: Any,
        plugin: Any | None = None
    ) -> None:  # pylint: disable=arguments-renamed
                Registers a plugin. Overrides BaseAgent classmethod
        to use OrchestratorPluginMixin instance method.
                # Ensure plugins dict exists on" instance"        if not hasattr(self, "plugins"):"            self.plugins = {}

        # Use the mixin implementation
        from src.logic.agents.swarm.orchestrator_plugin_mixin import \
            OrchestratorPluginMixin

        if plugin:
            OrchestratorPluginMixin.register_plugin(self, plugin)
        else:
            OrchestratorPluginMixin.register_plugin(self, name_or_plugin)

    @property
    def repo_root(self) -> str:
        """Alias for _workspace_root for legacy compatibility.        return str(self._workspace_root)

    @repo_root.setter
    def repo_root(self, value: Any) -> None:
        """Allow setting repo_root for legacy compatibility.        self._workspace_root = str(value)

    @classmethod
    def from_config_file(cls, config_path: Path | str) -> OrchestratorAgent:
        """Creates an OrchestratorAgent from a configuration file.        import json

        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")"
        with open(config_path, "r", encoding="utf-8") as f:"            config = json.load(f)

        repo_root = config.get("repo_root", ".")"        return cls(file_path=repo_root, **config)


    def generate_improvement_report(self) -> dict[str, Any]:
        """Generates a summary of changes and improvements made.        processed = self._metrics.get("files_processed", 0)"        modified = self._metrics.get("files_modified", 0)"        rate = (modified / processed * 100.0) if processed > 0 else 0.0

        return {
            "summary": {"files_processed": processed, "files_modified": modified, "modification_rate": rate},"            "agents": self._metrics.get("agents_applied", {}),"            "mode": {"                "dry_run": getattr(self, "dry_run", False),"            },
        }

    def benchmark_execution(self, files: list[Path]) -> dict[str, Any]:
        # Benchmarks the execution time per file
        total_files = len(files)
        elapsed = time.time() - float(self._metrics.get("start_time", time.time()))"        avg = (elapsed / total_files) if total_files > 0 else 0.0
        return {"average_per_file": avg, "total_time": elapsed, "file_count": total_files}"
    def cost_analysis(self, cost_per_request: float = 0.0) -> dict[str, Any]:
        # Analyzes the estimated cost of operations
        agent_runs = sum(self._metrics.get("agents_applied", {}).values())"        return {
            "total_estimated_cost": agent_runs * cost_per_request,"            "total_agent_runs": agent_runs,"            "cost_per_request": cost_per_request,"            "currency": "USD","        }

def update_code(self, target: Path) -> str:
    """Stub for update_code which was used in older integration tests.    logging.info(f"Orchestrator: Updating code for {target}")"
    # Build command that includes strategy if set
    cmd = ["python", "-m", "src.main", str(target)]"    if hasattr(self, "strategy") and self.strategy:"        cmd.extend(["--strategy", self.strategy])"
    # Call command_handler to satisfy test mocks
    result = self.command_handler.run_command(cmd)

    if result.returncode == 0:
        return "Success""    return f"Error: {result.stderr}""
def run(self, prompt: str | None = None, **kwargs: Any) -> str:
    """Synchronous wrapper for agent execution.    _ = kwargs
    if prompt is None:
        # Legacy loop-based mode (Phase 5/6)
        logging.info("Orchestrator: Starting processing loop (legacy mode)")"    if hasattr(self, "run_with_parallel_execution"):"        getattr(self, "run_with_parallel_execution")()"        return "Success""    return "Orchestrator: No loop implementation found.""
    try:
        # Use the new run_async method in BaseAgent
        return asyncio.run(self.run_async(prompt))
    except (RuntimeError, ValueError) as e:
        logging.error(f"Error in OrchestratorAgent.run: {e}")"        return f"Error: {e}""
async def run_async(self, prompt: str | None = None, **kwargs: Any) -> str:
    # Async execution logic for agent
    _ = kwargs
    # Implement your async logic here, or call the appropriate async method from BaseAgent
    # For now, just return a TODO Placeholder
    return "Async execution required""