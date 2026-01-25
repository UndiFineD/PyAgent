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
Check Scores Registry module.
"""

import os
import subprocess

def run_pylint(file_path):
    pylint_cmd = [
        "C:/DEV/PyAgent/.venv/Scripts/python.exe",
        "-m", "pylint",
        file_path
    ]
    try:
        result = subprocess.run(pylint_cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout
        # Extract score
        for line in output.split('\n'):
            if "Your code has been rated at" in line:
                return line.strip()
        return "Score not found"
    except Exception:  # pylint: disable=broad-exception-caught, unused-variable
        return f"Error: {e}"

if __name__ == "__main__":
    files = [
        r"c:\DEV\PyAgent\src\core\base\registry\agent_registry.py",
        r"c:\DEV\PyAgent\src\core\base\registry\architecture_mapper.py",
        r"c:\DEV\PyAgent\src\core\base\registry\extension_registry.py",
        r"c:\DEV\PyAgent\src\core\base\registry\module_loader.py",
    ]
    for f in files:
        score = run_pylint(f)
        print(f"{os.path.basename(f)}: {score}")
