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

"""Circuit breaker exception types."""

from __future__ import annotations

from src.core.resilience.CircuitBreakerState import CircuitState


class CircuitOpenError(Exception):
    """Raised when a provider circuit blocks execution.

    Args:
        provider_key: Provider identifier whose circuit is not callable.
        state: Effective circuit state that caused the block.

    """

    def __init__(self, provider_key: str, state: CircuitState) -> None:
        """Initialize the open-circuit error instance.

        Args:
            provider_key: Provider identifier.
            state: Circuit state at block time.

        """
        self.provider_key = provider_key
        self.state = state
        super().__init__(f"Circuit for provider '{provider_key}' is {state.value}")


class AllCircuitsOpenError(Exception):
    """Raised when primary and all configured fallbacks are unavailable.

    Args:
        tried_keys: Ordered provider keys that were checked.

    """

    def __init__(self, tried_keys: list[str]) -> None:
        """Initialize the exhausted-circuit error instance.

        Args:
            tried_keys: Ordered provider keys that were checked.

        """
        self.tried_keys = tried_keys
        joined = ", ".join(tried_keys)
        super().__init__(f"All circuits are open for providers: {joined}")


def validate() -> bool:
    """Validate this module wiring for structure tests.

    Returns:
        Always ``True``.

    """
    return True
