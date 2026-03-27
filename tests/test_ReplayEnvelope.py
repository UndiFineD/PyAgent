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

"""Per-module red tests for ReplayEnvelope contract module."""

from __future__ import annotations

from typing import Any

from tests.test_shadow_replay import _replay_envelope_payload, _require_symbol


def test_replay_envelope_exposes_contract_constructor() -> None:
    """Verify ReplayEnvelope can construct and validate canonical payloads.

    This test is intentionally red until the replay contract module exists.
    """
    replay_envelope_cls = _require_symbol("ReplayEnvelope", "ReplayEnvelope")
    envelope = replay_envelope_cls.from_dict(_replay_envelope_payload())
    payload: dict[str, Any] = envelope.to_dict()
    assert payload["session_id"] == "s-001"
