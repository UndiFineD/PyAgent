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
from infrastructure.engine.speculative.ngram_proposer import NgramConfig, NgramMatch, NgramProposalResult, NgramCache, NgramProposer, WeightedNgramProposer, PromptLookupProposer, HybridNgramProposer, NgramProposerFactory


def test_ngramconfig_basic():
    assert NgramConfig is not None


def test_ngrammatch_basic():
    assert NgramMatch is not None


def test_ngramproposalresult_basic():
    assert NgramProposalResult is not None


def test_ngramcache_basic():
    assert NgramCache is not None


def test_ngramproposer_basic():
    assert NgramProposer is not None


def test_weightedngramproposer_basic():
    assert WeightedNgramProposer is not None


def test_promptlookupproposer_basic():
    assert PromptLookupProposer is not None


def test_hybridngramproposer_basic():
    assert HybridNgramProposer is not None


def test_ngramproposerfactory_basic():
    assert NgramProposerFactory is not None
