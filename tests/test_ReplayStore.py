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

"""Per-module red tests for ReplayStore contract module."""

from __future__ import annotations

from typing import Any

import pytest

from tests.test_shadow_replay import _build_envelope, _require_symbol


@pytest.mark.asyncio
async def test_replay_store_persists_and_loads_one_envelope(tmp_path: Any) -> None:
    """Verify ReplayStore persists and loads one envelope in-session.

    This test is intentionally red until the replay store module exists.
    """
    replay_store_cls = _require_symbol("ReplayStore", "ReplayStore")
    store = replay_store_cls(root_path=tmp_path)
    await store.append_envelope(_build_envelope(sequence_no=1, session_id="s-module-store"))
    loaded = await store.load_session("s-module-store")
    assert len(loaded) == 1
    assert loaded[0].sequence_no == 1
