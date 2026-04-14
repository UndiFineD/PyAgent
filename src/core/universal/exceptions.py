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

"""Exception hierarchy for the universal shell facade."""


class UniversalShellError(Exception):
    """Base exception for all universal shell failures."""


class EnvelopeValidationError(UniversalShellError):
    """Raised when a dispatch envelope violates the shell contract."""


class RoutingContractError(UniversalShellError):
    """Raised when router output violates expected routing semantics."""


class CoreRegistrationError(UniversalShellError):
    """Raised when core registration or handler contracts are invalid."""


class CoreNotRegisteredError(UniversalShellError):
    """Raised when resolving an unregistered core intent."""


class CoreExecutionError(UniversalShellError):
    """Raised when a core handler fails while executing a dispatch request."""


class CoreTimeoutError(UniversalShellError):
    """Raised when a core handler exceeds the configured execution timeout."""


class LegacyDispatchError(UniversalShellError):
    """Raised when legacy dispatch fails after a route or fallback decision."""


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when the module is importable and symbols are available.

    """
    return True


__all__ = [
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
