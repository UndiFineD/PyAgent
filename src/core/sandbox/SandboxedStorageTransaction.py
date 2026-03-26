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

"""SandboxedStorageTransaction — StorageTransaction subclass with path allowlist enforcement."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxViolationError import SandboxViolationError
from src.transactions.StorageTransactionManager import StorageTransaction


class SandboxedStorageTransaction(StorageTransaction):
    """StorageTransaction subclass that enforces a path allowlist from SandboxConfig.

    All write, delete, mkdir, and commit operations are validated against
    the resolved allowed_paths before the operation is queued or executed.
    Symlink escapes and path traversal attempts are caught by resolving all
    paths via Path.resolve() before comparison.

    Attributes:
        _sandbox: The SandboxConfig governing which paths and hosts are permitted.

    """

    def __init__(self, sandbox: SandboxConfig, target: Optional[Path] = None) -> None:
        """Initialize with a SandboxConfig and an optional legacy-mode target path.

        Args:
            sandbox: The SandboxConfig that defines the path and host allowlists.
            target:  Optional single-file target for legacy (sync) mode.

        """
        super().__init__(target=target)
        self._sandbox = sandbox

    # ------------------------------------------------------------------
    # Internal path validation helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_subpath(path: Path, allowed: Path) -> bool:
        """Return True when *path* is equal to or contained within *allowed*.

        Both paths are resolved before comparison to catch symlinks and traversal.

        Args:
            path:    The candidate path to test.
            allowed: The root directory to test containment against.

        Returns:
            True if resolved path is under (or equal to) resolved allowed.

        """
        resolved = path.resolve()
        resolved_allowed = allowed.resolve()
        allowed_parts = resolved_allowed.parts
        return resolved.parts[: len(allowed_parts)] == allowed_parts

    def _validate_path(self, path: Path) -> None:
        """Validate that *path* resolves to within one of the configured allowed_paths.

        Raises SandboxViolationError if none of the allowed_paths contain the path.
        An empty allowed_paths list is a deny-all policy.

        Args:
            path: The path to validate.

        Raises:
            SandboxViolationError: When the resolved path is not inside any allowed root.

        """
        resolved = path.resolve()
        for allowed in self._sandbox.allowed_paths:
            if self._is_subpath(path, allowed):
                return
        raise SandboxViolationError(
            resource=str(resolved),
            reason=f"path not in allowed_paths: {self._sandbox.allowed_paths}",
        )

    # ------------------------------------------------------------------
    # Multi-op async overrides
    # ------------------------------------------------------------------

    async def write(self, path: Path, content: bytes, *, user_id: Optional[str] = None) -> None:
        """Validate path allowlist then queue a write operation.

        Args:
            path:    Target file path (must be under an allowed root).
            content: Raw bytes to write.
            user_id: Optional user identifier for per-user encryption.

        Raises:
            SandboxViolationError: When *path* resolves outside allowed_paths.

        """
        self._validate_path(path)
        await super().write(path, content, user_id=user_id)

    async def delete(self, path: Path) -> None:
        """Validate path allowlist then queue a delete operation.

        Args:
            path: File or directory path to delete (must be under an allowed root).

        Raises:
            SandboxViolationError: When *path* resolves outside allowed_paths.

        """
        self._validate_path(path)
        await super().delete(path)

    async def mkdir(self, path: Path) -> None:
        """Validate path allowlist then queue a mkdir operation.

        Args:
            path: Directory path to create (must be under an allowed root).

        Raises:
            SandboxViolationError: When *path* resolves outside allowed_paths.

        """
        self._validate_path(path)
        await super().mkdir(path)

    # ------------------------------------------------------------------
    # Legacy sync override
    # ------------------------------------------------------------------

    def commit(self) -> None:
        """Validate the legacy target path before performing an atomic write.

        Overrides StorageTransaction.commit() to check self._target against the
        allowlist before anything is written to disk.

        Raises:
            SandboxViolationError: When self._target resolves outside allowed_paths.

        """
        if self._target is not None:
            self._validate_path(self._target)
        super().commit()
