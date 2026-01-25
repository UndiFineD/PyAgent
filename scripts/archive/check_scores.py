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
Check Scores module.
"""

import subprocess
import sys

files = [
    "c:/DEV/PyAgent/src/core/base/execution/agent_command_handler.py",
    "c:/DEV/PyAgent/src/core/base/execution/agent_delegator.py",
    "c:/DEV/PyAgent/src/core/base/execution/shell_executor.py"
]

for f in files:
    print(f"Checking {f}...")
    result = subprocess.run([sys.executable, "-m", "pylint", f], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "Your code has been rated at" in line:
            print(line)