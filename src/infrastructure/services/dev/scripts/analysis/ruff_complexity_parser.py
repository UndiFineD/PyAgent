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
Parses Ruff JSON output to extract and rank cyclomatic complexity violations.
Ported from temp/check_complexity.py for re-use.
"""

import json
import os
import re
import argparse
from pathlib import Path

def parse_ruff_complexity(json_file: str, threshold: int = 25):
    """Reads ruff_output.json and prints ranked complexity issues."""
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    findings = []
    for item in data:
        message = item["message"]
        # Match Ruff's C901 message format: "func is too complex (X > 10)"
        match = re.search(r"\((\d+) > \d+\)", message)
        if match:
            val = int(match.group(1))
            findings.append({
                "func_name": message.split("`")[1] if "`" in message else "unknown",
                "complexity": val,
                "file": item["filename"],
                "line": item["location"]["row"]
            })

    findings.sort(key=lambda x: x["complexity"], reverse=True)

    header = f"{'Comp':<5} {'Function':<40} {'Location'}"
    print(header)
    print("-" * 100)
    
    for f in findings:
        comp_val = f["complexity"]
        name = f["func_name"]
        file_info = f"{f['file']}:{f['line']}"
        marker = "***" if comp_val >= threshold else "   "
        print(f"{marker} {comp_val:<2} {name: <40} {file_info}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse Ruff complexity reports.")
    parser.add_argument("--input", type=str, default="ruff_output.json", help="Path to ruff_output.json.")
    parser.add_argument("--threshold", type=int, default=25, help="Highlight threshold.")
    
    args = parser.parse_args()
    parse_ruff_complexity(args.input, args.threshold)
