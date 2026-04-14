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

"""Policy versioning helpers for routing decisions."""

from __future__ import annotations


def resolve_policy_version(policy: dict[str, object]) -> str:
    """Resolve immutable policy version string.

    Args:
        policy: Routing policy map.

    Returns:
        Policy version string.

    """
    value = policy.get("policy_version", "spr-v1")
    return str(value)


def validate() -> bool:
    """Validate policy version resolution behavior.

    Returns:
        True when policy version is resolved to a non-empty string.

    """
    return resolve_policy_version({"policy_version": "spr-v1"}) == "spr-v1"
