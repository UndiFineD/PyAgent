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
from .test_phase42_templates import TestTemplateType, TestModelType, TestTemplateConfig, TestRenderOptions, TestChatTemplate, TestJinjaTemplate, TestChatTemplateRegistry, TestTemplateResolver, TestConvenienceFunctions


def test_testtemplatetype_basic():
    assert TestTemplateType is not None


def test_testmodeltype_basic():
    assert TestModelType is not None


def test_testtemplateconfig_basic():
    assert TestTemplateConfig is not None


def test_testrenderoptions_basic():
    assert TestRenderOptions is not None


def test_testchattemplate_basic():
    assert TestChatTemplate is not None


def test_testjinjatemplate_basic():
    assert TestJinjaTemplate is not None


def test_testchattemplateregistry_basic():
    assert TestChatTemplateRegistry is not None


def test_testtemplateresolver_basic():
    assert TestTemplateResolver is not None


def test_testconveniencefunctions_basic():
    assert TestConvenienceFunctions is not None
