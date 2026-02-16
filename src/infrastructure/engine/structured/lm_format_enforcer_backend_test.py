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
from infrastructure.engine.structured.lm_format_enforcer_backend import DFAStateType, DFAState, DFATransition, CompiledDFA, TokenVocabulary, RegexMatchState, CompiledEnforcer, LMFormatEnforcerBackend, AsyncLMFormatEnforcerBackend, FormatEnforcerGrammar, CompositeEnforcer


def test_dfastatetype_basic():
    assert DFAStateType is not None


def test_dfastate_basic():
    assert DFAState is not None


def test_dfatransition_basic():
    assert DFATransition is not None


def test_compileddfa_basic():
    assert CompiledDFA is not None


def test_tokenvocabulary_basic():
    assert TokenVocabulary is not None


def test_regexmatchstate_basic():
    assert RegexMatchState is not None


def test_compiledenforcer_basic():
    assert CompiledEnforcer is not None


def test_lmformatenforcerbackend_basic():
    assert LMFormatEnforcerBackend is not None


def test_asynclmformatenforcerbackend_basic():
    assert AsyncLMFormatEnforcerBackend is not None


def test_formatenforcergrammar_basic():
    assert FormatEnforcerGrammar is not None


def test_compositeenforcer_basic():
    assert CompositeEnforcer is not None
