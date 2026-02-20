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
    from core.security.external_tools import SecurityLevel, ThreatCategory, SecurityPolicy, ToolSignature, ExternalToolSecurity
except ImportError:
    from core.security.external_tools import SecurityLevel, ThreatCategory, SecurityPolicy, ToolSignature, ExternalToolSecurity



def test_securitylevel_basic():
    assert SecurityLevel is not None


def test_threatcategory_basic():
    assert ThreatCategory is not None


def test_securitypolicy_basic():
    assert SecurityPolicy is not None


def test_toolsignature_basic():
    assert ToolSignature is not None


def test_externaltoolsecurity_basic():
    assert ExternalToolSecurity is not None
