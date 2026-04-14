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

"""Public exports for the universal shell facade package."""

from src.core.universal.exceptions import (
    CoreExecutionError,
    CoreNotRegisteredError,
    CoreRegistrationError,
    CoreTimeoutError,
    EnvelopeValidationError,
    LegacyDispatchError,
    RoutingContractError,
    UniversalShellError,
)
from src.core.universal.UniversalAgentShell import DispatchResult, UniversalAgentShell
from src.core.universal.UniversalCoreRegistry import UniversalCoreRegistry
from src.core.universal.UniversalIntentRouter import RoutingDecision, TaskEnvelope, UniversalIntentRouter


def validate() -> bool:
    """Run package-level validation checks.

    Returns:
        True when facade package exports are importable.

    """
    return True


__all__ = [
    "TaskEnvelope",
    "RoutingDecision",
    "DispatchResult",
    "UniversalIntentRouter",
    "UniversalCoreRegistry",
    "UniversalAgentShell",
    "UniversalShellError",
    "EnvelopeValidationError",
    "RoutingContractError",
    "CoreRegistrationError",
    "CoreNotRegisteredError",
    "CoreExecutionError",
    "CoreTimeoutError",
    "LegacyDispatchError",
    "validate",
]
