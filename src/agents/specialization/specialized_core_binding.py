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

"""Binding planner between specialization requests and core contracts."""

from __future__ import annotations

from typing import Any

from src.agents.specialization.adapter_contracts import CoreInvocationPlan, ShellExecutionRequest
from src.agents.specialization.errors import CoreBindingError


class SpecializedCoreBinding:
    """Resolve core handlers for specialization shell requests.

    Args:
        core_registry: Registry exposing has_intent() and resolve().

    """

    def __init__(self, core_registry: Any) -> None:
        """Initialize core binding planner.

        Args:
            core_registry: Universal core registry dependency.

        """
        self._core_registry = core_registry

    def plan(self, shell_request: ShellExecutionRequest) -> CoreInvocationPlan:
        """Build invocation plan for a specialization shell request.

        Args:
            shell_request: Canonical shell execution request.

        Returns:
            Core invocation plan with resolved handler.

        Raises:
            CoreBindingError: If core target cannot be resolved.

        """
        target = shell_request.core_target.strip().lower()
        if not self._core_registry.has_intent(target):
            raise CoreBindingError(
                f"Unresolved core target: {target}",
                reason_code="core_target_unresolved",
            )

        handler = self._core_registry.resolve(target)
        return CoreInvocationPlan(core_target=target, handler=handler)


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when core binding planner is importable.

    """
    return True


__all__ = ["SpecializedCoreBinding", "validate"]
