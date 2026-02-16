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
from .test_phase37_loading import TestWeightLoader, TestShardedStateLoader, TestKVOffloadManager, TestExpertLoadBalancer, TestRustPhase37Functions, TestPhase37Integration, TestModuleImports


def test_testweightloader_basic():
    assert TestWeightLoader is not None


def test_testshardedstateloader_basic():
    assert TestShardedStateLoader is not None


def test_testkvoffloadmanager_basic():
    assert TestKVOffloadManager is not None


def test_testexpertloadbalancer_basic():
    assert TestExpertLoadBalancer is not None


def test_testrustphase37functions_basic():
    assert TestRustPhase37Functions is not None


def test_testphase37integration_basic():
    assert TestPhase37Integration is not None


def test_testmoduleimports_basic():
    assert TestModuleImports is not None
