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
from infrastructure.engine.parallel_sampling.suggested import SamplingStrategy, OutputKind, SamplingParams, CompletionOutput, ParentRequest, ParallelSamplingManager, BeamState, BeamSearchManager, DiverseSamplingManager, BestOfNFilter, IterationStats


def test_samplingstrategy_basic():
    assert SamplingStrategy is not None


def test_outputkind_basic():
    assert OutputKind is not None


def test_samplingparams_basic():
    assert SamplingParams is not None


def test_completionoutput_basic():
    assert CompletionOutput is not None


def test_parentrequest_basic():
    assert ParentRequest is not None


def test_parallelsamplingmanager_basic():
    assert ParallelSamplingManager is not None


def test_beamstate_basic():
    assert BeamState is not None


def test_beamsearchmanager_basic():
    assert BeamSearchManager is not None


def test_diversesamplingmanager_basic():
    assert DiverseSamplingManager is not None


def test_bestofnfilter_basic():
    assert BestOfNFilter is not None


def test_iterationstats_basic():
    assert IterationStats is not None
