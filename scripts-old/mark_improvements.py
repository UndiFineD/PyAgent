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

import os
import sys
import argparse
from pathlib import Path

def mark_improvements(autodoc_dir: str) -> None:
    """
    Scans the autodoc directory for *_improvements.md files.
    If a file contains '[ ]' followed by an improvement description,
    it replaces it with '[X]'.
    """
    autodoc_path = Path(autodoc_dir)
    if not autodoc_path.is_dir():
        print(f"Error: {autodoc_dir} is not a directory.")
        return

    processed_count = 0
    replacement_count = 0

    for file_path in autodoc_path.glob("*_improvements.md"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if "[ ]" in content:
                new_content = content.replace("[ ]", "[X]")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                replacement_count += content.count("[ ]")
                processed_count += 1
                print(f"Processed: {file_path.name}")
        except (OSError, IOError, UnicodeDecodeError) as e:
            print(f"Error processing {file_path.name}: {e}")

    print("\nSummary:")
    print(f"Files modified: {processed_count}")
    print(f"Improvements marked: {replacement_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mark improvements in autodoc files as [X]")
    parser.add_argument("--dir", default="docs/autodoc", help="Path to autodoc directory")
    args = parser.parse_args()

    mark_improvements(args.dir)
