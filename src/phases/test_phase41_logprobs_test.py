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
from .test_phase41_logprobs import TestLogprobFormat, TestTopLogprob, TestLogprobEntry, TestPromptLogprobs, TestSampleLogprobs, TestFlatLogprobs, TestLogprobsProcessor, TestStreamingLogprobs, TestLogprobsAnalyzer, TestUtilityFunctions


def test_testlogprobformat_basic():
    assert TestLogprobFormat is not None


def test_testtoplogprob_basic():
    assert TestTopLogprob is not None


def test_testlogprobentry_basic():
    assert TestLogprobEntry is not None


def test_testpromptlogprobs_basic():
    assert TestPromptLogprobs is not None


def test_testsamplelogprobs_basic():
    assert TestSampleLogprobs is not None


def test_testflatlogprobs_basic():
    assert TestFlatLogprobs is not None


def test_testlogprobsprocessor_basic():
    assert TestLogprobsProcessor is not None


def test_teststreaminglogprobs_basic():
    assert TestStreamingLogprobs is not None


def test_testlogprobsanalyzer_basic():
    assert TestLogprobsAnalyzer is not None


def test_testutilityfunctions_basic():
    assert TestUtilityFunctions is not None
