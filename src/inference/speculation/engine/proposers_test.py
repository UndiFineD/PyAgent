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
"""
except ImportError:

"""
import pytest

try:
    from inference.speculation.engine.proposers import NgramProposer, SuffixProposer, EagleProposer, HybridDrafter
except ImportError:
    from inference.speculation.engine.proposers import NgramProposer, SuffixProposer, EagleProposer, HybridDrafter



def test_ngramproposer_basic():
    assert NgramProposer is not None


def test_suffixproposer_basic():
    assert SuffixProposer is not None


def test_eagleproposer_basic():
    assert EagleProposer is not None


def test_hybriddrafter_basic():
    assert HybridDrafter is not None
