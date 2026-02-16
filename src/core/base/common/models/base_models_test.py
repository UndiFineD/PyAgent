#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from core.base.common.models.base_models import CacheEntry, AuthConfig, SerializationConfig, FilePriorityConfig, ExecutionCondition, ValidationRule, ModelConfig, ConfigProfile, DiffResult, EnvironmentConfig, EnvironmentInstance


def test_cacheentry_basic():
    assert CacheEntry is not None


def test_authconfig_basic():
    assert AuthConfig is not None


def test_serializationconfig_basic():
    assert SerializationConfig is not None


def test_filepriorityconfig_basic():
    assert FilePriorityConfig is not None


def test_executioncondition_basic():
    assert ExecutionCondition is not None


def test_validationrule_basic():
    assert ValidationRule is not None


def test_modelconfig_basic():
    assert ModelConfig is not None


def test_configprofile_basic():
    assert ConfigProfile is not None


def test_diffresult_basic():
    assert DiffResult is not None


def test_environmentconfig_basic():
    assert EnvironmentConfig is not None


def test_environmentinstance_basic():
    assert EnvironmentInstance is not None
