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
    from core.base.logic.security.privilege_escalation_core import LUID, LUID_AND_ATTRIBUTES, TOKEN_PRIVILEGES, PROCESSENTRY32, PrivilegeEscalationCore
except ImportError:
    from core.base.logic.security.privilege_escalation_core import LUID, LUID_AND_ATTRIBUTES, TOKEN_PRIVILEGES, PROCESSENTRY32, PrivilegeEscalationCore



def test_luid_basic():
    assert LUID is not None


def test_luid_and_attributes_basic():
    assert LUID_AND_ATTRIBUTES is not None


def test_token_privileges_basic():
    assert TOKEN_PRIVILEGES is not None


def test_processentry32_basic():
    assert PROCESSENTRY32 is not None


def test_privilegeescalationcore_basic():
    assert PrivilegeEscalationCore is not None
