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
from core.base.logic.core.active_directory_analysis_core import PrivilegeLevel, ADObjectType, ADObject, ADEnumerationResult, ADVulnerability, ActiveDirectoryAnalysisCore


def test_privilegelevel_basic():
    assert PrivilegeLevel is not None


def test_adobjecttype_basic():
    assert ADObjectType is not None


def test_adobject_basic():
    assert ADObject is not None


def test_adenumerationresult_basic():
    assert ADEnumerationResult is not None


def test_advulnerability_basic():
    assert ADVulnerability is not None


def test_activedirectoryanalysiscore_basic():
    assert ActiveDirectoryAnalysisCore is not None
