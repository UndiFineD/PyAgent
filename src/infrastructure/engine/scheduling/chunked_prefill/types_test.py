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
    from infrastructure.engine.scheduling.chunked_prefill.types import ChunkState, ChunkPriority, ChunkMetrics, PrefillChunk, ChunkedRequest, ChunkedPrefillConfig
except ImportError:
    from infrastructure.engine.scheduling.chunked_prefill.types import ChunkState, ChunkPriority, ChunkMetrics, PrefillChunk, ChunkedRequest, ChunkedPrefillConfig



def test_chunkstate_basic():
    assert ChunkState is not None


def test_chunkpriority_basic():
    assert ChunkPriority is not None


def test_chunkmetrics_basic():
    assert ChunkMetrics is not None


def test_prefillchunk_basic():
    assert PrefillChunk is not None


def test_chunkedrequest_basic():
    assert ChunkedRequest is not None


def test_chunkedprefillconfig_basic():
    assert ChunkedPrefillConfig is not None
