#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE - 2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Agent: Orchestrates work among sub - agents for code improvement.

Assigns tasks to various agents to improve code files, their documentation,
tests, and related artifacts.

## Description
This module provides the main Agent that coordinates the improvement process
across code files by calling specialized sub - agents for different aspects
of code quality and documentation.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add better error handling
- Implement async execution for agents

## Improvements
- Enhanced coordination between agents
- Better progress tracking
"""

import subprocess
import sys
import os
import logging
import uuid
from pathlib import Path
from typing import List, Set, Optional, Dict, Any, Callable
import argparse
import fnmatch
import importlib.util
import time
import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import json
import hashlib
import signal
import threading
import difflib
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

    def tqdm(iterable, *args, **kwargs):
        """Fallback if tqdm not available."""
        return iterable


# Import markdown fixing functionality


def _load_fix_markdown_content() -> callable:
    """Load the markdown fixer module dynamically."""
    fix_dir = Path(__file__).parent.parent / 'fix'
    spec = importlib.util.spec_from_file_location(
        "fix_markdown_lint", str(fix_dir / "fix_markdown_lint.py"))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules["fix_markdown_lint"] = module
        spec.loader.exec_module(module)
        return module.fix_markdown_content
    return lambda x: x  # Fallback


fix_markdown_content = _load_fix_markdown_content()


# Global cache for .codeignore patterns to avoid re - parsing
_CODEIGNORE_CACHE: Dict[str, Set[str]] = {}
_CODEIGNORE_CACHE_TIME: Dict[str, float] = {}


# =============================================================================
# Enums for Type Safety
# =============================================================================


class AgentExecutionState(Enum):
    """Execution state for an agent run."""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()
    PAUSED = auto()


class RateLimitStrategy(Enum):
    """Rate limiting strategy for API calls."""
    FIXED_WINDOW = auto()      # Fixed time window rate limiting
    SLIDING_WINDOW = auto()    # Sliding window rate limiting
    TOKEN_BUCKET = auto()      # Token bucket algorithm
    LEAKY_BUCKET = auto()      # Leaky bucket algorithm


class ConfigFormat(Enum):
    """Configuration file format."""
    YAML = auto()
    TOML = auto()
    JSON = auto()
    INI = auto()


class LockType(Enum):
    """File locking type."""
    SHARED = auto()       # Multiple readers allowed
    EXCLUSIVE = auto()    # Single writer only
    ADVISORY = auto()     # Advisory lock (not enforced by OS)


class DiffOutputFormat(Enum):
    """Output format for diff preview."""
    UNIFIED = auto()      # Unified diff format
    CONTEXT = auto()      # Context diff format
    SIDE_BY_SIDE = auto()  # Side by side diff
    HTML = auto()         # HTML formatted diff


class AgentPriority(Enum):
    """Priority level for agent execution."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


class HealthStatus(Enum):
    """Health status for components."""
    HEALTHY = auto()
    DEGRADED = auto()
    UNHEALTHY = auto()
    UNKNOWN = auto()


