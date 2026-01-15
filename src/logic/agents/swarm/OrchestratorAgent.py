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

"""
OrchestratorAgent for PyAgent Swarm Management.

This agent acts as the primary coordinator for sub-swarms, managing task delegation,
resource allocation, and final response synthesis. It implements advanced
self-healing and multi-agent synergy protocols.
"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.ConfigLoader import ConfigLoader
from pathlib import Path
from types import TracebackType
from typing import Any
from collections.abc import Callable
import logging
from src.core.base.managers.AgentMetrics import AgentMetrics
from src.core.base.utils.AgentFileManager import AgentFileManager
from src.core.base.utils.AgentGitHandler import AgentGitHandler
from src.core.base.AgentCommandHandler import AgentCommandHandler
from src.logic.agents.swarm.core.OrchestratorCore import OrchestratorCore
from src.core.base.utils.ParallelProcessor import ParallelProcessor
from src.core.base.utils.NotificationManager import NotificationManager
from src.core.base.AgentUpdateManager import AgentUpdateManager
from src.core.base.interfaces import ContextRecorderInterface
from src.core.base.ConnectivityManager import ConnectivityManager
from src.core.base.AgentCore import BaseCore
from src.logic.agents.swarm.OrchestratorFeatures import OrchestratorFeatures
from src.logic.agents.swarm.OrchestratorDelegates import OrchestratorDelegates

__version__ = VERSION




class OrchestratorAgent(OrchestratorFeatures, OrchestratorDelegates):
    """Main agent that orchestrates sub-agents for code improvement.

    This class has been refactored to delegate logic to specialized managers
    and mixins to maintain a small file size (<30KB).
    """
    SUPPORTED_EXTENSIONS = {'.py', '.sh', '.js', '.ts', '.go', '.rb'}

    def __init__(self,
                 repo_root: str = '.',
                 agents_only: bool = False,
                 max_files: int | None = None,
                 loop: int = 1,
                 skip_code_update: bool = False,
                 no_git: bool = False,
                 dry_run: bool = False,
                 selective_agents: list[str] | None = None,
                 timeout_per_agent: dict[str, int] | None = None,
                 enable_async: bool = False,
                 enable_multiprocessing: bool = False,
                 max_workers: int = 4,
                 strategy: str = 'direct',
                 models_config: dict[str, Any] | None = None) -> None:
        """Initialize the Agent with repository configuration."""
        logging.info(f"Initializing Agent with repo_root={repo_root}")
        provided_path = Path(repo_root)

        # Temp core for initial workspace detection
        temp_core = BaseCore()

        if str(repo_root) and str(repo_root) != '.':
            self.repo_root = provided_path.resolve()
        else:
            self.repo_root = Path(temp_core.detect_workspace_root(provided_path))

        if not self.repo_root.exists():
            raise FileNotFoundError(f"Repository root not found: {self.repo_root}")

        self.agents_only = agents_only
        self.max_files = max_files
        self.loop = loop
        self.skip_code_update = skip_code_update
        self.no_git = no_git
        self.dry_run = dry_run
        self.selective_agents = set(selective_agents or [])
        self.timeout_per_agent = timeout_per_agent or {}
        self.enable_async = enable_async
        self.enable_multiprocessing = enable_multiprocessing
        self.max_workers = max_workers
        self._strategy = strategy
        self.models = models_config or {}

        # Intelligence & Resilience Layer (Phase 108)
        # Infrastructure bridge (Phase 130: evaluated moving to abstract providers)
        from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder
        self.recorder: ContextRecorderInterface = LocalContextRecorder(workspace_root=self.repo_root)
        self.connectivity = ConnectivityManager()

        # Delegated Managers
        self.core = OrchestratorCore(workspace_root=str(self.repo_root))
        # Alias for backward compatibility/base access
        self.base_core = self.core

        self.metrics_manager = AgentMetrics()
        self.git_handler = AgentGitHandler(self.repo_root, no_git, recorder=self.recorder)
        self.file_manager = AgentFileManager(self.repo_root, agents_only)
        self.command_handler = AgentCommandHandler(self.repo_root, self.models, recorder=self.recorder)
        self.update_manager = AgentUpdateManager(
            self.repo_root, self.models, self._strategy,
            self.command_handler, self.file_manager, self.core
        )
        self.parallel_processor = ParallelProcessor(max_workers=max_workers)
        self.notifications = NotificationManager(workspace_root=str(self.repo_root))

        # Compatibility layers
        self.ignored_patterns = self.file_manager.ignored_patterns

        logging.info(
            f"Agent initialized: repo={self.repo_root}, "
            f"agents_only={agents_only}"
        )
        if dry_run:
            logging.info("DRY RUN MODE: No files will be modified")
        if selective_agents:
            logging.info(f"Selective execution: agents={selective_agents}")

    @property
    def metrics(self) -> dict[str, Any]:
        """Provides backward compatibility for the metrics attribute (flattened)."""
        d = self.metrics_manager.to_dict()
        summary = d.pop('summary', {})
        d.update(summary)
        return d

    @metrics.setter
    def metrics(self, value: dict[str, Any]) -> None:
        """Allow manual override of metrics (legacy support)."""
        if 'files_processed' in value:
            self.metrics_manager.files_processed = value['files_processed']
        if 'files_modified' in value:
            self.metrics_manager.files_modified = value['files_modified']
        if 'agents_applied' in value:
            self.metrics_manager.agents_applied = value['agents_applied']
        if 'start_time' in value:
            self.metrics_manager.start_time = value['start_time']
        if 'end_time' in value:
            self.metrics_manager.end_time = value['end_time']

    @property
    def webhooks(self) -> list[str]:
        """Backward compatibility for webhooks list."""
        return self.notifications.webhooks

    @property
    def callbacks(self) -> list[Callable]:
        """Backward compatibility for callbacks list."""
        return self.notifications.callbacks

    def process_files_multiprocessing(self, files: list[Path]) -> None:
        """Compatibility wrapper for multiprocessing file processing."""
        # Simple implementation for now as it's primarily used for testing presence
        # and basic functionality in this version's unit tests.
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            list(executor.map(self.process_file, files))

    @property
    def strategy(self) -> str:
        """Returns the current execution strategy."""
        return self._strategy

    @strategy.setter
    def strategy(self, value: str) -> None:
        """Sets the execution strategy and propagates to managers."""
        self._strategy = value
        if hasattr(self, 'update_manager'):
            self.update_manager.strategy = value
        if hasattr(self, 'command_handler'):
            self.command_handler.strategy = value

    def __enter__(self) -> OrchestratorAgent:
        """Context manager entry. Returns self for use in 'with' statement."""
        logging.debug("OrchestratorAgent entering context manager")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        """Context manager exit. Handles cleanup if needed."""
        logging.debug("Agent exiting context manager")
        if exc_type is not None:
            logging.error(f"Agent context manager error: {exc_type.__name__}: {exc_val}")
        return False  # Don't suppress exceptions

    def should_execute_agent(self, agent_name: str) -> bool:
        """Check if an agent should be executed based on selective filters.

        Delegates to OrchestratorCore.
        """
        return self.core.should_execute_agent(agent_name, self.selective_agents)

    def get_timeout_for_agent(self, agent_name: str, default: int = 120) -> int:
        """Get configured timeout for a specific agent.

        Delegates to OrchestratorCore.
        """
        return self.core.get_timeout_for_agent(agent_name, self.timeout_per_agent, default)

    def print_metrics_summary(self) -> None:
        """Print a summary of execution metrics.

        Delegates to AgentMetrics.
        """
        summary = self.metrics_manager.get_summary(self.dry_run)
        logging.info(summary)

    def generate_improvement_report(self) -> dict[str, Any]:
        """Generate comprehensive improvement report.

        Delegates to AgentMetrics.
        """
        report = self.metrics_manager.to_dict()
        report['mode'] = {
            'dry_run': self.dry_run,
            'async_enabled': self.enable_async,
            'multiprocessing_enabled': self.enable_multiprocessing,
        }
        report['agents'] = report.get('agents_applied', {})

        files_proc = report['summary'].get('files_processed', 0)
        files_mod = report['summary'].get('files_modified', 0)
        report['summary']['modification_rate'] = self.core.calculate_improvement_score(files_proc, files_mod)

        logging.info(f"Generated improvement report: {files_proc} files processed, {files_mod} modified")
        return report

    def benchmark_execution(self, files: list[Path]) -> dict[str, Any]:
        """Benchmark execution time per file and per agent.

        Delegates to AgentMetrics.
        """
        return self.metrics_manager.benchmark_execution(files)

    def cost_analysis(self, backend: str = 'github-models',
                      cost_per_request: float = 0.0001) -> dict[str, Any]:
        """Analyze API usage cost for the agent execution.

        Delegates to AgentMetrics.
        """
        return self.metrics_manager.cost_analysis(backend, cost_per_request)

    def cleanup_old_snapshots(self, max_age_days: int = 7,
                              max_snapshots_per_file: int = 10) -> int:
        """Clean up old file snapshots.

        Delegates to AgentFileManager.
        """
        return self.file_manager.cleanup_old_snapshots(max_age_days, max_snapshots_per_file)

    def validate_with_consensus(self, task: str, proposals: dict[str, str]) -> dict[str, Any]:
        """
        Validates proposals using the ByzantineConsensusAgent.
        Delegates to OrchestratorCore.
        """
        log_path = self.repo_root / "data" / "logs" / "consensus.log"
        return self.core.validate_with_consensus(task, proposals, log_path)

    # =========================================================================
    # Configuration File Methods
    # =========================================================================

    @classmethod
    def from_config_file(cls, config_path: Path) -> OrchestratorAgent:
        """Create an Agent instance from a configuration file."""
        loader = ConfigLoader(config_path)
        config = loader.load()

        agent = cls(
            repo_root=config.repo_root,
            agents_only=config.agents_only,
            max_files=config.max_files,
            loop=config.loop,
            dry_run=config.dry_run,
            no_git=config.no_git,
            selective_agents=config.selective_agents or None,
            timeout_per_agent=config.timeout_per_agent or None,
            enable_async=config.enable_async,
            enable_multiprocessing=config.enable_multiprocessing,
            max_workers=config.max_workers,
            strategy=config.strategy
        )

        if config.rate_limit:
            agent.enable_rate_limiting(config.rate_limit)
        if config.enable_file_locking:
            agent.enable_file_locking()
        if config.incremental:
            agent.enable_incremental_processing()
        if config.webhook:
            for url in config.webhook:
                agent.register_webhook(url)

        agent.models = config.models or {}
        if config.plugins:
            agent.load_plugins_from_config(config.plugins)

        return agent

    @classmethod
    def auto_configure(cls, repo_root: str = ".") -> OrchestratorAgent:
        """Auto-configure agent from config file if found."""
        root = Path(repo_root).resolve()
        config_path = ConfigLoader.find_config_file(root)

        if config_path:
            return cls.from_config_file(config_path)
        else:
            return cls(repo_root=repo_root)

    def run(self) -> None:
        """Run the main agent loop.

        Executes the main agent loop, processing all code files found.
        Uses parallel execution if enabled, otherwise sequential processing.
        Triggers webhooks and callbacks on completion.
        """
        super().run()
