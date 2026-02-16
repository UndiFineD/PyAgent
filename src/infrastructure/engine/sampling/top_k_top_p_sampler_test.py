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
from infrastructure.engine.sampling.top_k_top_p_sampler import SamplingBackend, NucleusSamplingVariant, TemperatureSchedule, SamplingConfig, SamplingState, BaseSampler, TopKTopPSampler, BatchTopKTopPSampler, GumbelSoftmaxSampler, create_sampler, apply_top_k_top_p


def test_samplingbackend_basic():
    assert SamplingBackend is not None


def test_nucleussamplingvariant_basic():
    assert NucleusSamplingVariant is not None


def test_temperatureschedule_basic():
    assert TemperatureSchedule is not None


def test_samplingconfig_basic():
    assert SamplingConfig is not None


def test_samplingstate_basic():
    assert SamplingState is not None


def test_basesampler_basic():
    assert BaseSampler is not None


def test_topktoppsampler_basic():
    assert TopKTopPSampler is not None


def test_batchtopktoppsampler_basic():
    assert BatchTopKTopPSampler is not None


def test_gumbelsoftmaxsampler_basic():
    assert GumbelSoftmaxSampler is not None


def test_create_sampler_basic():
    assert callable(create_sampler)


def test_apply_top_k_top_p_basic():
    assert callable(apply_top_k_top_p)
