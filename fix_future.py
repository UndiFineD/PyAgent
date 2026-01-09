import os
import re

src_path = r"c:\DEV\PyAgent\src"
for root, _, files in os.walk(src_path):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            if "from __future__ import annotations" in content:
                lines = content.splitlines()
                annotation_line = ""
                other_lines = []
                for line in lines:
                    if "from __future__ import annotations" in line:
                        annotation_line = line
                    else:
                        other_lines.append(line)
                
                if annotation_line:
                    # Find insertion point (after shebang/encoding)
                    insert_idx = 0
                    if other_lines and other_lines[0].startswith("#!"):
                        insert_idx = 1
                    if len(other_lines) > insert_idx and ("coding:" in other_lines[insert_idx] or "-*-" in other_lines[insert_idx]):
                        insert_idx += 1
                    
                    other_lines.insert(insert_idx, "from __future__ import annotations")
                    new_content = "\n".join(other_lines) + ("\n" if content.endswith("\n") else "")
                    
                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Repositioned: {path}")
