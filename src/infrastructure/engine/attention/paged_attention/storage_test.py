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
from infrastructure.engine.attention.paged_attention.storage import BlockTable, SlotMapping, PagedKVCache, AttentionMetadata


def test_blocktable_basic():
    assert BlockTable is not None


def test_slotmapping_basic():
    assert SlotMapping is not None


def test_pagedkvcache_basic():
    assert PagedKVCache is not None


def test_attentionmetadata_basic():
    assert AttentionMetadata is not None