# =============================================================================
# Dataclasses for Data Structures
# =============================================================================


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting.

    Attributes:
        requests_per_second: Maximum requests per second.
        requests_per_minute: Maximum requests per minute.
        burst_size: Maximum burst size for token bucket.
        strategy: Rate limiting strategy to use.
        cooldown_seconds: Cooldown period after hitting limit.
    """
    requests_per_second: float = 10.0
    requests_per_minute: int = 60
    burst_size: int = 10
    strategy: RateLimitStrategy = RateLimitStrategy.TOKEN_BUCKET
    cooldown_seconds: float = 1.0


@dataclass
class AgentPluginConfig:
    """Configuration for an agent plugin.

    Attributes:
        name: Unique plugin name.
        module_path: Path to the plugin module.
        entry_point: Entry point function name.
        priority: Execution priority.
        enabled: Whether the plugin is enabled.
        config: Plugin - specific configuration.
    """
    name: str
    module_path: str
    entry_point: str = "run"
    priority: AgentPriority = AgentPriority.NORMAL
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FileLock:
    """File lock information.

    Attributes:
        file_path: Path to the locked file.
        lock_type: Type of lock.
        owner: Lock owner identifier.
        acquired_at: Timestamp when lock was acquired.
        expires_at: Timestamp when lock expires (optional).
    """
    file_path: Path
    lock_type: LockType
    owner: str
    acquired_at: float
    expires_at: Optional[float] = None


@dataclass
class DiffResult:
    """Result of a diff operation.

    Attributes:
        file_path: Path to the file.
        original_content: Original file content.
        modified_content: Modified content after changes.
        diff_lines: List of diff lines.
        additions: Number of lines added.
        deletions: Number of lines deleted.
        changes: Number of lines changed.
    """
    file_path: Path
    original_content: str
    modified_content: str
    diff_lines: List[str] = field(default_factory=list)
    additions: int = 0
    deletions: int = 0
    changes: int = 0


@dataclass
class IncrementalState:
    """State for incremental processing.

    Attributes:
        last_run_timestamp: Timestamp of last successful run.
        processed_files: Dict of file paths to their last processed timestamp.
        file_hashes: Dict of file paths to their content hashes.
        pending_files: List of files pending processing.
    """
    last_run_timestamp: float = 0.0
    processed_files: Dict[str, float] = field(default_factory=dict)
    file_hashes: Dict[str, str] = field(default_factory=dict)
    pending_files: List[str] = field(default_factory=list)


@dataclass
class AgentHealthCheck:
    """Health check result for an agent.

    Attributes:
        agent_name: Name of the agent.
        status: Health status.
        response_time_ms: Response time in milliseconds.
        last_check: Timestamp of last health check.
        error_message: Error message if unhealthy.
        details: Additional health details.
    """
    agent_name: str
    status: HealthStatus
    response_time_ms: float = 0.0
    last_check: float = field(default_factory=time.time)
    error_message: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShutdownState:
    """State for graceful shutdown.

    Attributes:
        shutdown_requested: Whether shutdown has been requested.
        current_file: Currently processing file.
        completed_files: List of completed files.
        pending_files: List of pending files.
        start_time: Processing start time.
    """
    shutdown_requested: bool = False
    current_file: Optional[str] = None
    completed_files: List[str] = field(default_factory=list)
    pending_files: List[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)


@dataclass
class AgentConfig:
    """Full agent configuration loaded from config file.

    Attributes:
        repo_root: Repository root directory.
        agents_only: Process only agent files.
        max_files: Maximum files to process.
        loop: Number of processing loops.
        dry_run: Preview mode without modifications.
        no_git: Skip git operations.
        verbosity: Logging verbosity level.
        rate_limit: Rate limiting configuration.
        plugins: List of plugin configurations.
        selective_agents: Agents to execute.
        timeout_per_agent: Timeout settings per agent.
    """
    repo_root: str = "."
    agents_only: bool = False
    max_files: Optional[int] = None
    loop: int = 1
    dry_run: bool = False
    no_git: bool = False
    verbosity: str = "normal"
    rate_limit: Optional[RateLimitConfig] = None
    plugins: List[AgentPluginConfig] = field(default_factory=list)
    selective_agents: List[str] = field(default_factory=list)
    timeout_per_agent: Dict[str, int] = field(default_factory=dict)


# =============================================================================
# Plugin Base Class
# =============================================================================


class AgentPluginBase(ABC):
    """Abstract base class for agent plugins.

    Provides interface for third - party agents to integrate with
    the agent orchestrator without modifying core code.

    Attributes:
        name: Plugin name.
        priority: Execution priority.
        config: Plugin configuration.
    """

    def __init__(self, name: str, priority: AgentPriority = AgentPriority.NORMAL,
                 config: Optional[Dict[str, Any]] = None):
        """Initialize the plugin.

        Args:
            name: Unique plugin name.
            priority: Execution priority.
            config: Plugin - specific configuration.
        """
        self.name = name
        self.priority = priority
        self.config = config or {}
        self.logger = logging.getLogger(f"plugin.{name}")

    @abstractmethod
    def run(self, file_path: Path, context: Dict[str, Any]) -> bool:
        """Execute the plugin on a file.

        Args:
            file_path: Path to the file to process.
            context: Execution context with agent state.

        Returns:
            bool: True if changes were made, False otherwise.
        """

    def setup(self) -> None:
        """Called once when plugin is loaded. Override for initialization."""

    def teardown(self) -> None:
        """Called once when plugin is unloaded. Override for cleanup."""

    def health_check(self) -> AgentHealthCheck:
        """Check plugin health status.

        Returns:
            AgentHealthCheck: Health check result.
        """
        return AgentHealthCheck(
            agent_name=self.name,
            status=HealthStatus.HEALTHY
        )


# =============================================================================
# Rate Limiter
# =============================================================================


class RateLimiter:
    """Rate limiter for API calls using token bucket algorithm.

    Manages API call rate to prevent throttling and ensure fair usage.
    Supports multiple strategies and configurable limits.

    Attributes:
        config: Rate limiting configuration.
        tokens: Current number of available tokens.
        last_refill: Timestamp of last token refill.
    """

    def __init__(self, config: Optional[RateLimitConfig] = None):
        """Initialize the rate limiter.

        Args:
            config: Rate limiting configuration. Uses defaults if not provided.
        """
        self.config = config or RateLimitConfig()
        self.tokens = float(self.config.burst_size)
        self.last_refill = time.time()
        self._lock = threading.Lock()
        self._request_timestamps: List[float] = []

    def _refill_tokens(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        refill_amount = elapsed * self.config.requests_per_second
        self.tokens = min(self.config.burst_size, self.tokens + refill_amount)
        self.last_refill = now

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Acquire a token for making an API call.

        Blocks until a token is available or timeout expires.

        Args:
            timeout: Maximum time to wait for a token. None=wait forever.

        Returns:
            bool: True if token acquired, False if timeout.
        """
        start_time = time.time()

        while True:
            with self._lock:
                self._refill_tokens()

                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    self._request_timestamps.append(time.time())
                    # Clean old timestamps
                    cutoff = time.time() - 60
                    self._request_timestamps = [
                        t for t in self._request_timestamps if t > cutoff
                    ]
                    return True

            # Check timeout
            if timeout is not None and (time.time() - start_time) >= timeout:
                return False

            # Wait before retry
            time.sleep(self.config.cooldown_seconds)

    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics.

        Returns:
            Dict with current tokens, request count, etc.
        """
        with self._lock:
            return {
                "tokens_available": self.tokens,
                "requests_last_minute": len(self._request_timestamps),
                "requests_per_second": self.config.requests_per_second,
                "burst_size": self.config.burst_size,
            }


# =============================================================================
# File Lock Manager
# =============================================================================


class FileLockManager:
    """Manages file locks to prevent concurrent modifications.

    Provides advisory file locking to coordinate access between
    multiple agent instances or processes.

    Attributes:
        locks: Dict of active file locks.
        lock_timeout: Default lock timeout in seconds.
    """

    def __init__(self, lock_timeout: float = 300.0):
        """Initialize the lock manager.

        Args:
            lock_timeout: Default lock timeout in seconds.
        """
        self.locks: Dict[str, FileLock] = {}
        self.lock_timeout = lock_timeout
        self._lock = threading.Lock()
        self._owner_id = f"{os.getpid()}_{threading.current_thread().ident}"

    def acquire_lock(self, file_path: Path,
                     lock_type: LockType = LockType.EXCLUSIVE,
                     timeout: Optional[float] = None) -> Optional[FileLock]:
        """Acquire a lock on a file.

        Args:
            file_path: Path to file to lock.
            lock_type: Type of lock to acquire.
            timeout: Timeout for acquiring lock.

        Returns:
            FileLock if acquired, None if timeout.
        """
        path_str = str(file_path.resolve())
        timeout = timeout or self.lock_timeout
        start_time = time.time()

        while True:
            with self._lock:
                # Check for expired locks
                self._cleanup_expired_locks()

                # Check if already locked
                existing_lock = self.locks.get(path_str)
                if existing_lock is None:
                    # Acquire new lock
                    lock = FileLock(
                        file_path=file_path,
                        lock_type=lock_type,
                        owner=self._owner_id,
                        acquired_at=time.time(),
                        expires_at=time.time() + self.lock_timeout
                    )
                    self.locks[path_str] = lock
                    logging.debug(f"Acquired {lock_type.name} lock on {file_path}")
                    return lock
                elif (existing_lock.lock_type == LockType.SHARED and
                      lock_type == LockType.SHARED):
                    # Shared locks can coexist
                    return existing_lock

            # Check timeout
            if (time.time() - start_time) >= timeout:
                logging.warning(f"Timeout acquiring lock on {file_path}")
                return None

            time.sleep(0.1)

    def release_lock(self, file_path: Path) -> bool:
        """Release a lock on a file.

        Args:
            file_path: Path to file to unlock.

        Returns:
            bool: True if lock released, False if not owner.
        """
        path_str = str(file_path.resolve())

        with self._lock:
            lock = self.locks.get(path_str)
            if lock and lock.owner == self._owner_id:
                del self.locks[path_str]
                logging.debug(f"Released lock on {file_path}")
                return True
            return False

    def _cleanup_expired_locks(self) -> None:
        """Remove expired locks."""
        now = time.time()
        expired = [
            path for path, lock in self.locks.items()
            if lock.expires_at and lock.expires_at < now
        ]
        for path in expired:
            logging.debug(f"Cleaning up expired lock on {path}")
            del self.locks[path]


# =============================================================================
# Diff Generator
# =============================================================================


class DiffGenerator:
    """Generates diffs to preview changes before applying them.

    Creates human - readable diffs in various formats to allow
    users to review changes before they are applied.

    Attributes:
        output_format: Default output format for diffs.
        context_lines: Number of context lines in diff.
    """

    def __init__(self, output_format: DiffOutputFormat = DiffOutputFormat.UNIFIED,
                 context_lines: int = 3):
        """Initialize the diff generator.

        Args:
            output_format: Default output format.
            context_lines: Number of context lines.
        """
        self.output_format = output_format
        self.context_lines = context_lines

    def generate_diff(self, file_path: Path, original: str,
                      modified: str) -> DiffResult:
        """Generate a diff between original and modified content.

        Args:
            file_path: Path to the file.
            original: Original file content.
            modified: Modified content.

        Returns:
            DiffResult with diff information.
        """
        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)

        # Generate unified diff
        diff_lines = list(difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile=f"a/{file_path.name}",
            tofile=f"b/{file_path.name}",
            n=self.context_lines
        ))

        # Count additions and deletions
        additions = sum(1 for line in diff_lines if line.startswith('+')
                        and not line.startswith('+++'))
        deletions = sum(1 for line in diff_lines if line.startswith('-')
                        and not line.startswith('---'))

        return DiffResult(
            file_path=file_path,
            original_content=original,
            modified_content=modified,
            diff_lines=diff_lines,
            additions=additions,
            deletions=deletions,
            changes=additions + deletions
        )

    def format_diff(self, diff_result: DiffResult,
                    output_format: Optional[DiffOutputFormat] = None) -> str:
        """Format a diff result for display.

        Args:
            diff_result: DiffResult to format.
            output_format: Output format (uses default if not provided).

        Returns:
            Formatted diff string.
        """
        fmt = output_format or self.output_format

        if fmt == DiffOutputFormat.UNIFIED:
            return ''.join(diff_result.diff_lines)
        elif fmt == DiffOutputFormat.CONTEXT:
            original = diff_result.original_content.splitlines(keepends=True)
            modified = diff_result.modified_content.splitlines(keepends=True)
            return ''.join(difflib.context_diff(
                original, modified,
                fromfile=f"a/{diff_result.file_path.name}",
                tofile=f"b/{diff_result.file_path.name}",
                n=self.context_lines
            ))
        elif fmt == DiffOutputFormat.HTML:
            differ = difflib.HtmlDiff()
            original = diff_result.original_content.splitlines()
            modified = diff_result.modified_content.splitlines()
            return differ.make_file(original, modified)
        else:
            return ''.join(diff_result.diff_lines)

    def print_diff(self, diff_result: DiffResult) -> None:
        """Print a colorized diff to console.

        Args:
            diff_result: DiffResult to print.
        """
        for line in diff_result.diff_lines:
            if line.startswith('+') and not line.startswith('+++'):
                print(f"\033[92m{line}\033[0m", end='')  # Green
            elif line.startswith('-') and not line.startswith('---'):
                print(f"\033[91m{line}\033[0m", end='')  # Red
            elif line.startswith('@@'):
                print(f"\033[96m{line}\033[0m", end='')  # Cyan
            else:
                print(line, end='')


# =============================================================================
# Incremental Processor
# =============================================================================


class IncrementalProcessor:
    """Processes only files changed since last run.

    Tracks file modification times and content hashes to enable
    incremental processing, avoiding reprocessing unchanged files.

    Attributes:
        state_file: Path to state persistence file.
        state: Current incremental processing state.
    """

    def __init__(self, repo_root: Path, state_file: str = ".agent_state.json"):
        """Initialize the incremental processor.

        Args:
            repo_root: Repository root directory.
            state_file: Name of state file.
        """
        self.repo_root = repo_root
        self.state_file = repo_root / state_file
        self.state = IncrementalState()
        self._load_state()

    def _load_state(self) -> None:
        """Load state from disk."""
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text())
                self.state = IncrementalState(
                    last_run_timestamp=data.get('last_run_timestamp', 0),
                    processed_files=data.get('processed_files', {}),
                    file_hashes=data.get('file_hashes', {}),
                    pending_files=data.get('pending_files', [])
                )
                logging.debug(f"Loaded incremental state from {self.state_file}")
            except Exception as e:
                logging.warning(f"Failed to load state: {e}")

    def _save_state(self) -> None:
        """Save state to disk."""
        try:
            data = {
                'last_run_timestamp': self.state.last_run_timestamp,
                'processed_files': self.state.processed_files,
                'file_hashes': self.state.file_hashes,
                'pending_files': self.state.pending_files
            }
            self.state_file.write_text(json.dumps(data, indent=2))
            logging.debug(f"Saved incremental state to {self.state_file}")
        except Exception as e:
            logging.warning(f"Failed to save state: {e}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute MD5 hash of file content."""
        try:
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except Exception:
            return ""

    def get_changed_files(self, files: List[Path]) -> List[Path]:
        """Get list of files changed since last run.

        Args:
            files: List of all files to consider.

        Returns:
            List of files that have changed.
        """
        changed = []

        for file_path in files:
            path_str = str(file_path)

            # Check if file is new
            if path_str not in self.state.processed_files:
                changed.append(file_path)
                continue

            # Check if file was modified
            try:
                mtime = file_path.stat().st_mtime
                if mtime > self.state.processed_files.get(path_str, 0):
                    # Verify with hash comparison
                    new_hash = self._compute_file_hash(file_path)
                    if new_hash != self.state.file_hashes.get(path_str, ""):
                        changed.append(file_path)
            except Exception:
                changed.append(file_path)

        logging.info(f"Incremental: {len(changed)}/{len(files)} files changed")
        return changed

    def mark_processed(self, file_path: Path) -> None:
        """Mark a file as processed.

        Args:
            file_path: Path to the processed file.
        """
        path_str = str(file_path)
        self.state.processed_files[path_str] = time.time()
        self.state.file_hashes[path_str] = self._compute_file_hash(file_path)

        # Remove from pending if present
        if path_str in self.state.pending_files:
            self.state.pending_files.remove(path_str)

    def complete_run(self) -> None:
        """Mark the run as complete and save state."""
        self.state.last_run_timestamp = time.time()
        self.state.pending_files = []
        self._save_state()

    def reset_state(self) -> None:
        """Reset incremental state (force full reprocessing)."""
        self.state = IncrementalState()
        if self.state_file.exists():
            self.state_file.unlink()
        logging.info("Incremental state reset")


