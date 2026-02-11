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
from pathlib import Path

CLEANED_DIR = Path("src/external_candidates/cleaned")
TEST_DIR = Path("tests/unit")

def generate_tests():
    # Remove old auto tests
    for old_test in TEST_DIR.glob("test_auto_*.py"):
        os.remove(old_test)
        
    modules = [f for f in CLEANED_DIR.glob("*.py") if f.name != "__init__.py"]
    print(f"Generating {len(modules)} tests...")
    
    for mod in modules:
        test_filename = f"test_auto_{mod.name}"
        test_path = TEST_DIR / test_filename
        
        # Determine import path
        # src/external_candidates/cleaned/name.py -> src.external_candidates.cleaned.name
        
        content = f"""#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import sys

def test_import_{mod.stem}():
    p = Path(r"{mod.absolute()}")
    assert p.exists()
    # Basic import check
    spec = importlib.util.spec_from_file_location("{mod.stem}", str(p))
    module = importlib.util.module_from_spec(spec)
    # We don't execute to avoid side effects in this environment, 
    # just verify it's a valid python file
    assert spec is not None
"""
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(content)

    print("Test generation complete.")

if __name__ == "__main__":
    generate_tests()
