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
"""MCP server ecosystem — exception hierarchy.

All exceptions derive from :class:`McpError` so callers can catch the entire
family with a single ``except McpError`` clause, or handle fine-grained cases
individually.

Hierarchy::

    McpError (base)
    ├── McpConfigError          — bad or missing config values
    ├── McpServerNotFound       — named server not in registry
    ├── McpServerNotEnabled     — server present but disabled
    ├── McpServerAlreadyEnabled — attempt to enable an already-running server
    ├── McpServerCrashed        — server process exited unexpectedly
    ├── McpCallTimeout          — tool call exceeded timeout_seconds
    ├── McpProtocolError        — malformed JSON-RPC message
    ├── McpToolError            — tool returned an error result from the server
    ├── McpSandboxError         — sandbox-level failure (spawn, env resolution)
    │   ├── McpPinMismatch      — SHA-256 pin did not match binary on disk
    │   ├── McpPathForbidden    — path not in allowed_paths allowlist
    │   └── McpSecretNotFound   — secret_refs entry absent from environment
    ├── McpToolNameCollision    — namespaced tool name already in registry
    └── McpHealthError          — health-monitor detected a non-recoverable state
"""

from __future__ import annotations

__all__ = [
    "McpError",
    "McpConfigError",
    "McpServerNotFound",
    "McpServerNotEnabled",
    "McpServerAlreadyEnabled",
    "McpServerCrashed",
    "McpCallTimeout",
    "McpProtocolError",
    "McpToolError",
    "McpSandboxError",
    "McpPinMismatch",
    "McpPathForbidden",
    "McpSecretNotFound",
    "McpToolNameCollision",
    "McpHealthError",
]


class McpError(Exception):
    """Base class for all MCP server ecosystem errors."""


class McpConfigError(McpError):
    """Raised when a server configuration value is missing or invalid."""


class McpServerNotFound(McpError):
    """Raised when the requested MCP server name is not registered."""


class McpServerNotEnabled(McpError):
    """Raised when an operation is attempted on a disabled server."""


class McpServerAlreadyEnabled(McpError):
    """Raised when :meth:`McpRegistry.enable` is called on an already-running server."""


class McpServerCrashed(McpError):
    """Raised when the MCP server subprocess exits unexpectedly."""


class McpCallTimeout(McpError):
    """Raised when a tool call exceeds ``timeout_seconds``."""


class McpProtocolError(McpError):
    """Raised when a JSON-RPC 2.0 message is malformed or unexpected."""


class McpToolError(McpError):
    """Raised when the MCP server returns an error result for a tool call."""


class McpSandboxError(McpError):
    """Raised for sandbox-level failures (process spawn, env resolution)."""


class McpPinMismatch(McpSandboxError):
    """Raised when the SHA-256 hash of a server binary does not match the configured pin."""


class McpPathForbidden(McpSandboxError):
    """Raised when a requested path falls outside the ``allowed_paths`` allowlist."""


class McpSecretNotFound(McpSandboxError):
    """Raised when a name listed in ``secret_refs`` is absent from the environment."""


class McpToolNameCollision(McpError):
    """Raised when a namespaced tool name is already present in the tool registry."""


class McpHealthError(McpError):
    """Raised by the health monitor on detection of a non-recoverable server state."""