# =============================================================================
# Graceful Shutdown Handler
# =============================================================================


class GracefulShutdown:
    """Handles graceful shutdown with state persistence.

    Captures SIGINT / SIGTERM and allows current operation to complete
    before stopping, saving state for resume.

    Attributes:
        state: Current shutdown state.
        state_file: Path to state persistence file.
    """

    def __init__(self, repo_root: Path, state_file: str = ".agent_shutdown.json"):
        """Initialize graceful shutdown handler.

        Args:
            repo_root: Repository root directory.
            state_file: Name of state file.
        """
        self.repo_root = repo_root
        self.state_file = repo_root / state_file
        self.state = ShutdownState()
        self._original_sigint = None
        self._original_sigterm = None

    def install_handlers(self) -> None:
        """Install signal handlers for graceful shutdown."""
        self._original_sigint = signal.signal(signal.SIGINT, self._handle_signal)
        if hasattr(signal, 'SIGTERM'):
            self._original_sigterm = signal.signal(signal.SIGTERM, self._handle_signal)
        logging.debug("Installed graceful shutdown handlers")

    def restore_handlers(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint:
            signal.signal(signal.SIGINT, self._original_sigint)
        if self._original_sigterm and hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self._original_sigterm)
        logging.debug("Restored original signal handlers")

    def _handle_signal(self, signum: int, frame: Any) -> None:
        """Handle shutdown signal."""
        signal_name = signal.Signals(signum).name
        logging.warning(f"Received {signal_name}, initiating graceful shutdown...")
        self.state.shutdown_requested = True
        self._save_state()

    def should_continue(self) -> bool:
        """Check if processing should continue.

        Returns:
            bool: True if should continue, False if shutdown requested.
        """
        return not self.state.shutdown_requested

    def set_current_file(self, file_path: Optional[Path]) -> None:
        """Set the currently processing file.

        Args:
            file_path: Path to current file, or None if not processing.
        """
        self.state.current_file = str(file_path) if file_path else None

    def mark_completed(self, file_path: Path) -> None:
        """Mark a file as completed.

        Args:
            file_path: Path to completed file.
        """
        self.state.completed_files.append(str(file_path))
        if str(file_path) in self.state.pending_files:
            self.state.pending_files.remove(str(file_path))

    def set_pending_files(self, files: List[Path]) -> None:
        """Set the list of pending files.

        Args:
            files: List of pending file paths.
        """
        self.state.pending_files = [str(f) for f in files]

    def _save_state(self) -> None:
        """Save shutdown state to disk."""
        try:
            data = {
                'shutdown_requested': self.state.shutdown_requested,
                'current_file': self.state.current_file,
                'completed_files': self.state.completed_files,
                'pending_files': self.state.pending_files,
                'start_time': self.state.start_time
            }
            self.state_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logging.error(f"Failed to save shutdown state: {e}")

    def load_resume_state(self) -> Optional[ShutdownState]:
        """Load state for resuming an interrupted run.

        Returns:
            ShutdownState if resume state exists, None otherwise.
        """
        if not self.state_file.exists():
            return None

        try:
            data = json.loads(self.state_file.read_text())
            state = ShutdownState(
                shutdown_requested=False,  # Reset for resume
                current_file=data.get('current_file'),
                completed_files=data.get('completed_files', []),
                pending_files=data.get('pending_files', []),
                start_time=data.get('start_time', time.time())
            )
            logging.info(f"Loaded resume state: {len(state.completed_files)} completed, "
                         f"{len(state.pending_files)} pending")
            return state
        except Exception as e:
            logging.warning(f"Failed to load resume state: {e}")
            return None

    def cleanup(self) -> None:
        """Clean up state file after successful completion."""
        if self.state_file.exists():
            self.state_file.unlink()
        self.restore_handlers()


# =============================================================================
# Configuration File Loader
# =============================================================================


