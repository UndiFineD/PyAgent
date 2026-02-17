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
from core.base.logic.core.ai_security_validation_core import SecurityIssue, SecurityScanResult, JailbreakAttempt, AISecurityValidationCore


def test_securityissue_basic():
    assert SecurityIssue is not None


def test_securityscanresult_basic():
    assert SecurityScanResult is not None


def test_jailbreakattempt_basic():
    assert JailbreakAttempt is not None


def test_aisecurityvalidationcore_basic():
    assert AISecurityValidationCore is not None
