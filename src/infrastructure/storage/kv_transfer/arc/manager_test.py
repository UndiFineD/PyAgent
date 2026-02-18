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

try:
    import pytest
except ImportError:
    import pytest

try:
    from infrastructure.storage.kv_transfer.arc.manager import ARCOffloadManager, AdaptiveARCManager, AsyncARCManager
except ImportError:
    from infrastructure.storage.kv_transfer.arc.manager import ARCOffloadManager, AdaptiveARCManager, AsyncARCManager



def test_arcoffloadmanager_basic():
    assert ARCOffloadManager is not None


def test_adaptivearcmanager_basic():
    assert AdaptiveARCManager is not None


def test_asyncarcmanager_basic():
    assert AsyncARCManager is not None
