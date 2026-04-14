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
"""MCP server subprocess sandbox.

Responsible for spawning server subprocesses with hardened environments,
enforcing path allowlists, optional SHA-256 binary pinning, and graceful
termination with SIGTERM → SIGKILL fallback.

Design: ``McpSandbox`` is intentionally stateless.  Each method that
affects a server process takes the :class:`~src.mcp.McpServerConfig.McpServerConfig`
(and/or the live :class:`asyncio.subprocess.Process`) as an explicit parameter.
This enables the registry to manage multiple servers from a single sandbox
instance and simplifies testing without constructor arg injection.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from src.mcp.exceptions import (
    McpPathForbidden,
    McpPinMismatch,
    McpSandboxError,
    McpSecretNotFound,
)
from src.mcp.McpServerConfig import McpServerConfig

__all__ = ["McpSandbox"]


def _is_subpath(child: Path, parent: Path) -> bool:
    """Return True if *child* is at or under *parent*."""
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


class McpSandbox:
    """Stateless sandbox helper for MCP server subprocesses.

    All operations receive the configuration and/or process handle as explicit
    parameters so one sandbox instance may be reused across reloads.
    """

    # ------------------------------------------------------------------
    # Environment construction
    # ------------------------------------------------------------------

    def build_env(self, config: McpServerConfig) -> tuple[dict[str, str], dict[str, str]]:
        """Build a sanitised subprocess environment from *config*.

        Starts from an **empty** base (never copies ``os.environ``) and adds:

        1. ``PATH`` set to the parent directory of ``config.command[0]``.
        2. All key/value pairs from ``config.env_vars``.
        3. Values of ``config.secret_refs`` resolved from ``os.environ``.

        The masked variant replaces every secret value with ``"[REDACTED]"``
        so it is safe to include in log output.

        Args:
            config: Server configuration describing env construction rules.

        Returns:
            A 2-tuple ``(env, masked_env)`` where *env* contains live secret
            values and *masked_env* is safe to log.

        Raises:
            McpSecretNotFound: If any name in ``config.secret_refs`` is absent
                from ``os.environ``.

        """
        import os

        binary_dir = str(Path(config.command[0]).parent)
        env: dict[str, str] = {"PATH": binary_dir}
        masked_env: dict[str, str] = {"PATH": binary_dir}

        env.update(config.env_vars)
        masked_env.update(config.env_vars)

        missing = next(
            (ref for ref in config.secret_refs if os.environ.get(ref) is None),
            None,
        )
        if missing is not None:
            raise McpSecretNotFound(
                f"Secret '{missing}' required by server '{config.name}' is not set in the environment"
            )
        env.update({ref: os.environ[ref] for ref in config.secret_refs})
        masked_env.update({ref: "[REDACTED]" for ref in config.secret_refs})

        return env, masked_env

    # ------------------------------------------------------------------
    # Subprocess lifecycle
    # ------------------------------------------------------------------

    async def spawn(self, config: McpServerConfig) -> asyncio.subprocess.Process:
        """Start the server subprocess and return the process handle.

        Builds a sanitised environment via :meth:`build_env`, optionally
        verifies the SHA-256 pin, then launches the subprocess.  The
        ``stdin``, ``stdout``, and ``stderr`` streams are all piped.

        Args:
            config: Server configuration describing all spawn parameters.

        Returns:
            The running :class:`asyncio.subprocess.Process`.

        Raises:
            McpPinMismatch: If ``config.sha256_pin`` is set and does not match
                the SHA-256 hash of ``config.command[0]``.
            McpSandboxError: If the subprocess executable is not found or
                fails to start.

        """
        import hashlib

        env, _masked_env = self.build_env(config)

        if config.sha256_pin is not None:
            binary = Path(config.command[0])
            try:
                binary_bytes = binary.read_bytes()
            except OSError as exc:
                raise McpPinMismatch(f"Cannot read binary '{binary}' to verify SHA-256 pin") from exc
            computed = hashlib.sha256(binary_bytes).hexdigest()
            if computed != config.sha256_pin:
                raise McpPinMismatch(
                    f"SHA-256 pin mismatch for '{binary}': expected {config.sha256_pin!r}, got {computed!r}"
                )

        try:
            process = await asyncio.create_subprocess_exec(
                *config.command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
        except (OSError, FileNotFoundError) as exc:
            raise McpSandboxError(f"Failed to spawn '{config.command[0]}': {exc}") from exc

        return process

    async def terminate(self, process: asyncio.subprocess.Process) -> None:
        """Terminate a subprocess gracefully with SIGTERM → SIGKILL fallback.

        Sends SIGTERM, waits up to 5 seconds, then sends SIGKILL if the
        process is still alive.  Always awaits :meth:`~asyncio.subprocess.Process.wait`
        to reap the child.

        Args:
            process: The subprocess to terminate.

        """
        process.terminate()
        try:
            await asyncio.wait_for(process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()

    # ------------------------------------------------------------------
    # Path validation
    # ------------------------------------------------------------------

    def validate_path(self, path: str, config: McpServerConfig) -> Path:
        """Resolve *path* and verify it falls within an allowed prefix.

        Symlinks are resolved before the prefix check so that
        ``/workspace/../etc/passwd`` cannot escape the allowlist.

        Args:
            path: An absolute or relative filesystem path to validate.
            config: Server configuration providing the ``allowed_paths``
                allowlist.

        Returns:
            The fully resolved :class:`pathlib.Path`.

        Raises:
            McpPathForbidden: If the resolved path is not under any entry in
                ``config.allowed_paths``, or if ``allowed_paths`` is empty.

        """
        resolved = Path(path).resolve()
        if not any(_is_subpath(resolved, Path(a).resolve()) for a in config.allowed_paths):
            raise McpPathForbidden(f"Path '{resolved}' is not under any allowed prefix: {config.allowed_paths!r}")
        return resolved
