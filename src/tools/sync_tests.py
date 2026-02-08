#!/usr/bin/env python3
import glob
import os
from pathlib import Path

CLEANED_DIR = Path(r"C:\DEV\PyAgent\src\external_candidates\cleaned")
TESTS_DIR = Path(r"C:\DEV\PyAgent\tests\unit")

def main():
    modules = glob.glob(str(CLEANED_DIR / "*.py"))
    print(f"Found {len(modules)} modules in cleaned.")

    for mod_path in modules:
        mod_name = Path(mod_path).name
        test_path = TESTS_DIR / f"test_auto_{mod_name}"
        
        # Simple test content pointing to 'cleaned'
        content = f'''
import importlib.util
from pathlib import Path

p = Path(r"{mod_path}")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
'''
        # Write the test file
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Regenerated all tests.")

if __name__ == "__main__":
    main()
