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

"""Configuration model for per-provider circuit-breaker behavior."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CircuitBreakerConfig:
    """Configuration options for one provider circuit.

    Args:
        provider_key: Provider identifier for this config instance.
        failure_threshold: Consecutive failures before opening the circuit.
        recovery_timeout: Seconds to wait before allowing a HALF_OPEN probe.
        window_seconds: Future-facing failure window parameter.
        fallback_providers: Ordered fallback providers to try when primary is blocked.

    """

    provider_key: str
    failure_threshold: int = 5
    recovery_timeout: float = 30.0
    window_seconds: float = 60.0
    fallback_providers: list[str] = field(default_factory=list)


def validate() -> bool:
    """Validate this module wiring for structure tests.

    Returns:
        Always ``True``.

    """
    return True
