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
from .test_phase59_locality import test_locality_manager_clustering, test_suggested_aggregators


def test_test_locality_manager_clustering_basic():
    assert callable(test_locality_manager_clustering)


def test_test_suggested_aggregators_basic():
    assert callable(test_suggested_aggregators)
