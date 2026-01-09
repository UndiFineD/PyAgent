import os
import re

src_path = r"c:\DEV\PyAgent\src"
for root, _, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            if "import annotations" in content and "from __future__ import annotations" not in content:
                new_content = re.sub(r"^import annotations$", r"from __future__ import annotations", content, flags=re.MULTILINE)
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed: {path}")