class ConfigLoader:
    """Loads agent configuration from YAML / TOML / JSON files.

    Supports multiple configuration file formats and provides
    validation and merging of configuration options.

    Attributes:
        config_path: Path to configuration file.
        format: Configuration file format.
    """

    SUPPORTED_EXTENSIONS = {
        '.yaml': ConfigFormat.YAML,
        '.yml': ConfigFormat.YAML,
        '.toml': ConfigFormat.TOML,
        '.json': ConfigFormat.JSON,
        '.ini': ConfigFormat.INI,
    }

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the config loader.

        Args:
            config_path: Path to configuration file.
        """
        self.config_path = config_path
        self.format: Optional[ConfigFormat] = None

        if config_path:
            ext = config_path.suffix.lower()
            self.format = self.SUPPORTED_EXTENSIONS.get(ext)

    def load(self) -> AgentConfig:
        """Load configuration from file.

        Returns:
            AgentConfig with loaded settings.
        """
        if not self.config_path or not self.config_path.exists():
            return AgentConfig()

        try:
            content = self.config_path.read_text()
            data = self._parse_content(content)
            return self._build_config(data)
        except Exception as e:
            logging.error(f"Failed to load config from {self.config_path}: {e}")
            return AgentConfig()

    def _parse_content(self, content: str) -> Dict[str, Any]:
        """Parse configuration content based on format."""
        if self.format == ConfigFormat.JSON:
            return json.loads(content)
        elif self.format == ConfigFormat.YAML:
            try:
                import yaml
                return yaml.safe_load(content)
            except ImportError:
                logging.warning("PyYAML not installed, falling back to JSON")
                return {}
        elif self.format == ConfigFormat.TOML:
            try:
                import tomllib
                return tomllib.loads(content)
            except ImportError:
                try:
                    import toml
                    return toml.loads(content)
                except ImportError:
                    logging.warning("tomllib / toml not installed")
                    return {}
        return {}

    def _build_config(self, data: Dict[str, Any]) -> AgentConfig:
        """Build AgentConfig from parsed data."""
        # Build rate limit config
        rate_limit = None
        if 'rate_limit' in data:
            rl_data = data['rate_limit']
            rate_limit = RateLimitConfig(
                requests_per_second=rl_data.get('requests_per_second', 10.0),
                requests_per_minute=rl_data.get('requests_per_minute', 60),
                burst_size=rl_data.get('burst_size', 10),
                cooldown_seconds=rl_data.get('cooldown_seconds', 1.0)
            )

        # Build plugin configs
        plugins = []
        for plugin_data in data.get('plugins', []):
            plugins.append(AgentPluginConfig(
                name=plugin_data.get('name', 'unknown'),
                module_path=plugin_data.get('module_path', ''),
                entry_point=plugin_data.get('entry_point', 'run'),
                enabled=plugin_data.get('enabled', True),
                config=plugin_data.get('config', {})
            ))

        return AgentConfig(
            repo_root=data.get('repo_root', '.'),
            agents_only=data.get('agents_only', False),
            max_files=data.get('max_files'),
            loop=data.get('loop', 1),
            dry_run=data.get('dry_run', False),
            no_git=data.get('no_git', False),
            verbosity=data.get('verbosity', 'normal'),
            rate_limit=rate_limit,
            plugins=plugins,
            selective_agents=data.get('selective_agents', []),
            timeout_per_agent=data.get('timeout_per_agent', {})
        )

    @staticmethod
    def find_config_file(repo_root: Path) -> Optional[Path]:
        """Find configuration file in repository.

        Args:
            repo_root: Repository root directory.

        Returns:
            Path to config file if found, None otherwise.
        """
        config_names = [
            'agent.yaml', 'agent.yml', 'agent.toml', 'agent.json',
            '.agent.yaml', '.agent.yml', '.agent.toml', '.agent.json',
            'agent_config.yaml', 'agent_config.json'
        ]

        for name in config_names:
            config_path = repo_root / name
            if config_path.exists():
                logging.info(f"Found config file: {config_path}")
                return config_path

        return None


# =============================================================================
# Health Checker
# =============================================================================


class HealthChecker:
    """Performs health checks on agent components.

    Verifies that all required components are available and functional
    before starting agent execution.

    Attributes:
        repo_root: Repository root directory.
        results: Dict of health check results.
    """

    def __init__(self, repo_root: Path):
        """Initialize the health checker.

        Args:
            repo_root: Repository root directory.
        """
        self.repo_root = repo_root
        self.results: Dict[str, AgentHealthCheck] = {}

    def check_agent_script(self, agent_name: str) -> AgentHealthCheck:
        """Check if an agent script exists and is valid.

        Args:
            agent_name: Name of the agent (e.g., 'coder', 'tests').

        Returns:
            AgentHealthCheck result.
        """
        start_time = time.time()
        script_path = self.repo_root / 'scripts' / 'agent' / f'agent-{agent_name}.py'

        if not script_path.exists():
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Script not found: {script_path}"
            )

        # Check if script is valid Python
        try:
            import ast
            content = script_path.read_text()
            ast.parse(content)
            response_time = (time.time() - start_time) * 1000
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.HEALTHY,
                response_time_ms=response_time,
                details={'script_path': str(script_path)}
            )
        except SyntaxError as e:
            return AgentHealthCheck(
                agent_name=agent_name,
                status=HealthStatus.UNHEALTHY,
                error_message=f"Syntax error: {e}"
            )

    def check_git(self) -> AgentHealthCheck:
        """Check if git is available.

        Returns:
            AgentHealthCheck result.
        """
        start_time = time.time()

        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            response_time = (time.time() - start_time) * 1000

            if result.returncode == 0:
                return AgentHealthCheck(
                    agent_name='git',
                    status=HealthStatus.HEALTHY,
                    response_time_ms=response_time,
                    details={'version': result.stdout.strip()}
                )
            else:
                return AgentHealthCheck(
                    agent_name='git',
                    status=HealthStatus.UNHEALTHY,
                    error_message=result.stderr
                )
        except Exception as e:
            return AgentHealthCheck(
                agent_name='git',
                status=HealthStatus.UNHEALTHY,
                error_message=str(e)
            )

    def check_python(self) -> AgentHealthCheck:
        """Check Python environment.

        Returns:
            AgentHealthCheck result.
        """
        start_time = time.time()
        response_time = (time.time() - start_time) * 1000

        return AgentHealthCheck(
            agent_name='python',
            status=HealthStatus.HEALTHY,
            response_time_ms=response_time,
            details={
                'version': sys.version,
                'executable': sys.executable
            }
        )

    def run_all_checks(self) -> Dict[str, AgentHealthCheck]:
        """Run all health checks.

        Returns:
            Dict of check name to AgentHealthCheck result.
        """
        agent_names = ['coder', 'tests', 'changes', 'context', 'errors',
                       'improvements', 'stats']

        # Check core components
        self.results['python'] = self.check_python()
        self.results['git'] = self.check_git()

        # Check agent scripts
        for name in agent_names:
            self.results[name] = self.check_agent_script(name)

        return self.results

    def is_healthy(self) -> bool:
        """Check if all components are healthy.

        Returns:
            bool: True if all healthy, False otherwise.
        """
        if not self.results:
            self.run_all_checks()

        return all(
            r.status == HealthStatus.HEALTHY
            for r in self.results.values()
        )

    def print_report(self) -> None:
        """Print health check report."""
        if not self.results:
            self.run_all_checks()

        print("\n=== Agent Health Check Report ===\n")
        for name, result in sorted(self.results.items()):
            status_symbol = {
                HealthStatus.HEALTHY: "✓",
                HealthStatus.DEGRADED: "!",
                HealthStatus.UNHEALTHY: "✗",
                HealthStatus.UNKNOWN: "?"
            }.get(result.status, "?")

            print(f"  [{status_symbol}] {name}: {result.status.name}")
            if result.error_message:
                print(f"      Error: {result.error_message}")
            if result.response_time_ms > 0:
                print(f"      Response: {result.response_time_ms:.1f}ms")

        print()


# =============================================================================
# Agent Chaining
# =============================================================================


@dataclass
class AgentChainStep:
    """A step in an agent chain.

    Attributes:
        agent_name: Name of the agent to execute.
        input_transform: Optional function to transform input.
        output_transform: Optional function to transform output.
        enabled: Whether this step is enabled.
        condition: Optional condition function to check before execution.
    """

    agent_name: str
    input_transform: Optional[Callable[[Any], Any]] = None
    output_transform: Optional[Callable[[Any], Any]] = None
    enabled: bool = True
    condition: Optional[Callable[[Any], bool]] = None


class AgentChain:
    """Chain multiple agents for sequential execution.

    Allows output of one agent to be used as input to the next.

    Example:
        chain=AgentChain()
        chain.add_step("coder", output_transform=extract_code)
        chain.add_step("tests", input_transform=prepare_for_tests)
        results=chain.execute(initial_input)
    """

    def __init__(self, name: str = "default_chain") -> None:
        """Initialize agent chain.

        Args:
            name: Chain name for identification.
        """
        self.name = name
        self._steps: List[AgentChainStep] = []
        self._results: List[Dict[str, Any]] = []

    def add_step(
        self,
        agent_name: str,
        input_transform: Optional[Callable[[Any], Any]] = None,
        output_transform: Optional[Callable[[Any], Any]] = None,
        condition: Optional[Callable[[Any], bool]] = None,
    ) -> "AgentChain":
        """Add a step to the chain.

        Args:
            agent_name: Name of agent to execute.
            input_transform: Transform input before agent.
            output_transform: Transform output after agent.
            condition: Condition to check before execution.

        Returns:
            Self for chaining.
        """
        step = AgentChainStep(
            agent_name=agent_name,
            input_transform=input_transform,
            output_transform=output_transform,
            condition=condition,
        )
        self._steps.append(step)
        return self

    def execute(self, initial_input: Any, agent_executor: Callable[[
                str, Any], Any]) -> List[Dict[str, Any]]:
        """Execute the chain.

        Args:
            initial_input: Input to first agent.
            agent_executor: Function to execute an agent.

        Returns:
            List of results from each step.
        """
        self._results = []
        current_input = initial_input

        for step in self._steps:
            if not step.enabled:
                continue

            # Check condition
            if step.condition and not step.condition(current_input):
                self._results.append({
                    "agent": step.agent_name,
                    "skipped": True,
                    "reason": "condition not met",
                })
                continue

            # Transform input
            if step.input_transform:
                current_input = step.input_transform(current_input)

            # Execute agent
            try:
                output = agent_executor(step.agent_name, current_input)

                # Transform output
                if step.output_transform:
                    output = step.output_transform(output)

                self._results.append({
                    "agent": step.agent_name,
                    "success": True,
                    "output": output,
                })

                current_input = output

            except Exception as e:
                self._results.append({
                    "agent": step.agent_name,
                    "success": False,
                    "error": str(e),
                })
                break

        return self._results

    def get_results(self) -> List[Dict[str, Any]]:
        """Get results from last execution."""
        return self._results


# =============================================================================
# Git Branch - Based Processing
# =============================================================================


class GitBranchProcessor:
    """Process files changed in a specific git branch.

    Example:
        processor=GitBranchProcessor(repo_root)
        changed_files=processor.get_changed_files("feature-branch")
        for file in changed_files:
            process(file)
    """

    def __init__(self, repo_root: Path) -> None:
        """Initialize processor.

        Args:
            repo_root: Repository root directory.
        """
        self.repo_root = repo_root

    def get_changed_files(
        self,
        branch: str,
        base_branch: str = "main",
        extensions: Optional[List[str]] = None,
    ) -> List[Path]:
        """Get files changed in branch compared to base.

        Args:
            branch: Branch to check.
            base_branch: Base branch for comparison.
            extensions: File extensions to include (e.g., [".py", ".md"]).

        Returns:
            List of changed file paths.
        """
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{base_branch}...{branch}"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                logging.warning(f"Git diff failed: {result.stderr}")
                return []

            files = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                file_path = self.repo_root / line
                if extensions:
                    if file_path.suffix in extensions:
                        files.append(file_path)
                else:
                    files.append(file_path)

            return files

        except Exception as e:
            logging.error(f"Error getting branch changes: {e}")
            return []

    def get_current_branch(self) -> Optional[str]:
        """Get current git branch name."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None

    def list_branches(self, pattern: Optional[str] = None) -> List[str]:
        """List branches, optionally filtered by pattern.

        Args:
            pattern: Glob pattern to match branch names.

        Returns:
            List of branch names.
        """
        try:
            result = subprocess.run(
                ["git", "branch", "--list", "--format=%(refname:short)"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                return []

            branches = result.stdout.strip().split("\n")
            if pattern:
                branches = [b for b in branches if fnmatch.fnmatch(b, pattern)]

            return branches

        except Exception:
            return []


# =============================================================================
# Custom Validation Rules
# =============================================================================


@dataclass
class ValidationRule:
    """A custom validation rule.

    Attributes:
        name: Rule name.
        file_pattern: Glob pattern for files to apply to.
        validator: Validation function.
        error_message: Message on validation failure.
        severity: Rule severity (error, warning, info).
    """

    name: str
    file_pattern: str
    validator: Callable[[str, Path], bool]
    error_message: str = "Validation failed"
    severity: str = "error"


class ValidationRuleManager:
    """Manage custom validation rules per file type.

    Example:
        manager=ValidationRuleManager()
        manager.add_rule(ValidationRule(
            name = "max_line_length",
            file_pattern = "*.py",
            validator=lambda content, path: all(len(l) <= 100 for l in content.split("\\n")),
            error_message = "Line too long (>100 chars)",
        ))
        results=manager.validate(file_path, content)
    """

    def __init__(self) -> None:
        """Initialize rule manager."""
        self._rules: Dict[str, ValidationRule] = {}

    def add_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule.

        Args:
            rule: Rule to add.
        """
        self._rules[rule.name] = rule

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name.

        Args:
            name: Rule name.

        Returns:
            True if removed, False if not found.
        """
        if name in self._rules:
            del self._rules[name]
            return True
        return False

    def validate(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """Validate content against applicable rules.

        Args:
            file_path: File path being validated.
            content: File content.

        Returns:
            List of validation results.
        """
        results = []

        for rule in self._rules.values():
            if fnmatch.fnmatch(file_path.name, rule.file_pattern):
                try:
                    passed = rule.validator(content, file_path)
                    results.append({
                        "rule": rule.name,
                        "passed": passed,
                        "severity": rule.severity,
                        "message": None if passed else rule.error_message,
                    })
                except Exception as e:
                    results.append({
                        "rule": rule.name,
                        "passed": False,
                        "severity": "error",
                        "message": f"Validation error: {e}",
                    })

        return results

    def get_rules_for_file(self, file_path: Path) -> List[ValidationRule]:
        """Get rules applicable to a file.

        Args:
            file_path: File path.

        Returns:
            List of applicable rules.
        """
        return [
            rule for rule in self._rules.values()
            if fnmatch.fnmatch(file_path.name, rule.file_pattern)
        ]


# =============================================================================
# Agent Priority Queue
# =============================================================================


class AgentPriorityQueue:
    """Priority queue for ordered agent execution.

    Executes agents in priority order with support for dependencies.

    Example:
        queue=AgentPriorityQueue()
        queue.add_agent("critical_fix", priority=1)
        queue.add_agent("tests", priority=5, depends_on=["critical_fix"])
        queue.add_agent("docs", priority=10)

        for agent in queue.get_execution_order():
            execute(agent)
    """

    def __init__(self) -> None:
        """Initialize priority queue."""
        self._agents: Dict[str, Dict[str, Any]] = {}

    def add_agent(
        self,
        name: str,
        priority: int = 5,
        depends_on: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add agent to queue.

        Args:
            name: Agent name.
            priority: Priority (lower=higher priority).
            depends_on: List of agents this depends on.
            metadata: Optional metadata.
        """
        self._agents[name] = {
            "priority": priority,
            "depends_on": depends_on or [],
            "metadata": metadata or {},
        }

    def remove_agent(self, name: str) -> bool:
        """Remove agent from queue.

        Args:
            name: Agent name.

        Returns:
            True if removed, False if not found.
        """
        if name in self._agents:
            del self._agents[name]
            return True
        return False

    def get_execution_order(self) -> List[str]:
        """Get agents in execution order.

        Returns:
            List of agent names in order.
        """
        # Topological sort with priority
        executed = set()
        order: list[str] = []

        while len(order) < len(self._agents):
            available = []

            for name, info in self._agents.items():
                if name in executed:
                    continue

                # Check if all dependencies are met
                deps_met = all(d in executed for d in info["depends_on"])
                if deps_met:
                    available.append((info["priority"], name))

            if not available:
                # Cycle detected or error
                remaining = [n for n in self._agents if n not in executed]
                logging.warning(f"Dependency cycle detected, adding remaining: {remaining}")
                order.extend(sorted(remaining))
                break

            # Sort by priority and take the highest priority
            available.sort()
            _, next_agent = available[0]
            order.append(next_agent)
            executed.add(next_agent)

        return order


# =============================================================================
# Telemetry and Observability
# =============================================================================


@dataclass
class TelemetrySpan:
    """A telemetry span for tracing.

    Attributes:
        name: Span name.
        trace_id: Trace identifier.
        span_id: Span identifier.
        parent_id: Parent span ID.
        start_time: Start timestamp.
        end_time: End timestamp.
        attributes: Span attributes.
        events: Span events.
    """

    name: str
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    parent_id: Optional[str] = None
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)


class TelemetryCollector:
    """Collect telemetry data for observability.

    Provides OpenTelemetry - compatible span collection.

    Example:
        collector=TelemetryCollector()

        with collector.span("process_file") as span:
            span.set_attribute("file", "test.py")
            # ... process file ...

        spans=collector.get_spans()
    """

    def __init__(self, service_name: str = "agent") -> None:
        """Initialize collector.

        Args:
            service_name: Service name for tracing.
        """
        self.service_name = service_name
        self._spans: List[TelemetrySpan] = []
        self._current_span: Optional[TelemetrySpan] = None

    @contextmanager
    def span(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Create a telemetry span.

        Args:
            name: Span name.
            attributes: Initial attributes.

        Yields:
            SpanContext for adding attributes and events.
        """
        parent_id = self._current_span.span_id if self._current_span else None
        trace_id = self._current_span.trace_id if self._current_span else str(uuid.uuid4())

        span = TelemetrySpan(
            name=name,
            trace_id=trace_id,
            parent_id=parent_id,
            attributes=attributes or {},
        )

        old_current = self._current_span
        self._current_span = span

        context = SpanContext(span)

        try:
            yield context
        except Exception as e:
            context.add_event("exception", {"message": str(e)})
            raise
        finally:
            span.end_time = time.time()
            self._spans.append(span)
            self._current_span = old_current

    def get_spans(self) -> List[TelemetrySpan]:
        """Get all collected spans."""
        return list(self._spans)

    def export_json(self) -> str:
        """Export spans as JSON.

        Returns:
            JSON string of spans.
        """
        spans_data = []
        for span in self._spans:
            spans_data.append({
                "name": span.name,
                "trace_id": span.trace_id,
                "span_id": span.span_id,
                "parent_id": span.parent_id,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "duration_ms": (span.end_time - span.start_time) * 1000 if span.end_time else None,
                "attributes": span.attributes,
                "events": span.events,
            })
        return json.dumps(spans_data, indent=2)

    def clear(self) -> None:
        """Clear all spans."""
        self._spans.clear()


class SpanContext:
    """Context for a telemetry span."""

    def __init__(self, span: TelemetrySpan) -> None:
        """Initialize context.

        Args:
            span: The span to manage.
        """
        self._span = span

    def set_attribute(self, key: str, value: Any) -> None:
        """Set a span attribute.

        Args:
            key: Attribute key.
            value: Attribute value.
        """
        self._span.attributes[key] = value

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add an event to the span.

        Args:
            name: Event name.
            attributes: Event attributes.
        """
        self._span.events.append({
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {},
        })


# =============================================================================
# Conditional Agent Execution
# =============================================================================


@dataclass
class ExecutionCondition:
    """A condition for agent execution.

    Attributes:
        name: Condition name.
        check: Function to check condition.
        description: Human - readable description.
    """

    name: str
    check: Callable[[Path, str], bool]
    description: str = ""


class ConditionalExecutor:
    """Execute agents based on file content conditions.

    Example:
        executor=ConditionalExecutor()
        executor.add_condition("has_todos", lambda p, c: "TODO" in c)
        executor.add_condition("is_large", lambda p, c: len(c) > 10000)

        if executor.should_execute("coder", file_path, content):
            run_coder(file_path)
    """

    def __init__(self) -> None:
        """Initialize executor."""
        self._conditions: Dict[str, ExecutionCondition] = {}
        self._agent_conditions: Dict[str, List[str]] = {}

    def add_condition(
        self,
        name: str,
        check: Callable[[Path, str], bool],
        description: str = "",
    ) -> None:
        """Add a condition.

        Args:
            name: Condition name.
            check: Function taking (path, content) returning bool.
            description: Human - readable description.
        """
        self._conditions[name] = ExecutionCondition(
            name=name,
            check=check,
            description=description,
        )

    def set_agent_conditions(
        self,
        agent_name: str,
        conditions: List[str],
        require_all: bool = False,
    ) -> None:
        """Set conditions for an agent.

        Args:
            agent_name: Name of the agent.
            conditions: List of condition names.
            require_all: If True, all conditions must pass.
        """
        self._agent_conditions[agent_name] = {
            "conditions": conditions,
            "require_all": require_all,
        }

    def should_execute(
        self,
        agent_name: str,
        file_path: Path,
        content: str,
    ) -> bool:
        """Check if agent should execute for file.

        Args:
            agent_name: Agent name.
            file_path: File path.
            content: File content.

        Returns:
            True if agent should execute.
        """
        if agent_name not in self._agent_conditions:
            return True  # No conditions, always execute

        config = self._agent_conditions[agent_name]
        condition_names = config["conditions"]
        require_all = config["require_all"]

        results = []
        for cond_name in condition_names:
            if cond_name not in self._conditions:
                continue
            condition = self._conditions[cond_name]
            try:
                results.append(condition.check(file_path, content))
            except Exception:
                results.append(False)

        if not results:
            return True

        if require_all:
            return all(results)
        else:
            return any(results)


# =============================================================================
# Agent Templates
# =============================================================================


@dataclass
class AgentTemplate:
    """A template for creating agents.

    Attributes:
        name: Template name.
        description: Template description.
        agents: List of agents to execute.
        config: Default configuration.
        file_patterns: File patterns to process.
    """

    name: str
    description: str = ""
    agents: List[str] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    file_patterns: List[str] = field(default_factory=lambda: ["*.py"])


class TemplateManager:
    """Manage agent templates for common use cases.

    Example:
        manager=TemplateManager()
        manager.add_template(AgentTemplate(
            name = "python_cleanup",
            agents = ["coder", "tests"],
            file_patterns = ["*.py"],
        ))

        template=manager.get_template("python_cleanup")
        agent=template_to_agent(template)
    """

    def __init__(self) -> None:
        """Initialize manager."""
        self._templates: Dict[str, AgentTemplate] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default templates."""
        self._templates["python_full"] = AgentTemplate(
            name="python_full",
            description="Full Python code improvement",
            agents=["coder", "tests", "documentation", "errors"],
            file_patterns=["*.py"],
        )

        self._templates["markdown_docs"] = AgentTemplate(
            name="markdown_docs",
            description="Markdown documentation improvement",
            agents=["documentation"],
            file_patterns=["*.md"],
        )

        self._templates["quick_fix"] = AgentTemplate(
            name="quick_fix",
            description="Quick fixes only",
            agents=["coder"],
            config={"max_files": 10},
            file_patterns=["*.py"],
        )

    def add_template(self, template: AgentTemplate) -> None:
        """Add a template.

        Args:
            template: Template to add.
        """
        self._templates[template.name] = template

    def get_template(self, name: str) -> Optional[AgentTemplate]:
        """Get a template by name.

        Args:
            name: Template name.

        Returns:
            Template or None if not found.
        """
        return self._templates.get(name)

    def list_templates(self) -> List[str]:
        """List available template names."""
        return list(self._templates.keys())


# =============================================================================
# Agent Dependency Resolution
# =============================================================================


class DependencyGraph:
    """Resolve agent dependencies for ordered execution.

    Example:
        graph=DependencyGraph()
        graph.add_dependency("tests", "coder")  # tests depends on coder
        graph.add_dependency("docs", "tests")

        order=graph.resolve()  # ["coder", "tests", "docs"]
    """

    def __init__(self) -> None:
        """Initialize dependency graph."""
        self._nodes: Set[str] = set()
        self._edges: Dict[str, Set[str]] = {}  # node -> dependencies

    def add_node(self, name: str) -> None:
        """Add a node.

        Args:
            name: Node name.
        """
        self._nodes.add(name)
        if name not in self._edges:
            self._edges[name] = set()

    def add_dependency(self, node: str, depends_on: str) -> None:
        """Add a dependency.

        Args:
            node: Node that has the dependency.
            depends_on: Node that must run first.
        """
        self.add_node(node)
        self.add_node(depends_on)
        self._edges[node].add(depends_on)

    def resolve(self) -> List[str]:
        """Resolve execution order.

        Returns:
            List of nodes in execution order.

        Raises:
            ValueError: If circular dependency detected.
        """
        in_degree = {n: 0 for n in self._nodes}

        for node, deps in self._edges.items():
            for dep in deps:
                # This is reverse - we need nodes with deps to have higher in_degree
                pass  # Actually, we track outgoing

        # Build reverse graph for topological sort
        reverse: dict[str, set[str]] = {n: set() for n in self._nodes}
        for node, deps in self._edges.items():
            for dep in deps:
                reverse[dep].add(node)

        # Calculate in - degree based on dependencies
        in_degree = {n: len(self._edges.get(n, set())) for n in self._nodes}

        # Start with nodes that have no dependencies
        queue = [n for n in self._nodes if in_degree[n] == 0]
        result = []

        while queue:
            node = queue.pop(0)
            result.append(node)

            for dependent in reverse[node]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(self._nodes):
            raise ValueError("Circular dependency detected")

        return result


# =============================================================================
# Agent Execution Profiles
# =============================================================================


@dataclass
class ExecutionProfile:
    """A profile for agent execution settings.

    Attributes:
        name: Profile name.
        max_files: Maximum files to process.
        timeout: Timeout per operation.
        parallel: Enable parallel execution.
        workers: Number of workers.
        dry_run: Dry run mode.
    """

    name: str
    max_files: Optional[int] = None
    timeout: int = 120
    parallel: bool = False
    workers: int = 4
    dry_run: bool = False


class ProfileManager:
    """Manage agent execution profiles.

    Example:
        manager=ProfileManager()
        manager.add_profile(ExecutionProfile("ci", dry_run=True, timeout=60))
        manager.add_profile(ExecutionProfile("full", parallel=True, workers=8))

        manager.activate("ci")
        config=manager.get_active_config()
    """

    def __init__(self) -> None:
        """Initialize manager."""
        self._profiles: Dict[str, ExecutionProfile] = {}
        self._active: Optional[str] = None
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default profiles."""
        self._profiles["default"] = ExecutionProfile(
            name="default",
            timeout=120,
            parallel=False,
        )

        self._profiles["fast"] = ExecutionProfile(
            name="fast",
            max_files=10,
            timeout=60,
            parallel=True,
            workers=4,
        )

        self._profiles["ci"] = ExecutionProfile(
            name="ci",
            timeout=300,
            parallel=True,
            workers=2,
            dry_run=True,
        )

    def add_profile(self, profile: ExecutionProfile) -> None:
        """Add a profile.

        Args:
            profile: Profile to add.
        """
        self._profiles[profile.name] = profile

    def activate(self, name: str) -> None:
        """Activate a profile.

        Args:
            name: Profile name.

        Raises:
            KeyError: If profile not found.
        """
        if name not in self._profiles:
            raise KeyError(f"Profile not found: {name}")
        self._active = name

    def get_active_config(self) -> Optional[ExecutionProfile]:
        """Get active profile configuration."""
        if self._active:
            return self._profiles[self._active]
        return None


# =============================================================================
# Agent Result Caching
# =============================================================================


@dataclass
class CachedResult:
    """A cached agent result.

    Attributes:
        file_path: File that was processed.
        agent_name: Agent that produced result.
        content_hash: Hash of input content.
        result: The cached result.
        timestamp: When cached.
        ttl_seconds: Time to live.
    """

    file_path: str
    agent_name: str
    content_hash: str
    result: Any
    timestamp: float = field(default_factory=time.time)
    ttl_seconds: int = 3600


class ResultCache:
    """Cache agent results for reuse.

    Example:
        cache=ResultCache()

        # Check cache
        result=cache.get("test.py", "coder", content_hash)
        if result is None:
            result=run_coder("test.py")
            cache.set("test.py", "coder", content_hash, result)
    """

    def __init__(self, cache_dir: Optional[Path] = None) -> None:
        """Initialize cache.

        Args:
            cache_dir: Directory for persistent cache.
        """
        self.cache_dir = cache_dir
        self._memory_cache: Dict[str, CachedResult] = {}

    def _make_key(self, file_path: str, agent_name: str, content_hash: str) -> str:
        """Create cache key."""
        return f"{file_path}:{agent_name}:{content_hash}"

    def get(
        self,
        file_path: str,
        agent_name: str,
        content_hash: str,
    ) -> Optional[Any]:
        """Get cached result.

        Args:
            file_path: File path.
            agent_name: Agent name.
            content_hash: Hash of content.

        Returns:
            Cached result or None.
        """
        key = self._make_key(file_path, agent_name, content_hash)

        if key in self._memory_cache:
            cached = self._memory_cache[key]
            # Check TTL
            if time.time() - cached.timestamp < cached.ttl_seconds:
                return cached.result
            else:
                del self._memory_cache[key]

        return None

    def set(
        self,
        file_path: str,
        agent_name: str,
        content_hash: str,
        result: Any,
        ttl_seconds: int = 3600,
    ) -> None:
        """Cache a result.

        Args:
            file_path: File path.
            agent_name: Agent name.
            content_hash: Hash of content.
            result: Result to cache.
            ttl_seconds: Time to live.
        """
        key = self._make_key(file_path, agent_name, content_hash)
        self._memory_cache[key] = CachedResult(
            file_path=file_path,
            agent_name=agent_name,
            content_hash=content_hash,
            result=result,
            ttl_seconds=ttl_seconds,
        )

    def invalidate(self, file_path: str) -> int:
        """Invalidate all cache entries for a file.

        Args:
            file_path: File path.

        Returns:
            Number of entries invalidated.
        """
        to_remove = [k for k in self._memory_cache if k.startswith(f"{file_path}:")]
        for key in to_remove:
            del self._memory_cache[key]
        return len(to_remove)

    def clear(self) -> None:
        """Clear all cached results."""
        self._memory_cache.clear()


# =============================================================================
# Agent Execution Scheduling
# =============================================================================


@dataclass
class ScheduledExecution:
    """A scheduled agent execution.

    Attributes:
        name: Schedule name.
        cron: Cron expression (simplified).
        agent_config: Agent configuration.
        enabled: Whether schedule is enabled.
        last_run: Last run timestamp.
        next_run: Next run timestamp.
    """

    name: str
    cron: str  # Simplified: "hourly", "daily", "weekly", or HH:MM
    agent_config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    last_run: Optional[float] = None
    next_run: Optional[float] = None


class ExecutionScheduler:
    """Schedule agent executions.

    Example:
        scheduler=ExecutionScheduler()
        scheduler.add_schedule("nightly", "daily", {"dry_run": True})

        # In a loop
        while True:
            if scheduler.is_due("nightly"):
                run_agent(scheduler.get_config("nightly"))
                scheduler.mark_complete("nightly")
            time.sleep(60)
    """

    def __init__(self) -> None:
        """Initialize scheduler."""
        self._schedules: Dict[str, ScheduledExecution] = {}

    def add_schedule(
        self,
        name: str,
        cron: str,
        agent_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a schedule.

        Args:
            name: Schedule name.
            cron: Timing (hourly, daily, weekly, or HH:MM).
            agent_config: Agent configuration.
        """
        schedule = ScheduledExecution(
            name=name,
            cron=cron,
            agent_config=agent_config or {},
        )
        schedule.next_run = self._calculate_next_run(cron)
        self._schedules[name] = schedule

    def _calculate_next_run(self, cron: str) -> float:
        """Calculate next run time."""
        now = time.time()

        if cron == "hourly":
            return now + 3600
        elif cron == "daily":
            return now + 86400
        elif cron == "weekly":
            return now + 604800
        elif ":" in cron:
            # HH:MM format
            try:
                hour, minute = map(int, cron.split(":"))
                import datetime
                today = datetime.date.today()
                target = datetime.datetime.combine(
                    today,
                    datetime.time(hour, minute)
                )
                if target.timestamp() <= now:
                    target += datetime.timedelta(days=1)
                return target.timestamp()
            except Exception:
                return now + 86400
        else:
            return now + 86400  # Default to daily

    def is_due(self, name: str) -> bool:
        """Check if schedule is due.

        Args:
            name: Schedule name.

        Returns:
            True if due for execution.
        """
        if name not in self._schedules:
            return False

        schedule = self._schedules[name]
        if not schedule.enabled:
            return False

        if schedule.next_run is None:
            return True

        return time.time() >= schedule.next_run

    def mark_complete(self, name: str) -> None:
        """Mark schedule as completed.

        Args:
            name: Schedule name.
        """
        if name in self._schedules:
            schedule = self._schedules[name]
            schedule.last_run = time.time()
            schedule.next_run = self._calculate_next_run(schedule.cron)

    def get_config(self, name: str) -> Dict[str, Any]:
        """Get agent configuration for schedule.

        Args:
            name: Schedule name.

        Returns:
            Agent configuration dict.
        """
        if name in self._schedules:
            return self._schedules[name].agent_config
        return {}


def _exponential_backoff_retry(
        func,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0):
    """Execute a function with exponential backoff retry on failure.

    Retries a function call if it raises an exception, with exponentially
    increasing delays between attempts. Useful for transient failures.

    Args:
        func: Callable that returns True on success, False on failure.
        max_attempts: Maximum number of attempts. Defaults to 3.
        base_delay: Initial delay in seconds. Defaults to 1.0.
        max_delay: Maximum delay between retries. Defaults to 30.0.

    Returns:
        bool: True if func succeeded, False after max_attempts.

    Note:
        - Delay formula: min(base_delay * (2 ^ attempt), max_delay)
        - Logs each retry attempt
        - Final failure is logged as error
    """
    for attempt in range(1, max_attempts + 1):
        try:
            result = func()
            if result:
                return True
        except Exception as e:
            if attempt == max_attempts:
                logging.error(f"Failed after {max_attempts} attempts: {e}")
                return False
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            logging.warning(f"Attempt {attempt} failed, retrying in {delay}s: {e}")
            time.sleep(delay)
    return False


# Module - level worker function for multiprocessing (cannot be a nested function)
def _multiprocessing_worker(agent_instance, file_path: Path) -> Optional[Path]:
    """Worker function for multiprocessing file processing.

    This function must be at module level to be pickleable for multiprocessing.
    """
    try:
        logging.debug(f"[worker] Processing {file_path.name}")
        agent_instance.process_file(file_path)
        logging.info(f"[worker] Completed {file_path.name}")
        return file_path
    except Exception as e:
        logging.error(f"[worker] Failed: {e}")
        return None


def setup_logging(verbosity: str) -> None:
    """Configure logging based on verbosity level.

    Args:
        verbosity: Verbosity level as string ('quiet', 'minimal', 'normal', 'elaborate'
                  or '0', '1', '2', '3'). Defaults to 'INFO' level.

    Returns:
        None. Configures the root logger with the specified level.

    Example:
        setup_logging('elaborate')  # Sets DEBUG level

    Note:
        This function configures the global logging system. Should be called
        once at application startup before other logging calls.
    """
    levels = {
        'quiet': logging.ERROR,
        'minimal': logging.WARNING,
        'normal': logging.INFO,
        'elaborate': logging.DEBUG,
        '0': logging.ERROR,
        '1': logging.WARNING,
        '2': logging.INFO,
        '3': logging.DEBUG,
    }
    level = levels.get(verbosity.lower(), logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    logging.debug(f"Logging configured at level: {logging.getLevelName(level)}")


def load_codeignore(root: Path) -> Set[str]:
    """Load and parse ignore patterns from .codeignore file.

    Reads the .codeignore file from the repository root and extracts all
    ignore patterns (lines that are not empty or comments).

    Caches patterns to avoid re - parsing on subsequent calls. Cache is invalidated
    if the file is modified (checked by file mtime).

    Args:
        root: Path to the repository root directory.

    Returns:
        Set of ignore patterns (strings) from the .codeignore file.
        Returns empty set if file doesn't exist.

    Raises:
        None. Logs warnings if file cannot be read but doesn't raise.

    Example:
        patterns=load_codeignore(Path('/repo'))
        # patterns might be: {'*.log', '__pycache__/', 'venv/**'}

    Note:
        - Lines starting with '#' are treated as comments and ignored
        - Empty lines are skipped
        - File encoding is assumed to be UTF - 8
        - Patterns are cached with mtime checking for efficiency
    """
    codeignore_path = root / ".codeignore"
    cache_key = str(codeignore_path)

    # Check cache validity
    if cache_key in _CODEIGNORE_CACHE and codeignore_path.exists():
        try:
            file_mtime = codeignore_path.stat().st_mtime
            cache_time = _CODEIGNORE_CACHE_TIME.get(cache_key, 0)
            if file_mtime == cache_time:
                logging.debug(f"Using cached .codeignore patterns for {cache_key}")
                return _CODEIGNORE_CACHE[cache_key]
        except OSError:
            pass

    if codeignore_path.exists():
        try:
            logging.debug(f"Loading .codeignore patterns from {codeignore_path}")
            content = codeignore_path.read_text(encoding='utf-8')
            patterns = {
                line.strip() for line in content.split('\n')
                if line.strip() and not line.strip().startswith('#')
            }
            logging.info(f"Loaded {len(patterns)} ignore patterns from .codeignore")

            # Cache the patterns
            _CODEIGNORE_CACHE[cache_key] = patterns
            try:
                _CODEIGNORE_CACHE_TIME[cache_key] = codeignore_path.stat().st_mtime
            except OSError:
                pass

            return patterns
        except Exception as e:
            logging.warning(f"Could not read .codeignore file: {e}")
    else:
        logging.debug(f"No .codeignore file found at {codeignore_path}")
    return set()


class CircuitBreaker:
    """Circuit breaker pattern for failing backends.

    Manages failing backends with exponential backoff and recovery.
    Tracks failure state and prevents cascading failures.

    States:
        CLOSED: Normal operation, requests pass through
        OPEN: Too many failures, requests fail immediately
        HALF_OPEN: Testing if backend recovered
    """

    def __init__(self, name: str, failure_threshold: int = 5,
                 recovery_timeout: int = 60, backoff_multiplier: float = 2.0):
        """Initialize circuit breaker.

        Args:
            name: Name of the backend / service
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            backoff_multiplier: Multiplier for exponential backoff
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.backoff_multiplier = backoff_multiplier

        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0.0
        self.consecutive_successes_needed = 2

    def call(self, func: Callable, *args, **kwargs):
        """Execute function through circuit breaker.

        Args:
            func: Callable to execute
            *args, **kwargs: Arguments to pass to function

        Returns:
            Result of func if successful

        Raises:
            Exception: If circuit is open or func fails
        """
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.success_count = 0
                logging.info(f"Circuit breaker '{self.name}' entering HALF_OPEN state")
            else:
                raise Exception(f"Circuit breaker '{self.name}' is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception:  # noqa: F841
            self.on_failure()
            raise

    def on_success(self):
        """Record successful call."""
        self.failure_count = 0

        if self.state == "HALF_OPEN":
            self.success_count += 1
            if self.success_count >= self.consecutive_successes_needed:
                self.state = "CLOSED"
                logging.info(f"Circuit breaker '{self.name}' closed (recovered)")

    def on_failure(self):
        """Record failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logging.error(f"Circuit breaker '{self.name}' opened (too many failures)")


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
                 max_workers: int = 4) -> None:
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

        Raises:
            FileNotFoundError: If repo_root doesn't exist.

        Note:
            The repository root is automatically detected by looking for .git,
            README.md, or package.json if not explicitly provided.

            Supports context manager protocol via __enter__ and __exit__.
        """
        logging.info(f"Initializing Agent with repo_root={repo_root}")
        self.repo_root = self._find_repo_root(Path(repo_root))
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
        self.ignored_patterns = load_codeignore(self.repo_root)

        # Webhook support
        self.webhooks: List[str] = []
        self.callbacks: List[Callable] = []

        # Metrics tracking
        self.metrics = {
            'files_processed': 0,
            'files_modified': 0,
            'agents_applied': {},
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

    def __enter__(self):
        """Context manager entry. Returns self for use in 'with' statement."""
        logging.debug("Agent entering context manager")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
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
        self.metrics['end_time'] - self.metrics['start_time']

        summary = """
=== Agent Execution Summary ===
Files processed: {self.metrics['files_processed']}
Files modified:  {self.metrics['files_modified']}
Execution time:  {elapsed:.2f}s
Dry - run mode:    {'Yes' if self.dry_run else 'No'}

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

        report = {
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
        files_proc = report['summary']['files_processed']
        files_mod = report['summary']['files_modified']
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

        benchmarks = {
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

        analysis = {
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

        all_patterns = set()
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
                     max_retries: int = 1) -> subprocess.CompletedProcess:
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
        def attempt_command():
            logging.debug(f"Running command: {' '.join(cmd[:3])}... (timeout={timeout}s)")
            try:
                result = subprocess.run(
                    cmd,
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    encoding='utf-8',
                    errors='replace',
                    check=False
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

        result = attempt_command()

        # Retry on failure with exponential backoff
        for attempt in range(1, max_retries):
            if result.returncode == 0:
                return result

            delay = min(1.0 * (2 ** (attempt - 1)), 30.0)  # Max 30 seconds
            logging.warning(f"Command failed (attempt {attempt}), retrying in {delay}s...")
            time.sleep(delay)
            result = attempt_command()

        return result

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
        logging.info("Searching for code files...")
        code_files: list[Path] = []
        for ext in self.SUPPORTED_EXTENSIONS:
            code_files.extend(self.repo_root.rglob(f'*{ext}'))
        logging.debug(f"Found {len(code_files)} files with supported extensions")

        # Filter to scripts / agent directory if agents_only is True
        if self.agents_only:
            scripts_agent_dir = self.repo_root / 'scripts' / 'agent'
            code_files = [f for f in code_files if f.is_relative_to(scripts_agent_dir)]
            logging.info(f"Filtered to scripts / agent directory: {len(code_files)} files")

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
            str(self.repo_root / 'scripts / agent / agent-stats.py'),
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
            str(self.repo_root / 'scripts / agent / agent-errors.py'),
            '--context', str(errors_file),
            '--prompt', prompt
        ]
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
            str(self.repo_root / 'scripts / agent / agent-improvements.py'),
            '--context', str(improvements_file),
            '--prompt', prompt
        ]
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
            pending = []
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
            new_lines = []
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
            str(self.repo_root / 'scripts / agent / agent-coder.py'),
            '--context', str(code_file),
            '--prompt', prompt
        ]
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
            str(self.repo_root / 'scripts / agent / agent-changes.py'),
            '--context', str(changes_file),
            '--prompt', prompt
        ]
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
            str(self.repo_root / 'scripts / agent / agent-context.py'),
            '--context', str(context_file),
            '--prompt', prompt
        ]
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
            str(self.repo_root / 'scripts / agent / agent-tests.py'),
            '--context', str(test_file_to_update),
            '--prompt', prompt,
        ]
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
        # Give a Stats update
        self.run_stats_update([code_file])
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
        if not HAS_REQUESTS or not self.webhooks:
            return

        payload = {
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
        modified_files = []

        async def process_file_async(file_path: Path):
            """Process a single file asynchronously."""
            try:
                logging.debug(f"[async] Processing {file_path.name}")
                self.process_file(file_path)
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
        processed_files = []

        def worker_thread_process_file(file_path: Path) -> Path:
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

        results = {}
        context = {
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
            timeout_per_agent=config.timeout_per_agent or None
        )

        # Apply rate limiting if configured
        if config.rate_limit:
            agent.enable_rate_limiting(config.rate_limit)

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
        if self.enable_async or self.enable_multiprocessing:
            self.run_with_parallel_execution()
        else:
            # Sequential execution (original behavior)
            code_files = self.find_code_files()
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Agent: Orchestrates code improvement agents'
    )
    parser.add_argument('--dir', default='.', help='Directory to process (default: .)')
    parser.add_argument('--agents-only', action='store_true',
                        help='Only process files in the scripts / agent directory')
    parser.add_argument('--max-files', type=int, help='Maximum number of files to process')
    parser.add_argument('--loop', type=int, default=1,
                        help='Number of times to loop through all files (default: 1)')
    parser.add_argument('--skip-code-update', action='store_true',
                        help='Skip code updates and tests, only update documentation')
    parser.add_argument('--verbose', default='normal',
                        help='Verbosity level: quiet, minimal, normal, elaborate (or 0-3)')
    parser.add_argument('--no-git', action='store_true',
                        help='Skip git commit and push operations')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without modifying files')
    parser.add_argument(
        '--only-agents',
        type=str,
        metavar='AGENTS',
        help='Comma-separated list of agents to execute (e.g., coder,tests,documentation)')
    parser.add_argument('--timeout', type=int, metavar='SECONDS', default=120,
                        help='Default timeout per agent in seconds (default: 120)')
    # Phase 4c: Parallel execution arguments
    parser.add_argument('--async', dest='enable_async', action='store_true',
                        help='Enable async file processing for concurrent I / O')
    parser.add_argument('--multiprocessing', dest='enable_multiprocessing', action='store_true',
                        help='Enable multiprocessing for parallel agent execution')
    parser.add_argument('--workers', type=int, default=4,
                        help='Number of worker threads / processes (default: 4)')
    parser.add_argument('--webhook', type=str, action='append',
                        help='Register webhook URL for notifications (can be used multiple times)')
    # Phase 6: New feature arguments
    parser.add_argument('--config', type=str, metavar='FILE',
                        help='Path to configuration file (YAML / TOML / JSON)')
    parser.add_argument('--rate-limit', type=float, metavar='RPS',
                        help='Rate limit API calls to RPS requests per second')
    parser.add_argument('--enable-file-locking', action='store_true',
                        help='Enable file locking to prevent concurrent modifications')
    parser.add_argument('--incremental', action='store_true',
                        help='Only process files changed since last run')
    parser.add_argument('--graceful-shutdown', action='store_true',
                        help='Enable graceful shutdown with state persistence')
    parser.add_argument('--health-check', action='store_true',
                        help='Run health checks and exit')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from previous interrupted run')
    parser.add_argument('--diff-preview', action='store_true',
                        help='Show diffs before applying changes (requires --dry-run)')

    args = parser.parse_args()
    setup_logging(args.verbose)
    os.environ['DV_AGENT_VERBOSITY'] = args.verbose

    # Health check mode
    if args.health_check:
        checker = HealthChecker(Path(args.dir).resolve())
        checker.run_all_checks()
        checker.print_report()
        sys.exit(0 if checker.is_healthy() else 1)

    # Load from config file if provided
    if args.config:
        agent = Agent.from_config_file(Path(args.config))
    else:
        # Parse selective agents if provided
        selective_agents = None
        if args.only_agents:
            selective_agents = [a.strip() for a in args.only_agents.split(',')]
            logging.info(f"Running with selective agents: {selective_agents}")

        agent = Agent(
            repo_root=args.dir,
            agents_only=args.agents_only,
            max_files=args.max_files,
            loop=args.loop,
            skip_code_update=args.skip_code_update,
            no_git=args.no_git,
            dry_run=args.dry_run,
            selective_agents=selective_agents,
            timeout_per_agent={'coder': args.timeout, 'tests': args.timeout},
            enable_async=args.enable_async,
            enable_multiprocessing=args.enable_multiprocessing,
            max_workers=args.workers
        )

    # Register webhooks if provided
    if args.webhook:
        for webhook_url in args.webhook:
            agent.register_webhook(webhook_url)

    # Enable rate limiting if provided
    if args.rate_limit:
        agent.enable_rate_limiting(RateLimitConfig(
            requests_per_second=args.rate_limit
        ))

    # Enable file locking if requested
    if args.enable_file_locking:
        agent.enable_file_locking()

    # Enable incremental processing if requested
    if args.incremental:
        agent.enable_incremental_processing()

    # Enable graceful shutdown if requested
    if args.graceful_shutdown:
        agent.enable_graceful_shutdown()

    # Enable diff preview if requested
    if args.diff_preview:
        agent.enable_diff_preview()

    # Resume from previous run if requested
    if args.resume:
        pending_files = agent.resume_from_shutdown()
        if pending_files:
            logging.info(f"Resuming with {len(pending_files)} pending files")

    try:
        agent.run()
    finally:
        # Always print metrics summary
        agent.print_metrics_summary()

        # Cleanup graceful shutdown state on successful completion
        if hasattr(agent, 'shutdown_handler'):
            agent.shutdown_handler.cleanup()

        # Save incremental processing state
        if hasattr(agent, 'incremental_processor'):
            agent.incremental_processor.complete_run()
