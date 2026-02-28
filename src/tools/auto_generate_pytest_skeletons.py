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
Script to automatically generate pytest test skeletons for all uncovered src/*.py modules.
Generates *_test.py files for each module missing tests, covering all public classes/functions.
"""

import ast
from pathlib import Path

SRC_ROOT = Path("src")


def find_py_files_without_tests():
    """Find all .py files in src/ that do not have a corresponding *_test.py file."""
    py_files = [f for f in SRC_ROOT.rglob("*.py") if not f.name.endswith("_test.py")]
    test_files = {f.with_suffix("").name for f in SRC_ROOT.rglob("*_test.py")}
    uncovered = [f for f in py_files if f.with_suffix("").name + "_test" not in test_files]
    return uncovered


def extract_public_symbols(filepath):
    """Extract public class and function names from a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
        classes = [n.name for n in tree.body if isinstance(n, ast.ClassDef) and not n.name.startswith("_")]
        functions = [n.name for n in tree.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")]
        return classes, functions
    except (SyntaxError, FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Error parsing {filepath}: {e}")
        return [], []


def generate_test_skeleton(module_path, classes, functions):
    """Generate a pytest skeleton test file for the given module and its public classes/functions."""
    test_path = module_path.parent / (module_path.stem + "_test.py")
    header = """
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

import pytest
"""
    # Compute absolute import path relative to src/
    rel_path = module_path.relative_to(SRC_ROOT).with_suffix("")
    import_path = ".".join(rel_path.parts)
    imports = f"from {import_path} import "
    imports += ", ".join(classes + functions) if (classes or functions) else "*"
    body = ""
    for cls in classes:
        body += f"\n\ndef test_{cls.lower()}_basic():\n    assert {cls} is not None\n"
    for fn in functions:
        body += f"\n\ndef test_{fn}_basic():\n    assert callable({fn})\n"
    with open(test_path, "w", encoding="utf-8") as f:
        f.write(header + imports + "\n" + body)
    print(f"Generated: {test_path}")


def main():
    """Main function to find uncovered modules and generate test skeletons."""
    uncovered = find_py_files_without_tests()
    for module_path in uncovered:
        classes, functions = extract_public_symbols(module_path)
        generate_test_skeleton(module_path, classes, functions)

if __name__ == "__main__":
    main()
