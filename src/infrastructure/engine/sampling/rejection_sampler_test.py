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
from infrastructure.engine.sampling.rejection_sampler import RejectionStrategy, RecoveryMode, RejectionConfig, AcceptanceStats, RejectionOutput, ProbabilityProvider, RejectionSampler, StreamingRejectionSampler, BatchRejectionSampler, create_rejection_sampler


def test_rejectionstrategy_basic():
    assert RejectionStrategy is not None


def test_recoverymode_basic():
    assert RecoveryMode is not None


def test_rejectionconfig_basic():
    assert RejectionConfig is not None


def test_acceptancestats_basic():
    assert AcceptanceStats is not None


def test_rejectionoutput_basic():
    assert RejectionOutput is not None


def test_probabilityprovider_basic():
    assert ProbabilityProvider is not None


def test_rejectionsampler_basic():
    assert RejectionSampler is not None


def test_streamingrejectionsampler_basic():
    assert StreamingRejectionSampler is not None


def test_batchrejectionsampler_basic():
    assert BatchRejectionSampler is not None


def test_create_rejection_sampler_basic():
    assert callable(create_rejection_sampler)
