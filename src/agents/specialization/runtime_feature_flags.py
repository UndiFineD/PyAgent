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

"""Runtime feature flag checks for specialization path gating."""

from __future__ import annotations


def specialization_enabled(*, flag_enabled: bool, policy_authorized: bool) -> bool:
    """Determine whether specialization route is allowed to run.

    Args:
        flag_enabled: Feature flag state.
        policy_authorized: Authorization precondition state.

    Returns:
        True only when both feature and policy preconditions are satisfied.

    """
    return flag_enabled and policy_authorized


def validate() -> bool:
    """Run module-level validation checks.

    Returns:
        True when feature-flag helper is importable.

    """
    return True


__all__ = ["specialization_enabled", "validate"]
