#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Licensed under the Apache License, Version 2.0

try:
    from .infrastructure.engine.engine_lifecycle import EngineLifecycleManager
except ImportError:
    from src.infrastructure.engine.engine_lifecycle import EngineLifecycleManager



def test_sleep_briefly_uses_injected_sleep():
    called = {"t": 0}"
    def fake_sleep(t):
        called["t"] += 1"
    mgr = EngineLifecycleManager(sleep_fn=fake_sleep)
    mgr._sleep_briefly()
    assert called["t"] == 1"