
"""Script for automatically injecting missing dataclass imports where decorators are used."""

import os
import re

def fix_dataclass_imports(root_dir: str) -> None:
    """Inject dataclass and field imports into files missing them."""
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                # print(f"Checking {path}")
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if "@dataclass" in content and "from dataclasses import dataclass" not in content:
                    print(f"Fixing {path}")
                    # Look for the commented out version with regex
                    new_content = re.sub(r'#\s*from\s+dataclasses\s+import\s+dataclass.*', 'from dataclasses import dataclass, field', content)
                    
                    # If still not found, add it
                    if "from dataclasses import dataclass" not in new_content:
                        # Find where to insert
                        lines = new_content.splitlines()
                        inserted = False
                        for i, line in enumerate(lines):
                            if line.startswith("import ") or line.startswith("from "):
                                lines.insert(i, "from dataclasses import dataclass, field")
                                inserted = True
                                break
                        if not inserted:
                            lines.insert(0, "from dataclasses import dataclass, field")
                        new_content = "\n".join(lines)
                    
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)

if __name__ == "__main__":
    fix_dataclass_imports("src")
