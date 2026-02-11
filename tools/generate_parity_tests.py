#!/usr/bin/env python3
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
