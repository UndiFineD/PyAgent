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
from infrastructure.engine.output_processor import EventType, RequestEvent, LoRARequest, ParentRequest, SamplingParams, EngineCoreRequest, EngineCoreOutput, EngineCoreOutputs, RequestOutput, OutputProcessorOutput, RequestOutputCollector, RequestState, LoRARequestStates, OutputProcessor, IterationStats


def test_eventtype_basic():
    assert EventType is not None


def test_requestevent_basic():
    assert RequestEvent is not None


def test_lorarequest_basic():
    assert LoRARequest is not None


def test_parentrequest_basic():
    assert ParentRequest is not None


def test_samplingparams_basic():
    assert SamplingParams is not None


def test_enginecorerequest_basic():
    assert EngineCoreRequest is not None


def test_enginecoreoutput_basic():
    assert EngineCoreOutput is not None


def test_enginecoreoutputs_basic():
    assert EngineCoreOutputs is not None


def test_requestoutput_basic():
    assert RequestOutput is not None


def test_outputprocessoroutput_basic():
    assert OutputProcessorOutput is not None


def test_requestoutputcollector_basic():
    assert RequestOutputCollector is not None


def test_requeststate_basic():
    assert RequestState is not None


def test_lorarequeststates_basic():
    assert LoRARequestStates is not None


def test_outputprocessor_basic():
    assert OutputProcessor is not None


def test_iterationstats_basic():
    assert IterationStats is not None
