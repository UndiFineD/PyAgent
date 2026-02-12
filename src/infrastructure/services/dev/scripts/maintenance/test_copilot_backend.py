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

"""
Test script for verifying Copilot backend integration.
"""

import sys
from pathlib import Path

# Robustly find the repository root
current_path = Path(__file__).resolve()
project_root = current_path
while project_root.name != 'src' and project_root.parent != project_root:
    project_root = project_root.parent
if project_root.name == 'src':
    project_root = project_root.parent

# Ensure the project root is in PYTHONPATH
sys.path.insert(0, str(project_root))

from src.infrastructure.compute.backend.llm_backends.copilot_cli_backend import \
    CopilotCliBackend  # noqa: E402 # pylint: disable=wrong-import-position


def test_copilot():
    """
    Test the Copilot CLI backend integration.
    """
    backend = CopilotCliBackend(None, None)  # Mock session/manager
    # Mock _is_working to return True as we don't have a connectivity manager
    # pylint: disable=protected-access
    backend._is_working = lambda x: True
    backend._record = lambda *args, **kwargs: None
    backend._update_status = lambda *args, **kwargs: None

    print("Testing Copilot CLI integration...")
    response = backend.chat("What is 2+2?", timeout_s=10)
    print(f"Response: {response}")


if __name__ == "__main__":
    test_copilot()
