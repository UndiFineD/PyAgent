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
from infrastructure.engine.engine_core_client import RequestType, ClientConfig, EngineCoreClient, InprocClient, SyncMPClient, AsyncMPClient, create_client


def test_requesttype_basic():
    assert RequestType is not None


def test_clientconfig_basic():
    assert ClientConfig is not None


def test_enginecoreclient_basic():
    assert EngineCoreClient is not None


def test_inprocclient_basic():
    assert InprocClient is not None


def test_syncmpclient_basic():
    assert SyncMPClient is not None


def test_asyncmpclient_basic():
    assert AsyncMPClient is not None


def test_create_client_basic():
    assert callable(create_client)
