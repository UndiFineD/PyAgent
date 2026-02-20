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
    from infrastructure.engine.structured.guidance_backend import GuidanceTemplateType, GuidanceVariable, GuidanceTemplate, GuidanceState, CompiledGuidanceProgram, GuidanceGrammar, GuidanceBackend, AsyncGuidanceBackend
except ImportError:
    from infrastructure.engine.structured.guidance_backend import GuidanceTemplateType, GuidanceVariable, GuidanceTemplate, GuidanceState, CompiledGuidanceProgram, GuidanceGrammar, GuidanceBackend, AsyncGuidanceBackend



def test_guidancetemplatetype_basic():
    assert GuidanceTemplateType is not None


def test_guidancevariable_basic():
    assert GuidanceVariable is not None


def test_guidancetemplate_basic():
    assert GuidanceTemplate is not None


def test_guidancestate_basic():
    assert GuidanceState is not None


def test_compiledguidanceprogram_basic():
    assert CompiledGuidanceProgram is not None


def test_guidancegrammar_basic():
    assert GuidanceGrammar is not None


def test_guidancebackend_basic():
    assert GuidanceBackend is not None


def test_asyncguidancebackend_basic():
    assert AsyncGuidanceBackend is not None
