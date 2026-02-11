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

"""Pytest fixtures for test_agent_test_utils tests."""

import pytest
from typing import Any

# Add src to path
import sys
from pathlib import Path
src_path = str(Path(__file__).parent.parent.parent.parent.parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from tests.utils.agent_test_utils import agent_dir_on_path  # noqa: E402


@pytest.fixture
def utils_module() -> Any:
    """Load and return the agent_test_utils module."""
    with agent_dir_on_path():
        import src.infrastructure.services.dev.test_utils as test_utils

        return test_utils
