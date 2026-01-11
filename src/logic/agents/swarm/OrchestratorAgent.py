#!/usr/bin/env python3

"""
OrchestratorAgent for PyAgent Swarm Management.

This agent acts as the primary coordinator for sub-swarms, managing task delegation,
resource allocation, and final response synthesis. It implements advanced 
self-healing and multi-agent synergy protocols.
"""

from __future__ import annotations

from src.core.base.AgentPluginBase import AgentPluginBase
from src.core.base.ConfigLoader import ConfigLoader
from src.core.base.utils.DiffGenerator import DiffGenerator
from src.core.base.models import (
    AgentHealthCheck,
    AgentPluginConfig,
    DiffOutputFormat,
    DiffResult,
    HealthStatus,
    RateLimitConfig
)
from src.core.base.utils.FileLockManager import FileLockManager
from src.core.base.GracefulShutdown import GracefulShutdown
from src.core.base.managers import HealthChecker
from src.core.base.models import HealthStatus
from src.core.base.IncrementalProcessor import IncrementalProcessor
from src.core.base.models import RateLimitConfig
from src.core.base.utils.RateLimiter import RateLimiter
from src.core.base.utils.core_utils import fix_markdown_content
from src.core.base.utils._helpers import HAS_REQUESTS, requests

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable
import asyncio
import functools
import importlib.util
import logging
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from src.core.base.managers.AgentMetrics import AgentMetrics
from src.core.base.utils.AgentFileManager import AgentFileManager
from src.core.base.utils.AgentGitHandler import AgentGitHandler
from src.core.base.AgentCommandHandler import AgentCommandHandler
from src.core.base.AgentCore import AgentCore
from src.core.base.utils.ParallelProcessor import ParallelProcessor
from src.core.base.utils.NotificationManager import NotificationManager
from src.core.base.AgentUpdateManager import AgentUpdateManager
from src.core.base.interfaces import ContextRecorderInterface
from src.core.base.ConnectivityManager import ConnectivityManager
from src.core.base.core import BaseCore

