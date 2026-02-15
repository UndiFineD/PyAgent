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

import json
import os

LINT_RESULTS_PATH = r"c:\Dev\PyAgent\lint_results.json"

def main():
    if not os.path.exists(LINT_RESULTS_PATH):
        print("Not found")
        return

    with open(LINT_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    file_issues = []
    for entry in data:
        issues = 0
        if "flake8" in entry and entry["flake8"]["stdout"]:
            issues += len(entry["flake8"]["stdout"].splitlines())
        if "ruff" in entry and entry["ruff"]["stdout"]:
            # Ruff output is more complex, but we can count lines starting with it
            issues += len([line for line in entry["ruff"]["stdout"].splitlines() if line.strip()])
        
        file_issues.append((entry["file"], issues))

    file_issues.sort(key=lambda x: x[1], reverse=True)

    print(f"Top 20 Offending Files (out of {len(data)}):")
    for f, count in file_issues[:20]:
        print(f"{count:4} : {f}")

if __name__ == "__main__":
    main()
