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
import re
import os
import sys

LINT_RESULTS_PATH = r"c:\Dev\PyAgent\lint_results.json"


def main():
    if len(sys.argv) < 2:
        print("Usage: python remove_lint_entry.py <file_path1> <file_path2> ...")
        sys.exit(1)

    target_files = [f.replace("/", "\\") for f in sys.argv[1:]]
    # Strip c:\Dev\PyAgent\ from each
    processed_targets = []
    for f in target_files:
        if f.lower().startswith(r"c:\dev\pyagent\\"):
            processed_targets.append(f[16:].lower())
        else:
            processed_targets.append(f.lower())

    if not os.path.exists(LINT_RESULTS_PATH):
        print(f"Error: {LINT_RESULTS_PATH} not found")
        sys.exit(1)

    with open(LINT_RESULTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    original_count = len(data)
    filtered_data = [entry for entry in data if entry["file"].lower() not in processed_targets]
    new_count = len(filtered_data)

    if original_count == new_count:
        print(f"No entries for {processed_targets} found or already removed.")
    else:
        with open(LINT_RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, indent=2)
        print(f"Removed {original_count - new_count} entries. {original_count} -> {new_count}")

    total_issues = 0
    for entry in filtered_data:
        # Count flake8 issues
        f8 = entry.get("flake8", {}).get("stdout", "").strip()
        if f8:
            total_issues += len(f8.splitlines())

        # Count ruff issues
        ruff = entry.get("ruff", {}).get("stdout", "").strip()
        if ruff and "All checks passed!" not in ruff:
            # Filter out summary lines if any
            lines = [l for l in ruff.splitlines() if not l.startswith("Found ") and not l.startswith("Checked ")]
            total_issues += len(lines)

        # Count mypy issues
        mypy = entry.get("mypy", {}).get("stdout", "").strip()
        if mypy and "Success: no issues found" not in mypy:
            match = re.search(r"Found (\d+) error", mypy)
            if match:
                total_issues += int(match.group(1))

    with open(LINT_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2)

    print(f"New file count: {new_count}")
    print(f"Total issues remaining: {total_issues}")


if __name__ == "__main__":
    main()

