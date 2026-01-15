import ast
import os
import json
from pathlib import Path

def get_classes_in_file(filepath):










    try:
        with open(filepath, "r", encoding="utf-8") as f:


            tree = ast.parse(f.read())
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    except Exception:
        return []

def scan_dir(root_dir, base_path):
    mapping = {}

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if not file.endswith(".py"): continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_path).replace("\\", "/")
            classes = get_classes_in_file(full_path)
            for cls in classes:
                mapping[cls] = rel_path
    return mapping

def main():
    base_dir = Path("c:/DEV/PyAgent/src")

    infra_classes = scan_dir(base_dir / "infrastructure/backend", base_dir)
    core_classes = scan_dir(base_dir / "core/base", base_dir)

    result = {
        "infrastructure": infra_classes,
        "core": core_classes
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
