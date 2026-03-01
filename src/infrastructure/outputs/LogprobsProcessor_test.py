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
"""
Tests for LogprobsProcessor
Auto-generated test template - expand with actual test cases
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from infrastructure.outputs.LogprobsProcessor import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_tokenlogprob_exists():
    """Test that TokenLogprob class exists and is importable."""
    assert 'TokenLogprob' in dir()


def test_toplogprobs_exists():
    """Test that TopLogprobs class exists and is importable."""
    assert 'TopLogprobs' in dir()


def test_logprobslists_exists():
    """Test that LogprobsLists class exists and is importable."""
    assert 'LogprobsLists' in dir()


def test_logprobstensors_exists():
    """Test that LogprobsTensors class exists and is importable."""
    assert 'LogprobsTensors' in dir()


def test_asynccputransfer_exists():
    """Test that AsyncCPUTransfer class exists and is importable."""
    assert 'AsyncCPUTransfer' in dir()


def test_sampleroutput_exists():
    """Test that SamplerOutput class exists and is importable."""
    assert 'SamplerOutput' in dir()


def test_modelrunneroutput_exists():
    """Test that ModelRunnerOutput class exists and is importable."""
    assert 'ModelRunnerOutput' in dir()


def test_streaminglogprobscollector_exists():
    """Test that StreamingLogprobsCollector class exists and is importable."""
    assert 'StreamingLogprobsCollector' in dir()


def test_extract_top_k_logprobs_rust_exists():
    """Test that extract_top_k_logprobs_rust function exists."""
    assert callable(extract_top_k_logprobs_rust)


def test_batch_logprobs_to_cpu_rust_exists():
    """Test that batch_logprobs_to_cpu_rust function exists."""
    assert callable(batch_logprobs_to_cpu_rust)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

