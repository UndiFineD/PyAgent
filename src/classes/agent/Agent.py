#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .AgentHealthCheck import AgentHealthCheck
from .AgentPluginBase import AgentPluginBase
from .AgentPluginConfig import AgentPluginConfig
from .ConfigLoader import ConfigLoader
from .DiffGenerator import DiffGenerator
from .DiffOutputFormat import DiffOutputFormat
from .DiffResult import DiffResult
from .FileLockManager import FileLockManager
from .GracefulShutdown import GracefulShutdown
from .HealthChecker import HealthChecker
from .HealthStatus import HealthStatus
from .IncrementalProcessor import IncrementalProcessor
from .RateLimitConfig import RateLimitConfig
from .RateLimiter import RateLimiter
from .utils import load_codeignore, fix_markdown_content
from ._helpers import HAS_REQUESTS, requests

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

class Agent:
    """Main agent that orchestrates sub-agents for code improvement.

    This class coordinates the improvement process across code files by delegating
    tasks to specialized sub - agents (CoderAgent, TestsAgent, etc.) that handle
    specific aspects of code quality and documentation.

    Supports context manager protocol for resource management.

    Attributes:
        repo_root (Path): Root directory of the target repository.
        agents_only (bool): If True, only process files in scripts / agent directory.
        max_files (Optional[int]): Maximum number of files to process. None=no limit.
        loop (int): Number of times to run the full improvement cycle (default: 1).
        skip_code_update (bool): If True, skip code update phase.
        no_git (bool): If True, don't commit changes to git.
        ignored_patterns (Set[str]): Patterns from .codeignore file.

    Class Attributes:
        SUPPORTED_EXTENSIONS (Set[str]): File extensions to process (py, sh, js, ts, etc.).

    Example:
        with Agent(repo_root='.', agents_only=True) as agent:
            files=agent.find_code_files()
            agent.run()

    Note:
        - Can be used as context manager for automatic cleanup
        - Recursively finds code files in the repository
        - Filters files according to .codeignore patterns
        - Runs sub - agents on each file for improvements
        - Optionally commits changes back to git
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
                 strategy: str = 'direct') -> None:
        """Initialize the Agent with repository configuration.

        Args:
            repo_root: Root directory of the repository to process. Defaults to '.'.
            agents_only: If True, only process files in scripts / agent. Defaults to False.
            max_files: Maximum number of files to process. None=unlimited. Defaults to None.
            loop: Number of full cycles to run. Defaults to 1.
            skip_code_update: If True, skip code update phase.
                Defaults to False.
            no_git: If True, don't commit changes to git.
                Defaults to False.
            dry_run: If True, preview changes without modifying files.
                Defaults to False.
            selective_agents: List of agent names to execute
                (e.g., ['coder', 'tests']). Defaults to None (all).
            timeout_per_agent: Dict mapping agent names to timeout values
                in seconds. Defaults to None.
            enable_async: If True, use async file processing.
                Defaults to False.
            enable_multiprocessing: If True, use multiprocessing for agents.
                Defaults to False.
            max_workers: Maximum number of worker threads / processes.
                Defaults to 4.
            strategy: Reasoning strategy to use (direct, cot, reflexion).
                Defaults to 'direct'.

        Raises:
            FileNotFoundError: If repo_root doesn't exist.

        Note:
            The repository root is automatically detected by looking for .git,
            README.md, or package.json if not explicitly provided.

            Supports context manager protocol via __enter__ and __exit__.
        """
        logging.info(f"Initializing Agent with repo_root={repo_root}")
        # If the user explicitly provided a directory (not the default '.'),
        # respect that path and do NOT search upward for repository markers.
        provided_path = Path(repo_root)
        if str(repo_root) and str(repo_root) != '.':
            # Use the exact provided directory (resolved to absolute path)
            self.repo_root = provided_path.resolve()
        else:
            # No explicit path provided (or default '.'), try to detect repo root
            self.repo_root = self._find_repo_root(provided_path)
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
        self.strategy = strategy
        self.ignored_patterns = load_codeignore(self.repo_root)

        # Webhook support
        self.webhooks: List[str] = []
        self.callbacks: list[Callable[..., Any]] = []

        # Metrics tracking
        agents_applied: dict[str, int] = {}
        self.metrics: dict[str, Any] = {
            'files_processed': 0,
            'files_modified': 0,
            'agents_applied': agents_applied,
            'start_time': time.time(),
            'end_time': None,
        }

        logging.info(
            f"Agent initialized: repo={self.repo_root}, loop={loop}, "
            f"agents_only={agents_only}"
        )
        if dry_run:
            logging.info("DRY RUN MODE: No files will be modified")
        if selective_agents:
            logging.info(f"Selective execution: agents={selective_agents}")
        if enable_async:
            logging.info("Async file processing enabled")
        if enable_multiprocessing:
            logging.info(f"Multiprocessing enabled with {max_workers} workers")

    def __enter__(self) -> "Agent":
        """Context manager entry. Returns self for use in 'with' statement."""
        logging.debug("Agent entering context manager")
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
        """Print a summary of execution metrics and statistics.

        Prints information about files processed, modifications made, agents applied,
        and execution time. Useful for understanding the impact of agent runs.

        Example:
            agent.run()
            agent.print_metrics_summary()
        """
        self.metrics['end_time'] = time.time()
        elapsed = self.metrics['end_time'] - self.metrics['start_time']

        summary = f"""
=== Agent Execution Summary ===
Files processed: {self.metrics['files_processed']}
Files modified:  {self.metrics['files_modified']}
Execution time:  {elapsed:.2f}s
Dry-run mode:    {'Yes' if self.dry_run else 'No'}

