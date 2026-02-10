
"""
Debug Engine Hints v2: Utility for checking missing type hints in __init__ methods.
"""
#!/usr/bin/env python3
import ast
import os
from typing import List, Tuple

def check_file_for_missing_hints(filepath: str) -> List[Tuple[str, int]]:
    """
    Parses a python file and returns a list of (function_name, lineno)
    for __init__ methods missing return type hints.
    """
    missing = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=filepath)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == "__init__":
                    if node.returns is None:
                        missing.append((node.name, node.lineno))
    except (SyntaxError, UnicodeDecodeError):
        # Skip files that can't be parsed
        pass
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")

    return missing

def scan_directory(root_path: str):
    print(f"Scanning {root_path} for missing __init__ return hints...")
    count = 0
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                missing_list = check_file_for_missing_hints(filepath)
                if missing_list:
                    print(f"\nFile: {filepath}")
                    for func, line in missing_list:
                        print(f"  Line {line}: {func} is missing -> None")
                        count += 1

    print(f"\nTotal missing hints found: {count}")

if __name__ == "__main__":
    target_dir = r"c:\DEV\PyAgent\src\infrastructure\engine"
    scan_directory(target_dir)
