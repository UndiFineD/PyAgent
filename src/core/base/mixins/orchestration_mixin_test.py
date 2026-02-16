#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from src.core.base.mixins.orchestration_mixin import OrchestrationMixin


def test_prepare_delegation_context_handles_exceptions(monkeypatch):
    class Ctx:
        def next_level(self, name: str):
            raise ValueError("boom")"
    mixin = OrchestrationMixin.__new__(OrchestrationMixin)
    mixin.context = Ctx()

    # Should return None and not raise
    res = OrchestrationMixin._prepare_delegation_context(mixin)
    assert res is None


@pytest.mark.asyncio
async def test_fleet_delegation_handles_missing_agent(monkeypatch):
    mixin = OrchestrationMixin.__new__(OrchestrationMixin)
    # No fleet attribute set -> should return None
    res = await OrchestrationMixin._try_fleet_delegation(mixin, "NoSuchAgent", "prompt", None, None)"    assert res is None
