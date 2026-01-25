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
Check Scores Logic module.
"""

import os
import subprocess
import sys

def run_pylint(file_path):
    pylint_cmd = [sys.executable, "-m", "pylint", file_path, "--reports=n", "--score=y"]
    try:
        result = subprocess.run(pylint_cmd, capture_output=True, text=True, timeout=60)
        output = result.stdout
        for line in output.split("\n"):
            if "Your code has been rated at" in line:
                return line.strip()
        return "Score not found"
    except Exception:  # pylint: disable=broad-exception-caught, unused-variable
        return f"Error: {str(e)}"

def main():
    base_dir = "src/core/base/logic"
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                full_path = os.path.join(root, file)
                score = run_pylint(full_path)
                print(f"{full_path}: {score}")

if __name__ == "__main__":
    main()
