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
"""MCP server configuration dataclass.

Parses and validates the per-server section of ``mcp_servers.yml``:

Example YAML entry::

    - name: github
      command: ["npx", "-y", "@modelcontextprotocol/server-github"]
      secret_refs: ["GITHUB_TOKEN"]
      allowed_hosts: ["api.github.com"]
      timeout_seconds: 30.0
      enabled: false
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from src.mcp.exceptions import McpConfigError

__all__ = ["McpServerConfig"]

_VALID_RESTART_POLICIES = {"on-failure", "always", "never"}
_VALID_TRANSPORTS = {"stdio", "http+sse"}
_VALID_STARTUP_MODES = {"eager", "lazy"}


@dataclass
class McpServerConfig:
    """Configuration for a single external MCP server process.

    Attributes:
        name: Unique slug used as the namespace prefix in tool names
            (e.g. ``"github"`` → ``mcp::github::create_issue``).
        command: argv list for the server subprocess.  The first element is
            the executable; never passed through a shell.
        env_vars: Static environment variables injected into the server
            process on top of the sanitised base environment.
        secret_refs: Names of OS environment variables whose values are
            injected at spawn-time and redacted in all log output.
        allowed_paths: Filesystem paths the sandbox permits the server to
            access.  Empty list means deny all.
        allowed_hosts: Hostnames the sandbox permits outbound connections to.
            Use ``"*"`` to allow all.
        timeout_seconds: Per-call timeout for :meth:`McpClient.call_tool`.
        restart_policy: One of ``"on-failure"``, ``"always"``, or ``"never"``.
        sha256_pin: Expected SHA-256 hex digest of the server executable.
            ``None`` disables pinning.
        transport: Wire transport — ``"stdio"`` (default) or ``"http+sse"``.
        startup_mode: ``"eager"`` (default, start at registry init) or
            ``"lazy"`` (start on first tool call).
        enabled: When ``False`` the server is ignored by the registry.
        heartbeat_interval_seconds: Seconds between health-monitor pings.
        max_restart_attempts: Maximum consecutive auto-restarts before the
            health monitor marks the server permanently failed.

    """

    name: str
    command: list[str]
    env_vars: dict[str, str] = field(default_factory=dict)
    secret_refs: list[str] = field(default_factory=list)
    allowed_paths: list[str] = field(default_factory=list)
    allowed_hosts: list[str] = field(default_factory=list)
    timeout_seconds: float = 30.0
    restart_policy: str = "on-failure"
    sha256_pin: Optional[str] = None
    transport: str = "stdio"
    startup_mode: str = "eager"
    enabled: bool = True
    heartbeat_interval_seconds: float = 30.0
    max_restart_attempts: int = 3

    def __post_init__(self) -> None:
        """Validate fields after dataclass initialisation.

        Raises:
            McpConfigError: If ``name`` or ``command`` are missing/empty, or
                if ``restart_policy``, ``transport``, or ``startup_mode``
                contain unrecognised values.

        """
        if not self.name:
            raise McpConfigError("McpServerConfig.name must not be empty")
        if not self.command:
            raise McpConfigError(f"McpServerConfig[{self.name!r}].command must not be empty")
        if self.restart_policy not in _VALID_RESTART_POLICIES:
            raise McpConfigError(
                f"McpServerConfig[{self.name!r}].restart_policy={self.restart_policy!r} "
                f"is not one of {sorted(_VALID_RESTART_POLICIES)}"
            )
        if self.transport not in _VALID_TRANSPORTS:
            raise McpConfigError(
                f"McpServerConfig[{self.name!r}].transport={self.transport!r} "
                f"is not one of {sorted(_VALID_TRANSPORTS)}"
            )
        if self.startup_mode not in _VALID_STARTUP_MODES:
            raise McpConfigError(
                f"McpServerConfig[{self.name!r}].startup_mode={self.startup_mode!r} "
                f"is not one of {sorted(_VALID_STARTUP_MODES)}"
            )

    @classmethod
    def from_dict(cls, data: dict) -> "McpServerConfig":
        """Construct a McpServerConfig from a plain dict (e.g. from PyYAML).

        Only keys that correspond to known dataclass fields are forwarded;
        unknown keys are silently ignored so that YAML files can carry
        documentation-only keys without breaking the parser.

        Args:
            data: Mapping produced by ``yaml.safe_load`` for a single server
                entry.  Must contain at least ``name`` and ``command``.

        Returns:
            A fully validated :class:`McpServerConfig` instance.

        Raises:
            McpConfigError: If ``name`` or ``command`` are absent in *data*,
                or if any field value fails the post-init validation.

        """
        if "name" not in data:
            raise McpConfigError("McpServerConfig.from_dict: 'name' is required")
        if "command" not in data:
            raise McpConfigError(
                f"McpServerConfig.from_dict[{data.get('name')!r}]: 'command' is required"
            )
        known_keys = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in known_keys}
        return cls(**filtered)
