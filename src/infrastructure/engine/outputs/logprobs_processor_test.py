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
from infrastructure.engine.outputs.logprobs_processor import TokenLogprob, TopLogprobs, LogprobsLists, LogprobsTensors, AsyncCPUTransfer, SamplerOutput, ModelRunnerOutput, StreamingLogprobsCollector, extract_top_k_logprobs_rust, batch_logprobs_to_cpu_rust


def test_tokenlogprob_basic():
    assert TokenLogprob is not None


def test_toplogprobs_basic():
    assert TopLogprobs is not None


def test_logprobslists_basic():
    assert LogprobsLists is not None


def test_logprobstensors_basic():
    assert LogprobsTensors is not None


def test_asynccputransfer_basic():
    assert AsyncCPUTransfer is not None


def test_sampleroutput_basic():
    assert SamplerOutput is not None


def test_modelrunneroutput_basic():
    assert ModelRunnerOutput is not None


def test_streaminglogprobscollector_basic():
    assert StreamingLogprobsCollector is not None


def test_extract_top_k_logprobs_rust_basic():
    assert callable(extract_top_k_logprobs_rust)


def test_batch_logprobs_to_cpu_rust_basic():
    assert callable(batch_logprobs_to_cpu_rust)
