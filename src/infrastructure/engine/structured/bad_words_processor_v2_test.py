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
except ImportError:
    import pytest

try:
    from infrastructure.engine.structured.bad_words_processor_v2 import BadWordsPenaltyMode, TrieNode, BadWordsProcessorV2, BadPhrasesProcessor, apply_bad_words, apply_bad_words_with_drafts
except ImportError:
    from infrastructure.engine.structured.bad_words_processor_v2 import BadWordsPenaltyMode, TrieNode, BadWordsProcessorV2, BadPhrasesProcessor, apply_bad_words, apply_bad_words_with_drafts



def test_badwordspenaltymode_basic():
    assert BadWordsPenaltyMode is not None


def test_trienode_basic():
    assert TrieNode is not None


def test_badwordsprocessorv2_basic():
    assert BadWordsProcessorV2 is not None


def test_badphrasesprocessor_basic():
    assert BadPhrasesProcessor is not None


def test_apply_bad_words_basic():
    assert callable(apply_bad_words)


def test_apply_bad_words_with_drafts_basic():
    assert callable(apply_bad_words_with_drafts)
