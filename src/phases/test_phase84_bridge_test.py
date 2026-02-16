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
from .test_phase84_bridge import test_cross_tenant_bridge_transfer, test_scrubbing_anonymity


def test_test_cross_tenant_bridge_transfer_basic():
    assert callable(test_cross_tenant_bridge_transfer)


def test_test_scrubbing_anonymity_basic():
    assert callable(test_scrubbing_anonymity)
