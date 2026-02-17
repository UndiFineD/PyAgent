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
from infrastructure.engine.sampling.kernels import TemperatureSampler, TopKSampler, TopPSampler, TopKTopPSampler, GumbelSampler, RepetitionPenaltySampler, PenaltySampler


def test_temperaturesampler_basic():
    assert TemperatureSampler is not None


def test_topksampler_basic():
    assert TopKSampler is not None


def test_toppsampler_basic():
    assert TopPSampler is not None


def test_topktoppsampler_basic():
    assert TopKTopPSampler is not None


def test_gumbelsampler_basic():
    assert GumbelSampler is not None


def test_repetitionpenaltysampler_basic():
    assert RepetitionPenaltySampler is not None


def test_penaltysampler_basic():
    assert PenaltySampler is not None