class OrchestratorAgent:
    """Main agent that orchestrates sub-agents for code improvement.
    
    This class has been refactored to delegate logic to specialized managers:
    - metrics_manager: Handles tracking and reporting of execution metrics
    - file_manager: Handles file discovery, snapshots, and ignore patterns
    - git_handler: Handles git operations (commit, branch)
    - command_handler: Handles subprocess execution and sub-agent orchestration
    - core: Pure logic and parsing (Rust-ready component)
    """
    SUPPORTED_EXTENSIONS = {'.py', '.sh', '.js', '.ts', '.go', '.rb'}

    def __init__(self,
                 repo_root: str = '.',
                 agents_only: bool = False,
                 max_files: Optional[int] = None,
                 loop: int = 1,
                 skip_code_update: bool = False,
                 no_git: bool = False,
                 dry_run: bool = False,
                 selective_agents: Optional[List[str]] = None,
                 timeout_per_agent: Optional[Dict[str,
                                                  int]] = None,
                 enable_async: bool = False,
                 enable_multiprocessing: bool = False,
                 max_workers: int = 4,
                 strategy: str = 'direct',
                 models_config: Optional[Dict[str, Any]] = None) -> None:
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
        self.core = AgentCore(workspace_root=str(self.repo_root))
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
    def metrics(self) -> Dict[str, Any]:
        """Provides backward compatibility for the metrics attribute (flattened)."""
        d = self.metrics_manager.to_dict()
        summary = d.pop('summary', {})
        d.update(summary)
        return d

    @metrics.setter
    def metrics(self, value: Dict[str, Any]) -> None:
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
    def webhooks(self) -> List[str]:
        """Backward compatibility for webhooks list."""
        return self.notifications.webhooks

    @property
    def callbacks(self) -> List[Callable]:
        """Backward compatibility for callbacks list."""
        return self.notifications.callbacks

    def process_files_multiprocessing(self, files: List[Path]) -> None:
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

    def __enter__(self) -> "OrchestratorAgent":
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

        Determines whether to run a specific agent based on the selective_agents
        configuration provided at initialization.

        Args:
            agent_name: Name of the agent (e.g., 'coder', 'tests', 'documentation').

        Returns:
            bool: True if the agent should execute, False otherwise.

        Example:
            if agent.should_execute_agent('coder'):
                coder_agent.run()
        """
        if not self.selective_agents:
            return True  # All agents run if no selective filter
        return agent_name.lower() in self.selective_agents

    def get_timeout_for_agent(self, agent_name: str, default: int = 120) -> int:
        """Get configured timeout for a specific agent.

        Returns the timeout value for a specific agent, or a default if not configured.

        Args:
            agent_name: Name of the agent (e.g., 'coder', 'tests').
            default: Default timeout in seconds if not configured. Defaults to 120.

        Returns:
            int: Timeout in seconds for the agent.

        Example:
            timeout=agent.get_timeout_for_agent('coder', default=60)
        """
        return self.timeout_per_agent.get(agent_name.lower(), default)

    def print_metrics_summary(self) -> None:
        """Print a summary of execution metrics.
        
        Delegates to AgentMetrics.
        """
        summary = self.metrics_manager.get_summary(self.dry_run)
        logging.info(summary)
        print(summary)

    def generate_improvement_report(self) -> Dict[str, Any]:
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
        report['summary']['modification_rate'] = (
            files_mod / files_proc * 100) if files_proc > 0 else 0

        logging.info(f"Generated improvement report: {files_proc} files processed, {files_mod} modified")
        return report

    def benchmark_execution(self, files: List[Path]) -> Dict[str, Any]:
        """Benchmark execution time per file and per agent.
        
        Delegates to AgentMetrics.
        """
        return self.metrics_manager.benchmark_execution(files)

    def cost_analysis(self, backend: str = 'github-models',
                      cost_per_request: float = 0.0001) -> Dict[str, Any]:
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

    def create_file_snapshot(self, file_path: Path) -> Optional[str]:
        """Create a snapshot of file content before modifications.
        
        Delegates to AgentFileManager.
        """
        return self.file_manager.create_file_snapshot(file_path)

    def restore_from_snapshot(self, file_path: Path, snapshot_id: str) -> bool:
        """Restore a file from a previously created snapshot.
        
        Delegates to AgentFileManager.
        """
        return self.file_manager.restore_from_snapshot(file_path, snapshot_id)

    def load_cascading_codeignore(self, directory: Optional[Path] = None) -> Set[str]:
        """Load .codeignore patterns with cascading support.
        
        Delegates to AgentFileManager.
        """
        return self.file_manager.load_cascading_codeignore(directory)

    def _run_command(self, cmd: List[str], timeout: int = 120,
                     max_retries: int = 1) -> subprocess.CompletedProcess[str]:
        """Run a command with timeout, error handling, retry logic, and logging.
        
        Delegates to AgentCommandHandler.
        """
        return self.command_handler.run_command(cmd, timeout, max_retries)

    @contextmanager
    def _with_agent_env(self, agent_name: str) -> bool:
        """Temporarily set environment variables for a specific agent.
        
        Delegates to AgentCommandHandler.
        """
        with self.command_handler.with_agent_env(agent_name):
            yield

    def find_code_files(self) -> List[Path]:
        """Recursively find all supported code files in the repository.
        
        Delegates to AgentFileManager for file discovery and filtering.
        """
        logging.info("Searching for code files (delegated to AgentFileManager)...")
        code_files = self.file_manager.find_code_files(max_files=self.max_files)
        
        # Sort for consistency
        code_files = sorted(code_files)
        logging.info(f"Found {len(code_files)} code files.")
        return code_files

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored.
        
        Delegates to AgentFileManager.
        """
        return self.file_manager.is_ignored(path)

    def run_stats_update(self, files: List[Path]) -> None:
        """Run stats update."""
        file_paths = [str(f) for f in files]
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / 'agent_stats.py'),
            '--files'] + file_paths
        self._run_command(cmd)

    def run_tests(self, code_file: Path) -> None:
        """Run tests for the code file."""
        # Look for test_{filename}.py (pytest convention)
        test_name = f"test_{code_file.stem}.py"
        tests_file = code_file.parent / test_name
        if tests_file.exists():
            logging.info(f"Running tests for {code_file.name}...")
            cmd = [sys.executable, '-m', 'pytest', str(tests_file), '-v']
            result = self._run_command(cmd)
            if result.returncode != 0:
                logging.warning(f"Tests failed for {code_file.name}:")
                logging.warning(result.stdout)
                logging.warning(result.stderr)
            else:
                logging.info(f"Tests passed for {code_file.name}")
        else:
            logging.debug(f"No tests file found for {code_file.name}")

    def update_errors_improvements(self, code_file: Path) -> bool:
        """Update errors and improvements.
        
        Delegates to AgentUpdateManager.
        """
        return self.update_manager.update_errors_improvements(code_file)

    def update_code(self, code_file: Path) -> bool:
        """Update the code file.
        
        Delegates to AgentUpdateManager.
        """
        return self.update_manager.update_code(code_file)

    def update_changelog_context_tests(self, code_file: Path) -> bool:
        """Update changelog, context, and tests.
        
        Delegates to AgentUpdateManager.
        """
        return self.update_manager.update_changelog_context_tests(code_file)

    def _check_files_ready(self, code_file: Path) -> bool:
        """Check if all supporting files exist and have content."""
        base = code_file.stem
        dir_path = code_file.parent
        context_file = dir_path / f"{base}.description.md"
        changes_file = dir_path / f"{base}.changes.md"
        errors_file = dir_path / f"{base}.errors.md"
        improvements_file = dir_path / f"{base}.improvements.md"
        return (
            context_file.exists() and
            len(context_file.read_text(encoding='utf-8').strip()) > 100 and
            changes_file.exists() and
            len(changes_file.read_text(encoding='utf-8').strip()) > 100 and
            errors_file.exists() and
            len(errors_file.read_text(encoding='utf-8').strip()) > 100 and
            improvements_file.exists() and
            len(improvements_file.read_text(encoding='utf-8').strip()) > 100
        )

    def _perform_iteration(self, code_file: Path) -> bool:
        """Perform one iteration of improvements on the code file."""
        changes_made = False
        # Note: stats update should be done once per loop iteration, not per-file.
        # The call to `run_stats_update` was previously here which caused the
        # stats agent to be invoked for every file in the loop. We intentionally
        # avoid calling it here to prevent repeated counting; stats are updated
        # once per loop in `run_with_parallel_execution`.
        # Run the Tests on the Codefile
        if not self.skip_code_update:
            self.run_tests(code_file)
        # Update Errors, Improvements
        changes_made |= self.update_errors_improvements(code_file)
        # Update Code
        if not self.skip_code_update:
            changes_made |= self.update_code(code_file)
        # Update Changelog, Context, Tests
        changes_made |= self.update_changelog_context_tests(code_file)
        return changes_made

    def _commit_and_push(self, code_file: Path) -> None:
        """Commit and push changes for the code file."""
        if self.no_git:
            logging.info(f"Skipping git operations for {code_file.name} (--no-git)")
            return

        logging.info(f"Committing changes for {code_file.name}")
        try:
            # git add -A
            self._run_command(['git', 'add', '-A'])
            # git commit
            commit_msg = f"Agent improvements for {code_file.name}"
            result = self._run_command(['git', 'commit', '-m', commit_msg])
            if result.returncode == 0:
                logging.info(f"Committed changes for {code_file.name}")
                # git push
                push_result = self._run_command(['git', 'push'])
                if push_result.returncode == 0:
                    logging.info(f"Pushed changes for {code_file.name}")
                else:
                    logging.error(f"Failed to push changes: {push_result.stderr}")
            else:
                logging.info(f"No changes to commit for {code_file.name}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Git operation failed for {code_file.name}: {e}")
        except FileNotFoundError:
            logging.error(f"Git not available for {code_file.name}")

    def register_webhook(self, webhook_url: str) -> None:
        """Register a webhook URL for event notifications."""
        self.notifications.register_webhook(webhook_url)

    def register_callback(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """Register a callback function for agent events."""
        self.notifications.register_callback(callback)

    def send_webhook_notification(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Send notification to all registered webhooks."""
        self.notifications.notify(event_name, event_data)

    def execute_callbacks(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Execute all registered callback functions for an event."""
        self.notifications.notify(event_name, event_data)

    async def async_process_files(self, files: List[Path]) -> List[Path]:
        """Process multiple files concurrently using async / await."""
        return await self.parallel_processor.async_process_files(files, self.process_file)

    def process_files_threaded(self, files: List[Path]) -> List[Path]:
        """Process multiple files using threading for concurrent I / O."""
        return self.parallel_processor.process_files_threaded(files, self.process_file)

    def run_with_parallel_execution(self) -> None:
        """Run the main agent loop with parallel execution strategy.

        Runs the agent with either async, multiprocessing, or threaded execution
        based on configuration. Falls back to sequential if neither enabled.

        Returns:
            None. Results logged and metrics updated.

        Note:
            - Priority: multiprocessing > async > threaded > sequential
            - Webhooks and callbacks triggered on completion
            - Metrics summary printed at end
        """
        code_files = self.find_code_files()
        logging.info(f"Found {len(code_files)} code files to process")

        for loop_iteration in range(1, self.loop + 1):
            logging.info(f"Starting loop iteration {loop_iteration}/{self.loop}")

            # Choose execution strategy
            if self.enable_multiprocessing:
                logging.info("Using multiprocessing for parallel execution")
                self.process_files_multiprocessing(code_files)
            elif self.enable_async:
                logging.info("Using async for concurrent execution")
                asyncio.run(self.async_process_files(code_files))
            else:
                logging.info("Using threaded execution")
                self.process_files_threaded(code_files)

            logging.info(f"Completed loop iteration {loop_iteration}/{self.loop}")

        # Trigger completion events
        self.execute_callbacks('agent_complete', self.metrics)
        self.send_webhook_notification('agent_complete', self.metrics)

        # Final stats update
        logging.info("Final stats:")
        self.run_stats_update(code_files)

    def process_file(self, code_file: Path) -> None:
        """Process a single code file through the improvement loop."""
        # Check graceful shutdown
        if hasattr(self, 'shutdown_handler') and not self.shutdown_handler.should_continue():
            logging.info(f"Skipping {code_file.name} due to shutdown request")
            return

        # Acquire file lock if enabled
        if hasattr(self, 'lock_manager'):
            lock = self.lock_manager.acquire_lock(code_file)
            if not lock:
                logging.warning(f"Could not acquire lock for {code_file.name}, skipping")
                return

        try:
            # Set current file for graceful shutdown
            if hasattr(self, 'shutdown_handler'):
                self.shutdown_handler.set_current_file(code_file)

            logging.info(f"Processing {code_file.relative_to(self.repo_root)}...")
            max_iterations = 1
            iteration = 0
            all_fixed = False
            while not all_fixed and iteration < max_iterations:
                iteration += 1
                logging.debug(f"Iteration {iteration} for {code_file.name}")
                files_ready = self._check_files_ready(code_file)
                
                try:
                    changes_made = self._perform_iteration(code_file)
                except Exception as e:
                    logging.error(f"Error in _perform_iteration for {code_file}: {e}")
                    # Record Debt to Relational Overlay (Self-Healing Bridge)
                    try:
                        sql = getattr(self.command_handler.models, "sql_metadata", None)
                        if sql:
                            sql.record_debt(
                                str(code_file.relative_to(self.repo_root)),
                                "Runtime Error",
                                f"Iteration failed: {str(e)}",
                                False
                            )
                    except Exception:
                        pass
                    changes_made = False # Stop loop on error
                
                # Check if all is marked as fixed (no more changes needed)
                if not changes_made:
                    all_fixed = True
                    logging.info(f"No changes made in iteration {iteration}, marking as fixed")
                else:
                    logging.info(f"Changes made in iteration {iteration}, continuing...")
            
            if iteration >= max_iterations:
                logging.info(f"Reached maximum iterations ({max_iterations}) for {code_file.name}")
            
            self._commit_and_push(code_file)

            # Mark as processed for incremental processing
            if hasattr(self, 'incremental_processor'):
                self.incremental_processor.mark_processed(code_file)

            # Mark completed for graceful shutdown
            if hasattr(self, 'shutdown_handler'):
                self.shutdown_handler.mark_completed(code_file)

        except Exception as global_e:
            logging.critical(f"Global failure processing {code_file}: {global_e}", exc_info=True)
        finally:
            # Release file lock
            if hasattr(self, 'lock_manager'):
                self.lock_manager.release_lock(code_file)

            # Clear current file
            if hasattr(self, 'shutdown_handler'):
                self.shutdown_handler.set_current_file(None)

    def validate_with_consensus(self, task: str, proposals: Dict[str, str]) -> Dict[str, Any]:
        """
        Validates proposals using the ByzantineConsensusAgent.
        This provides a Phase 129 quality gate for critical changes.
        """
        from src.logic.agents.security.ByzantineConsensusAgent import ByzantineConsensusAgent
        log_path = self.repo_root / "data" / "logs" / "consensus.log"
        consensus_agent = ByzantineConsensusAgent(str(log_path))
        return consensus_agent.run_committee_vote(task, proposals)

    # =========================================================================
    # Plugin System Methods
    # =========================================================================

    def register_plugin(self, plugin: AgentPluginBase) -> None:
        """Register a custom agent plugin.

        Allows third - party agents to be added without modifying core code.
        Plugins are called during file processing after built - in agents.

        Args:
            plugin: Plugin instance implementing AgentPluginBase.

        Example:
            class MyPlugin(AgentPluginBase):
                def run(self, file_path, context) -> bool:
                    # Custom processing
                    return True

            agent.register_plugin(MyPlugin("custom"))
        """
        if not hasattr(self, 'plugins'):
            self.plugins: Dict[str, AgentPluginBase] = {}

        plugin.setup()
        self.plugins[plugin.name] = plugin
        logging.info(f"Registered plugin: {plugin.name} (priority: {plugin.priority.name})")

    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin by name.

        Args:
            plugin_name: Name of plugin to remove.

        Returns:
            bool: True if plugin was removed, False if not found.
        """
        if not hasattr(self, 'plugins') or plugin_name not in self.plugins:
            return False

        plugin = self.plugins[plugin_name]
        plugin.teardown()
        del self.plugins[plugin_name]
        logging.info(f"Unregistered plugin: {plugin_name}")
        return True

    def get_plugin(self, plugin_name: str) -> Optional[AgentPluginBase]:
        """Get a registered plugin by name.

        Args:
            plugin_name: Name of plugin to retrieve.

        Returns:
            Plugin instance or None if not found.
        """
        if not hasattr(self, 'plugins'):
            return None
        return self.plugins.get(plugin_name)

    def run_plugins(self, file_path: Path) -> Dict[str, bool]:
        """Run all registered plugins on a file.

        Args:
            file_path: Path to file to process.

        Returns:
            Dict mapping plugin name to success status.
        """
        if not hasattr(self, 'plugins') or not self.plugins:
            return {}

        results: dict[str, bool] = {}
        context: dict[str, Any] = {
            'agent': self,
            'repo_root': self.repo_root,
            'dry_run': self.dry_run,
            'metrics': self.metrics
        }

        # Sort plugins by priority
        sorted_plugins = sorted(
            self.plugins.values(),
            key=lambda p: p.priority.value
        )

        for plugin in sorted_plugins:
            if not plugin.config.get('enabled', True):
                continue

            try:
                # Apply rate limiting if configured
                if hasattr(self, 'rate_limiter'):
                    self.rate_limiter.acquire(timeout=30.0)

                # Non-essential plugins must finish within 5 seconds (Phase 104)
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(plugin.run, file_path, context)
                    try:
                        result = future.result(timeout=5.0)
                    except TimeoutError:
                        logging.warning(f"Plugin {plugin.name} timed out after 5 seconds. Skipping.")
                        result = False

                results[plugin.name] = result

                if result:
                    self.metrics['agents_applied'][plugin.name] = \
                        self.metrics['agents_applied'].get(plugin.name, 0) + 1

            except Exception as e:
                logging.error(f"Plugin {plugin.name} failed: {e}")
                results[plugin.name] = False

        return results

    def load_plugins_from_config(self, plugin_configs: List[AgentPluginConfig]) -> None:
        """Load plugins from configuration.

        Args:
            plugin_configs: List of plugin configurations.
        """
        for config in plugin_configs:
            if not config.enabled:
                continue

            try:
                # Import plugin module
                spec = importlib.util.spec_from_file_location(
                    config.name, config.module_path
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Get entry point
                    plugin_class = getattr(module, config.entry_point, None)
                    if plugin_class and issubclass(plugin_class, AgentPluginBase):
                        plugin = plugin_class(
                            config.name,
                            config.priority,
                            config.config
                        )
                        self.register_plugin(plugin)
                    else:
                        logging.warning(f"Invalid plugin entry point: {config.entry_point}")
            except Exception as e:
                logging.error(f"Failed to load plugin {config.name}: {e}")

    # =========================================================================
    # Rate Limiting Methods
    # =========================================================================

    def enable_rate_limiting(self, config: Optional[RateLimitConfig] = None) -> None:
        """Enable rate limiting for API calls.

        Args:
            config: Rate limiting configuration. Uses defaults if not provided.

        Example:
            agent.enable_rate_limiting(RateLimitConfig(
                requests_per_second = 5.0,
                burst_size = 10
            ))
        """
        self.rate_limiter = RateLimiter(config)
        logging.info(f"Rate limiting enabled: {config or 'default settings'}")

    def get_rate_limit_stats(self) -> Dict[str, Any]:
        """Get current rate limiter statistics.

        Returns:
            Dict with rate limiter stats.
        """
        if hasattr(self, 'rate_limiter'):
            return self.rate_limiter.get_stats()
        return {}

    # =========================================================================
    # File Locking Methods
    # =========================================================================

    def enable_file_locking(self, lock_timeout: float = 300.0) -> None:
        """Enable file locking for concurrent modification prevention.

        Args:
            lock_timeout: Default lock timeout in seconds.

        Example:
            agent.enable_file_locking(lock_timeout=600.0)
        """
        self.lock_manager = FileLockManager(lock_timeout)
        logging.info(f"File locking enabled (timeout: {lock_timeout}s)")

    # =========================================================================
    # Diff Preview Methods
    # =========================================================================

    def enable_diff_preview(
            self,
            output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED) -> None:
        """Enable diff preview mode.

        Args:
            output_format: Output format for diffs.

        Example:
            agent.enable_diff_preview(DiffOutputFormat.HTML)
        """
        self.diff_generator = DiffGenerator(output_format)
        logging.info(f"Diff preview enabled (format: {output_format.name})")

    def preview_changes(self, file_path: Path, new_content: str) -> DiffResult:
        """Preview changes to a file without applying them.

        Args:
            file_path: Path to the file.
            new_content: Proposed new content.

        Returns:
            DiffResult with change information.
        """
        if not hasattr(self, 'diff_generator'):
            self.diff_generator = DiffGenerator()

        original = file_path.read_text() if file_path.exists() else ""
        return self.diff_generator.generate_diff(file_path, original, new_content)

    def show_pending_diffs(self) -> None:
        """Show all pending diffs for dry-run mode."""
        if not hasattr(self, 'pending_diffs'):
            self.pending_diffs: List[DiffResult] = []

        if not self.pending_diffs:
            print("No pending changes.")
            return

        print(f"\n=== Pending Changes ({len(self.pending_diffs)} files) ===\n")
        for diff in self.pending_diffs:
            print(f"--- {diff.file_path} ---")
            print(f"  +{diff.additions} -{diff.deletions}")
            if hasattr(self, 'diff_generator'):
                self.diff_generator.print_diff(diff)
            print()

    # =========================================================================
    # Incremental Processing Methods
    # =========================================================================

    def enable_incremental_processing(self) -> None:
        """Enable incremental processing (only changed files).

        Tracks file modification times and hashes to skip unchanged files.
        State is persisted to disk for resume across runs.

        Example:
            agent.enable_incremental_processing()
            files=agent.find_code_files()  # All files
            changed=agent.get_changed_files(files)  # Only changed
        """
        self.incremental_processor = IncrementalProcessor(self.repo_root)
        logging.info("Incremental processing enabled")

    def get_changed_files(self, files: List[Path]) -> List[Path]:
        """Get files that changed since last run.

        Args:
            files: List of all files to check.

        Returns:
            List of files that have changed.
        """
        if hasattr(self, 'incremental_processor'):
            return self.incremental_processor.get_changed_files(files)
        return files

    def reset_incremental_state(self) -> None:
        """Reset incremental processing state (force full reprocessing)."""
        if hasattr(self, 'incremental_processor'):
            self.incremental_processor.reset_state()

    # =========================================================================
    # Graceful Shutdown Methods
    # =========================================================================

    def enable_graceful_shutdown(self) -> None:
        """Enable graceful shutdown with state persistence.

        Installs signal handlers to allow current operation to complete
        and saves state for resume.

        Example:
            agent.enable_graceful_shutdown()
            agent.run()  # Can be interrupted with Ctrl + C
        """
        self.shutdown_handler = GracefulShutdown(self.repo_root)
        self.shutdown_handler.install_handlers()
        logging.info("Graceful shutdown enabled")

    def resume_from_shutdown(self) -> Optional[List[Path]]:
        """Resume processing from interrupted state.

        Returns:
            List of pending files to process, or None if no resume state.
        """
        if not hasattr(self, 'shutdown_handler'):
            self.shutdown_handler = GracefulShutdown(self.repo_root)

        state = self.shutdown_handler.load_resume_state()
        if state and state.pending_files:
            return [Path(f) for f in state.pending_files]
        return None

    # =========================================================================
    # Health Check Methods
    # =========================================================================

    def run_health_checks(self) -> Dict[str, AgentHealthCheck]:
        """Run health checks on all agent components.

        Returns:
            Dict of component name to health check result.

        Example:
            results=agent.run_health_checks()
            if all(r.status == HealthStatus.HEALTHY for r in results.values()):
                agent.run()
        """
        checker = HealthChecker(self.repo_root)
        return checker.run_all_checks()

    def is_healthy(self) -> bool:
        """Check if all components are healthy.

        Returns:
            bool: True if all healthy, False otherwise.
        """
        results = self.run_health_checks()
        return all(r.status == HealthStatus.HEALTHY for r in results.values())

    def print_health_report(self) -> None:
        """Print a health check report."""
        checker = HealthChecker(self.repo_root)
        checker.run_all_checks()
        checker.print_report()

    # =========================================================================
    # Configuration File Methods
    # =========================================================================

    @classmethod
    def from_config_file(cls, config_path: Path) -> "Agent":
        """Create an Agent instance from a configuration file.

        Args:
            config_path: Path to YAML / TOML / JSON config file.

        Returns:
            Configured Agent instance.

        Example:
            agent=Agent.from_config_file(Path("agent.yaml"))
            agent.run()
        """
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

        # Apply rate limiting if configured
        if config.rate_limit:
            agent.enable_rate_limiting(config.rate_limit)

        # Apply file locking if requested
        if config.enable_file_locking:
            agent.enable_file_locking()

        # Enable incremental processing if requested
        if config.incremental:
            agent.enable_incremental_processing()

        # Register webhooks
        if config.webhook:
            for url in config.webhook:
                agent.register_webhook(url)

        # Attach per-agent models mapping
        agent.models = config.models or {}

        # Load plugins if configured
        if config.plugins:
            agent.load_plugins_from_config(config.plugins)

        return agent

    @classmethod
    def auto_configure(cls, repo_root: str = ".") -> "Agent":
        """Auto-configure agent from config file if found.

        Args:
            repo_root: Repository root directory.

        Returns:
            Configured Agent instance.

        Example:
            agent=Agent.auto_configure()  # Looks for agent.yaml etc.
            agent.run()
        """
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
        print("Entering agent.run()", file=sys.stderr)
        if self.enable_async or self.enable_multiprocessing:
            self.run_with_parallel_execution()
        else:
            # Sequential execution (original behavior)
            code_files = self.find_code_files()
            print(f"Found {len(code_files)} code files to process", file=sys.stderr)
            logging.info(f"Found {len(code_files)} code files to process")
            for loop_iteration in range(1, self.loop + 1):
                logging.info(f"Starting loop iteration {loop_iteration}/{self.loop}")
                for code_file in code_files:
                    self.process_file(code_file)
                logging.info(f"Completed loop iteration {loop_iteration}/{self.loop}")
            # Final stats update
            logging.info("Final stats:")
            self.run_stats_update(code_files)

            # Trigger completion events
            self.execute_callbacks('agent_complete', self.metrics)
            self.send_webhook_notification('agent_complete', self.metrics)

