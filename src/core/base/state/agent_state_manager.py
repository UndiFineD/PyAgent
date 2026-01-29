from __future__ import annotations
#!/usr/bin/env python3
"""
Module: agent_state_manager
Provides transactional file-system state management for PyAgent agents.
"""
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
State management for swarm agents.
Handles persistence of agent memory, history, and metadata.
"""

import collections
import json
import logging
from subprocess import CalledProcessError
from subprocess import TimeoutExpired
import time
from pathlib import Path
from typing import Any

from src.core.base.common.file_system_core import FileSystemCore
from src.core.base.lifecycle.version import VERSION
from src.core.base.common.models.core_enums import FailureClassification

__version__: str = VERSION


class EmergencyEventLog:
    """Phase 278: Ring buffer recording the last 10 filesystem actions for recovery."""

    def __init__(self, log_path: Path = Path("data/logs/emergency_recovery.log")) -> None:
        self.log_path: Path = log_path
        self.buffer = collections.deque(maxlen=10)
        self._fs = FileSystemCore()

        self._load_buffer()

    def _load_buffer(self) -> None:
        if self.log_path.exists():
            try:
                content: str = self.log_path.read_text(encoding="utf-8")
                self.buffer.extend(content.splitlines())

            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass

    def record_action(self, action: str, details: str) -> None:
        """Record an action to the emergency log."""
        event: str = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {action}: {details}"

        self.buffer.append(event)
        try:
            self._fs.atomic_write(self.log_path, "\n".join(self.buffer))
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"StructuredLogger: Failed to write emergency log: {e}")


# Global instance for easy access (Phase 278)


EMERGENCY_LOG = EmergencyEventLog()

class AgentCircuitBreaker:
    """
    Phase 336: Circuit breaker for autonomous agents to prevent cascading failures.
    Tracks failure rates and halts operations if threshold is exceeded.
    """

    def __init__(self, agent_id: str, failure_threshold: float = 0.5, window_size: int = 10) -> None:
        self.agent_id: str = agent_id
        self.threshold: float = failure_threshold
        self.window = collections.deque(maxlen=window_size)
        self._state_file = Path(f"data/agent_cache/{agent_id}_cb.json")
        self._load()

    def _load(self) -> None:
        """Load circuit breaker state."""
        if self._state_file.exists():
            try:
                data = json.loads(self._state_file.read_text(encoding="utf-8"))
                self.window.extend(data.get("history", []))
            except Exception: # pylint: disable=broad-except
                pass

    def _save(self) -> None:
        """Persist circuit breaker state."""
        try:
            self._state_file.parent.mkdir(parents=True, exist_ok=True)
            FileSystemCore().atomic_write(
                self._state_file, 
                json.dumps({"history": list(self.window)})
            )
        except (OSError, TypeError) as e:  # pylint: disable=broad-exception-caught, unused-variable
            pass

    def record_result(self, success: bool) -> None:
        """Record a success (True) or failure (False)."""
        self.window.append(1 if success else 0)
        self._save()

    @property
    def failure_rate(self) -> float:
        """Calculate current failure rate."""
        if not self.window:
            return 0.0
        failures: int = self.window.count(0)
        return failures / len(self.window)

    def is_open(self) -> bool:
        """Check if circuit breaker is open (halt operations)."""
        # Only check if we have enough data (at least 5 samples)
        if len(self.window) < 5:
            return False
        return self.failure_rate > self.threshold

    def reset(self) -> None:
        """Reset the circuit breaker."""
        self.window.clear()
        self._save()


class AgentCheckpointManager:
    """
    Phase 336: Manages agent state snapshots and restoration.
    Provides logic to rollback agent memory layer and file system changes atomically.
    """

    def __init__(self, agent_id: str, workspace_root: Path) -> None:
        self.agent_id: str = agent_id
        self.checkpoint_dir: Path = workspace_root / "data" / "checkpoints" / agent_id
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self._fs = FileSystemCore()

    def create_checkpoint(self, state_data: dict[str, Any], associated_files: list[Path] | None = None) -> str:
        """
        Creates a snapshot of agent state and optionally backups associated files.
        Returns: Checkpoint ID
        """
        checkpoint_id: str = f"cp_{int(time.time())}_{self.agent_id}"
        cp_path: Path = self.checkpoint_dir / checkpoint_id
        cp_path.mkdir(exist_ok=True)

        # Save State Data
        self._fs.atomic_write(cp_path / "state.json", json.dumps(state_data, indent=2))

        # Backup Files
        if associated_files:
            file_manifest = {}
            for file_path in associated_files:
                if file_path.exists():
                    backup_name: str = f"{file_path.name}.bak"
                    self._fs.safe_copy(file_path, cp_path / backup_name)
                    file_manifest[str(file_path)] = backup_name
            
            self._fs.atomic_write(cp_path / "files.json", json.dumps(file_manifest))

        return checkpoint_id

    def restore_checkpoint(self, checkpoint_id: str) -> dict[str, Any]:
        """
        Restores agent state and files from a checkpoint.
        """
        cp_path: Path = self.checkpoint_dir / checkpoint_id
        if not cp_path.exists():
            raise FileNotFoundError(f"Checkpoint {checkpoint_id} not found")

        # Restore Files
        file_manifest_path: Path = cp_path / "files.json"
        if file_manifest_path.exists():
            manifest = json.loads(file_manifest_path.read_text(encoding="utf-8"))
            for original_path_str, backup_name in manifest.items():
                original_path = Path(original_path_str)
                backup_file = cp_path / backup_name
                if backup_file.exists():
                    self._fs.safe_copy(backup_file, original_path)
                    logging.info(f"Restored file {original_path} from checkpoint {checkpoint_id}")

        # Restore State
        state_path: Path = cp_path / "state.json"
        if state_path.exists():
            return json.loads(state_path.read_text(encoding="utf-8"))
        
        return {}

class StateDriftDetector:
    """
    Phase 336: Validates pre/post execution state to detect corruption.
    """
    def __init__(self, target_files: list[Path]) -> None:
        self.snapshots: dict[Path, str] = {}
        self.target_files: list[Path] = target_files

    def snapshot(self) -> None:
        """Capture hash of current files."""
        import hashlib
        for p in self.target_files:
            if p.exists():
                self.snapshots[p] = hashlib.sha256(p.read_bytes()).hexdigest()

    def detect_drift(self) -> list[str]:
        """Check if files changed unexpectedly (if used for monitoring invalid changes)."""
        # Logic depends on usage. For StateTransaction, we expect changes.
        # But this can be used to verify that *only* the intended files changed,
        # or that the changes match some criteria.
        # For now, we implement a basic corruption check (empty files).
        drift_warnings = []
        for p in self.target_files:
            if p.exists() and p.stat().st_size == 0:
                drift_warnings.append(f"Corruption: File {p} is empty after operation.")
        return drift_warnings


class StructuredErrorValidator:
    """
    Phase 336: Validates and classifies errors to prevent 'Unknown failure' states.
    Captures diagnostic metadata for swarm intelligence.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger("StructuredErrorValidator")

    def capture_failure(self, context_id: str, error: BaseException, traceback_obj: Any) -> dict[str, Any]:
        """
        Classify error and return structured metadata.
        """
        import traceback

        error_type: str = type(error).__name__
        stack_trace: str = "".join(traceback.format_tb(traceback_obj)) if traceback_obj else str(error)

        # Phase 336: Enhanced Taxonomy Mapping
        classification: str = FailureClassification.UNKNOWN.value  # Default
        
        if isinstance(error, RecursionError):
            classification: str = FailureClassification.RECURSION_LIMIT.value
        elif isinstance(error, ValueError):
             # Check if it's a validation error
             if "validation" in str(error).lower():
                 classification: str = FailureClassification.STATE_CORRUPTION.value
             else:
                classification: str = FailureClassification.AI_ERROR.value 
        elif isinstance(error, IOError):
            classification: str = FailureClassification.STATE_CORRUPTION.value
        elif isinstance(error, ImportError):
            classification: str = FailureClassification.STATE_CORRUPTION.value
        elif isinstance(error, MemoryError):
            classification: str = FailureClassification.RESOURCE_EXHAUSTION.value
        elif isinstance(error, ConnectionError):
            classification: str = FailureClassification.NETWORK_FAILURE.value

        report = {
            "error_type": error_type,
            "classification": classification,
            "message": str(error),
            "context_id": context_id,
            "timestamp": time.time(),
            "stack_trace_snippet": stack_trace[-1000:] if stack_trace else "",
            "full_stack_trace": stack_trace
        }

        self.logger.error(f"Swarm Failure Captured [{classification}]: {error_type} in {context_id}")
        return report


