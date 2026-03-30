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

"""Shared host-contract helpers for canonical base mixins."""

from __future__ import annotations

from src.core.base.mixins.host_contract import validate_host_contract


class BaseBehaviorMixin:
    """Provide common host-contract and event helper behavior for mixins."""

    def validate_host_contract(self) -> None:
        """Validate that this host satisfies the canonical host contract.

        Raises:
            ValueError: Host is missing required contract attributes/methods.

        """
        validate_host_contract(self)

    def _emit_migration_event(self, event_name: str, payload: dict[str, object]) -> None:
        """Emit migration events when the host exposes the event callback.

        Args:
            event_name: Event identifier.
            payload: JSON-like payload for observability.

        """
        emit = getattr(self, "emit_migration_event", None)
        if emit is None or not callable(emit):
            return

        emit(event_name, payload)


def validate() -> bool:
    """Validate module import wiring for shared base behavior helpers.

    Returns:
        True when module symbols are importable.

    """
    return True


__all__ = ["BaseBehaviorMixin", "validate"]
