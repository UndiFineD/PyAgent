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
from core.base.logic.structures.flat_logprobs import Logprob, FlatLogprobs, LogprobsAccumulator, create_prompt_logprobs, create_sample_logprobs


def test_logprob_basic():
    assert Logprob is not None


def test_flatlogprobs_basic():
    assert FlatLogprobs is not None


def test_logprobsaccumulator_basic():
    assert LogprobsAccumulator is not None


def test_create_prompt_logprobs_basic():
    assert callable(create_prompt_logprobs)


def test_create_sample_logprobs_basic():
    assert callable(create_sample_logprobs)
