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

import pytest
from infrastructure.engine.engine_client.types import ClientMode, WorkerState, EngineClientConfig, SchedulerOutput, EngineOutput, WorkerInfo


def test_clientmode_basic():
    assert ClientMode is not None


def test_workerstate_basic():
    assert WorkerState is not None


def test_engineclientconfig_basic():
    assert EngineClientConfig is not None


def test_scheduleroutput_basic():
    assert SchedulerOutput is not None


def test_engineoutput_basic():
    assert EngineOutput is not None


def test_workerinfo_basic():
    assert WorkerInfo is not None