Agents applied:
"""
        for agent, count in sorted(self.metrics['agents_applied'].items()):
            summary += f"  - {agent}: {count} files\n"

        logging.info(summary)
        print(summary)

    def generate_improvement_report(self) -> Dict[str, Any]:
        """Generate comprehensive improvement report with statistics.

        Creates detailed report including:
        - Overall statistics (files processed, modified, time)
        - Per - file summaries with improvements made
        - Agent effectiveness (improvements per agent)
        - Performance metrics

        Returns:
            Dict with report structure and statistics

        Example:
            report=agent.generate_improvement_report()
            print(f"Report generated: {report['summary']}")

        Note:
            - Aggregates metrics from all processed files
            - Calculates effectiveness metrics
            - Includes timing and performance data
        """
        self.metrics['end_time'] = time.time()
        elapsed = self.metrics['end_time'] - self.metrics['start_time']

        report: dict[str, Any] = {
            'timestamp': time.time(),
            'summary': {
                'files_processed': self.metrics.get('files_processed', 0),
                'files_modified': self.metrics.get('files_modified', 0),
                'total_time_seconds': elapsed,
                'average_time_per_file': elapsed / max(self.metrics.get('files_processed', 1), 1),
            },
            'agents': dict(self.metrics.get('agents_applied', {})),
            'mode': {
                'dry_run': self.dry_run,
                'async_enabled': self.enable_async,
                'multiprocessing_enabled': self.enable_multiprocessing,
            }
        }

        # Calculate effectiveness metrics
        files_proc = cast(int, report['summary']['files_processed'])
        files_mod = cast(int, report['summary']['files_modified'])
        report['summary']['modification_rate'] = (
            files_mod / files_proc * 100) if files_proc > 0 else 0

        logging.info(
            f"Generated improvement report: {files_proc} files processed, {files_mod} modified")
        return report

    def benchmark_execution(self, files: List[Path]) -> Dict[str, Any]:
        """Benchmark execution time per file and per agent.

        Measures and tracks execution time for individual files and agents.
        Useful for identifying performance bottlenecks and optimization targets.

        Args:
            files: List of files that were processed

        Returns:
            Dict with timing statistics per file and agent

        Example:
            agent.run()
            benchmarks=agent.benchmark_execution(files)
            slowest=max(benchmarks['per_file'].items(), key=lambda x: x[1])
            print(f"Slowest file: {slowest[0]} ({slowest[1]:.2f}s)")

        Note:
            - Requires enable_async or enable_multiprocessing for meaningful data
            - Tracks timing from metrics collected during execution
            - Per - file timing estimated from total / file count
        """
        total_time = (self.metrics.get('end_time', time.time()) -
                      self.metrics.get('start_time', time.time()))
        files_count = len(files)
        avg_per_file = total_time / max(files_count, 1)

        benchmarks: dict[str, Any] = {
            'total_time': total_time,
            'file_count': files_count,
            'average_per_file': avg_per_file,
            'per_file': {
                str(f.name): avg_per_file for f in files  # Estimated
            },
            'per_agent': dict(self.metrics.get('agents_applied', {})),
        }

        logging.debug(f"Benchmarks: {files_count} files in {total_time:.2f}s "
                      f"({avg_per_file:.2f}s / file)")
        return benchmarks

    def cost_analysis(self, backend: str = 'github-models',
                      cost_per_request: float = 0.0001) -> Dict[str, Any]:
        """Analyze API usage cost for the agent execution.

        Estimates cost based on files processed, agents applied, and backend pricing.
        Useful for understanding operational costs of running the agent.

        Args:
            backend: Backend service name (e.g., 'github-models', 'openai', 'anthropic')
            cost_per_request: Cost per API request in currency units

        Returns:
            Dict with cost analysis and estimates

        Example:
            cost=agent.cost_analysis(backend='github-models', cost_per_request=0.0001)
            print(f"Estimated cost: ${cost['total_estimated_cost']:.4f}")

        Note:
            - Cost is estimated based on files and agents
            - Actual cost depends on token usage and pricing model
            - Multiple agents per file multiply the request count
        """
        files_processed = self.metrics.get('files_processed', 0)
        agents_applied = self.metrics.get('agents_applied', {})
        total_agent_runs = sum(agents_applied.values())

        # Estimate requests: one per file per agent type
        estimated_requests = total_agent_runs
        estimated_cost = estimated_requests * cost_per_request

        analysis: dict[str, Any] = {
            'backend': backend,
            'files_processed': files_processed,
            'agents_applied': dict(agents_applied),
            'total_agent_runs': total_agent_runs,
            'cost_per_request': cost_per_request,
            'estimated_requests': estimated_requests,
            'total_estimated_cost': estimated_cost,
            'cost_per_file': estimated_cost / max(files_processed, 1),
        }

        logging.info(f"Cost analysis: {estimated_requests} requests, "
                     f"${estimated_cost:.4f} estimated")
        return analysis

    def cleanup_old_snapshots(self, max_age_days: int = 7,
                              max_snapshots_per_file: int = 10) -> int:
        """Clean up old file snapshots according to retention policy.

        Removes snapshots older than max_age_days or exceeding max_snapshots_per_file
        per file. Helps manage disk space used by snapshots.

        Args:
            max_age_days: Keep snapshots newer than this many days
            max_snapshots_per_file: Maximum snapshots to keep per file

        Returns:
            Number of snapshots deleted

        Example:
            cleaned=agent.cleanup_old_snapshots(max_age_days=7, max_snapshots_per_file=5)
            print(f"Cleaned up {cleaned} old snapshots")

        Note:
            - Deletes files from .agent_snapshots directory
            - Preserves most recent snapshots
            - Be careful with aggressive cleanup (data loss risk)
        """
        snapshot_dir = self.repo_root / '.agent_snapshots'
        if not snapshot_dir.exists():
            logging.debug("No snapshot directory found, nothing to clean")
            return 0

        try:
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60
            snapshots_deleted = 0

            # Group snapshots by file
            snapshots_by_file: Dict[str, List[Path]] = {}
            for snapshot_file in snapshot_dir.glob('*'):
                if snapshot_file.is_file():
                    # Extract filename from snapshot name (format: timestamp_hash_filename)
                    parts = snapshot_file.name.split('_', 2)
                    if len(parts) >= 3:
                        filename = parts[2]
                        if filename not in snapshots_by_file:
                            snapshots_by_file[filename] = []
                        snapshots_by_file[filename].append(snapshot_file)

            # Clean by age and count
            for filename, snapshots in snapshots_by_file.items():
                # Sort by modification time (newest first)
                snapshots.sort(key=lambda x: x.stat().st_mtime, reverse=True)

                for i, snapshot in enumerate(snapshots):
                    # Delete if too old
                    mtime = snapshot.stat().st_mtime
                    age = current_time - mtime
                    if age > max_age_seconds:
                        snapshot.unlink()
                        snapshots_deleted += 1
                        logging.debug(f"Deleted old snapshot: {snapshot.name}")
                    # Or if exceeds max count
                    elif i >= max_snapshots_per_file:
                        snapshot.unlink()
                        snapshots_deleted += 1
                        logging.debug(f"Deleted excess snapshot: {snapshot.name}")

            logging.info(f"Cleaned up {snapshots_deleted} old snapshots")
            return snapshots_deleted

        except Exception as e:
            logging.error(f"Failed to cleanup snapshots: {e}")
            return 0

    def create_file_snapshot(self, file_path: Path) -> Optional[str]:
        """Create a snapshot of file content before modifications.

        Saves the current content of a file for potential rollback later.
        Useful for preserving pre - agent versions before applying improvements.

        Args:
            file_path: Path to the file to snapshot.

        Returns:
            str: Snapshot ID (timestamp - based) for later rollback, or None if snapshot failed.

        Example:
            snapshot_id=agent.create_file_snapshot(Path('src / main.py'))
            # Make changes...
            if something_wrong:
                agent.restore_from_snapshot('src / main.py', snapshot_id)
        """
        try:
            if not file_path.exists():
                logging.debug(f"Cannot snapshot non-existent file: {file_path}")
                return None

            # Create snapshots directory if needed
            snapshot_dir = self.repo_root / '.agent_snapshots'
            snapshot_dir.mkdir(exist_ok=True)

            # Generate snapshot ID based on timestamp
            import hashlib
            content = file_path.read_text(encoding='utf-8', errors='replace')
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            snapshot_id = f"{time.time():.0f}_{content_hash}"

            # Save relative path and content
            rel_path = file_path.relative_to(self.repo_root)
            snapshot_file = snapshot_dir / f"{snapshot_id}_{rel_path.name}"
            snapshot_file.write_text(content, encoding='utf-8')

            logging.debug(f"Created snapshot {snapshot_id} for {rel_path}")
            return snapshot_id

        except Exception as e:
            logging.error(f"Failed to create snapshot for {file_path}: {e}")
            return None

    def restore_from_snapshot(self, file_path: Path, snapshot_id: str) -> bool:
        """Restore a file from a previously created snapshot.

        Restores file content from a snapshot created by create_file_snapshot().
        Useful for rollback when agent modifications are undesirable.

        Args:
            file_path: Path to the file to restore.
            snapshot_id: Snapshot ID returned by create_file_snapshot().

        Returns:
            bool: True if restoration successful, False otherwise.

        Example:
            snapshot_id=agent.create_file_snapshot(Path('src / main.py'))
            # Modifications...
            agent.restore_from_snapshot(Path('src / main.py'), snapshot_id)
        """
        try:
            snapshot_dir = self.repo_root / '.agent_snapshots'
            if not snapshot_dir.exists():
                logging.warning(f"Snapshot directory not found: {snapshot_dir}")
                return False

            # Find snapshot file matching pattern
            rel_path = file_path.relative_to(self.repo_root)
            pattern = f"{snapshot_id}_{rel_path.name}"

            snapshot_file = snapshot_dir / pattern
            if not snapshot_file.exists():
                logging.warning(f"Snapshot not found: {pattern}")
                return False

            # Restore content
            content = snapshot_file.read_text(encoding='utf-8')
            file_path.write_text(content, encoding='utf-8')

            logging.info(f"Restored {rel_path} from snapshot {snapshot_id}")
            return True

        except Exception as e:
            logging.error(f"Failed to restore snapshot for {file_path}: {e}")
            return False

    def load_cascading_codeignore(self, directory: Optional[Path] = None) -> Set[str]:
        """Load .codeignore patterns with cascading support.

        Loads ignore patterns from .codeignore files in the directory and all
        parent directories up to the repository root. This enables hierarchical
        ignore patterns where subdirectories can have their own .codeignore.

        Args:
            directory: Directory to start searching from. Defaults to repo_root.

        Returns:
            Set[str]: Combined set of ignore patterns from all .codeignore files.

        Example:
            # Load patterns from /repo/.codeignore and /repo / src/.codeignore
            patterns=agent.load_cascading_codeignore(Path('src'))

        Note:
            - Patterns closer to the target directory take precedence
            - All patterns are combined into a single set for efficiency
            - Duplicate patterns are automatically deduplicated
        """
        if directory is None:
            directory = self.repo_root

        all_patterns: set[str] = set()
        current_dir = directory.resolve()

        # Walk up to repo root, loading .codeignore files
        while current_dir >= self.repo_root:
            codeignore_file = current_dir / '.codeignore'
            if codeignore_file.exists():
                try:
                    patterns = load_codeignore(current_dir)
                    all_patterns.update(patterns)
                    logging.debug(f"Loaded {len(patterns)} patterns from {codeignore_file}")
                except Exception as e:
                    logging.warning(f"Failed to load {codeignore_file}: {e}")

            # Stop at repo root
            if current_dir == self.repo_root:
                break

            current_dir = current_dir.parent

        logging.debug(f"Total cascading patterns from {directory}: {len(all_patterns)}")
        return all_patterns

    def _run_command(self, cmd: List[str], timeout: int = 120,
                     max_retries: int = 1) -> subprocess.CompletedProcess[str]:
        """Run a command with timeout, error handling, retry logic, and logging.

        Executes a subprocess command with comprehensive error handling,
        timeout protection, exponential backoff retry, and logging of results.

        Args:
            cmd: Command as list of strings (e.g., ['python', 'script.py', '--arg']).
            timeout: Timeout in seconds for command execution. Defaults to 120.
            max_retries: Number of retry attempts on failure. Defaults to 1 (no retry).

        Returns:
            subprocess.CompletedProcess: Contains returncode, stdout, stderr.

        Raises:
            None. All errors are caught and logged. Returns failed CompletedProcess.

        Example:
            result=agent._run_command(['python', '-m', 'pytest', 'test.py'], max_retries=2)
            if result.returncode == 0:
                print("Success")
            else:
                print(f"Failed: {result.stderr}")

        Note:
            - Uses UTF - 8 encoding with 'replace' error handling for robustness
            - Captures both stdout and stderr
            - Logs command execution at DEBUG level
            - Returns CompletedProcess even on timeout (returncode=-1)
            - Retries with exponential backoff: 1s, 2s, 4s, etc.
        """
        def attempt_command() -> subprocess.CompletedProcess[str]:
            logging.debug(f"Running command: {' '.join(cmd[:3])}... (timeout={timeout}s)")
            try:
                # Copy command so we don't mutate caller's list
                local_cmd = list(cmd)
                env = os.environ.copy()

                # Detect python-invoked agent scripts (e.g., python <...>/agent_*.py)
                try:
                    is_agent_script = (
                        len(local_cmd) > 1 and
                        local_cmd[0] == sys.executable and
                        Path(local_cmd[1]).name.startswith('agent_')
                    )
                except Exception:
                    is_agent_script = False

                if is_agent_script:
                    # Mark child so it can avoid cascading further invocations
                    env['DV_AGENT_PARENT'] = '1'
                    # Ensure child receives a --no-cascade flag to disable spawning
                    if '--no-cascade' not in local_cmd:
                        local_cmd = local_cmd[:2] + ['--no-cascade'] + local_cmd[2:]
                    # Inject per-agent model/provider settings from Agent.models
                    try:
                        script_name = Path(local_cmd[1]).name
                        # script pattern: agent_<name>.py
                        if script_name.startswith('agent_') and script_name.endswith('.py'):
                            agent_name = script_name[len('agent_'):-3]
                        else:
                            agent_name = None
                    except Exception:
                        agent_name = None

                    model_spec = None
                    if hasattr(self, 'models') and agent_name:
                        model_spec = self.models.get(agent_name) or self.models.get('default')

                    if model_spec and isinstance(model_spec, dict):
                        if 'provider' in model_spec:
                            env['DV_AGENT_MODEL_PROVIDER'] = str(model_spec.get('provider', ''))
                        if 'model' in model_spec:
                            env['DV_AGENT_MODEL_NAME'] = str(model_spec.get('model', ''))
                        if 'temperature' in model_spec:
                            env['DV_AGENT_MODEL_TEMPERATURE'] = str(model_spec.get('temperature', ''))
                        if 'max_tokens' in model_spec:
                            env['DV_AGENT_MODEL_MAX_TOKENS'] = str(model_spec.get('max_tokens', ''))

                result = subprocess.run(
                    local_cmd,
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='replace',
                    check=False,
                    env=env,
                )
                logging.debug(f"Command completed with returncode={result.returncode}")
                return result
            except subprocess.TimeoutExpired:
                logging.error(f"Command timed out after {timeout}s: {' '.join(cmd[:3])}...")
                return subprocess.CompletedProcess(
                    cmd, returncode=-1, stdout="", stderr="Timeout expired")
            except OSError as e:
                logging.error(f"Command failed to start: {e}")
                return subprocess.CompletedProcess(cmd, returncode=-1, stdout="", stderr=str(e))
            except Exception as e:
                logging.error(f"Command failed with unexpected error: {e}")
                return subprocess.CompletedProcess(cmd, returncode=-1, stdout="", stderr=str(e))

        result: subprocess.CompletedProcess[str] = attempt_command()

        # Retry on failure with exponential backoff
        for attempt in range(1, max_retries):
            if result.returncode == 0:
                return result

            delay = min(1.0 * (2 ** (attempt - 1)), 30.0)  # Max 30 seconds
            logging.warning(f"Command failed (attempt {attempt}), retrying in {delay}s...")
            time.sleep(delay)
            result = attempt_command()

        return result

    @contextmanager
    def _with_agent_env(self, agent_name: str):
        """Temporarily set environment variables for a specific agent.

        Sets DV_AGENT_MODEL_* env vars from self.models[agent_name] (or default)
        for the duration of the context manager, then restores previous values.
        """
        prev: dict[str, str | None] = {}
        keys = ['DV_AGENT_MODEL_PROVIDER', 'DV_AGENT_MODEL_NAME',
                'DV_AGENT_MODEL_TEMPERATURE', 'DV_AGENT_MODEL_MAX_TOKENS']
        try:
            spec = None
            if hasattr(self, 'models') and isinstance(self.models, dict):
                spec = self.models.get(agent_name) or self.models.get('default')

            for k in keys:
                prev[k] = os.environ.get(k)

            if spec and isinstance(spec, dict):
                if 'provider' in spec:
                    os.environ['DV_AGENT_MODEL_PROVIDER'] = str(spec.get('provider', ''))
                if 'model' in spec:
                    os.environ['DV_AGENT_MODEL_NAME'] = str(spec.get('model', ''))
                if 'temperature' in spec:
                    os.environ['DV_AGENT_MODEL_TEMPERATURE'] = str(spec.get('temperature', ''))
                if 'max_tokens' in spec:
                    os.environ['DV_AGENT_MODEL_MAX_TOKENS'] = str(spec.get('max_tokens', ''))

            yield
        finally:
            # restore previous values
            for k, v in prev.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

    def _find_repo_root(self, start_path: Path) -> Path:
        """Find the repository root by looking for repository markers.

        Walks up the directory tree from the start path looking for markers
        that indicate a repository root (.git, README.md, package.json).

        Args:
            start_path: Starting directory path to search from.

        Returns:
            Path: Repository root directory, or start_path if no markers found.

        Example:
            root=agent._find_repo_root(Path('/some / nested / dir'))
            # Returns Path to repo root if .git found in parents

        Note:
            - Checks the starting path first, then walks up to parents
            - Uses multiple markers to identify repo roots
            - Returns start_path if no markers found (doesn't raise error)
        """
        current = start_path.resolve()
        logging.debug(f"Searching for repository root from {current}")
        # Walk up the directory tree looking for repository markers
        for path in [current] + list(current.parents):
            if (path / '.git').exists() or (path / 'README.md').exists() or \
                    (path / 'package.json').exists():
                logging.info(f"Found repository root at {path}")
                return path
        # If no markers found, return the original path
        logging.debug(f"No repository markers found, using {start_path} as root")
        return start_path

    def find_code_files(self) -> List[Path]:
        """Recursively find all supported code files in the repository.

        Searches the repository for files with supported extensions, optionally
        filtered to the scripts / agent directory, and respects .codeignore patterns.

        Returns:
            List[Path]: Sorted list of code files found, limited by max_files if set.

        Example:
            files=agent.find_code_files()
            print(f"Found {len(files)} code files")

        Note:
            - Uses recursive glob patterns for efficiency
            - Filters by SUPPORTED_EXTENSIONS (py, sh, js, ts, go, rb)
            - Respects .codeignore patterns
            - Returns sorted list for reproducibility
            - Limited by max_files parameter if set
        """
        print("DEBUG: Entering find_code_files", file=sys.stderr)
        logging.info("Searching for code files...")
        code_files: list[Path] = []
        for ext in self.SUPPORTED_EXTENSIONS:
            print(f"DEBUG: Searching for *{ext}", file=sys.stderr)
            code_files.extend(self.repo_root.rglob(f'*{ext}'))
        logging.debug(f"Found {len(code_files)} files with supported extensions")
        print(f"DEBUG: Found {len(code_files)} files", file=sys.stderr)

        # Filter to agent-related files if agents_only is True
        if self.agents_only:
            logging.debug("agents_only=True: filtering to agent-related files")
            allowed_extra = {
                'base_agent.py',
                'generate_agent_reports.py',
                'agent_backend.py',
                'agent_test_utils.py',
                'agent.py'
            }
            def is_agent_file(p: Path) -> bool:
                name = p.name
                # Exclude test files explicitly
                if name.startswith('test'):
                    return False
                # Accept files starting with 'agent' or 'agent_'
                if name.startswith('agent') or name.startswith('agent_'):
                    return True
                # Accept a small set of helper filenames used by the agent system
                return name in allowed_extra

            code_files = [f for f in code_files if is_agent_file(f)]
            logging.info(f"Filtered to agent-related files: {len(code_files)} files")

        # Apply ignore patterns
        code_files = sorted([f for f in code_files if not self._is_ignored(f)])
        logging.info(f"After filtering ignores: {len(code_files)} files")

        if self.max_files:
            code_files = code_files[:self.max_files]
            logging.info(f"Limited to max_files={self.max_files}")

        return code_files

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored based on .codeignore patterns.

        Checks if a path matches any of the ignore patterns from .codeignore,
        using fnmatch patterns for flexible matching.

        Args:
            path: Path object to check.

        Returns:
            bool: True if path matches any ignore pattern, False otherwise.

        Example:
            ignored=agent._is_ignored(Path('venv / lib / file.py'))
            # Returns True if 'venv/**' or 'lib/**' in ignore patterns

        Note:
            - Checks against full path, filename, and path components
            - Uses fnmatch for Unix - style glob patterns
            - Returns False if no ignore patterns loaded
        """
        path_str = str(path)
        for pattern in self.ignored_patterns:
            if (fnmatch.fnmatch(path_str, pattern) or
                fnmatch.fnmatch(path.name, pattern) or
                    any(fnmatch.fnmatch(part, pattern) for part in path.parts)):
                logging.debug(f"Path {path} ignored by pattern: {pattern}")
                return True
        return False

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
        """Update errors and improvements."""
        base = code_file.stem
        dir_path = code_file.parent
        errors_file = dir_path / f"{base}.errors.md"
        improvements_file = dir_path / f"{base}.improvements.md"
        changes_made = False
        # Create errors file if it doesn't exist
        if not errors_file.exists():
            content = f"# Errors\n\nNo errors reported for {code_file.name}.\n"
            errors_file.write_text(fix_markdown_content(content), encoding='utf-8')
            logging.info(f"Created {errors_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update errors
        prompt = f"Analyze and improve the error report for {code_file.name}"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / 'agent_errors.py'),
            '--context', str(errors_file),
            '--prompt', prompt,
            '--strategy', self.strategy
        ]
        with self._with_agent_env('errors'):
            result = self._run_command(cmd)

        # Check if changes were made based on output
        stdout_ok = result.stdout and "No changes made" not in result.stdout
        stderr_ok = not result.stderr or "No changes made" not in result.stderr

        if stdout_ok and stderr_ok:
            changes_made = True
        # Create improvements file if it doesn't exist
        if not improvements_file.exists():
            content = f"# Improvements\n\nNo improvements suggested for {code_file.name}.\n"
            improvements_file.write_text(
                fix_markdown_content(content),
                encoding='utf - 8'
            )
            logging.info(f"Created {improvements_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update improvements
        prompt = f"Suggest and improve improvements for {code_file.name}"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / 'agent_improvements.py'),
            '--context', str(improvements_file),
            '--prompt', prompt,
            '--strategy', self.strategy
        ]
        with self._with_agent_env('improvements'):
            result = self._run_command(cmd)

        # Check if changes were made based on output
        stdout_ok = result.stdout and "No changes made" not in result.stdout
        stderr_ok = not result.stderr or "No changes made" not in result.stderr

        if stdout_ok and stderr_ok:
            changes_made = True
        return bool(changes_made)

    def _get_pending_improvements(self, improvements_file: Path) -> List[str]:
        """Extract pending improvements from the improvements file."""
        if not improvements_file.exists():
            return []
        try:
            content = improvements_file.read_text(encoding='utf-8')
            lines = content.splitlines()
            pending: list[str] = []
            import re
            # Match "1. ", "1) ", "- [ ]", "- ", "* "
            list_pattern = re.compile(r'^(\d+[\.\)]|\*|\-)\s+(\[ \]\s+)?(.*)')

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue

                # Skip checked items
                if '[x]' in stripped or '[Fixed]' in stripped:
                    continue

                match = list_pattern.match(stripped)
                if match:
                    item_text = match.group(3).strip()
                    # Filter out some obvious non - tasks or headers that look like lists
                    if item_text.lower().startswith('current strengths'):
                        continue
                    if len(item_text) > 5:
                        pending.append(item_text)
            return pending
        except Exception as e:
            logging.warning(f"Failed to read improvements file: {e}")
            return []

    def _mark_improvements_fixed(self, improvements_file: Path, fixed_items: List[str]) -> None:
        """Mark improvements as fixed in the file."""
        if not improvements_file.exists() or not fixed_items:
            return
        try:
            content = improvements_file.read_text(encoding='utf-8')
            lines = content.splitlines()
            new_lines: list[str] = []
            for line in lines:
                updated = False
                for item in fixed_items:
                    if item in line:
                        if '- [ ]' in line:
                            new_lines.append(line.replace('- [ ]', '- [x]'))
                            updated = True
                            break
                        elif '[x]' not in line and '[Fixed]' not in line:
                            new_lines.append(line + " [Fixed]")
                            updated = True
                            break
                if not updated:
                    new_lines.append(line)
            improvements_file.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
            logging.info(
                f"Marked {len(fixed_items)} improvements as fixed in "
                f"{improvements_file.name}"
            )
        except Exception as e:
            logging.warning(f"Failed to update improvements file: {e}")

    def _log_changes(self, changes_file: Path, fixed_items: List[str]) -> None:
        """Log fixed items to the changes file."""
        if not changes_file.exists() or not fixed_items:
            return
        try:
            content = changes_file.read_text(encoding='utf-8')
            new_entries = "\n".join([f"- Fixed: {item}" for item in fixed_items])
            # Append to the end or after the header
            if "# Changelog" in content:
                # Just append to end for now
                new_content = content.rstrip() + "\n\n" + new_entries + "\n"
            else:
                new_content = content + "\n" + new_entries + "\n"
            changes_file.write_text(new_content, encoding='utf-8')
            logging.info(f"Logged {len(fixed_items)} fixes to {changes_file.name}")
        except Exception as e:
            logging.warning(f"Failed to update changes file: {e}")

    def update_code(self, code_file: Path) -> bool:
        """Update the code file."""
        base = code_file.stem
        dir_path = code_file.parent
        improvements_file = dir_path / f"{base}.improvements.md"
        changes_file = dir_path / f"{base}.changes.md"
        pending_improvements = self._get_pending_improvements(improvements_file)
        # Limit to top 3 to avoid overwhelming
        target_improvements = pending_improvements[:3]
        if target_improvements:
            improvements_text = "\n".join(
                [f"- {item}" for item in target_improvements]
            )
            prompt = (
                f"Improve the code in {code_file.name} by implementing "
                f"the following specific improvements:\n"
                f"{improvements_text}\n\n"
                f"Ensure the code remains functional and follows best "
                f"practices."
            )
            logging.info(f"Targeting {len(target_improvements)} improvements for {code_file.name}")
        else:
            prompt = (
                f"Improve the code in {code_file.name} based on its context, "
                f"errors, and improvements")
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / 'agent_coder.py'),
            '--context', str(code_file),
            '--prompt', prompt,
            '--strategy', self.strategy
        ]
        with self._with_agent_env('coder'):
            result = self._run_command(cmd, timeout=300)

        # Check if changes were made based on output
        stdout_ok = result.stdout and "No changes made" not in result.stdout
        stderr_ok = not result.stderr or "No changes made" not in result.stderr

        changes_made = stdout_ok and stderr_ok
        if changes_made and target_improvements:
            # Assume targeted improvements were fixed if code changed
            self._mark_improvements_fixed(improvements_file, target_improvements)
            self._log_changes(changes_file, target_improvements)
        return bool(changes_made)

    def update_changelog_context_tests(self, code_file: Path) -> bool:
        """Update changelog, context, and tests."""
        base = code_file.stem
        dir_path = code_file.parent
        changes_file = dir_path / f"{base}.changes.md"
        context_file = dir_path / f"{base}.description.md"
        tests_file = dir_path / f"test_{base}.py"
        changes_made = False
        # Create changelog file if it doesn't exist
        if not changes_file.exists():
            content = f"# Changelog\n\n- Initial version of {code_file.name}\n"
            changes_file.write_text(fix_markdown_content(content), encoding='utf-8')
            logging.info(f"Created {changes_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update changelog
        prompt = f"Update the changelog for {code_file.name} with recent changes"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / 'agent_changes.py'),
            '--context', str(changes_file),
            '--prompt', prompt,
            '--strategy', self.strategy
        ]
        with self._with_agent_env('changes'):
            result = self._run_command(cmd)

        # Check if changes were made based on output
        stdout_ok = result.stdout and "No changes made" not in result.stdout
        stderr_ok = not result.stderr or "No changes made" not in result.stderr

        if stdout_ok and stderr_ok:
            changes_made = True
        # Create context file if it doesn't exist
        if not context_file.exists():
            content = f"# Description\n\n{code_file.name} - Description to be added.\n"
            context_file.write_text(fix_markdown_content(content), encoding='utf-8')
            logging.info(f"Created {context_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update context
        prompt = f"Update the description for {code_file.name} based on current code"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / 'agent_context.py'),
            '--context', str(context_file),
            '--prompt', prompt,
            '--strategy', self.strategy
        ]
        with self._with_agent_env('context'):
            result = self._run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout and (
                not result.stderr or "No changes made" not in result.stderr):
            changes_made = True
        # Create tests file if it doesn't exist and the code file is not already a test file
        if not tests_file.exists() and not base.startswith('test_'):
            content = """# Tests for {code_file.name}
import pytest

def test_placeholder():
    \"\"\"Placeholder test - replace with actual tests.\"\"\"
    assert True

## Add more tests here
"""
            # Tests are Python files; do not run markdown normalization on them
            tests_file.write_text(content, encoding='utf-8')
            logging.info(f"Created {tests_file.relative_to(self.repo_root)}")
            changes_made = True
        # Update tests - if this is a test file, update it directly; otherwise
        # update the associated test file
        if base.startswith('test_'):
            # This is already a test file, update it directly
            test_file_to_update = code_file
            prompt = f"Update and expand the test suite for {base.replace('test_', '')}"
        else:
            # This is a code file, update its associated test file
            test_file_to_update = tests_file
            prompt = f"Update and expand the test suite for {code_file.name}"
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent / 'agent_tests.py'),
            '--context', str(test_file_to_update),
            '--prompt', prompt,
            '--strategy', self.strategy
        ]
        with self._with_agent_env('tests'):
            result = self._run_command(cmd)
        if result.stdout and "No changes made" not in result.stdout and (
                not result.stderr or "No changes made" not in result.stderr):
            changes_made = True
        return bool(changes_made)

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
        """Register a webhook URL for event notifications.

        Registers a webhook URL that will receive POST requests for agent events
        (file processing, completion, errors, etc.). Useful for integration with
        external systems like Slack, Discord, or custom monitoring dashboards.

        Args:
            webhook_url: Full URL of the webhook endpoint.

        Returns:
            None. Logs registration.

        Example:
            agent.register_webhook('https://hooks.slack.com / services / xxx')
            agent.register_webhook('https://example.com / agent-events')

        Note:
            - Multiple webhooks can be registered
            - Webhooks are sent asynchronously and don't block execution
            - Failed webhook sends are logged but don't halt execution
        """
        self.webhooks.append(webhook_url)
        logging.info(f"Registered webhook: {webhook_url}")

    def register_callback(self, callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """Register a callback function for agent events.

        Registers a Python callable that will be invoked for agent events.
        Callbacks are called synchronously and can receive event data.

        Args:
            callback: Callable accepting (event_name: str, event_data: Dict).

        Returns:
            None. Logs registration.

        Example:
            def my_callback(event_name: str, event_data: Dict):
                print(f"Event: {event_name}")
                print(f"Data: {event_data}")

            agent.register_callback(my_callback)

        Note:
            - Multiple callbacks can be registered
            - Callbacks are called in registration order
            - Exceptions in callbacks are caught and logged
        """
        self.callbacks.append(callback)
        callback_name = getattr(callback, '__name__', repr(callback))
        logging.info(f"Registered callback: {callback_name}")

    def send_webhook_notification(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Send notification to all registered webhooks.

        Sends event notifications to all registered webhook URLs via HTTP POST.
        Uses JSON encoding for the payload. Failed sends are logged but don't halt.

        Args:
            event_name: Name of the event (e.g., 'file_processed', 'error').
            event_data: Event data as dictionary (will be JSON - encoded).

        Returns:
            None. Logs results.

        Example:
            agent.send_webhook_notification('agent_complete', {
                'files_processed': 42,
                'files_modified': 15,
                'duration_seconds': 123.45
            })

        Note:
            - Webhooks are sent asynchronously in background threads
            - If requests library not available, webhooks are skipped
            - Timeouts are set to 5 seconds per webhook
        """
        if not HAS_REQUESTS or requests is None or not self.webhooks:
            return

        payload: dict[str, Any] = {
            'event': event_name,
            'timestamp': time.time(),
            'data': event_data
        }

        for webhook_url in self.webhooks:
            try:
                logging.debug(f"Sending webhook: {webhook_url}")
                requests.post(
                    webhook_url,
                    json=payload,
                    timeout=5
                )
                logging.debug(f"Webhook sent successfully to {webhook_url}")
            except Exception as e:
                logging.warning(f"Failed to send webhook to {webhook_url}: {e}")

    def execute_callbacks(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Execute all registered callback functions for an event.

        Invokes all registered callback functions with event data.
        Exceptions in callbacks are caught and logged, allowing other callbacks to run.

        Args:
            event_name: Name of the event (e.g., 'file_processed').
            event_data: Event data to pass to callbacks.

        Returns:
            None. Logs execution results.

        Example:
            agent.execute_callbacks('processing_complete', {
                'file': 'main.py',
                'changes_made': True
            })

        Note:
            - Callbacks are called synchronously in registration order
            - Exceptions in one callback don't prevent others from running
            - Failures are logged as warnings but don't halt execution
        """
        for callback in self.callbacks:
            try:
                callback_name = getattr(callback, '__name__', repr(callback))
                logging.debug(f"Executing callback: {callback_name}")
                callback(event_name, event_data)
            except Exception as e:
                callback_name = getattr(callback, '__name__', repr(callback))
                logging.warning(f"Callback {callback_name} failed: {e}")

    async def async_process_files(self, files: List[Path]) -> List[Path]:
        """Process multiple files concurrently using async / await.

        Processes files concurrently using asyncio for I / O - bound operations.
        Useful when the bottleneck is waiting for external services rather than CPU.
        Returns immediately; file processing happens asynchronously.

        Args:
            files: List of file paths to process.

        Returns:
            List[Path]: List of files that were modified.

        Example:
            files=agent.find_code_files()
            modified=await agent.async_process_files(files)
            print(f"Modified {len(modified)} files")

        Note:
            - Requires enable_async=True in __init__
            - Uses ThreadPoolExecutor for I / O operations
            - Respects max_workers setting
            - File processing happens in separate threads
            - Modified files are tracked in metrics
        """
        modified_files: list[Path] = []
        import concurrent.futures

        loop = asyncio.get_running_loop()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            async def process_file_async(file_path: Path) -> None:
                """Process a single file asynchronously."""
                try:
                    logging.debug(f"[async] Processing {file_path.name}")
                    await loop.run_in_executor(executor, self.process_file, file_path)
                    modified_files.append(file_path)
                    self.metrics['files_processed'] += 1
                    logging.info(f"[async] Completed {file_path.name}")
                except Exception as e:
                    logging.error(f"[async] Failed to process {file_path.name}: {e}")

            # Create tasks for all files
            tasks = [process_file_async(f) for f in files]

            # Run tasks concurrently
            if tasks:
                await asyncio.gather(*tasks)

        return modified_files

    def process_files_multiprocessing(self, files: List[Path]) -> List[Path]:
        """Process multiple files using multiprocessing for parallel execution.

        Processes files in parallel using separate Python processes.
        Useful for CPU - intensive operations or avoiding Python's GIL.
        Each worker processes multiple files sequentially.

        Args:
            files: List of file paths to process.

        Returns:
            List[Path]: List of files that were processed.

        Example:
            files=agent.find_code_files()
            processed=agent.process_files_multiprocessing(files)
            print(f"Processed {len(processed)} files")

        Note:
            - Requires enable_multiprocessing=True in __init__
            - Uses ProcessPoolExecutor for CPU - bound operations
            - Respects max_workers setting
            - Each worker has its own Python interpreter
            - Progress tracking works with tqdm if available
            - Modified count is estimated from total processed
        """
        processed_files = []

        # Use ThreadPoolExecutor for parallel processing (easier pickling than ProcessPoolExecutor)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Create partial functions that can be pickled more easily
            worker_func = functools.partial(_multiprocessing_worker, self)

            results = list(tqdm(
                executor.map(worker_func, files),
                total=len(files),
                desc="Processing files (multiprocessing)"
            ) if HAS_TQDM else executor.map(worker_func, files))

        # Filter out None results
        processed_files = [f for f in results if f is not None]
        self.metrics['files_processed'] = len(processed_files)

        return processed_files

    def process_files_threaded(self, files: List[Path]) -> List[Path]:
        """Process multiple files using threading for concurrent I / O.

        Processes files concurrently using worker threads. Good for I / O - bound
        operations while keeping code simpler than async. Works around Python's GIL.

        Args:
            files: List of file paths to process.

        Returns:
            List[Path]: List of files that were processed.

        Example:
            files=agent.find_code_files()
            processed=agent.process_files_threaded(files)
            print(f"Processed {len(processed)} files")

        Note:
            - Uses ThreadPoolExecutor for concurrent I / O
            - Respects max_workers setting
            - Good middle ground between sequential and multiprocessing
            - Shared state (metrics) is updated from worker threads
            - Progress tracking with tqdm if available
        """
        processed_files: list[Path] = []

        def worker_thread_process_file(file_path: Path) -> Optional[Path]:
            """Worker function to process a file in a separate thread."""
            try:
                logging.debug(f"[thread] Processing {file_path.name}")
                self.process_file(file_path)
                logging.info(f"[thread] Completed {file_path.name}")
                return file_path
            except Exception as e:
                logging.error(f"[thread] Failed: {e}")
                return None

        # Use ThreadPoolExecutor for parallel I / O
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(tqdm(
                executor.map(worker_thread_process_file, files),
                total=len(files),
                desc="Processing files (threaded)"
            ) if HAS_TQDM else executor.map(worker_thread_process_file, files))

        # Filter out None results
        processed_files = [f for f in results if f is not None]
        self.metrics['files_processed'] = len(processed_files)

        return processed_files

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
                logging.info(f"Iteration {iteration} for {code_file.name}")
                files_ready = self._check_files_ready(code_file)
                if not files_ready and iteration == 1:
                    logging.info(f"Creating initial supporting files for {code_file.name}")
                changes_made = self._perform_iteration(code_file)
                # Check if all is marked as fixed (no more changes needed)
                if not changes_made:
                    all_fixed = True
                    logging.info(f"No changes made in iteration {iteration}, marking as fixed")
                else:
                    logging.info(f"Changes made in iteration {iteration}, continuing...")
            if iteration >= max_iterations:
                logging.info(f"Reached maximum iterations ({max_iterations}) for {code_file.name}")
            logging.info(f"Completed processing {code_file.name} in {iteration} iterations")
            self._commit_and_push(code_file)

            # Mark as processed for incremental processing
            if hasattr(self, 'incremental_processor'):
                self.incremental_processor.mark_processed(code_file)

            # Mark completed for graceful shutdown
            if hasattr(self, 'shutdown_handler'):
                self.shutdown_handler.mark_completed(code_file)

        finally:
            # Release file lock
            if hasattr(self, 'lock_manager'):
                self.lock_manager.release_lock(code_file)

            # Clear current file
            if hasattr(self, 'shutdown_handler'):
                self.shutdown_handler.set_current_file(None)

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
                def run(self, file_path, context):
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

                result = plugin.run(file_path, context)
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
