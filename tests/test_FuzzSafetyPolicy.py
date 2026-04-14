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

"""Per-module red tests for the FuzzSafetyPolicy contract module."""

from __future__ import annotations

from tests.test_fuzzing_core import _require_symbol


def test_fuzz_safety_policy_exposes_local_guard_contract() -> None:
    """Verify FuzzSafetyPolicy exposes target validation for local-only enforcement."""
    policy_cls = _require_symbol("FuzzSafetyPolicy", "FuzzSafetyPolicy")
    policy = policy_cls(
        allowed_hosts={"127.0.0.1", "localhost"},
        allowed_operators={"bit_flip"},
        max_cases=1,
        max_payload_bytes=16,
        max_total_bytes=16,
        max_duration_seconds=5,
    )
    assert hasattr(policy, "validate_target")
