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

"""Routing policy loading helpers."""

from __future__ import annotations


def load_policy(policy: dict[str, object] | None = None) -> dict[str, object]:
    """Load routing policy with deterministic defaults.

    Args:
        policy: Optional caller-provided policy map.

    Returns:
        Routing policy map.

    """
    if policy is None:
        return {"policy_version": "spr-v1", "confidence_threshold": 0.75}
    return dict(policy)


def validate() -> bool:
    """Validate policy loader defaults and copy behavior.

    Returns:
        True when defaults exist and provided policy is loaded.

    """
    defaults = load_policy()
    loaded = load_policy({"policy_version": "spr-v2", "confidence_threshold": 0.8})
    return (
        defaults.get("policy_version") == "spr-v1"
        and defaults.get("confidence_threshold") == 0.75
        and loaded.get("policy_version") == "spr-v2"
    )
