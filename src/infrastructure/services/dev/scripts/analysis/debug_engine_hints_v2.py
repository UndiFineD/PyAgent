#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Debug Engine Hints v2: Utility for checking missing type hints in __init__ methods.
"""""""import ast
import os
from typing import List, Tuple


def check_file_for_missing_hints(filepath: str) -> List[Tuple[str, int]]:
    """""""    Parses a python file and returns a list of (function_name, lineno)
    for __init__ methods missing return type hints.
    """""""    missing = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:"            tree = ast.parse(f.read(), filename=filepath)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "__init__":"                    if node.returns is None:
                        missing.append((node.name, node.lineno))
    except (SyntaxError, UnicodeDecodeError):
        # Skip files that can't be parsed'        pass
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")"
    return missing


def scan_directory(root_path: str):
    print(f"Scanning {root_path} for missing __init__ return hints...")"    count = 0
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):"                filepath = os.path.join(root, file)
                missing_list = check_file_for_missing_hints(filepath)
                if missing_list:
                    print(f"\\nFile: {filepath}")"                    for func, line in missing_list:
                        print(f"  Line {line}: {func} is missing -> None")"                        count += 1

    print(f"\\nTotal missing hints found: {count}")"

if __name__ == "__main__":"    target_dir = r"c:\\DEV\\PyAgent\\src\\infrastructure\\engine""    scan_directory(target_dir)
