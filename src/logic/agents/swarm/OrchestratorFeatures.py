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

"""
OrchestratorFeatures: Mixin class for OrchestratorAgent features.
"""

from __future__ import annotations
import logging
import importlib.util
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Any
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from contextlib import contextmanager
from src.observability.StructuredLogger import StructuredLogger
from src.core.base.AgentPluginBase import AgentPluginBase
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
from src.core.base.IncrementalProcessor import IncrementalProcessor
from src.core.base.utils.RateLimiter import RateLimiter




class OrchestratorFeatures:
    """
    Mixin class that provides additional features to OrchestratorAgent.
    This helps keep the main OrchestratorAgent file small (<30KB).
    """

    # =========================================================================
    # Plugin System Methods
    # =========================================================================

    def register_plugin(self, plugin: AgentPluginBase) -> None:
        """Register a custom agent plugin."""
        if not hasattr(self, 'plugins'):
            self.plugins: dict[str, AgentPluginBase] = {}

        plugin.setup()
        self.plugins[plugin.name] = plugin
        logging.info(f"Registered plugin: {plugin.name} (priority: {plugin.priority.name})")

    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin by name."""
        if not hasattr(self, 'plugins') or plugin_name not in self.plugins:
            return False

        plugin = self.plugins[plugin_name]
        plugin.teardown()
        del self.plugins[plugin_name]
        logging.info(f"Unregistered plugin: {plugin_name}")
        return True

    def get_plugin(self, plugin_name: str) -> AgentPluginBase | None:
        """Get a registered plugin by name."""
        if not hasattr(self, 'plugins'):
            return None
        return self.plugins.get(plugin_name)

    def run_plugins(self, file_path: Path) -> dict[str, bool]:
        """Run all registered plugins on a file."""
        if not hasattr(self, 'plugins') or not self.plugins:
            return {}

        results: dict[str, bool] = {}
        context: dict[str, Any] = {
            'agent': self,
            'repo_root': getattr(self, 'repo_root', Path('.')),
            'dry_run': getattr(self, 'dry_run', False),
            'metrics': getattr(self, 'metrics', {})
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
                if hasattr(self, 'rate_limiter'):
                    self.rate_limiter.acquire(timeout=30.0)

                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(plugin.run, file_path, context)
                    try:
                        result = future.result(timeout=5.0)
                    except TimeoutError:
                        logging.warning(f"Plugin {plugin.name} timed out. Skipping.")
                        result = False

                results[plugin.name] = result
                if result and hasattr(self, 'metrics'):
                    if 'agents_applied' not in self.metrics:
                        self.metrics['agents_applied'] = {}
                    self.metrics['agents_applied'][plugin.name] = \
                        self.metrics['agents_applied'].get(plugin.name, 0) + 1

            except Exception as e:
                logging.error(f"Plugin {plugin.name} failed: {e}")
                results[plugin.name] = False

        return results

    def load_plugins_from_config(self, plugin_configs: list[AgentPluginConfig]) -> None:
        """Load plugins from configuration."""
        for config in plugin_configs:
            if not config.enabled:
                continue

            try:
                spec = importlib.util.spec_from_file_location(config.name, config.module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugin_class = getattr(module, config.entry_point, None)
                    if plugin_class and issubclass(plugin_class, AgentPluginBase):
                        plugin = plugin_class(config.name, config.priority, config.config)
                        self.register_plugin(plugin)
            except Exception as e:
                logging.error(f"Failed to load plugin {config.name}: {e}")

    # =========================================================================
    # Rate Limiting Methods
    # =========================================================================

    def enable_rate_limiting(self, config: RateLimitConfig | None = None) -> None:
        """Enable rate limiting for API calls."""
        self.rate_limiter = RateLimiter(config)
        logging.info(f"Rate limiting enabled: {config or 'default settings'}")

    def get_rate_limit_stats(self) -> dict[str, Any]:
        """Get current rate limiter statistics."""
        if hasattr(self, 'rate_limiter'):
            return self.rate_limiter.get_stats()
        return {}

    # =========================================================================
    # File Locking Methods
    # =========================================================================

    def enable_file_locking(self, lock_timeout: float = 300.0) -> None:
        """Enable file locking."""
        self.lock_manager = FileLockManager(lock_timeout)
        logging.info(f"File locking enabled (timeout: {lock_timeout}s)")

    # =========================================================================
    # Diff Preview Methods
    # =========================================================================

    def enable_diff_preview(self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED) -> None:
        """Enable diff preview mode."""
        self.diff_generator = DiffGenerator(output_format)
        logging.info(f"Diff preview enabled (format: {output_format.name})")

    def preview_changes(self, file_path: Path, new_content: str) -> DiffResult:
        """Preview changes to a file without applying them."""
        if not hasattr(self, 'diff_generator'):
            self.diff_generator = DiffGenerator()
        original = file_path.read_text() if file_path.exists() else ""
        return self.diff_generator.generate_diff(file_path, original, new_content)

    def show_pending_diffs(self) -> None:
        """Show all pending diffs for dry-run mode."""
        if not hasattr(self, 'pending_diffs'):
            logging.info("No pending changes.")
            return
        logging.info(f"=== Pending Changes ({len(self.pending_diffs)} files) ===")
        for diff in self.pending_diffs:
            logging.info(f"--- {diff.file_path} ---")
            logging.info(f"  +{diff.additions} -{diff.deletions}")
            if hasattr(self, 'diff_generator'):
                self.diff_generator.print_diff(diff)
            logging.info("")

    # =========================================================================
    # Incremental Processing Methods
    # =========================================================================

    def enable_incremental_processing(self) -> None:
        """Enable incremental processing."""
        repo_root = getattr(self, 'repo_root', Path('.'))
        self.incremental_processor = IncrementalProcessor(repo_root)
        logging.info("Incremental processing enabled")

    def get_changed_files(self, files: list[Path]) -> list[Path]:
        """Get files that changed since last run."""
        if hasattr(self, 'incremental_processor'):
            return self.incremental_processor.get_changed_files(files)
        return files

    def reset_incremental_state(self) -> None:
        """Reset incremental state."""
        if hasattr(self, 'incremental_processor'):
            self.incremental_processor.reset_state()

    # =========================================================================
    # Graceful Shutdown Methods
    # =========================================================================

    def enable_graceful_shutdown(self) -> None:
        """Enable graceful shutdown."""
        repo_root = getattr(self, 'repo_root', Path('.'))
        self.shutdown_handler = GracefulShutdown(repo_root)
        self.shutdown_handler.install_handlers()
        logging.info("Graceful shutdown enabled")

    def resume_from_shutdown(self) -> list[Path] | None:
        """Resume from interrupted state."""
        repo_root = getattr(self, 'repo_root', Path('.'))
        if not hasattr(self, 'shutdown_handler'):
            self.shutdown_handler = GracefulShutdown(repo_root)
        state = self.shutdown_handler.load_resume_state()
        if state and state.pending_files:
            return [Path(f) for f in state.pending_files]
        return None

    # =========================================================================
    # Health Check Methods
    # =========================================================================

    def run_health_checks(self) -> dict[str, AgentHealthCheck]:
        """Run health checks."""
        repo_root = getattr(self, 'repo_root', Path('.'))
        checker = HealthChecker(repo_root)
        return checker.run_all_checks()

    def is_healthy(self) -> bool:
        """Check if all components are healthy."""
        results = self.run_health_checks()
        return all(r.status == HealthStatus.HEALTHY for r in results.values())

    def print_health_report(self) -> None:
        """Print a health report."""
        repo_root = getattr(self, 'repo_root', Path('.'))
        checker = HealthChecker(repo_root)
        checker.run_all_checks()
        checker.print_report()

    # =========================================================================
    # Execution & Flow Control Methods
    # =========================================================================

    def _run_command(self, cmd: list[str], timeout: int = 120,
                     max_retries: int = 1) -> subprocess.CompletedProcess[str]:
        """Run a command with timeout, error handling, retry logic, and logging."""
        return getattr(self, 'command_handler').run_command(cmd, timeout, max_retries)

    @contextmanager
    def _with_agent_env(self, agent_name: str) -> bool:
        """Temporarily set environment variables for a specific agent."""
        with getattr(self, 'command_handler').with_agent_env(agent_name):
            yield

    def run_stats_update(self, files: list[Path]) -> None:
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

    def _perform_iteration(self, code_file: Path) -> bool:
        """Perform one iteration of improvements on the code file."""
        changes_made = False
        if not getattr(self, 'skip_code_update'):
            self.run_tests(code_file)
        # Update Errors, Improvements
        changes_made |= self.update_errors_improvements(code_file)
        # Update Code
        if not getattr(self, 'skip_code_update'):
            changes_made |= self.update_code(code_file)
        # Update Changelog, Context, Tests
        changes_made |= self.update_changelog_context_tests(code_file)
        return changes_made

    def _commit_and_push(self, code_file: Path) -> None:
        """Commit and push changes for the code file."""
        if getattr(self, 'no_git'):
            logging.info(f"Skipping git operations for {code_file.name} (--no-git)")
            return

        logging.info(f"Committing changes for {code_file.name}")
        try:
            self._run_command(['git', 'add', '-A'])
            commit_msg = f"Agent improvements for {code_file.name}"
            result = self._run_command(['git', 'commit', '-m', commit_msg])
            if result.returncode == 0:
                logging.info(f"Committed changes for {code_file.name}")
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

    def run_with_parallel_execution(self) -> None:
        """Run the main agent loop with parallel execution strategy."""
        code_files = self.find_code_files()
        logging.info(f"Found {len(code_files)} code files to process")

        for loop_iteration in range(1, getattr(self, 'loop') + 1):
            logging.info(f"Starting loop iteration {loop_iteration}/{getattr(self, 'loop')}")

            if getattr(self, 'enable_multiprocessing'):
                logging.info("Using multiprocessing for parallel execution")
                self.process_files_multiprocessing(code_files)
            elif getattr(self, 'enable_async'):
                logging.info("Using async for concurrent execution")
                asyncio.run(self.async_process_files(code_files))
            else:
                logging.info("Using threaded execution")
                self.process_files_threaded(code_files)

            logging.info(f"Completed loop iteration {loop_iteration}/{getattr(self, 'loop')}")

        self.execute_callbacks('agent_complete', self.metrics)
        self.send_webhook_notification('agent_complete', self.metrics)

        logging.info("Final stats:")
        self.run_stats_update(code_files)

    def process_file(self, code_file: Path) -> None:
        """Process a single code file through the improvement loop."""
        if hasattr(self, 'shutdown_handler') and not self.shutdown_handler.should_continue():
            logging.info(f"Skipping {code_file.name} due to shutdown request")
            return

        if hasattr(self, 'lock_manager'):
            lock = self.lock_manager.acquire_lock(code_file)
            if not lock:
                logging.warning(f"Could not acquire lock for {code_file.name}, skipping")
                return

        try:
            if hasattr(self, 'shutdown_handler'):
                self.shutdown_handler.set_current_file(code_file)

            logging.info(f"Processing {code_file.relative_to(getattr(self, 'repo_root'))}...")
            max_iterations = 1
            iteration = 0
            all_fixed = False
            while not all_fixed and iteration < max_iterations:
                iteration += 1
                logging.debug(f"Iteration {iteration} for {code_file.name}")
                self._check_files_ready(code_file)

                try:
                    changes_made = self._perform_iteration(code_file)
                except Exception as e:
                    logging.error(f"Error in _perform_iteration for {code_file}: {e}")
                    try:
                        sql = getattr(getattr(self, 'command_handler').models, "sql_metadata", None)
                        if sql:
                            sql.record_debt(
                                str(code_file.relative_to(getattr(self, 'repo_root'))),
                                "Runtime Error",
                                f"Iteration failed: {str(e)}",
                                False
                            )
                    except Exception:
                        pass
                    changes_made = False

                if not changes_made:
                    all_fixed = True
                    logging.info(f"No changes made in iteration {iteration}, marking as fixed")
                else:
                    logging.info(f"Changes made in iteration {iteration}, continuing...")

            if iteration >= max_iterations:
                logging.info(f"Reached maximum iterations ({max_iterations}) for {code_file.name}")

            self._commit_and_push(code_file)

            if hasattr(self, 'incremental_processor'):
                self.incremental_processor.mark_processed(code_file)

            if hasattr(self, 'shutdown_handler'):
                self.shutdown_handler.mark_completed(code_file)

        except Exception as global_e:
            logging.critical(f"Global failure processing {code_file}: {global_e}", exc_info=True)
        finally:
            if hasattr(self, 'lock_manager'):
                self.lock_manager.release_lock(code_file)

            if hasattr(self, 'shutdown_handler'):
                self.shutdown_handler.set_current_file(None)

    def run(self) -> None:
        """Run the main agent loop."""
        if not hasattr(self, 'logger'):
            self.logger = StructuredLogger(agent_id=self.__class__.__name__)

        self.logger.info("Entering agent.run()")
        if getattr(self, 'enable_async') or getattr(self, 'enable_multiprocessing'):
            self.run_with_parallel_execution()
        else:
            code_files = self.find_code_files()
            self.logger.info(f"Found {len(code_files)} code files to process", count=len(code_files))
            for loop_iteration in range(1, getattr(self, 'loop') + 1):
                logging.info(f"Starting loop iteration {loop_iteration}/{getattr(self, 'loop')}")
                for code_file in code_files:
                    self.process_file(code_file)
                logging.info(f"Completed loop iteration {loop_iteration}/{getattr(self, 'loop')}")
            logging.info("Final stats:")
            self.run_stats_update(code_files)

            self.execute_callbacks('agent_complete', self.metrics)
            self.send_webhook_notification('agent_complete', self.metrics)
