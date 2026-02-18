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
    from core.base.common.base_exceptions import PyAgentException, InfrastructureError, LogicError, SecurityError, ModelError, ConfigurationError, CycleInterrupt
except ImportError:
    from core.base.common.base_exceptions import PyAgentException, InfrastructureError, LogicError, SecurityError, ModelError, ConfigurationError, CycleInterrupt



def test_pyagentexception_basic():
    assert PyAgentException is not None


def test_infrastructureerror_basic():
    assert InfrastructureError is not None


def test_logicerror_basic():
    assert LogicError is not None


def test_securityerror_basic():
    assert SecurityError is not None


def test_modelerror_basic():
    assert ModelError is not None


def test_configurationerror_basic():
    assert ConfigurationError is not None


def test_cycleinterrupt_basic():
    assert CycleInterrupt is not None
