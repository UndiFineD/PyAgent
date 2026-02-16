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
from infrastructure.storage.kv_transfer.connector.types import KVConnectorRole, KVTransferMode, KVTransferConfig, KVConnectorMetadata, KVCacheBlocks, ForwardContext, Request


def test_kvconnectorrole_basic():
    assert KVConnectorRole is not None


def test_kvtransfermode_basic():
    assert KVTransferMode is not None


def test_kvtransferconfig_basic():
    assert KVTransferConfig is not None


def test_kvconnectormetadata_basic():
    assert KVConnectorMetadata is not None


def test_kvcacheblocks_basic():
    assert KVCacheBlocks is not None


def test_forwardcontext_basic():
    assert ForwardContext is not None


def test_request_basic():
    assert Request is not None
