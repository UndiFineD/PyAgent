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
from infrastructure.services.dev.scripts.management.debug_phase_20_21 import test_visualization_and_memory, test_observability, test_gui_backend


def test_test_visualization_and_memory_basic():
    assert callable(test_visualization_and_memory)


def test_test_observability_basic():
    assert callable(test_observability)


def test_test_gui_backend_basic():
    assert callable(test_gui_backend)
