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

"""SandboxMixin — mixin providing sandboxed I/O factory and host validation."""

from __future__ import annotations

from src.core.sandbox.SandboxConfig import SandboxConfig
from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction
from src.core.sandbox.SandboxViolationError import SandboxViolationError


class SandboxMixin:
    """Mixin that equips an agent class with sandbox-enforced I/O helpers.

    Expects the consuming class to set ``self._sandbox_config`` to a
    ``SandboxConfig`` instance before calling any mixin method.

    Usage::

        class MyAgent(SandboxMixin):
            def __init__(self, allowed_dir: Path) -> None:
                self._sandbox_config = SandboxConfig.from_strings([str(allowed_dir)], [])
    """

    _sandbox_config: SandboxConfig

    def sandbox_tx(self) -> SandboxedStorageTransaction:
        """Return a new SandboxedStorageTransaction bound to this agent's sandbox config.

        Returns:
            A fresh SandboxedStorageTransaction instance ready for queuing operations.

        """
        return SandboxedStorageTransaction(sandbox=self._sandbox_config)

    def _validate_host(self, host: str) -> None:
        """Raise SandboxViolationError when *host* is not in the allowed_hosts list.

        A no-op when allow_all_hosts is True.

        Args:
            host: Hostname or IP string to validate against the allowlist.

        Raises:
            SandboxViolationError: When host is not in allowed_hosts and allow_all_hosts is False.

        """
        if self._sandbox_config.allow_all_hosts:
            return
        if host not in self._sandbox_config.allowed_hosts:
            raise SandboxViolationError(resource=host, reason="host not in allowed_hosts")
