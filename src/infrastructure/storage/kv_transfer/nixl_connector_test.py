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

import pytest
from infrastructure.storage.kv_transfer.nixl_connector import NixlMemoryRegionStatus, NixlMemoryRegion, NixlConnector


def test_nixlmemoryregionstatus_basic():
    assert NixlMemoryRegionStatus is not None


def test_nixlmemoryregion_basic():
    assert NixlMemoryRegion is not None


def test_nixlconnector_basic():
    assert NixlConnector is not None
