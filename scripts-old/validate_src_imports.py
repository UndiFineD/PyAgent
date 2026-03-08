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
import importlib.util
from pathlib import Path

def validate_imports(src_dir: Path):
    """
    Attempts to import every .py file in the src directory to identify
    missing dependencies or syntax errors caused by imports.
    """
    print(f"Starting import validation in: {src_dir}")
    python_files = list(src_dir.rglob("*.py"))
    total_files = len(python_files)
    failed_imports = []

    # Add src to sys.path so relative/absolute imports within src resolve
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    # Also add the root directory as the workspace root is often expected
    root_dir = src_dir.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))

    for i, file_path in enumerate(python_files, 1):
        # Calculate module name relative to root for more accurate import testing
        try:
            relative_path = file_path.relative_to(root_dir)
            module_name = str(relative_path).replace(os.sep, ".").removesuffix(".py")
            print(f"[{i}/{total_files}] Checking {module_name}...", end="\r")
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                # We use exec_module to actually run the code and trigger import/syntax errors
                try:
                    spec.loader.exec_module(module)
                except BaseException as e:
                    # Catch Skipped errors from pytest.skip calls at module level (Skipped is a BaseException)
                    if e.__class__.__name__ == "Skipped":
                        print(f"\nSKIPPED: {file_path} (pytest.skip called: {getattr(e, 'msg', 'No reason')})")
                        continue
                    raise
        except BaseException as e:
            failed_imports.append((str(file_path), str(e)))
            print(f"\nFAILED: {file_path}")
            print(f"ERROR: {e}")

    print("\n" + "="*50)
    print(f"Validation Complete: {total_files} files checked.")
    if failed_imports:
        print(f"Found {len(failed_imports)} files with import/syntax errors:")
        for path, error in failed_imports:
            print(f"- {path}\n  Error: {error}")
        return False
    else:
        print("All files imported successfully!")
        return True

if __name__ == "__main__":
    workspace_root = Path(__file__).parent.parent
    src_path = workspace_root / "src"
    if not src_path.exists():
        print(f"Error: Source directory {src_path} not found.")
        sys.exit(1)

    success = validate_imports(src_path)
    sys.exit(0 if success else 1)
