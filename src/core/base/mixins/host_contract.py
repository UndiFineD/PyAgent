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

"""Host protocol and runtime validator for canonical base mixins."""

from __future__ import annotations

from typing import Protocol


class BaseMixinHostProtocol(Protocol):
    """Define minimum host capabilities used by canonical base mixins."""

    logger: object

    def get_runtime_context(self) -> dict[str, object]:
        """Return a runtime context payload used by mixin flows."""

    def emit_migration_event(self, event_name: str, payload: dict[str, object]) -> None:
        """Emit migration/compatibility events for observability."""


def validate_host_contract(host: object) -> None:
    """Validate required host capabilities for canonical mixin contracts.

    Args:
        host: Host instance that consumes canonical mixins.

    Raises:
        ValueError: Host is missing one or more required capabilities.

    """
    missing: list[str] = []

    if not hasattr(host, "logger"):
        missing.append("logger")

    runtime_context = getattr(host, "get_runtime_context", None)
    if not callable(runtime_context):
        missing.append("get_runtime_context")

    migration_event = getattr(host, "emit_migration_event", None)
    if not callable(migration_event):
        missing.append("emit_migration_event")

    if missing:
        raise ValueError("Host is missing required contract attributes/methods: " + ", ".join(missing))


def validate() -> bool:
    """Validate module import wiring for host contract helpers.

    Returns:
        True when module symbols are importable.

    """
    return BaseMixinHostProtocol is not None and validate_host_contract is not None


__all__ = ["BaseMixinHostProtocol", "validate_host_contract", "validate"]
