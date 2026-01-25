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
Check Base Agent module.
"""

import os
import subprocess

def run_pylint(file_path):
    pylint_cmd = [
        "C:/DEV/PyAgent/.venv/Scripts/python.exe",
        "-m", "pylint",
        file_path
    ]
    result = subprocess.run(pylint_cmd, capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    file_to_check = r"c:\DEV\PyAgent\src\core\base\lifecycle\base_agent.py"
    output = run_pylint(file_to_check)
    with open("final_score.txt", 'w', encoding='utf-8') as f:
        f.write(output)
    print("Done")