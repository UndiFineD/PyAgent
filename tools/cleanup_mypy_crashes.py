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


def cleanup_mypy_crashes(json_path):
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    original_count = len(data)
    new_data = []

    removal_count = 0

    for entry in data:
        # Check if flake8 and ruff pass
        f8_stdout = entry.get("flake8", {}).get("stdout")
        f8_clean = entry.get("flake8", {}).get("exit_code") == 0 and not f8_stdout
        ruff_out = entry.get("ruff", {}).get("stdout", "")
        ruff_clean = entry.get("ruff", {}).get("exit_code") == 0 and (
            "All checks passed" in ruff_out or not ruff_out
        )
        # Check if mypy crashed with the specific KeyError or similar internal error
        mypy_stderr = entry.get("mypy", {}).get("stderr", "")
        mypy_crashed = (
            entry.get("mypy", {}).get("exit_code") != 0
            and "KeyError: 'setter_type'" in mypy_stderr
        )
        if f8_clean and ruff_clean and mypy_crashed:
            removal_count += 1
            # Calculate issues removed (though here it's just a crash)
            continue

        new_data.append(entry)

    if removal_count > 0:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=2)
        print(f"Removed {removal_count} entries with mypy crashes. {original_count} -> {len(new_data)}.")
    else:
        print("No mypy crashes found to remove.")


if __name__ == "__main__":
    cleanup_mypy_crashes("lint_results.json")

