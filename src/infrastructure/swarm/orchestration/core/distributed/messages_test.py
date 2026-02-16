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
from infrastructure.swarm.orchestration.core.distributed.messages import CoordinatorMessage, RequestMessage, ResponseMessage, ControlMessage, MetricsMessage


def test_coordinatormessage_basic():
    assert CoordinatorMessage is not None


def test_requestmessage_basic():
    assert RequestMessage is not None


def test_responsemessage_basic():
    assert ResponseMessage is not None


def test_controlmessage_basic():
    assert ControlMessage is not None


def test_metricsmessage_basic():
    assert MetricsMessage is not None