class StateTransaction:
    """Phase 267: Transactional context manager for agent file operations."""

    target_files: list[Path]
    run_tests: bool
    backups: dict[Path, Path]
    temp_dir: Path
    _fs: FileSystemCore
    id: str
    drift_detector: 'StateDriftDetector'

    def __init__(self, target_files: list[Path], run_tests: bool = False) -> None:
        self.target_files = target_files
        self.run_tests = run_tests
        self.backups = {}
        self.temp_dir = Path("temp/transactions")
        self._fs = FileSystemCore()
        self._fs.ensure_directory(self.temp_dir)
        self.id = f"tx_{int(time.time() * 1000)}"
        self.drift_detector = StateDriftDetector(target_files)

    def __enter__(self) -> 'StateTransaction':
        self.drift_detector.snapshot()
        for file in self.target_files:
            if file.exists():
                backup_path: Path = self.temp_dir / f"{file.name}_{self.id}.bak"
                self._fs.safe_copy(file, backup_path)
                self.backups[file] = backup_path
        logging.info(f"Transaction {self.id} started. {len(self.backups)} files backed up.")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context with validation and commit/rollback logic."""
        validator = StructuredErrorValidator()

        if exc_type is not None:
            validator.capture_failure(self.id, exc_val, exc_tb)
            self.rollback()
        else:
            try:
                self.validate()
                self.commit()
            except Exception as e:  # pylint: disable=broad-exception-caught
                import sys
                logging.error(f"Transaction validation failed: {e}")
                validator.capture_failure(self.id, e, sys.exc_info()[2])
                self.rollback()
                raise e

    def validate(self) -> None:
        """Phase 280: Validate Python files before commit (AST Check, Immutable Test Check, Drift)."""
        import ast

        # Drift/Corruption Check
        warnings: list[str] = self.drift_detector.detect_drift()
        for w in warnings:
            logging.error(f"Transaction Drift Warning: {w}")
            # We treat file corruption (empty files) as a hard failure
            raise ValueError(w)

        # Phase 336: Immutable Test Suite Protection

        # We explicitly block modification of core testing infrastructure by self-improving agents.
        protected_paths: list[str] = [
            # Core fixtures
            "tests/conftest.py",
            # Base test cases
            "tests/base_test_case.py",
            # Critical core tests
            "tests/unit/core/",
        ]

        for file in self.target_files:
            # Check for immutable violations
            resolved: Path = file.resolve()
            str_path: str = str(resolved).replace("\\", "/")  # normalize
            for protected in protected_paths:
                if protected in str_path and file.exists():
                    # Calculate checksum or just fail if it's being modified within a generated transaction
                    # For now, we assume if it's in target_files, it's intended to be modified.
                    # We check if content actually changed.
                    if file in self.backups:
                        orig_content: bytes = self.backups[file].read_bytes()
                        new_content: bytes = file.read_bytes()
                        if orig_content != new_content:
                            msg: str = ("Security Violation: Attempted modification of "
                                   f"immutable test infrastructure: {file}")
                            logging.critical(msg)
                            raise PermissionError(msg)

            if file.exists() and file.suffix == ".py":
                try:
                    content: str = file.read_text(encoding="utf-8")
                    ast.parse(content)
                except SyntaxError as e:
                    logging.error(f"Validation failed for {file}: {e}")
                    raise ValueError(f"Generated code has syntax errors: {e}") from e

        if self.run_tests:
            self._run_associated_tests()

    def _run_associated_tests(self) -> None:
        """Run associated tests for modified files."""
        import subprocess
        for file in self.target_files:
            if not file.exists() or file.suffix != ".py":
                continue

            # Simple heuristic: run the file if it is a test, or try to find a test
            test_targets = []
            if file.name.startswith("test_") or "tests" in file.parts:
                test_targets.append(file)

            # Add more heuristics if needed (e.g. src/foo.py -> tests/unit/test_foo.py)

            for test_path in test_targets:
                try:
                    # Run pytest on the target
                    subprocess.run(
                        ["python", "-m", "pytest", str(test_path), "--tb=short"],
                        check=True,
                        capture_output=True,
                        timeout=30
                    )
                except subprocess.CalledProcessError as e:
                    err_msg: Any | str = e.stderr.decode() if e.stderr else 'Unknown error'
                    logging.error(f"Pre-commit test failure for {test_path}: {err_msg}")
                    raise ValueError(f"Verification tests failed for {file.name}") from e
                except subprocess.TimeoutExpired as e:
                    logging.error(f"Pre-commit test timeout for {test_path}")
                    raise ValueError(f"Verification tests timed out for {file.name}") from e

    def commit(self) -> None:
        """Discard backups after successful transaction."""
        for backup in self.backups.values():
            if backup.exists():
                backup.unlink()
        logging.info(f"Transaction {self.id} committed successfully.")

    def rollback(self) -> None:
        """Restore files from backups after failure."""
        for original, backup in self.backups.items():
            if backup.exists():
                self._fs.safe_copy(backup, original)
                backup.unlink()
        logging.warning(f"Transaction {self.id} ROLLED BACK. Files restored.")


class AgentStateManager:
    """Manages saving and loading agent state to/from disk."""

    @staticmethod
    # pylint: disable=too-many-positional-arguments
    def save_state(
        file_path: Path,
        current_state: str,
        token_usage: int,
        state_data: dict[str, Any],
        history_len: int,
        path: Path | None = None,
    ) -> None:
        """Save agent state to disk."""
        state_path: Path = path or file_path.with_suffix(".state.json")
        state: dict[str, Any] = {
            "file_path": str(file_path),
            "state": current_state,
            "token_usage": token_usage,
            "state_data": state_data,
            "history_length": history_len,
        }
        FileSystemCore().atomic_write(state_path, json.dumps(state, indent=2))
        logging.debug(f"State saved to {state_path}")

    @staticmethod
    def load_state(file_path: Path, path: Path | None = None) -> dict[str, Any] | None:
        """Load agent state from disk."""
        state_path: Path = path or file_path.with_suffix(".state.json")
        if not state_path.exists():
            return None

        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.warning(f"Failed to load state: {e}")
            return None
