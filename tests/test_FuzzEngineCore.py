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

"""Per-module red tests for the FuzzEngineCore contract module."""

from __future__ import annotations

from tests.test_fuzzing_core import _require_symbol


def test_fuzz_engine_core_exposes_campaign_scheduler_contract() -> None:
    """Verify FuzzEngineCore exposes a scheduling API for deterministic campaigns."""
    engine_cls = _require_symbol("FuzzEngineCore", "FuzzEngineCore")
    assert hasattr(engine_cls, "schedule_cases")
