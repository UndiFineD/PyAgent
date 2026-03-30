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

"""Canonical sandbox mixin implementation for base mixin architecture."""

from __future__ import annotations

from src.core.base.mixins.base_behavior_mixin import BaseBehaviorMixin


class SandboxMixin(BaseBehaviorMixin):
    """Provide sandbox-enforced I/O helpers and host allow-list checks."""

    _sandbox_config: object

    def sandbox_tx(self) -> object:
        """Return a new storage transaction bound to this host sandbox config.

        Returns:
            Fresh sandboxed storage transaction.

        """
        from src.core.sandbox.SandboxedStorageTransaction import SandboxedStorageTransaction

        return SandboxedStorageTransaction(sandbox=self._sandbox_config)

    def _validate_host(self, host: str) -> None:
        """Reject a host that is not in the configured allowed-hosts list.

        Args:
            host: Hostname or IP string to validate.

        Raises:
            SandboxViolationError: Host is not allow-listed.

        """
        if self._sandbox_config.allow_all_hosts:
            return
        if host not in self._sandbox_config.allowed_hosts:
            self._emit_migration_event(
                "host_contract_error",
                {"mixin": "SandboxMixin", "host": host},
            )
            from src.core.sandbox.SandboxViolationError import SandboxViolationError

            raise SandboxViolationError(resource=host, reason="host not in allowed_hosts")


def validate() -> bool:
    """Validate that the canonical sandbox mixin module is importable.

    Returns:
        True when module symbols are importable.

    """
    assert SandboxMixin is not None
    return True


__all__ = ["SandboxMixin", "validate"]
